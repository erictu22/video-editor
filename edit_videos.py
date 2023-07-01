import cv2
from math import *
import numpy
import moviepy.editor as me
import os
import uuid
from const import STREAMER

from process_video import process_video
from scoring import calc_similarity

image_data_dir = f'image-data/{STREAMER}'
image_data = [cv2.imread(f'{image_data_dir}/{x}')
              for x in os.listdir(image_data_dir) if x != '.DS_Store']

def cut_video(file_path):
    cuts = get_cuts(file_path)
    video = me.VideoFileClip(file_path)
    print("Cutting at " + str(cuts))
    for cut in cuts:
        file_name = str(uuid.uuid4())
        clip = video.subclip(cut[0], cut[1])
        clip.write_videofile(f'cuts/{file_name}.mp4', temp_audiofile=f'temp/temp-audio-{file_name}.m4a',
                             remove_temp=True, codec="libx264", audio_codec="aac")

    os.remove(file_path)

def get_cuts(file_path, intervals = 30, start_grace = 5, end_grace = 5):
    frame_match_scores, timestamps = calc_frame_match_scores(file_path, intervals)
    is_frame_match = apply_bool_filter(frame_match_scores)

    cuts = []
    start_time = -1
    stop_time = -1
    end_offset = 2
    for intv in range(0, len(is_frame_match)):
        is_ingame = all(is_frame_match[intv: intv + start_grace])
        is_game_over = all(
            not is_frame_match for is_frame_match in is_frame_match[intv: intv + end_grace])

        if start_time == -1 and is_ingame:
            start_time = timestamps[intv]
        elif start_time != -1 and stop_time == -1 and is_game_over:
            stop_time = timestamps[intv]
            cuts.append((start_time, stop_time + end_offset))
            start_time = -1
            stop_time = -1
        elif start_time != -1 and intv + end_grace >= len(is_frame_match): # video is over
            stop_time = timestamps[intv]
            cuts.append((start_time, stop_time + end_grace))
            break

    return cuts

# Returns a list of timestamps and their frame match scores
def calc_frame_match_scores(file_path, intervals):
    cap = cv2.VideoCapture(file_path)
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    match_scores_and_timestamps = []
    
    def on_frame(curr_frame, frame_no):
        frame_match_score = max([calc_similarity(img, curr_frame)
                            for img in image_data])
        match_scores_and_timestamps.append(
                (int(frame_no / video_fps), frame_match_score))
        
    process_video(file_path, on_frame, intervals)

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
