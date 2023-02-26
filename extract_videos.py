import os
import json
import twitchdl
import pprint
# TODO: Delete irrelevant videos from /videos

def extract_videos(channel_names):
    for channel in channel_names:
        video_list_str = os.popen(f'twitch-dl videos -j {channel}').read()
        video_list = json.loads(video_list_str)
        pprint.pprint(video_list)

extract_videos()




