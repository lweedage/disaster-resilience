import csv
import math
import re
import numpy as np
import settings as settings
import plotly.graph_objects as go
import scipy.stats as st
import enum
import pickle
import os


def from_data(name):
    if os.path.exists(name):
        return pickle.load(open(name, 'rb'))
    else:
        return None

def to_data(data, name):
    pickle.dump(data, open(name, 'wb'), protocol=4)

def distance_2d(x1, y1, x2, y2):
    dist_x = abs(x1 - x2)
    dist_y = abs(y1 - y2)
    return math.sqrt(dist_x ** 2 + dist_y ** 2)

def distance_3d(h1, h2, x1=None, y1=None, x2=None, y2=None, d2d=None):
    d_2d = d2d
    if d_2d is None:
        d_2d = distance_2d(x1, y1, x2, y2)
    dist_h = abs(h1 - h2)
    return math.sqrt(d_2d ** 2 + dist_h ** 2)

def to_pwr(db):
    return 10 ** (db / 10)

def to_db(pwr):
    return 10 * math.log10(pwr)

def dbw_to_dbm(pwr):
    return pwr + 30


@enum.unique
class BaseStationRadioType(enum.Enum):
    NR = enum.auto()
    LTE = enum.auto()
    GSM = enum.auto()
    UMTS = enum.auto()



@enum.unique
class AreaType(enum.Enum):
    UMA = enum.auto()
    UMI = enum.auto()
    RMA = enum.auto()


def str_to_float(string):
    s = re.sub(r'[^\d.]+', '', string)
    return float(s)

def find_cities(municipality):
    with open("data/cities_per_province") as f:
        data = f.read()
        data = data.split('\n')
    if municipality == 'Netherlands':
        print(municipality)
        cities = []
        for line in data:
            line = line.split(':')
            for city in line[1].split(','):
                cities.append(city)
        print(cities)
        return cities
    else:
        for line in data:
            line = line.split(':')
            if line[0] == municipality:
                return line[1].split(',')

def find_provider(frequency): # frequency in MHz
    frequency_dict = {(758, 768): 'Vodafone', (768, 778): 'KPN', (778, 788): 'T-Mobile', (791, 801): 'T-Mobile', (801, 811): 'Vodafone', (811, 821): 'KPN', (925, 935): 'Vodafone', (935, 945): 'KPN', (945, 960): 'T-Mobile',
     (1452, 1467): 'Vodafone', (1467, 1482): 'KPN', (1482, 1492): 'T-Mobile', (1805, 1825): 'Vodafone', (1825, 1845): 'KPN', (1845, 1875): 'T-Mobile', (2110, 2124.9): 'Vodafone', (2124.9, 2139.7): 'KPN',
     (2139.7, 2149.7): 'T-Mobile', (2149.7, 2154.7): 'KPN', (2154.7, 2159.7): 'Vodafone', (2159.7, 2170): 'T-Mobile', (2110, 2130): 'Vodafone', (2130, 2150): 'T-Mobile', (2150, 2170): 'KPN', (2565, 2590): 'T-Mobile',
                      (2590, 2620): 'KPN', (2620, 2630): 'Vodafone', (2630, 2650): 'Vodafone', (2650, 2655): 'T-Mobile', (2655, 2665): 'KPN', (2665, 2685): 'T-Mobile', (2685, 2690): 'T-Mobile'}
    if frequency == 3275: # one BS in Poeldijk has the wrong frequency in the data set - this should be 2672.5 MHz
        frequency = 2672.5
    for key, provider in frequency_dict.items(): #TODO explain this method in paper
        (min_freq, max_freq) = key
        if min_freq <= frequency < max_freq:
            bandwidth = max_freq - min_freq
            # bandwidth = min(frequency-min_freq, max_freq - frequency) * 2
            # if bandwidth >= 20:
            #     bandwidth = 20
            # elif bandwidth >= 15:
            #     bandwidth = 15
            # elif bandwidth >= 10:
            #     bandwidth = 10
            # elif bandwidth >= 5:
            #     bandwidth = 5
            # elif bandwidth >= 3:
            #     bandwidth = 3
            # else:
            #     bandwidth = 1.4
            return provider, bandwidth*10**6
    return 'None', 0

def find_closest_BS(user_coords, x_bs, y_bs):
    x = np.array(x_bs) - user_coords[0]
    y = np.array(y_bs) - user_coords[1]
    return np.argsort(x ** 2 + y ** 2)

def average(data):
    if len(data) > 0:
        return (sum(data) / len(data))
    else:
        return None

def find_geo(coord_1, coord_2):
    dy = coord_2[1] - coord_1[1]
    dx = coord_2[0] - coord_1[0]
    radians = math.atan2(dy, dx)
    return np.degrees(radians)