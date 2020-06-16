from collections import Counter

import bs4
import requests

COMMON_DOMAINS = ("https://bites-data.s3.us-east-2.amazonaws.com/"
                  "common-domains.html")
TARGET_DIV = {"class": "middle_info_noborder"}


def get_common_domains(url=COMMON_DOMAINS):
    """Scrape the url return the 100 most common domain names"""
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    div = soup.find_all('div', attrs=TARGET_DIV)[0]
    domains = []
    for row in div.find_all('tr'):
        cols = row.find_all('td')
        domain = cols[2].text.strip()
        percent = float(cols[3].text.strip(' %'))
        domains.append((percent, domain))
    domains = sorted(domains, key=lambda d: d[0], reverse=True)[0:100]
    return [d[1] for d in domains]


def get_most_common_domains(emails, common_domains=None):
    """Given a list of emails return the most common domain names,
       ignoring the list (or set) of common_domains"""
    if common_domains is None:
        common_domains = get_common_domains()

    all_domains = [email.split('@')[1] for email in emails]
    domain_counter = Counter(
        [domain for domain in all_domains if domain not in common_domains])
    return domain_counter.most_common()

