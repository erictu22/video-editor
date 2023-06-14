import twitchdl.commands.download as download
from pprint import pprint
from models import DotDict


def download_videos(videos):
    if len(videos) == 0:
        print('No relevant videos to download')
        return

    video_ids = [video['id'] for video in videos]
    for video_id in video_ids:
        try:
            download_video(video_id)
        except:
            print('Failed to download ' + str(video_id))


def download_video(video_id):
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
            "output": "videos/{channel}_{id}.{format}",
        }
    )
    download(download_args)
