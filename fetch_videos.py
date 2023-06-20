from datetime import datetime
import json
import os

def is_video_relevant(video, thresh):
    date = datetime.strptime(video['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
    video_age = datetime.now() - date
    return video_age.days < thresh


def fetch_recent_video_metadata(channel_name, thresh, max_per_channel=5):
    output = []
    video_list_str = os.popen(f'twitch-dl videos -j {channel_name}').read()
    video_list = json.loads(video_list_str)['videos']
    relevant_videos = [x for x in video_list if is_video_relevant(
        x, thresh)][0:max_per_channel]
    output.extend(relevant_videos)
    return output


def fetch_videos(channel_name, video_ids):
    matching_videos = []
    video_list_str = os.popen(f'twitch-dl videos -j {channel_name}').read()
    video_list = json.loads(video_list_str)['videos']
    matching_channel_videos = [x for x in video_list if int(x['id']) in video_ids]
    matching_videos.extend(matching_channel_videos)
    return matching_videos
