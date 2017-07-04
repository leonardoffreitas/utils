from os import listdir as list_dir
from os import chdir
from os import getcwd
from os.path import splitext
from os.path import isfile as is_file
from os.path import isdir as is_dir
from os.path import realpath as real_path

from contextlib import contextmanager

@contextmanager
def working_directory(path):
    '''Simple context manager to change the working directory'''
    current_dir = getcwd()
    chdir(path)
    try:
        yield
    finally:
        chdir(current_dir)
