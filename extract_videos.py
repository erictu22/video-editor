import os
import json
import twitchdl
from pprint import pprint
from datetime import datetime

# TODO: Delete irrelevant videos from /videos  
VIDEO_AGE_THRESHOLD = 1 #weeks
TOP_LANE_STREAMERS = ['Sanchovies' ,'yung_fappy','Dragoon','Lourlo','Thebausffs','Bwipolol','foggedftw2','SoloRenektonOnly']

def is_video_relevant(video):
    date = datetime.strptime(video['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
    video_age = datetime.now() - date
    return video_age.days < VIDEO_AGE_THRESHOLD

def get_relevant_videos(channel_names):
    output = []
    for channel in channel_names:
        video_list_str = os.popen(f'twitch-dl videos -j {channel}').read()
        video_list = json.loads(video_list_str)['videos']
        relevant_videos = [x for x in video_list if is_video_relevant(x)]
        output.extend(relevant_videos)
    return output

def get_local_videos():
    videos = []
    for video_id in os.listdir('videos'):
        # TODO: Maybe check if video_id is valid
        p = os.popen((f'twitch-dl info -j {video_id}'))
        video = json.load(p.read())
        videos.append(video)
    print(videos)
    return videos

def download_videos(videos):
    video_ids = [video['id'] for video in videos]
    id_str = ' '.join(video_ids)
    p = os.popen(f'cd videos && twitch-dl download -q 160p30 {id_str}')
    p.read()

# TODO: Save video metadata

def get_diff():
    relevant_videos = get_relevant_videos(['Lourlo'])
    local_videos = get_local_videos()
    local_video_ids = [video['id'] for video in local_videos]
    videos_to_delete = [video for video in local_videos if not is_video_relevant(video)]
    videos_to_download = [video for video in relevant_videos if not video['id'] in local_video_ids]
    return videos_to_delete, videos_to_download

delete, download = get_diff()
download_videos(download)