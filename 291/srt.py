from datetime import timedelta
from datetime import datetime
from typing import List
import re


def get_srt_section_ids(text: str) -> List[int]:
    """Parse a caption (srt) text passed in and return a
       list of section numbers ordered descending by
       highest speech speed
       (= ratio of "time past:characters spoken")

       e.g. this section:

       1
       00:00:00,000 --> 00:00:01,000
       let's code

       (10 chars in 1 second)

       has a higher ratio then:

       2
       00:00:00,000 --> 00:00:03,000
       code

       (4 chars in 3 seconds)

       You can ignore milliseconds for this exercise.
    """
    metrics = []
    for chunk in text.strip().split('\n\n'):
        (number, duration, caption) = chunk.strip().split('\n')
        start_time, end_time = [datetime.strptime(
            s, '%H:%M:%S,%f') for s in re.findall('\d\d:\d\d:\d\d,\d\d\d', duration)]
        duration = end_time - start_time
        speech_speed = len(caption.strip()) / duration.total_seconds()
        metrics.append((int(number), speech_speed))

    metrics.sort(key=lambda x: x[1], reverse=True)
    return [metric[0] for metric in metrics]
