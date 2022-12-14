import os

CWD = os.path.dirname(__file__)
BASE_DIR = os.path.abspath(os.path.join(CWD, '..'))
INPUT_BASE = os.path.join(BASE_DIR, 'input')
OUTPUT_BASE = os.path.join(BASE_DIR, 'output')
TEMP_BASE = os.path.join(BASE_DIR, 'temp')
CONFIG_PATH = os.path.join(BASE_DIR, 'config')

