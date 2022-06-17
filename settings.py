from pathlib import Path
import os
import pandas as pd
import numpy as np
import seaborn as sns

# code from Bart Meyers

colors = sns.color_palette("Paired", n_colors=100)

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

ROOT_DIR = Path(__file__).parent

BS_PATH = os.path.join(ROOT_DIR, "data", "antennas.json")

# Average height of buildings in an area (used for RMa 5G NR only)
AVG_BUILDING_HEIGHT = 15  # current number based on average two-story building
AVG_STREET_WIDTH = 10

# BASE STATION PROPERTIES
BS_RANGE = 5000  # maximum range of base stations based on the fact that UMa and UMi models cannot exceed 5km

# User equipment properties
UE_HEIGHT = 1.5  # height in meters

# to calculate the noise power
BOLTZMANN = 1.38e-23
TEMPERATURE = 283.15

VERTICAL_BORE = 8  # degrees

VERTICAL_BEAMWIDTH3DB = 65
HORIZONTAL_BEAMWIDTH3DB = 65

MINIMUM_SNR = 5  # dB

# RATE_REQUIREMENT, FRACTION = {1: 40e6, 2: 150e6, 3: 1000e6}, {1: 0.77, 2: 0.2, 3: 0.04}
RATE_REQUIREMENT, FRACTION = {1: 10e6, 2: 100e6, 3: 1000e6}, {1: 1, 2: 0, 3: 0}

CUTOFF_VALUE_INTERFERENCE = 2  # the x highest signal BSs will not interfere.
POWER_PERCENTAGE = 0.75

#ASSUMPTION maybe change the power percentage!
