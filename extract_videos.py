import os
import json
import twitchdl
import pprint

def extract_videos(channel_names):
    video_list_str = os.popen("twitch-dl videos -j Lourlo").read()
    video_list = json.loads(video_list_str)
    pprint.pprint(video_list)

extract_videos()