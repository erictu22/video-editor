
import os

import cv2
from edit_videos import calc_similarity

from process_video import process_video

SLICE_WIDTH = 425
SLICE_HEIGHT = 720  

def fetch_frames(file_path):
    frames = []

    def on_frame(curr_frame, frame_no):
        frames.append(curr_frame)

    process_video(file_path, on_frame, intervals=10)
    return frames

def rate_frames(frames):
    image_directory = 'image-data/gameplay'
    images = [cv2.imread(f'{image_directory}/{x}') for x in os.listdir(image_directory)]
    frame_match_scores = []

    for frame in frames:
        frame_match_score = max([calc_similarity(img, frame) for img in images])

        # convert frame to grayscale, but keep the color
        grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        grayscale_frame = cv2.cvtColor(grayscale_frame, cv2.COLOR_GRAY2BGR)
        difference = cv2.absdiff(grayscale_frame, frame)

        # quantify the difference matrix into a single number
        grayscale_score = difference.sum() / (difference.shape[0] * difference.shape[1] * difference.shape[2])
        print(grayscale_score)

        frame_match_scores.append(frame_match_score)
    return frame_match_scores

def slice(frames):
    slices = []
    for frame in frames:
        # slice up frame so that it's 425 pixels wide and 720 pixels tall
        _, width = frame.shape[:2]
        slice_start = int(width / 2) - int(SLICE_WIDTH / 2) + 60
        slice = frame[0:SLICE_HEIGHT, slice_start:slice_start + SLICE_WIDTH]
        slices.append(slice)
    return slices

def stitch(slices):
    # pick three frame slices and stich them together
    thumbnails = []
    thumbnail = cv2.hconcat([slices[0], slices[1], slices[2]])
    thumbnails.append(thumbnail)
    return thumbnails
    

def save_result(video_file_path, thumbnail, id):
    try:
        os.mkdir('thumbnails')
    except FileExistsError:
        pass
    
    # create a directory with the video file name
    thumbnail_dir = f'thumbnails/{video_file_path.split(".")[0]}'
    try:
        os.mkdir(thumbnail_dir)
    except FileExistsError:
        pass

    # write the thumbnail to the directory
    file_name = f'{thumbnail_dir}/thumbnail_{id}.jpg'
    cv2.imwrite(file_name, thumbnail)


if __name__ == '__main__':
    video_files = [x for x in os.listdir('cuts') if x != '.DS_Store']
    for video_file in video_files:
        frames = fetch_frames(f'cuts/{video_file}')

        frame_scores = rate_frames(frames)
        
        # find indices for thee highest-scoring frames
        best_indices = sorted(range(len(frame_scores)), key=lambda i: frame_scores[i])[-3:]
        frames = [frames[i] for i in best_indices]

        slices = slice(frames)
        thumbnails = stitch(slices)
        for i, thumbnail in enumerate(thumbnails):
            save_result(video_file, thumbnail, i)
