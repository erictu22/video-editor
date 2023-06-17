import cv2
import numpy as np
from skimage.metrics import structural_similarity

def calculate_busyness(image):
    # Apply Canny edge detection
    edges = cv2.Canny(image, 100, 200)

    # Calculate the percentage of edge pixels
    total_pixels = image.shape[0] * image.shape[1]
    edge_pixels = np.sum(edges) / 255  # Divide by 255 to get the count of white pixels

    busyness_percentage = (edge_pixels / total_pixels) * 100

    return busyness_percentage

def calc_color_score(frame):
    # convert frame to grayscale, but keep the color
    grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grayscale_frame = cv2.cvtColor(grayscale_frame, cv2.COLOR_GRAY2BGR)
    difference = cv2.absdiff(grayscale_frame, frame)

    # quantify the difference matrix into a single number

    width, height, _ = frame.shape
    grayscale_score = int(difference.sum() / (width * height))
    return grayscale_score

def calc_similarity_score(frame, images):
    similarity_score = max([calc_similarity(img, frame) for img in images]) * 10
    return similarity_score

def calc_similarity(image1, image2):
    # Convert the images to grayscale
    gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    resize_dimensions = (360, 480)
    resized_image1 = cv2.resize(gray_image1, resize_dimensions)
    resized_image2 = cv2.resize(gray_image2, resize_dimensions)

    # Compute the SSIM between the two images
    (score, diff) = structural_similarity(
        resized_image1, resized_image2, full=True)

    return score