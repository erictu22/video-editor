from extract_videos import get_relevant_videos, download_videos, get_local_videos
from edit_videos import cut_video
import os

STREAMERS = ['Bwipolol', 'ShokLoL', 'Dragoon', 'Revenge']
VIDEO_AGE_THRESHOLD = 7  # days

SAMPLE_INTERVALS = 30  # seconds
START_PERIOD = 5
END_PERIOD = 10

if __name__ == '__main__':
    # 1. extract videos
    videos = get_relevant_videos(STREAMERS, VIDEO_AGE_THRESHOLD)
    # download_videos(videos) # files are saved in /videos/

    # 2. cut videos
    video_ids = [x.split('.')[0]
                 for x in os.listdir('videos') if x != '.DS_Store']
    for video_id in video_ids:
        cut_video(video_id, intervals=SAMPLE_INTERVALS,
                  start_grace=START_PERIOD, end_grace=END_PERIOD)

    # 3. score videos
