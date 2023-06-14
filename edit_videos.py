import cv2
from math import *
import numpy
from skimage.metrics import structural_similarity
import moviepy.editor as me
import os
from time import time
image_data = [cv2.imread(f'image-data/{x}')
              for x in os.listdir('image-data') if x != '.DS_Store']


def cut_video(video_id, intervals = 30, start_grace = 5, end_grace = 7):
    cuts = get_cuts(video_id, intervals=intervals,
                    start_grace=start_grace, end_grace=end_grace)
    video = me.VideoFileClip(f'videos/{video_id}.mp4')
    print("Cutting at ")
    print(cuts)

    count = 1
    for cut in cuts:
        clip = video.subclip(cut[0], cut[1])
        h, m, s = seconds_to_hms(cut[0])
        clip.write_videofile(f'cuts/{count}_{video_id}_{h}h{m}m{s}s.mp4', temp_audiofile=f'temp/temp-audio-{video_id}.m4a',
                             remove_temp=True, codec="libx264", audio_codec="aac")
        count = count + 1

    os.remove(f'./videos/{video_id}.mp4')


def seconds_to_hms(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return h, m, s


def get_cuts(video_id, intervals, start_grace, end_grace):
    frame_match_scores_with_timestamps = calc_frame_match_scores(video_id=video_id, intervals=intervals, should_display=False)

    frame_match_scores = [datum[1]
                          for datum in frame_match_scores_with_timestamps]
    timestamps = [datum[0] for datum in frame_match_scores_with_timestamps]

    frame_match_threshold = calc_frame_match_threshold(frame_match_scores)
    is_frame_match = [
        score > frame_match_threshold for score in frame_match_scores]

    cuts = []
    start_time = -1
    stop_time = -1
    for i in range(0, len(is_frame_match) - end_grace):

        is_ingame = all(is_frame_match[i: i + start_grace])
        is_game_over = all(
            not is_frame_match for is_frame_match in is_frame_match[i: i + end_grace])

        if start_time == -1 and is_ingame:
            start_time = timestamps[i]
        elif start_time != -1 and stop_time == -1 and is_game_over:
            stop_time = timestamps[i + 2]
            cuts.append((start_time, stop_time))
            start_time = -1
            stop_time = -1

    return cuts


def calc_frame_match_threshold(frame_match_scores):
    first_q = numpy.percentile(frame_match_scores, 25)
    third_q = numpy.percentile(frame_match_scores, 75)
    thresh = (third_q - first_q) / 2 + first_q
    return thresh


def calc_similarity(image1, image2):
    # Convert the images to grayscale
    gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    resize_dimensions = (360, 480)
    resized_image1 = cv2.resize(gray_image1, resize_dimensions)
    resized_image2 = cv2.resize(gray_image2, resize_dimensions)

    # Compute the SSIM between the two images
    (score, diff) = structural_similarity(
        resized_image1, resized_image2, full=True)

    return score

# Returns a list of timestamps and their frame match scores


def calc_frame_match_scores(video_id, intervals=1, start=0, should_display=False):
    print(f'Reading {video_id}')
    cap = cv2.VideoCapture(f'videos/{video_id}.mp4')
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if start != 0:  # Don't seek unless we have to
        cap.set(cv2.CAP_PROP_POS_FRAMES, start)
    frame_no = 0

    start = time()
    frame_match_scores = []
    while (cap.isOpened()):
        frame_exists, curr_frame = cap.read()
        if frame_exists:
            if frame_no % int(intervals * video_fps) == 0:
                if should_display:
                    cv2.imshow('frame', curr_frame)
                    cv2.waitKey(1)
                frame_match_score = max([calc_similarity(img, curr_frame)
                                            for img in image_data])
                frame_match_scores.append(
                    (int(frame_no / video_fps), frame_match_score))
        else:
            break
        frame_no += 1
    cap.release()
    end = time()
    log_runtime(video_id, start, end, total_frames / video_fps)
    return frame_match_scores


def log_runtime(video_id, start, end, video_runtime):
    h1, m1, s1 = seconds_to_hms(int(end - start))
    h2, m2, s2 = seconds_to_hms(int(video_runtime))
    print(
        f'\nProcessed {video_id}, a {h2}h {m2}m {s2}s video in {h1}h {m1}m {s1}s')
