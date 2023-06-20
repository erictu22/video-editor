import twitchdl.commands.download as download
from pprint import pprint
from models import DotDict
from util import *

def download_videos(videos, path="videos/ | {channel} (streamed on {date}).{format}"):
    if len(videos) == 0:
        print('Video list is empty')
        return

    for video in videos:
        try:
            print(f'Downloading "{str(video["title"])}"')
            block_print()
            download_video(video['id'],path)
            enable_print()
        except:
            enable_print()
            print('Failed to download ' + str(video['title']))


def download_video(video_id, path):
    download_args = DotDict(
        {
            "videos": [str(video_id)],
            "format": "mp4",
            "keep": False,
            "quality": "source",
            "max_workers": 20,
            "no_join": False,
            "overwrite": True,
            "start": None,
            "end": None,
            "output": path,
        }
    )
    download(download_args)
