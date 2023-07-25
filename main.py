from const import STREAMER
from download_videos import download_videos
from fetch_videos import fetch_recent_video_metadata, fetch_videos
from edit_videos import cut_video
import os
import multiprocessing

from util import safe_mkdir

SHOULD_DOWNLOAD = True
SHOULD_USE_IDS = True
VIDEO_IDS = [1877442987, 1876259617, 1875331077]
VIDEO_AGE_THRESHOLD = 2  # days

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
        videos = fetch_videos(STREAMER, VIDEO_IDS)
    else:
        videos = fetch_recent_video_metadata(
            STREAMER, VIDEO_AGE_THRESHOLD)

    # a video has an 'id', 'title', 'lengthSeconds' field
    if SHOULD_DOWNLOAD:
        download_videos(videos)

    # 2. cut videos
    video_file_names = [x for x in os.listdir('videos') if x != '.DS_Store']

    pool = multiprocessing.Pool(processes=8)
    pool.map(edit_video, video_file_names)
    pool.close()
    pool.join()
