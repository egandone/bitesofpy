from datetime import datetime, timedelta
import re

NOW = datetime(year=2019, month=2, day=6,
               hour=22, minute=0, second=0)

def str_to_timedelta(delay_spec: str):
    td = None
    if delay_spec[-1] == 'd':
        td = timedelta(days = int(delay_spec[:-1]))
    elif delay_spec[-1] == 'h':
        td = timedelta(hours = int(delay_spec[:-1]))
    elif delay_spec[-1] == 'm':
        td = timedelta(minutes = int(delay_spec[:-1]))
    elif delay_spec[-1] == 's':
        td = timedelta(seconds = int(delay_spec[:-1]))
    else:
        td = timedelta(seconds = int(delay_spec))
    return td

def add_todo(delay_time: str, task: str,
             start_time: datetime = NOW) -> datetime:
    """
    Add a todo list item in the future with a delay time.

    Parse out the time unit from the passed in delay_time str:
    - 30d = 30 days
    - 1h 10m = 1 hour and 10 min
    - 5m 3s = 5 min and 3 seconds
    - 45 or 45s = 45 seconds

    Return the task and planned time which is calculated from
    provided start_time (here default = NOW):
    >>> add_todo("1h 10m", "Wash my car")
    >>> "Wash my car @ 2019-02-06 23:10:00"
    """
    all_specs = re.findall(r'\d+[dhms]?', delay_time)
    total_delta = timedelta()
    for spec in all_specs:
        total_delta += str_to_timedelta(spec)

    run_time = start_time + total_delta
    return f'{task} @ {run_time:%Y-%m-%d %H:%M:%S}'    
