import os
from datetime import date, timedelta
from pathlib import Path
from typing import Dict, List
from urllib.request import urlretrieve
import json

URL = "https://bites-data.s3.us-east-2.amazonaws.com/exchangerates.json"
TMP = Path(os.getenv("TMP", "/tmp"))
RATES_FILE = TMP / "exchangerates.json"

if not RATES_FILE.exists():
    urlretrieve(URL, RATES_FILE)

with open(RATES_FILE) as rates_fp:
    rates_data = json.load(rates_fp)


def gen_dates(start_date, end_date, interval=timedelta(days=1)):
    # Generator to generate dates >= start_date and <= end_date
    d = start_date
    while d <= end_date:
        yield d
        d += interval


def get_all_days(start_date: date, end_date: date) -> List[date]:
    return [d for d in gen_dates(start_date, end_date)]


def match_daily_rates(start: date, end: date, daily_rates: dict) -> Dict[date, date]:
    all_dates = get_all_days(start, end)
    daily_rates_dates = [date.fromisoformat(d) for d in daily_rates]
    matched_daily_rates = dict()
    for d in all_dates:
        matched_date = d
        if matched_date.isoformat() not in daily_rates:
            matched_date = max([_ for _ in daily_rates_dates if _ < d])
        matched_daily_rates[d] = matched_date
    return matched_daily_rates


def exchange_rates(
    start_date: str = "2020-01-01", end_date: str = "2020-09-01"
) -> Dict[date, dict]:
    min_date = date.fromisoformat(rates_data["start_at"])
    max_date = date.fromisoformat(rates_data["end_at"])

    start_date = date.fromisoformat(start_date)
    if start_date < min_date:
        raise ValueError(f"start_date cannot be before {min_date}")

    end_date = date.fromisoformat(end_date)
    if end_date > max_date:
        raise ValueError(f"end_date cannot be after {max_date}")

    matched_rates = match_daily_rates(
        start_date, end_date, rates_data["rates"])
    exchange_rates = {}
    for d in matched_rates:
        rates_key = matched_rates[d].isoformat()
        exchange_rate = {}
        exchange_rate["Base Date"] = matched_rates[d]
        exchange_rate["USD"] = rates_data["rates"][rates_key]["USD"]
        exchange_rate["GBP"] = rates_data["rates"][rates_key]["GBP"]
        exchange_rates[d] = exchange_rate
    return exchange_rates
