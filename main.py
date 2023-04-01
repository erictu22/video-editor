from extract_videos import get_relevant_videos, download_videos, get_local_videos
from edit_videos import cut_video
import os
import multiprocessing

STREAMERS = ['ShokLoL']
VIDEO_AGE_THRESHOLD = 7  # days

SAMPLE_INTERVALS = 30  # seconds
START_PERIOD = 5
END_PERIOD = 10

SHOULD_CUT_IN_PARALLEL = True


def edit_video(video_id):
    cut_video(video_id, intervals=SAMPLE_INTERVALS,
              start_grace=START_PERIOD, end_grace=END_PERIOD)


if __name__ == '__main__':
    # 1. extract videos
    videos = get_relevant_videos(
        STREAMERS, VIDEO_AGE_THRESHOLD, max_per_channel=3)
    download_videos(videos)  # files are saved in /videos/

    # or use... twitch-dl download -q source 1717734745 1719653944 1721719514 1728794232 1736757792 -w 20 --output {id}.mp4

    # 2. cut videos

    video_ids = [x.split('.')[0]
                 for x in os.listdir('videos') if x != '.DS_Store']

    if SHOULD_CUT_IN_PARALLEL:
        pool = multiprocessing.Pool(processes=4)
        pool.map(edit_video, video_ids)
        pool.close()
        pool.join()
    else:
        for video_id in video_ids:
            edit_video(video_id)
