
import os

import cv2

from process_video import process_video

def create_thumbnails(file_path):

    frame_slices = []

    def on_frame(curr_frame, frame_no):
        # slice up frame so that it's 425 pixels wide and 720 pixels tall
        curr_frame = curr_frame[0:720, 0:425]
        frame_slices.append(curr_frame)

    process_video(file_path, on_frame, intervals=20)

    # pick three frame slices and stich them together
    thumbnail = cv2.hconcat([frame_slices[0], frame_slices[1], frame_slices[2]])

    # write thumbnail to file
    file_name = f'{file_path}/thumbnail.jpg'
    cv2.imwrite('thumbnail.jpg', thumbnail)

if __name__ == '__main__':
    video_files = [x for x in os.listdir('cuts') if x != '.DS_Store']
    for video_file in video_files:
        create_thumbnails(f'cuts/{video_file}')