import os

TESTS_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.abspath(os.path.join(TESTS_DIR, 'data'))
CONFIGS = os.path.join(DATA_DIR, 'configs')
INPUTS = os.path.join(DATA_DIR, 'inputs')
EXPECTEDS = os.path.join(DATA_DIR, 'expecteds')
ACTUALS = os.path.join(DATA_DIR, 'actuals')
