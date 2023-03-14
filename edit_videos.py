import cv2
from math import *
import numpy
from skimage.metrics import structural_similarity

def cut_video(video_id):
    cap = cv2.VideoCapture(f'videos/{video_id}.mp4')
    cap.set(cv2.CAP_PROP_POS_FRAMES,1000)
    frame_no = 0
    
    while(cap.isOpened()):
        frame_exists, curr_frame = cap.read()
        if frame_exists:
            cv2.imshow('frame', curr_frame)
            cv2.waitKey(1)

            if frame_no % 60 == 0:
                compare_images(cv2.imread('image-data/rift'), curr_frame)
        else:
            break
        frame_no += 1

    cap.release()

def is_in_game(frame):
    y_start = 0
    y_end = floor(0.287 * frame.shape[0])
    x_start = floor(0.855 * frame.shape[1])
    x_end = frame.shape[1] - 1
    
    score = numpy.array([row[x_start:x_end] for row in frame[y_start:y_end]])

def compare_images(image1, image2):
    # Convert the images to grayscale
    gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    resized_image1 = cv2.resize(gray_image1, (720, 1280))
    resized_image2 = cv2.resize(gray_image2, (720, 1280))

    # Compute the SSIM between the two images
    (score, diff) = structural_similarity(resized_image1, resized_image2, full=True)

    if score > 0.4:
        print("The images are similar " + str(score))
    else:
        print("The images are not similar" + str(score))

cut_video(1760630552)