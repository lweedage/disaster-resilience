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


def distance(x1, y1, x2, y2):
    # Rewritten to use EPSG:28992
    return distance_2d(x1, y1, x2, y2)


def distance_2d(x1, y1, x2, y2):
    """
    Calculates distance in meters assuming EPSG:28992 coordinate system
    :param x1: x of first point
    :param y1: y of first point
    :param x2: x of second point
    :param y2: y of second point
    :return: distance in metres
    """
    dist_x = abs(x1 - x2)
    dist_y = abs(y1 - y2)

    return math.sqrt(dist_x ** 2 + dist_y ** 2)


def distance_3d(h1, h2, x1=None, y1=None, x2=None, y2=None, d2d=None):
    """
    Calculates distance in meters assuming EPSG:28992 coordinate system.
    Either distance between the points or x,y coordinates for the two points is needed
    :param h1: height of first point
    :param h2: height of second point
    :param x1: x of first point
    :param y1: y of first point
    :param x2: x of second point
    :param y2: y of second point
    :param d2d: distance between the points
    :return:
    """

    d_2d = d2d
    if d_2d is None:
        d_2d = distance_2d(x1, y1, x2, y2)
    dist_h = abs(h1 - h2)
    return math.sqrt(d_2d ** 2 + dist_h ** 2)


def isolated_users(ue):
    counter = 0
    for user in ue:
        if user.link is None:
            counter += 1
    return counter / len(ue)


def received_service(ue):
    percentages = []

    for user in ue:
        if user.link is not None:
            percentages.append(
                1 if user.link.shannon_capacity / user.requested_capacity > 1
                else user.link.shannon_capacity / user.requested_capacity)
        else:
            percentages.append(0)

    return sum(percentages) / len(percentages) if len(percentages) != 0 else 0


def received_service_half(ue):
    counter = 0

    for user in ue:
        if user.link is not None:
            if user.link.shannon_capacity / user.requested_capacity >= 0.5:
                counter += 1

    return counter / len(ue)


def avg_distance(ue):
    distances = []
    for user in ue:
        if user.link:
            distances.append(user.link.distance)

    return sum(distances) / len(distances) if len(distances) != 0 else None  # not 1 user is connected so infinite


def isolated_systems(base_stations):
    systems = 0
    bs_copy = base_stations[:]
    while len(bs_copy) != 0:
        systems += 1
        first = bs_copy.pop(0)
        checked = [link.other(first) for link in first.connected_BS[:]]
        while len(checked) != 0:
            second = checked.pop(0)
            if second in bs_copy:
                bs_copy.remove(second)
                checked = checked + [link.other(second) for link in second.connected_BS[:]]

    return systems


def snr_averages(ue):
    snrs = []
    for user in ue:
        if user.link:
            snrs.append(user.snr)
        else:
            snrs.append(0)
    return sum(snrs) / len(snrs) if len(snrs) > 0 else 0


def active_channels(bs):
    ac = 0
    for b in bs:
        for c in b.channels:
            if c.enabled:
                ac += 1
    return ac


def connected_ue_bs(base_stations):
    return sum([len(bs.connected_UE) for bs in base_stations]) / len(base_stations)


def to_pwr(db):
    """
    Convert dB to W
    :param db: Decibel dB
    :return: power in W
    """
    return 10 ** (db / 10)


def to_db(pwr):
    """
    convert value to dB scale
    convert mW to dBm
    :param pwr: value to convert
    :return: dB
    """
    return 10 * math.log10(pwr)


def dbw_to_dbm(pwr):
    """
    Converts dBW power to dBm power
    :param pwr: power in dBW
    :return:
    """
    return pwr + 30


def avg(lst):
    length = 0
    total_sum = 0

    for i in lst:
        if i is not None:
            length += 1
            total_sum += i

    return total_sum / length if length > 0 else -1


def get_unit(index):
    if index == 0:
        return "Isolated Users (%)"
    elif index == 1:
        return "Satisfaciton level (%)"
    elif index == 2:
        return "50% Satisfaction level (%)"
    elif index == 3:
        return "Avg. Distance to BS (meters)"
    elif index == 4:
        return "#Isolated Systems"
    elif index == 5:
        return "#Active BS"
    elif index == 6:
        return "Avg. SNR (ratio)"
    elif index == 7:
        return "Avg. #users connected to BS"
    elif index == 8:
        return "#Active channels"
    else:
        return "Error"


def get_x_values():
    if settings.LARGE_DISASTER:
        return [settings.RADIUS_PER_SEVERITY * r for r in range(settings.SEVERITY_ROUNDS)], "Radius disaster (meters)"
    elif settings.MALICIOUS_ATTACK:
        return [(settings.FUNCTIONALITY_DECREASED_PER_SEVERITY * s) for s in
                range(settings.SEVERITY_ROUNDS)], "Functionality decreased of BS"
    elif settings.INCREASING_REQUESTED_DATA:
        return [s for s in range(settings.SEVERITY_ROUNDS)], "Severity level of increasing data"


def create_plot(city_results):
    x_values, unit = get_x_values()

    #    for z in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
    for z in [0, 1]:
        fig = go.Figure()
        for city in city_results:
            results = [m.get_metrics() for m in city_results[city]]
            errors = [m.get_cdf() for m in city_results[city]]
            fig.add_trace(go.Scatter(
                x=x_values,
                y=[r[z] for r in results if r[z] is not None],
                mode='lines+markers',
                name=str(city),
                error_y=dict(
                    type='data',
                    array=[e[z] for e in errors if e[z] is not None],
                    visible=True
                )
            ))
        if z == 0:
            fig.update_layout(xaxis_title=unit, yaxis_title=get_unit(z),
                              legend=dict(yanchor="top", y=0.95, xanchor="left", x=0.05))
        else:
            fig.update_layout(xaxis_title=unit, yaxis_title=get_unit(z),
                              legend=dict(yanchor="bottom", y=0.05, xanchor="left", x=0.05))
        fig.show()

    pass


def cdf(data, confidence=0.95):
    processed_data = [d for d in data if d is not None]
    if len(processed_data) == 0 or len(processed_data) == 1:
        return 0

    mean, se = np.mean(processed_data), st.sem(processed_data)
    h = se * st.t.ppf((1 + confidence) / 2, len(processed_data) - 1)
    return h


def create_new_file():
    with open(settings.SAVE_CSV_PATH, 'w', newline='') as f:
        fieldnames = ['city', 'severity', 'isolated_users', 'received_service', 'received_service_half', 'avg_distance',
                      'isolated_systems', 'active_base_stations', 'avg_snr', 'connected_UE_BS', 'active_channels']
        csv_writer = csv.writer(f)
        csv_writer.writerow(fieldnames)


def save_data(city, metrics):
    with open(settings.SAVE_CSV_PATH, 'a', newline='') as f:
        csv_writer = csv.writer(f)
        for i in range(settings.SEVERITY_ROUNDS):
            metric = metrics[i].csv_export()
            for m in metric:
                csv_writer.writerow([city.name, i] + m)


@enum.unique
class BaseStationRadioType(enum.Enum):
    """
    Radio type for the basestation
    NR: 5G NR
    LTE: 4G LTE
    mmWave: 5G mmWave (6GHz+)
    """
    NR = enum.auto()
    LTE = enum.auto()
    GSM = enum.auto()
    UMTS = enum.auto()



@enum.unique
class AreaType(enum.Enum):
    """
    Type of area a BS or UE is in.
    UMA: Urban macro cell
    UMI: Urban micro cell (street canyon)
    RMA: Rural macro cell
    """
    UMA = enum.auto()
    UMI = enum.auto()
    RMA = enum.auto()


def str_to_float(string):
    """
    Strips all non digit characters from string (except .) and transforms to float
    :param string:
    :return:
    """
    s = re.sub(r'[^\d.]+', '', string)
    return float(s)


def get_angle(x1, y1, x2, y2):
    """
    Calculates the angle between two points with the x-axis as reference
    The second point is set as 0 point
    """
    x = x1 - x2
    y = y1 - y2
    angle = math.atan2(y, x)
    return math.degrees(angle)

def find_cities(municipality):
    with open("data/cities_per_province") as f:
        data = f.read()
        data = data.split('\n')
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
    for key, provider in frequency_dict.items():
        (min_freq, max_freq) = key
        if min_freq <= frequency < max_freq:
            bandwidth = min(frequency-min_freq, max_freq - frequency) * 2
            if bandwidth >= 20:
                bandwidth = 20
            elif bandwidth >= 15:
                bandwidth = 15
            elif bandwidth >= 10:
                bandwidth = 10
            elif bandwidth >= 5:
                bandwidth = 5
            elif bandwidth >= 3:
                bandwidth = 3
            else:
                bandwidth = 1.4
            return provider, bandwidth*10**6
    print(frequency)
    return 'None', 0

def find_closest_BS(user_coords, x_bs, y_bs):
    x = np.array(x_bs) - user_coords[0]
    y = np.array(y_bs) - user_coords[1]
    return np.argsort(x ** 2 + y ** 2)


def save_object(obj, filename):
    with open(filename, 'wb') as outp:
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)

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