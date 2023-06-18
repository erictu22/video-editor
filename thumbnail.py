
import multiprocessing
import os
import random

import cv2
from edit_videos import calc_similarity
from image_effects import add_border

from process_video import process_video
from scoring import calc_color_score, calc_similarity_score, calculate_busyness
from util import add_weight, pick_n_highest_scores, safe_mkdir
import shutil
from PIL import ImageDraw

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
    images = [cv2.imread(f'{image_directory}/{x}')
              for x in os.listdir(image_directory)]
    frame_match_scores = []

    for frame in frames:
        similarity_score = calc_similarity_score(frame, images)
        color_score = calc_color_score(frame)
        busyness = calculate_busyness(frame)

        frame_match_score = color_score * \
            add_weight(similarity_score, 3) * busyness

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


def add_effects(thumbnails):
    output = []
    for image in thumbnails:
        # pick a random color that's bright
        brightness = 140
        angry_colors = [
            (0, 0, 255),   # Red
            (0, 69, 255),  # Orange-Red
            (0, 165, 255),  # Orange
            (71, 99, 255)  # Tomato
        ]
        color = random.choice(angry_colors)

        # add a colored border to the image
        thickness = 32
        image = add_border(image, color, thickness)

        output.append(image)

    return output


def save_result(video_file_path, thumbnail, id):
    safe_mkdir('thumbnails')

    # create a directory with the video file name
    thumbnail_dir = f'thumbnails/{video_file_path.split("/")[-1].split(".")[0]}'
    safe_mkdir(thumbnail_dir)

    # write the thumbnail to the directory
    file_name = f'{thumbnail_dir}/thumbnail_{id}.jpg'
    cv2.imwrite(file_name, thumbnail)


def create_thumbnail(video_file_path, top_n=10):
    frames = fetch_frames(video_file_path)
    print(f'Scoring frames for {video_file_path}')
    frame_scores = rate_frames(frames)

    # find indices for the highest-scoring frames
    best_indices = sorted(range(len(frame_scores)),
                          key=lambda i: frame_scores[i])[-1 * top_n:]
    frames = [frames[i] for i in best_indices]

    slices = slice(frames)
    thumbnails = stitch(slices)
    thumbnails = add_effects(thumbnails)

    thumbnails = pick_n_highest_scores(
        thumbnails, NUM_CHOICES, calculate_busyness)

    for i, thumbnail in enumerate(thumbnails):
        save_result(video_file_path, thumbnail, i)


if __name__ == '__main__':
    video_directory = 'cuts'
    video_files = [x for x in os.listdir(video_directory) if x != '.DS_Store']
    file_paths = [f'{video_directory}/{x}' for x in video_files]
    try:
        shutil.rmtree('thumbnails')
    except FileNotFoundError:
        pass

    pool = multiprocessing.Pool(processes=8)
    pool.map(create_thumbnail, file_paths)
    pool.close()
    pool.join()
