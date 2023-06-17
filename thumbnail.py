
import multiprocessing
import os
import random

import cv2
from edit_videos import calc_similarity

from process_video import process_video
from scoring import calc_color_score, calculate_busyness
from util import pick_n_highest_scores, safe_mkdir

NUM_CHOICES = 5
BEST_N = 10

SLICE_WIDTH = 640
SLICE_HEIGHT = 720  

def fetch_frames(file_path):
    frames = []

    def on_frame(curr_frame, frame_no):
        frames.append(curr_frame)

    process_video(file_path, on_frame, intervals=5)
    return frames

def rate_frames(frames):
    image_directory = 'image-data/action'
    images = [cv2.imread(f'{image_directory}/{x}') for x in os.listdir(image_directory)]
    frame_match_scores = []

    for frame in frames:
        similarity_score = max([calc_similarity(img, frame) for img in images])
        color_score = calc_color_score(frame)
        busyness = calculate_busyness(frame)

        frame_match_score = color_score * similarity_score * busyness

        frame_match_scores.append(frame_match_score)
    return frame_match_scores

def slice(frames):
    slices = []
    for frame in frames:
        # slice up frame so that it's 640 pixels wide and 720 pixels tall
        _, width = frame.shape[:2]
        slice_start = int(width / 2) - int(SLICE_WIDTH / 2)
        slice = frame[0:SLICE_HEIGHT, slice_start:slice_start + SLICE_WIDTH]
        slices.append(slice)
    return slices

def stitch(slices):
    # pick two frame slices and stich them together
    thumbnails = []
    
    # randomly stich together three slices. do this 10 times
    for _ in range(10):
        stack = slices.copy()

        # scramble the stack
        random.shuffle(stack)

        # pick three slices
        thumbnail = cv2.hconcat([stack.pop() for _ in range(2)])
        thumbnails.append(thumbnail)

    return thumbnails
    

def save_result(video_file_path, thumbnail, id):
    safe_mkdir('thumbnails')
    
    # create a directory with the video file name
    thumbnail_dir = f'thumbnails/{video_file_path.split(".")[0]}'
    try:
        os.mkdir(thumbnail_dir)
    except FileExistsError:
        pass

    # write the thumbnail to the directory
    file_name = f'{thumbnail_dir}/thumbnail_{id}.jpg'
    cv2.imwrite(file_name, thumbnail)

def create_thumbnail(video_file_name):
    frames = fetch_frames(f'cuts/{video_file_name}')
    print(f'Scoring frames for {video_file_name}')
    frame_scores = rate_frames(frames)
    
    # find indices for the highest-scoring frames
    best_indices = sorted(range(len(frame_scores)), key=lambda i: frame_scores[i])[-50:]
    frames = [frames[i] for i in best_indices]

    slices = slice(frames)
    thumbnails = stitch(slices)

    thumbnails = pick_n_highest_scores(thumbnails, NUM_CHOICES, calculate_busyness)

    for i, thumbnail in enumerate(thumbnails):
        save_result(video_file_name, thumbnail, i)


if __name__ == '__main__':
    video_files = [x for x in os.listdir('cuts') if x != '.DS_Store']
    os.rmdir('thumbnails')

    pool = multiprocessing.Pool(processes=8)
    pool.map(create_thumbnail, video_files)
    pool.close()
    pool.join()
