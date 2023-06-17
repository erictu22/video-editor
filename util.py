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