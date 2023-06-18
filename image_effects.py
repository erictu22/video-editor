import cv2
import numpy as np

def add_border(image, border_color, border_thickness):
    image_with_border= cv2.rectangle(
        image,
        (0, 0),
        (image.shape[1] - 1, image.shape[0] - 1),
        border_color,
        thickness=border_thickness
    )

    return image_with_border
