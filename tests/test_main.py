
import time
import json
import os.path
from sys import platform as _platform
from os import path
import os


def test_fake():
    assert 1

def test_ensure_readme():
    CURRENT_DIR = os.getcwd()
    assert os.path.isfile( CURRENT_DIR + '/README.md')
    
