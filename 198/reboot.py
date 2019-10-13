from dateutil.parser import parse

MAC1 = """
reboot    ~                         Wed Apr 10 22:39
reboot    ~                         Wed Mar 27 16:24
reboot    ~                         Wed Mar 27 15:01
reboot    ~                         Sun Mar  3 14:51
reboot    ~                         Sun Feb 17 11:36
reboot    ~                         Thu Jan 17 21:54
reboot    ~                         Mon Jan 14 09:25
"""


def calc_max_uptime(reboots):
    """Parse the passed in reboots output,
       extracting the datetimes.

       Calculate the highest uptime between reboots =
       highest diff between extracted reboot datetimes.

       Return a tuple of this max uptime in days (int) and the
       date (str) this record was hit.

       For the output above it would be (30, '2019-02-17'),
       but we use different outputs in the tests as well ...
    """
    # Split the string into lines
    #    and split each line so we can isolate the timestamp
    lines = [l.split('~') for l in reboots.split('\n') if l.strip()]
    # Convert each string date into a datetime
    times = [parse(t[-1].strip()) for t in lines]
    # Find all the end times
    ends = times[:-1]
    # Find all the start times
    starts = times[1:]
    # For each pair save the endtime and the difference
    diffs = [(end, end - start) for (start, end) in zip(starts, ends)]
    # Find the one with the largest diff
    max_uptime = max(diffs, key=lambda d: d[1])
    # Return the result in the expected format
    return (max_uptime[1].days, f'{max_uptime[0]:%Y-%m-%d}')
