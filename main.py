from download_videos import download_videos
from fetch_videos import fetch_recent_video_metadata, fetch_videos
from edit_videos import cut_video
import os
import multiprocessing

from util import safe_mkdir

STREAMERS = ['bwipolol']
SHOULD_USE_IDS = True
VIDEO_IDS = [1843365077, 1840763504]
VIDEO_AGE_THRESHOLD = 11  # days

def edit_video(file_name):
    cut_video(f'videos/{file_name}')

if __name__ == '__main__':
    # set up
    safe_mkdir('videos')
    safe_mkdir('cuts')
    safe_mkdir('temp')

    # 1. extract videos
    videos = []
    if SHOULD_USE_IDS:
        videos = fetch_videos(STREAMERS, VIDEO_IDS)
    else:
        videos = fetch_recent_video_metadata(
            STREAMERS, VIDEO_AGE_THRESHOLD, max_per_channel=3)

    # a video has an 'id', 'title', 'lengthSeconds' field
    # download_videos(videos)

    # 2. cut videos
    video_file_names = [x for x in os.listdir('videos') if x != '.DS_Store']

    pool = multiprocessing.Pool(processes=4)
    pool.map(edit_video, video_file_names)
    pool.close()
    pool.join()
