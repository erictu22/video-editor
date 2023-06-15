from download_videos import download_videos
from fetch_videos import fetch_recent_video_metadata, fetch_videos
from edit_videos import cut_video
import os
import multiprocessing

STREAMERS = ['bwipolol']
SHOULD_USE_IDS = True
VIDEO_IDS = [1843365077]
VIDEO_AGE_THRESHOLD = 11  # days

def edit_video(video_id):
    cut_video(video_id)

if __name__ == '__main__':
    # 1. extract videos
    videos = []
    if SHOULD_USE_IDS:
        videos = fetch_videos(STREAMERS, VIDEO_IDS)
    else:
        videos = fetch_recent_video_metadata(
            STREAMERS, VIDEO_AGE_THRESHOLD, max_per_channel=3)

    # a video has an 'id', 'title', 'lengthSeconds' field
    download_videos(videos)

    # 2. cut videos
    video_ids = [x.split('.')[0]
                 for x in os.listdir('videos') if x != '.DS_Store']

    pool = multiprocessing.Pool(processes=4)
    pool.map(edit_video, video_ids)
    pool.close()
    pool.join()
