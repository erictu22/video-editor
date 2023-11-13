
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

NUM_THUMBNAILS = 10
BEST_N = 15

SLICE_WIDTH = 640
SLICE_HEIGHT = 720

INTERVALS = 5

def fetch_frames(file_path):
    frames = []

    def on_frame(curr_frame, frame_no):
        frames.append(curr_frame)

    process_video(file_path, on_frame, intervals=INTERVALS)
    return frames


def rate_frame(frame):
    image_directory = 'image-data/action'
    images = [cv2.imread(f'{image_directory}/{x}')
              for x in os.listdir(image_directory) if x != '.DS_Store']
    return calc_similarity_score(frame, images) + calc_color_score(frame) * 100 + calculate_busyness(frame) * 100

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

    # randomly stich together three slices
    for _ in range(NUM_THUMBNAILS):
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
        angry_colors = [(0, 69, 255),(0, 165, 255),(71, 99, 255)]
        random_color = random.choice(angry_colors)

        # add a colored border to the image
        thickness = 64
        image = add_border(image, random_color, thickness)

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


def create_thumbnail(video_file_path, top_n=BEST_N):
    frames = fetch_frames(video_file_path)
    print(f'Scoring frames for {video_file_path}')
    best_frames = pick_n_highest_scores(frames, top_n, rate_frame)
    slices = slice(best_frames)
    thumbnails = stitch(slices)
    thumbnails = add_effects(thumbnails)

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
