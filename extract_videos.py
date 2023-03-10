import os
import json
import twitchdl
from pprint import pprint
from datetime import datetime
import subprocess
import sys

# TODO: Delete irrelevant videos from /videos
# To-add: Lourlo
VIDEO_AGE_THRESHOLD = 1 # days
TOP_LANE_STREAMERS = ['Sanchovies' ,'yung_fappy','Dragoon','Lourlo','Thebausffs','Bwipolol','foggedftw2','SoloRenektonOnly']
TEST_STREAMERS = ['yung_fappy']
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
    for file_name in os.listdir('videos'):
        skip_values = ['.DS_Store']
        if file_name in skip_values:
            continue

        video_id = file_name.split('.')[0]

        p = os.popen((f'twitch-dl info -j {video_id}'))

        video = json.loads(p.read())
        videos.append(video)
    return videos

def download_videos(videos):
    if len(videos) == 0:
        print('No relevant videos to download')
        return

    video_ids = [video['id'] for video in videos]
    id_str = ' '.join(video_ids)
    print(f'Downloading {id_str}')
    cmd = f'twitch-dl download -q source -f mp4 -o videos/{"{id}.mp4"} {id_str}'
    with subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, text=True, bufsize=1) as p:
        for line in p.stdout:
            print('\r' + str(line).replace('\n',''), end='')

    if p.returncode != 0:
        raise subprocess.CalledProcessError(p.returncode, p.args)
    print('\r')
    p.kill()

# TODO: Save video metadata

def get_diff():
    relevant_videos = get_relevant_videos(TEST_STREAMERS)
    local_videos = get_local_videos()
    local_video_ids = [video['id'] for video in local_videos]
    videos_to_delete = [video for video in local_videos if not is_video_relevant(video)]
    videos_to_download = [video for video in relevant_videos if not video['id'] in local_video_ids]
    return videos_to_delete, videos_to_download

delete, download = get_diff()
download_videos(download)
print('Done')