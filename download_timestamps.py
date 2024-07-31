import twitchdl.commands.download as download
from pprint import pprint
from models import DotDict
from util import *

def time_to_seconds(time):
    return sum(x * int(t) for x, t in zip([3600, 60, 1], time.split(":")))

def download_videos(videos):
    if len(videos) == 0:
        print('Video list is empty')
        return

    for video in videos:
        video_title = video.get("title")

        try:
            print(f'Downloading "{video_title}"')
            download_video(video,"videos/" + video_title)
        except(Exception) as e:
            enable_print()
            print('Failed to download ' + video_title)
            print(e)


def download_video(video):
    download_args = DotDict(
        {
            "format": "mp4",
            "keep": False,
            "quality": "source",
            "max_workers": 20,
            "no_join": False,
            "overwrite": True,
            "output": "cuts/" + video.get("title") + ".mp4",
            "start": time_to_seconds(video.get("start")),
            "end": time_to_seconds(video.get("end"))
        }
    )
    download.download([str(video.get("id"))], download_args)

download_video(DotDict({
        "title": "Aurora vs Vayne",
        "id": 2204695355,
        "start": "02:40:00",
        "end": "03:03:50"
    }))