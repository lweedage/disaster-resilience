from dataclasses import dataclass
import numpy as np
import math

import util
import settings


@dataclass
class ModelParameters:
    distance_2d: float
    distance_3d: float = None
    los: bool = None
    frequency: float = settings.CARRIER_FREQUENCY  # in MHz
    bs_height: float = settings.HEIGHT_ABOVE_BUILDINGS
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


def pathloss_nr(params: ModelParameters):
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
                los_pl = pathloss_nr(p)
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


def pathloss_urban_los(d_2d, d_3d, f, ue_h, bs_h, a, b, c):
    """
    Determine pathloss under urban LoS conditions.
    For the parameters see paper: they differ for UMi/UMa scenarios
    :param d_2d: 2d distance
    :param d_3d: 3d distance
    :param f: frequency
    :param ue_h: UE height
    :param bs_h: BS height
    :param a: parameter alpha
    :param b: parameter beta
    :param c: parameter gamma
    :return: path loss in dB
    """
    if d_2d < 10:
        return settings.MCL
    elif d_2d <= breakpoint_distance(f, bs_h, ue_h):
        return a + b * np.log10(d_3d) + 20 * np.log10(f)
    elif d_2d <= 5000:
        return a + 40 * np.log10(d_3d) + 20 * np.log10(f) \
               - c * np.log10(breakpoint_distance(f, bs_h, ue_h) ** 2 + (bs_h - ue_h) ** 2)
    else:
        raise ValueError("Pathloss urban los model does not function for d_2d>5km")


def pathloss_urban_nlos(d_3d, f, ue_h, a, b, c, d):
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
    return a + b * np.log10(d_3d) + c * np.log10(f) - d * (ue_h - 1.5)


def pathloss_lte(params):
    """
    Calculates the path-loss for LTE towers.
    :param params: model parameters
    :return: path-loss in dBW
    """
    hab = settings.HEIGHT_ABOVE_BUILDINGS
    MODEL_A = -18 * np.log10(hab) + 21 * np.log10(params.frequency) + 80
    MODEL_B = 40 * (1 - 4 * (10 ** -3) * hab)
    return (MODEL_A + MODEL_B * math.log10(params.distance_2d / 1000)) + math.sqrt(10) * np.random.random()


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
    This value is picked from a log-normal distribution with standard deviation sd
    :param sd: the standard deviation of the distribution
    :return:
    """
    return float(np.random.lognormal(0, sd, None))


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


def received_power(radio, tx, params, g_tx=settings.G_TX, g_rx=settings.G_RX):
    """
    Calculates the power received
    :param radio: radio type (LTE, 5G NR, mmWave)
    :type radio: util.BaseStationRadioType
    :param tx: transmitted power in dBm
    :param params: Model parameters
    :return: power received in mW
    """
    if radio == util.BaseStationRadioType.LTE:
        return util.to_pwr(tx - max(pathloss_lte(params) - settings.G_TX - settings.G_RX, settings.MCL))
    elif radio == util.BaseStationRadioType.NR:
        # ModelParams contains frequency in MHz while the models use GHz, change the value here
        params.frequency = params.frequency / 1000
        # Determine LOS condition and add to parameters for the model
        params.los = los_probability(params.distance_2d, params.area, params.ue_height)
        return util.to_pwr(tx - pathloss_nr(params) + g_tx + g_rx)


def snr(power, noise=settings.SIGNAL_NOISE):
    """
    Calculates signal to noise ratio
    :param power: power of the signal in mW
    :param noise: noise in dbm
    :return: signal to noise ratio in db
    """
    return power / util.to_pwr(noise)


def shannon_capacity(snr, bandwidth):
    """
    Calculated the shannon capacity
    :param snr:
    :param bandwidth:
    :return:
    """
    return bandwidth * shannon_second_param(snr)


def shannon_second_param(snr):
    """
    Calculates the second parameter of the shannon capacity formula
    :param snr: signal-to-noise ratio
    :return:
    """
    return math.log2(1 + snr)


def beamforming():
    """
    Simplistic model for beamforming
    Assumes direct aim of the antenna thus resulting in a static gain
    :return:
    """
    return settings.BEAMFORMING_GAIN


def test():
    params = ModelParameters(500, util.distance_3d(1.5, 30, d2d=500), True, 26000)
    pwr = received_power(util.BaseStationRadioType.NR, 60, params)
    print(util.to_db(pwr))


if __name__ == "__main__":
    test()
