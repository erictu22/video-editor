import cv2
from math import *
import numpy
from skimage.metrics import structural_similarity
from time import sleep

samples = [cv2.imread(f'image-data/{x}.png') for x in ['lane','shop', 'tab', 'spawn']]

SAMPLE_INTERVALS = 30 # seconds
START_PERIOD = 5
END_PERIOD = 6

def get_cuts(video_id, start=0):
    data = play_video(video_id=video_id, start=start, should_record_data=True, should_display=False)
    
    scores = [datum[1] for datum in data]
    frame_nums = [datum[0] for datum in data]
    first_q = numpy.percentile(scores, 25)
    third_q = numpy.percentile(scores, 75)
    thresh = (third_q - first_q) / 2 + first_q
    is_ingame_checks = [score > thresh for score in scores]

    cuts = []
    start = -1
    stop = -1
    for i in range(0, len(is_ingame_checks) - END_PERIOD):
        if start == -1 and all(is_ingame for is_ingame in is_ingame_checks[i: i + START_PERIOD]):
            start = frame_nums[i]
        elif start != -1 and stop == -1 and all(not is_ingame for is_ingame in is_ingame_checks[i: i + END_PERIOD]):
            stop = frame_nums[i]
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
                    data.append((frame_no, score))
                print(f'id:{video_id} Progress:{round(frame_no / total_frames * 100, 2)}%', end='\r')
        else:
            break
        frame_no += 1
    cap.release()
    return data


videos = [1762866433, 1760630552]
play_video(1760630552, 216000)