import cv2
from math import *
import numpy
from skimage.metrics import structural_similarity
import moviepy.editor as me
import os
from time import time
samples = [cv2.imread(f'image-data/{x}')
           for x in os.listdir('image-data') if x != '.DS_Store']


def cut_video(video_id, intervals, start_grace, end_grace):
    cuts = get_cuts(video_id, intervals=intervals,
                    start_grace=start_grace, end_grace=end_grace)
    video = me.VideoFileClip(f'videos/{video_id}.mp4')

    for cut in cuts:
        clip = video.subclip(cut[0], cut[1])
        h, m, s = seconds_to_hms(cut[0])
        clip.write_videofile(f'cuts/{video_id}_{h}h{m}m{s}s.mp4', temp_audiofile=f'temp/temp-audio-{video_id}.m4a',
                             remove_temp=True, codec="libx264", audio_codec="aac")

    os.remove(f'./videos/{video_id}.mp4')


def seconds_to_hms(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return h, m, s


def get_cuts(video_id, intervals, start_grace, end_grace):
    data = play_video(video_id=video_id, intervals=intervals,
                      should_record_data=True, should_display=False)

    scores = [datum[1] for datum in data]
    timestamps = [datum[0] for datum in data]
    first_q = numpy.percentile(scores, 25)
    third_q = numpy.percentile(scores, 75)
    thresh = (third_q - first_q) / 2 + first_q
    is_ingame_checks = [score > thresh for score in scores]

    cuts = []
    start = -1
    stop = -1
    for i in range(0, len(is_ingame_checks) - end_grace):
        if start == -1 and all(is_ingame for is_ingame in is_ingame_checks[i: i + start_grace]):
            start = timestamps[i]
        elif start != -1 and stop == -1 and all(not is_ingame for is_ingame in is_ingame_checks[i: i + end_grace]):
            stop = timestamps[i + 1]
            cuts.append((start, stop))
            start = -1
            stop = -1

    return cuts


def similarity(image1, image2):
    # Convert the images to grayscale
    gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    resized_image1 = cv2.resize(gray_image1, (720, 1280))
    resized_image2 = cv2.resize(gray_image2, (720, 1280))

    # Compute the SSIM between the two images
    (score, diff) = structural_similarity(
        resized_image1, resized_image2, full=True)

    return score


def play_video(video_id, intervals=1, start=0, should_record_data=False, should_display=True):
    cap = cv2.VideoCapture(f'videos/{video_id}.mp4')
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if start != 0:  # Don't seek unless we have to
        cap.set(cv2.CAP_PROP_POS_FRAMES, start)
    frame_no = 0

    start = time()
    data = []
    while (cap.isOpened()):
        frame_exists, curr_frame = cap.read()
        if frame_exists:
            if frame_no % int(intervals * video_fps) == 0:
                if should_display:
                    cv2.imshow('frame', curr_frame)
                    cv2.waitKey(1)
                if should_record_data:
                    score = max([similarity(img, curr_frame)
                                 for img in samples])
                    data.append((int(frame_no / video_fps), score))
                print(
                    f'id:{video_id} Progress:{round(frame_no / total_frames * 100, 2)}%', end='\r')
        else:
            break
        frame_no += 1
    cap.release()
    end = time()
    log_runtime(video_id, start, end, total_frames / video_fps)
    return data


def log_runtime(video_id, start, end, video_runtime):
    process_time = end - start
    h1, m1, s1 = seconds_to_hms(int(end - start))
    h2, m2, s2 = seconds_to_hms(int(video_runtime))
    print(
        f'\nProcessed {video_id}, a {h2}:{m2}:{s2} video in {h1}:{m1}:{s1} time. Factor:{round(process_time / video_runtime, 2)})')
