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

VERTICAL_BORE = np.radians(8)  # degrees

VERTICAL_BEAMWIDTH3DB = np.radians(65)
HORIZONTAL_BEAMWIDTH3DB = 65

MINIMUM_SNR = 5 # dB

# RATE_REQUIREMENT, FRACTION = {1: 40e6, 2: 150e6, 3: 1000e6}, {1: 0.77, 2: 0.2, 3: 0.04}
RATE_REQUIREMENT, FRACTION = {1: 42e6, 2: 150e6, 3: 1000e6}, {1: 1, 2: 0, 3: 0}

CUTOFF_VALUE_INTERFERENCE = 0  # the x highest signal BSs will not interfere.
POWER_PERCENTAGE = 0.90

#ASSUMPTION maybe change the power percentage!

channels = {'Drenthe': {'KPN': 2906, 'Vodafone': 1329, 'T-Mobile': 3047, 'all_MNOs': 2906+1329+3047},
            'Flevoland': {'KPN': 2504, 'Vodafone': 1008, 'T-Mobile': 2486, 'all_MNOs': 2504+1008+2486},
            'Friesland': {'KPN': 2466, 'Vodafone': 1225, 'T-Mobile': 2888, 'all_MNOs': 2466+1225+2888},
            'Gelderland': {'KPN': 13545, 'Vodafone': 4873, 'T-Mobile': 12396, 'all_MNOs': 13545+4873+12396},
            'Groningen': {'KPN': 2734, 'Vodafone': 1280, 'T-Mobile': 2666, 'all_MNOs': 2734+1280+2666},
            'Limburg': {'KPN': 8622, 'Vodafone': 3317, 'T-Mobile': 7969, 'all_MNOs': 8622+3317+7969},
            'Noord-Brabant': {'KPN': 16832, 'Vodafone': 5946, 'T-Mobile': 16324, 'all_MNOs':16832+5946+16324},
            'Noord-Holland': {'KPN': 15086, 'Vodafone': 5899, 'T-Mobile': 15336, 'all_MNOs': 15086+5899+15336},
            'Overijssel': {'KPN': 6480, 'Vodafone': 2557, 'T-Mobile': 6505, 'all_MNOs': 6480+2557+6505},
            'Utrecht': {'KPN': 7743, 'Vodafone': 2740, 'T-Mobile': 7313, 'all_MNOs': 7743+2740+7313},
            'Zeeland': {'KPN': 2278, 'Vodafone': 984, 'T-Mobile': 2689, 'all_MNOs': 2278+984+2689},
            'Zuid-Holland': {'KPN': 18447, 'Vodafone': 6711, 'T-Mobile': 19853, 'all_MNOs': 18447+6711+19853}}