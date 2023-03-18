import os
import json
import twitchdl.commands.download as download
from pprint import pprint
from datetime import datetime
import subprocess
import sys


def is_video_relevant(video, thresh):
    date = datetime.strptime(video['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
    video_age = datetime.now() - date
    return video_age.days < thresh


def get_relevant_videos(channel_names, thresh, max_per_channel=5):
    output = []
    for channel in channel_names:
        video_list_str = os.popen(f'twitch-dl videos -j {channel}').read()
        video_list = json.loads(video_list_str)['videos']
        relevant_videos = [x for x in video_list if is_video_relevant(
            x, thresh)][0:max_per_channel]
        output.extend(relevant_videos)
    return output


def get_local_videos():
    videos = []
    for file_name in os.listdir('videos'):
        skip_values = ['.DS_Store']
        if file_name in skip_values:
            continue

        video_id = file_name.split('.')[0]

        # TODO: Handle case where video is not found
        p = os.popen((f'twitch-dl info -j {video_id}'))

        video = json.loads(p.read())
        videos.append(video)
    return videos


class DotDict(dict):
    """dot.notation access to dictionary attributes"""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


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
            "output": "videos/{id}.{format}",
        }
    )
    download(download_args)


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
