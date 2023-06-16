
import os

import cv2

from process_video import process_video

SLICE_WIDTH = 425
SLICE_HEIGHT = 720  

def fetch_frames(file_path):
    frames = []

    def on_frame(curr_frame, frame_no):
        # TODO - add logic to only save frames that are 'high quality' candidates
        frames.append(curr_frame)

    process_video(file_path, on_frame, intervals=10)
    return frames

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
        candidates = fetch_frames(f'cuts/{video_file}')
        slices = slice(candidates)
        thumbnails = stitch(slices)
        for i, thumbnail in enumerate(thumbnails):
            save_result(video_file, thumbnail, i)
