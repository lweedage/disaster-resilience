import math
from dataclasses import dataclass
import numpy as np
import settings
import util


# code from Bart Meyers


@dataclass
class ModelParameters:
    distance_2d: float
    distance_3d: float
    los: bool
    frequency: float  # in Hz
    bs_height: float
    ue_height: float = settings.UE_HEIGHT
    area: util.AreaType = util.AreaType.UMA
    avg_building_height: float = settings.AVG_BUILDING_HEIGHT
    avg_street_width: float = settings.AVG_STREET_WIDTH

    @property
    def distance(self):
        return self.distance_2d

    def __copy__(self):
        return ModelParameters(self.distance_2d, self.distance_3d, self.los, self.frequency, self.bs_height,
                               self.ue_height, self.area, self.avg_building_height, self.avg_street_width)


def pathloss(params: ModelParameters):
    """
    Determines the path-loss for 5G radio types.
    :param params: parameter class containing needed parameters
    :return:The path-loss in dB
    """
    if params.area == util.AreaType.UMA:
        pl_los = pathloss_urban_los(params.distance_2d, params.distance_3d, params.frequency, params.ue_height,
                                    params.bs_height, 28, 22, 9)
        if params.los:
            return pl_los + atmospheric_attenuation(params.frequency, params.distance_2d) + shadow_fading(4)
        else:
            pl_nlos = pathloss_urban_nlos(params.distance_3d, params.frequency, params.ue_height,
                                          13.54, 39.08, 20, 0.6)
            return max(pl_los, pl_nlos) + atmospheric_attenuation(params.frequency, params.distance_2d) + shadow_fading(
                6)
    elif params.area == util.AreaType.UMI:
        pl_los = pathloss_urban_los(params.distance_2d, params.distance_3d, params.frequency, params.ue_height,
                                    params.bs_height, 32.4, 21, 9.5)
        if params.los:
            return pl_los + atmospheric_attenuation(params.frequency, params.distance_2d) + shadow_fading(4)
        else:
            pl_nlos = pathloss_urban_nlos(params.distance_3d, params.frequency, params.ue_height,
                                          22.4, 35.3, 21.3, 0.3)
            return max(pl_los, pl_nlos) + atmospheric_attenuation(params.frequency, params.distance_2d) + shadow_fading(
                7.82)
    elif params.area == util.AreaType.RMA:
        if params.los:
            if params.distance_2d < 10:
                return settings.MCL
            elif params.distance_2d <= breakpoint_distance(params.frequency, params.bs_height):
                return pathloss_rma_los_pl1(params.distance_3d, params.avg_building_height, params.frequency) + \
                       atmospheric_attenuation(params.frequency, params.distance_2d) + shadow_fading(4)
            elif params.distance_2d <= 10000:
                bp = breakpoint_distance(params.frequency, params.bs_height)
                pl1 = pathloss_rma_los_pl1(bp, params.avg_building_height, params.frequency)
                return pl1 + 40 * np.log10(params.distance_3d / bp) + atmospheric_attenuation(params.frequency,
                                                                                              params.distance_2d) + shadow_fading(
                    6)
            else:
                raise ValueError("LoS model for RMa does not function for d_2D>10km")
        else:  # NLoS
            if params.distance_2d < 10:
                return settings.MCL
            elif params.distance_2d <= 5000:
                nlos_pl = 161.04 - 7.1 * np.log10(params.avg_street_width) + 7.5 * np.log10(params.avg_building_height) \
                          - (24.37 - 3.7 * (params.avg_building_height / params.bs_height) ** 2) * np.log10(
                    params.bs_height) \
                          + (43.42 - 3.1 * np.log10(params.bs_height)) * (np.log10(params.distance_3d) - 3) \
                          + 20 * np.log10(params.frequency) - (3.2 * np.log10(11.75 * params.ue_height) - 4.97)
                p = params.__copy__()
                p.los = True
                los_pl = pathloss(p)
                return max(los_pl, nlos_pl) + atmospheric_attenuation(params.frequency,
                                                                      params.distance_2d) + shadow_fading(8)
            else:
                raise ValueError("NLoS model for RMa does not function for d_2D>5km")
    else:
        raise ValueError("Unknown area type")


def pathloss_rma_los_pl1(distance, avg_building_height, frequency):
    a = 40 * math.pi * distance * frequency / 3
    hp = avg_building_height ** 1.72
    return 20 * np.log10(a) + min(0.03 * hp, 10) * np.log10(distance) - min(0.044 * hp, 14.77) + \
           0.002 * np.log10(avg_building_height) * distance


def pathloss_urban_los(d_2d, d_3d, freq, ue_height, bs_height, a, b, c):
    """
    Determine pathloss under urban LoS conditions.
    For the parameters see paper: they differ for UMi/UMa scenarios
    :param d_2d: 2d distance
    :param d_3d: 3d distance
    :param freq: frequency (in Hz)
    :param ue_height: UE height
    :param bs_height: BS height
    :param a: parameter alpha
    :param b: parameter beta
    :param c: parameter gamma
    :return: path loss in dB
    """
    if d_2d < 10:
        return settings.MCL
    elif d_2d <= breakpoint_distance(freq, bs_height, ue_height):
        return a + b * np.log10(d_3d) + 20 * np.log10(freq / 1e9)
    elif d_2d <= 5000:
        return a + 40 * np.log10(d_3d) + 20 * np.log10(freq / 1e9) \
               - c * np.log10(breakpoint_distance(freq, bs_height, ue_height) ** 2 + (bs_height - ue_height) ** 2)
    else:
        raise ValueError("Pathloss urban los model does not function for d_2d>5km")


def pathloss_urban_nlos(d_3d, freq, ue_height, a, b, c, d):
    """
    Determines pathloss for urban nlos scenario
    :param d_3d: 3D distance
    :param f: frequency
    :param ue_h: UE height
    :param a: parameter alpha
    :param b: parameter beta
    :param c: parameter gamma
    :param d: parameter delta
    :return:
    """

    return a + b * np.log10(d_3d) + c * np.log10(freq / 1e9) - d * (ue_height - 1.5)


def breakpoint_distance(frequency, bs_height, ue_height=settings.UE_HEIGHT):
    """
    Determines the breakpoint distance for the 5G model
    :param frequency: centre frequency of the channnel
    :param bs_height: height of the basestation
    :param ue_height: height of the user equipment
    :return: breakpoint distance
    """
    c = 3.0 * 10 ** 8
    return 2 * math.pi * bs_height * ue_height * frequency / c


# TODO
def atmospheric_attenuation(frequency, distance):
    return 0.0


def shadow_fading(sd):
    """
    Determines the shadow fading part of the 5G model.
    This value is picked from a normal distribution with standard deviation sd
    :param sd: the standard deviation of the distribution
    :return:
    """
    return float(np.random.normal(0, sd))


def los_probability(d_2d, area, ue_h):
    """
    Determines the probability of LoS condition
    :param d_2d: 2d distance
    :param area: area type (RMa,UMa,UMi)
    :param ue_h: UE height
    :return: probability of LoS condition
    """
    if area == util.AreaType.RMA:
        if d_2d <= 10:
            return 1
        else:
            return np.exp(-((d_2d - 10) / 1000))
    elif area == util.AreaType.UMA:
        if d_2d <= 18:
            return 1
        else:
            return 18 / d_2d + np.exp(-d_2d / 36) * (1 - 18 / d_2d)
    elif area == util.AreaType.UMI:
        if d_2d <= 18:
            return 1
        else:
            if ue_h > 23:
                raise ValueError("LoS probability model does not function for height larger than 23m")
            c = 0 if ue_h <= 13 else ((ue_h - 13) / 10) ** 1.5
            return (18 / d_2d + np.exp(-d_2d / 63) * (1 - 18 / d_2d)) * (
                    1 + c * (5 / 4) * (d_2d / 100) * np.exp(-d_2d / 150))
    else:
        raise TypeError("Unknown area type")


def received_power(radio, tx, params):
    """
    Calculates the power received
    :param radio: radio type (LTE, 5G NR, mmWave)
    :type radio: util.BaseStationRadioType
    :param tx: transmitted power in dBm
    :param params: Model parameters
    :return: power received in mW
    """
    if radio == util.BaseStationRadioType.LTE:
        return util.to_pwr(tx - max(pathloss(params), settings.MCL))
    elif radio == util.BaseStationRadioType.NR:
        # ModelParams contains frequency in MHz while the models use GHz, change the value here
        # Determine LOS condition and add to parameters for the model
        params.los = los_probability(params.distance_2d, params.area, params.ue_height)
        return util.to_pwr(tx - pathloss(params))


def snr(user_coords, base_station, channel):
    """
    Calculates signal to noise ratio in dB
    :param power: power of the signal in mW
    :return: signal to noise ratio in db
    """
    bs_coords = (base_station.x, base_station.y)
    power = channel.power
    boresight_angle = channel.main_direction
    beamwidth = channel.beamwidth
    bandwidth = channel.bandwidth
    radio = base_station.radio

    gain = find_gain(user_coords, bs_coords, boresight_angle, beamwidth)
    noise = find_noise(bandwidth, radio)

    return power + gain - noise

def sinr(user_coords, base_station, channel):
    SNR = snr(user_coords, base_station, channel)
    interference = 3  # todo: change this!
    return SNR - interference

def shannon_capacity(snr, bandwidth):
    """
    Calculated the shannon capacity
    :param snr:
    :param bandwidth:
    :return:
    """
    snr = 10**(snr/10)
    return bandwidth * math.log2(1 + snr)

def beamforming():
    """
    Simplistic model for beamforming
    Assumes direct aim of the antenna thus resulting in a static gain
    :return:
    """
    return settings.BEAMFORMING_GAIN

def thermal_noise(bandwidth):
    thermal_noise = settings.BOLTZMANN * settings.TEMPERATURE * bandwidth
    return 10 * math.log10(thermal_noise) + 30 # 30 is to go from dBW to dBm

def find_noise(bandwidth, radio):
    if radio == util.BaseStationRadioType.NR:
        noise_figure = 7.8
    else:
        noise_figure = 5
    return thermal_noise(bandwidth) + noise_figure

def find_gain(coord_1, coord_2, boresight_angle, beamwidth_ml):
    alpha = find_misalignment(boresight_angle, find_geo(coord_1, coord_2))
    w = beamwidth_ml / 2.58
    G0 = 20 * math.log10(1.62 / math.sin(math.radians(w / 2)))

    if 0 <= abs(alpha) <= beamwidth_ml / 2:
        return (G0 - 3.01 * (2 * alpha / w) ** 2) # in dB
    else:
        return -0.4111 * math.log(math.degrees(w)) - 10.579 # in dB

def find_geo(coord_1, coord_2):
    dy = coord_2[1] - coord_1[1]
    dx = coord_2[0] - coord_1[0]
    radians = math.atan2(dy, dx)
    return radians

def find_misalignment(boresight_angle, geo):
    if boresight_angle == 'Omnidirectional' or boresight_angle == 360:
        alpha = 0
    else:
        alpha = math.degrees(abs(boresight_angle - geo))

    if alpha > 180:
        alpha = alpha - 360
    return alpha

def find_links(users, base_stations, x_bs, y_bs):
    links = np.zeros((len(users), len(base_stations)))
    snrs = np.zeros((len(users), len(base_stations)))
    channel_link = np.zeros((len(users), len(base_stations)))

    for user in users:
        user_coords = [user.x, user.y]
        BSs = util.find_closest_BS(user_coords, x_bs, y_bs)
        SNR = - math.inf
        for bs in BSs[:10]:  # assuming that the highest SNR BS will be within the closest 10 BSs
            base_station = base_stations[bs]
            for channel in base_station.channels:
                new_SNR = snr(user_coords, base_station, channel)
                if new_SNR > SNR:
                    SNR = new_SNR
                    best_bs = bs
                    channel_id = channel.id
            # base_station.channels[int(channel_id)].add_user(user)
        snrs[user.id, best_bs] = SNR
        channel_link[user.id, best_bs] = channel_id
        links[user.id, best_bs] = 1

    return links, channel_link, snrs

def find_capacity(users, base_stations, SNR ,links):
    capacity = np.zeros((len(users), len(base_stations)))
    for bs in base_stations:
        bs_id = bs.id
        for user in users:
            user_id = user.id
            if links[user_id, bs_id] > 0:
                bandwidth = bs.channels[int(links[user_id, bs_id])].bandwidth
                print(SNR[user.id, bs.id])
                capacity[user_id, bs_id] = shannon_capacity(SNR[user.id, bs.id], bandwidth)
    return capacity
