import cv2
from math import *
import numpy
from skimage.metrics import structural_similarity
import moviepy.editor as me
import os
import uuid

from process_video import process_video
image_data = [cv2.imread(f'image-data/gameplay/{x}')
              for x in os.listdir('image-data/gameplay') if x != '.DS_Store']

def cut_video(file_path):
    cuts = get_cuts(file_path)
    video = me.VideoFileClip(file_path)
    print("Cutting at " + str(cuts))

    file_name = str(uuid.uuid4())
    cut_id = 1
    for cut in cuts:
        clip = video.subclip(cut[0], cut[1])
        clip.write_videofile(f'cuts/{file_name}.mp4', temp_audiofile=f'temp/temp-audio-{file_name}.m4a',
                             remove_temp=True, codec="libx264", audio_codec="aac")
        cut_id = cut_id + 1

    os.remove(file_path)

def get_cuts(file_path, intervals = 15, start_grace = 5, end_grace = 5):
    frame_match_scores, timestamps = calc_frame_match_scores(file_path, intervals=intervals)
    is_frame_match = apply_bool_filter(frame_match_scores)

    cuts = []
    start_time = -1
    stop_time = -1
    for intv in range(0, len(is_frame_match) - end_grace):
        is_ingame = all(is_frame_match[intv: intv + start_grace])
        is_game_over = all(
            not is_frame_match for is_frame_match in is_frame_match[intv: intv + end_grace])

        if start_time == -1 and is_ingame:
            start_time = timestamps[intv]
        elif start_time != -1 and stop_time == -1 and is_game_over:
            stop_time = timestamps[intv + 2]
            cuts.append((start_time, stop_time))
            start_time = -1
            stop_time = -1

    return cuts

# Returns a list of timestamps and their frame match scores
def calc_frame_match_scores(file_path, intervals=15):
    cap = cv2.VideoCapture(file_path)
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    match_scores_and_timestamps = []
    
    def on_frame(curr_frame, frame_no):
        frame_match_score = max([calc_similarity(img, curr_frame)
                            for img in image_data])
        match_scores_and_timestamps.append(
                (int(frame_no / video_fps), frame_match_score))
        
    process_video(file_path, on_frame, intervals=intervals)

    match_scores = [datum[1]
                          for datum in match_scores_and_timestamps]
    timestamps = [datum[0] for datum in match_scores_and_timestamps]
    return match_scores, timestamps

def apply_bool_filter(frame_match_scores):
    frame_match_threshold = calc_frame_match_threshold(frame_match_scores)
    return [
        score > frame_match_threshold for score in frame_match_scores]

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
