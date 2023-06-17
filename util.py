import os
import sys

def block_print():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enable_print():
    sys.stdout = sys.__stdout__

def safe_mkdir(dir_name):
    try:
        os.mkdir(dir_name)
    except:
        pass

def pick_n_highest_scores(arr, n, calc_score):
    # pick the n highest scores from arr
    # calc_score is a function that takes in an element of arr and returns a score
    # returns a list of tuples (score, element)
    # arr is not sorted
    scores = [(calc_score(x), x) for x in arr]
    scores.sort(key=lambda x: x[0], reverse=True)
    return [pair[1] for pair in scores[:n]]