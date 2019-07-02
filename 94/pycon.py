from collections import namedtuple
import os
import pickle
import urllib.request
import tempfile
import re

# prework
# download pickle file and store it in a tmp file
pycon_videos = tempfile.mkstemp(suffix='.pkl')[1]
pkl_file = os.path.basename(pycon_videos)
data = 'http://projects.bobbelderbos.com/pcc/{}'.format('pycon_videos.pkl')
urllib.request.urlretrieve(data, pycon_videos)

# the pkl contains a list of Video namedtuples
Video = namedtuple('Video', 'id title duration metrics')


def load_pycon_data(pycon_videos=pycon_videos):
    """Load the pickle file (pycon_videos) and return the data structure
       it holds"""
    return pickle.load(open(pycon_videos, 'rb'))


def get_most_popular_talks_by_views(videos):
    """Return the pycon video list sorted by viewCount"""
    return sorted(videos, key=lambda v: int(v.metrics['viewCount']), reverse=True)


def get_most_popular_talks_by_like_ratio(videos):
    """Return the pycon video list sorted by most likes relative to
       number of views, so 10 likes on 175 views ranks higher than
       12 likes on 300 views. Discount the dislikeCount from the likeCount.
       Return the filtered list"""
    return sorted(videos, key=lambda v: float(int(v.metrics['likeCount']) - int(v.metrics['dislikeCount']))/float(v.metrics['viewCount']), reverse=True)

def duration_to_seconds(duration):
   match = re.match('PT(\d+H)?(\d+M)?(\d+S)?', duration).groups()
   hours = int(match[0][:-1]) if match[0] else 0
   minutes = int(match[1][:-1]) if match[1] else 0
   seconds = int(match[2][:-1]) if match[2] else 0
   return hours * 3600 + minutes * 60 + seconds

def get_talks_gt_one_hour(videos):
    """Filter the videos list down to videos of > 1 hour"""
    return [video for video in videos if duration_to_seconds(video.duration) >= 3600]


def get_talks_lt_twentyfour_min(videos):
    """Filter videos list down to videos that have a duration of less than
       24 minutes"""
    return [video for video in videos if duration_to_seconds(video.duration) < (24*60)]