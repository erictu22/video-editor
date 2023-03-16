import numpy
from math import *

def get_score_image(frame):
    y_start = 0
    y_end = floor(0.287 * frame.shape[0])
    x_start = floor(0.855 * frame.shape[1])
    x_end = frame.shape[1] - 1
    
    return numpy.array([row[x_start:x_end] for row in frame[y_start:y_end]])