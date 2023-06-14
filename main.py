from download_videos import download_videos
from fetch_videos import fetch_recent_video_metadata, fetch_videos
from edit_videos import cut_video
import os
import multiprocessing

STREAMERS = ['bwipolol']
SHOULD_USE_IDS = True
VIDEO_IDS = [1843365077, 1840763504]
VIDEO_AGE_THRESHOLD = 11  # days

SECONDS_PER_INTERVAL = 30
INTERVALS_FOR_START = 5
INTERVALS_FOR_END = 7


def edit_video(video_id):
    cut_video(video_id, intervals=SECONDS_PER_INTERVAL,
              start_grace=INTERVALS_FOR_START, end_grace=INTERVALS_FOR_END)


if __name__ == '__main__':
    # 1. extract videos
    videos = fetch_recent_video_metadata(
        STREAMERS, VIDEO_AGE_THRESHOLD, max_per_channel=3)
    download_videos(videos)  # files are saved in /videos/

    # or use... twitch-dl download -q source 1717734745 1719653944 1721719514 1728794232 1736757792 -w 20 --output {id}.mp4

    # 2. cut videos
    video_ids = [x.split('.')[0]
                 for x in os.listdir('videos') if x != '.DS_Store']

    pool = multiprocessing.Pool(processes=4)
    pool.map(edit_video, video_ids)
    pool.close()
    pool.join()
