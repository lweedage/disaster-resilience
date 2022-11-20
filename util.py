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
        return cities
    else:
        for line in data:
            line = line.split(':')
            if line[0] == municipality:
                return line[1].split(',')

def find_provider(frequency): # frequency in MHz
    frequency_dict = {(758, 768): 'Vodafone', (768, 778): 'KPN', (778, 788): 'T-Mobile', (791, 801): 'T-Mobile', (801, 811): 'Vodafone', (811, 821): 'KPN', (925, 935): 'Vodafone', (935, 945): 'KPN', (945, 960): 'T-Mobile',
     (1452, 1467): 'Vodafone', (1467, 1482): 'KPN', (1482, 1492): 'T-Mobile', (1805, 1825): 'KPN', (1825, 1845): 'Vodafone', (1845, 1875): 'T-Mobile', (2110, 2130): 'Vodafone', (2130, 2150): 'T-Mobile', (2150, 2170): 'KPN', (2565, 2590): 'T-Mobile',
                      (2590, 2620): 'KPN', (2620, 2630): 'Vodafone', (2630, 2650): 'Vodafone', (2650, 2655): 'T-Mobile', (2655, 2665): 'KPN', (2665, 2685): 'T-Mobile', (2685, 2690): 'T-Mobile'}

    BW = dict()
    BW[4] = {2652}
    BW[5] = {942.2, 2152.6, 957.4}
    BW[10] = {773, 810, 2660, 796, 950, 1487, 783, 1850, 763, 806, 2644.4, 816}
    BW[15] = {1474.5, 2137.5, 2572.5, 1459.5, 2117.5, 2672.5}
    BW[20] = {1815, 2160, 1865, 2580, 2675, 1835, 2120, 2630}
    BW[30] = {2605, 1860}

    if frequency == 3275.0: # one BS in Poeldijk has the wrong frequency in the data set - this should be 2672.5 MHz
        frequency = 2672.5
    for key, provider in frequency_dict.items(): #TODO explain this method in paper
        (min_freq, max_freq) = key
        if min_freq <= frequency < max_freq:
            for key, values in BW.items():
                if frequency in BW[key]:
                    bandwidth = key
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

def municipality_dict():
    with open("data/zipcode_to_municipality_number.csv", "r") as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None)
        lines = list(reader)

    municipality_code = dict()
    for line in lines:
        municipality_code[line[0][:-2]] = int(line[3])
    municipality_code['9914'] = 24
    municipality_code['9915'] = 24

    with open("data/municipalities.csv", "r") as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None)
        lines = list(reader)

    code = dict()
    for line in lines:
        code[int(line[0])] = line[1]

    mun_dict = dict()
    for k, v in municipality_code.items():
        if code[v] in mun_dict.keys():
            mun_dict[code[v]].append(int(k))
        else:
            mun_dict[code[v]] = [int(k)]
    return mun_dict

def get_color(i):
    colors_ = ['blueviolet', 'dodgerblue', 'mediumseagreen', 'deeppink', 'coral', 'royalblue', 'midnightblue',
               'yellowgreen', 'darkgreen', 'mediumblue', 'DarkOrange', 'green', 'red', 'MediumVioletRed',
               'darkcyan', 'orangered', 'purple', 'cornflowerblue', 'saddlebrown', 'indianred', 'fuchsia', 'DarkViolet',
               'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue',
               'slategray', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'black', 'grey',
               'tomato', 'turquoise', 'violet', 'wheat', 'whitesmoke', 'yellow']
    return colors_[i % len(colors_)]


def get_bar_color(i):
    colors_ = ['blueviolet', 'mediumseagreen', 'deeppink', 'coral', 'royalblue', "MediumVioletRed", 'midnightblue',
               'yellowgreen', 'darkgreen', 'mediumblue', 'DarkViolet', 'DarkOrange', 'green', 'red',
               'darkcyan', 'orangered', 'purple', 'cornflowerblue', 'saddlebrown', 'indianred', 'fuchsia',
               'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue',
               'slategray', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'black', 'grey',
               'tomato', 'turquoise', 'violet', 'wheat', 'whitesmoke', 'yellow']
    return colors_[i % len(colors_)]

def get_boxplot_color(i):
    colors_ = [(0.5411764705882353, 0.16862745098039217, 0.8862745098039215, 0.5), (0.11764705882352941, 0.5647058823529412, 1.0, 0.5),
               (0.23529411764705882, 0.7019607843137254, 0.44313725490196076, 0.5), (1.0, 0.0784313725490196, 0.5764705882352941, 0.5), 'coral', 'royalblue', 'midnightblue',
               'yellowgreen', 'darkgreen', 'mediumblue', 'DarkOrange', 'green', 'red', 'MediumVioletRed',
               'darkcyan', 'orangered', 'purple', 'cornflowerblue', 'saddlebrown', 'indianred', 'fuchsia', 'DarkViolet',
               'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue',
               'slategray', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'black', 'grey',
               'tomato', 'turquoise', 'violet', 'wheat', 'whitesmoke', 'yellow']
    return colors_[i % len(colors_)]