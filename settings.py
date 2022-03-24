from pathlib import Path
import os
import pandas as pd
import numpy as np
# code from Bart Meyers

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22',
          '#17becf'] * 1000
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

ROOT_DIR = Path(__file__).parent

BS_PATH = os.path.join(ROOT_DIR, "data", "antennas.json")

SAVE_IN_CSV = False
CREATE_PLOT = False

UE_CAPACITY_MIN = 10
UE_CAPACITY_MAX = 100

MINIMUM_POWER = -80  # dbm

# CITY SPECIFIC PARAMETERS
# percentage of population using the network
ACTIVITY = 0.007  # 0.7%

# Average height of buildings in an area (used for RMa 5G NR only)
AVG_BUILDING_HEIGHT = 15  # current number based on average two-story building
AVG_STREET_WIDTH = 10

# BASE STATION PROPERTIES
BS_RANGE = 5000  # maximum range of base stations based on the fact that UMa and UMi models cannot exceed 5km

MCL = 70  # in dBm # minimum coupling loss?

# User equipment properties
UE_HEIGHT = 1.5  # height in meters

# to calculate the noise power
BOLTZMANN = 1.38e-23
TEMPERATURE = 283.15

BEAMWIDTH3DB = 65

MINIMUM_SNR = 5 # dB
