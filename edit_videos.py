import cv2
from math import *
import numpy
from skimage.metrics import structural_similarity
from time import sleep
import moviepy.editor as me
import os
samples = [cv2.imread(f'image-data/{x}') for x in os.listdir('image-data')]

SAMPLE_INTERVALS = 45 # seconds
START_PERIOD = 3
END_PERIOD = 6

def cut_video(video_id):
    cuts = get_cuts(video_id)
    video = me.VideoFileClip(f'videos/{video_id}.mp4')

    for cut in cuts:
        clip = video.subclip(cut[0], cut[1])

        m, s = divmod(cut[0], 60)
        h, m = divmod(m, 60)
        clip.write_videofile(f'cuts/{video_id}_{h}h{m}m{s}s.mp4', temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")

def get_cuts(video_id, start=0):
    data = play_video(video_id=video_id, start=start, should_record_data=True, should_display=False)
    
    scores = [datum[1] for datum in data]
    timestamps = [datum[0] for datum in data]
    first_q = numpy.percentile(scores, 25)
    third_q = numpy.percentile(scores, 75)
    thresh = (third_q - first_q) / 2 + first_q
    is_ingame_checks = [score > thresh for score in scores]

    cuts = []
    start = -1
    stop = -1
    for i in range(0, len(is_ingame_checks) - END_PERIOD):
        if start == -1 and all(is_ingame for is_ingame in is_ingame_checks[i: i + START_PERIOD]):
            start = timestamps[i]
        elif start != -1 and stop == -1 and all(not is_ingame for is_ingame in is_ingame_checks[i: i + END_PERIOD]):
            stop = timestamps[i + 1]
            cuts.append((start, stop))
            start = -1
            stop = -1

    print(cuts)
    return cuts

def similarity(image1, image2):
    # Convert the images to grayscale
    gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    resized_image1 = cv2.resize(gray_image1, (720, 1280))
    resized_image2 = cv2.resize(gray_image2, (720, 1280))

    # Compute the SSIM between the two images
    (score,diff) = structural_similarity(resized_image1, resized_image2, full=True)

    return score

def play_video(video_id, start, should_record_data=False, should_display=True):
    cap = cv2.VideoCapture(f'videos/{video_id}.mp4')
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.set(cv2.CAP_PROP_POS_FRAMES,start)
    frame_no = 0

    data = []
    while(cap.isOpened()):
        frame_exists, curr_frame = cap.read()
        if frame_exists:
            if frame_no % int(SAMPLE_INTERVALS * video_fps) == 0:
                if should_display:
                    cv2.imshow('frame',curr_frame)
                    cv2.waitKey(1)
                if should_record_data:
                    score = max([similarity(img, curr_frame) for img in samples])
                    data.append((int(frame_no / video_fps), score))
                print(f'id:{video_id} Progress:{round(frame_no / total_frames * 100, 2)}%', end='\r')
        else:
            break
        frame_no += 1
    cap.release()
    return data

videos = [1762866433, 1760630552]
cut_video(1762866433)