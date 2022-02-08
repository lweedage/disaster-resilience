from pathlib import Path
import os

ROOT_DIR = Path(__file__).parent

BS_PATH = os.path.join(ROOT_DIR, "data", "antennas.json")
CITY_PATH = os.path.join(ROOT_DIR, "data", "city.json")

SAVE_IN_CSV = False
CREATE_PLOT = False
SAVE_CSV_PATH = os.path.join(ROOT_DIR, "results", "disaster_power_mmwave_100.csv")

AMOUNT_THREADS = None

UE_CAPACITY_MIN = 10
UE_CAPACITY_MAX = 100

SEVERITY_ROUNDS = 10
ROUNDS_PER_SEVERITY = 4
ROUNDS_PER_USER = 75

MINIMUM_POWER = -80  # dbm

# CITY SPECIFIC PARAMETERS
# percentage of population using the network
ACTIVITY = 0.007  # 0.7%
# Average height of buildings in an area (used for RMa 5G NR only)
AVG_BUILDING_HEIGHT = 14  # current number based on average two-story building
AVG_STREET_WIDTH = 10

# BASE STATION PROPERTIES
BS_RANGE = 5000  # maximum range of base stations based on the fact that UMa and UMi models cannot exceed 5km

MCL = 70  # in dbm
HEIGHT_ABOVE_BUILDINGS = 20  # Average height a BS is above buildings (used for LTE)
CARRIER_FREQUENCY = 2000  # TODO remove?
BASE_POWER = 43  # TODO remove
G_TX = 15  # dB
G_RX = 0  # dB

CHANNEL_BANDWIDTHS = [20, 15, 10, 5, 3, 1.4]
SIGNAL_NOISE = -100  # dBm

# mmWave channel properties
MMWAVE_PROBABILITY = 1
MMWAVE_FREQUENCY = 26000  # 26GHz in MHz
MMWAVE_POWER = 60  # dBm
BEAMFORMING_GAIN = G_TX + 10  # dB
BEAMFORMING_CLEARANCE = 10  # degrees around the beam

# User equipment properties
UE_HEIGHT = 1.5  # height in meters

# RISKS ENABLED
# if a large disaster occurred, for instance a natural disaster or a depending failure
LARGE_DISASTER = True
POWER_OUTAGE = True
RADIUS_PER_SEVERITY = 1000

# malicious attacks on a certain region, for instance a DDoS
MALICIOUS_ATTACK = False
PERCENTAGE_BASE_STATIONS = 0.5
FUNCTIONALITY_DECREASED_PER_SEVERITY = 0.1

# increasing requested data
INCREASING_REQUESTED_DATA = False
OFFSET = 10
DATA_PER_SEV = 10
WINDOW_SIZE = 10
