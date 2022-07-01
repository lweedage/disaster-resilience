import settings
import util
import objects.Params as p

import numpy as np
import math
import matplotlib.pyplot as plt


def pathloss(params, u_id, bs_id, area_type, distance_2d, distance_3d, frequency, bs_height,
             ue_height=settings.UE_HEIGHT, save=True):
    if params.path_loss[frequency][u_id, bs_id] != 0 and save:
        return params.path_loss[frequency][u_id, bs_id], params
    else:
        avg_building_height = settings.AVG_BUILDING_HEIGHT
        avg_street_width = settings.AVG_STREET_WIDTH
        if params.los_probabilities[u_id, bs_id] == 0:
            params.los_probabilities[u_id, bs_id] = np.random.uniform(0, 1)
        p = params.los_probabilities[u_id, bs_id]
        los = (p <= los_probability(distance_2d, area_type))

        if params.rain:
            rain = rain_attenuation(frequency, distance_2d, params.rain)
        else:
            rain = 0

        if area_type == util.AreaType.UMA:
            pl_los = pathloss_urban_los(distance_2d, distance_3d, frequency, ue_height,
                                        bs_height, 28, 22, 9)
            if los:
                if params.fading4[u_id, bs_id] == 0:
                    params.fading4[u_id, bs_id] = np.random.normal(0, 4)
                pl = pl_los + rain + params.fading4[u_id, bs_id]
            else:
                pl_nlos = pathloss_urban_nlos(distance_3d, frequency, ue_height,
                                              13.54, 39.08, 20, 0.6)
                if params.fading6[u_id, bs_id] == 0:
                    params.fading6[u_id, bs_id] = np.random.normal(0, 6)
                pl = max(pl_los, pl_nlos) + rain + params.fading6[u_id, bs_id]
        elif area_type == util.AreaType.UMI:
            pl_los = pathloss_urban_los(distance_2d, distance_3d, frequency, ue_height,
                                        bs_height, 32.4, 21, 9.5)
            if los:
                if params.fading4[u_id, bs_id] == 0:
                    params.fading4[u_id, bs_id] = np.random.normal(0, 4)
                pl = pl_los + rain + params.fading4[u_id, bs_id]

            else:
                pl_nlos = pathloss_urban_nlos(distance_3d, frequency, ue_height,
                                              22.4, 35.3, 21.3, 0.3)
                if params.fading78[u_id, bs_id] == 0:
                    params.fading78[u_id, bs_id] = np.random.normal(0, 7.8)
                pl = max(pl_los, pl_nlos) + rain + params.fading78[u_id, bs_id]
        elif area_type == util.AreaType.RMA:
            if los:
                bp = breakpoint_distance(frequency, bs_height)
                if distance_2d < 10:
                    if params.fading4[u_id, bs_id] == 0:
                        params.fading4[u_id, bs_id] = np.random.normal(0, 4)
                    pl = pathloss_rma_los_pl1(util.distance_3d(bs_height, ue_height, d2d=10), avg_building_height,
                                              frequency) + rain + params.fading4[u_id, bs_id]
                elif distance_2d <= bp:
                    if params.fading4[u_id, bs_id] == 0:
                        params.fading4[u_id, bs_id] = np.random.normal(0, 4)
                    pl = pathloss_rma_los_pl1(distance_3d, avg_building_height, frequency) + rain + params.fading4[
                        u_id, bs_id]
                elif distance_2d <= 10000:
                    pl1 = pathloss_rma_los_pl1(bp, avg_building_height, frequency)
                    if params.fading6[u_id, bs_id] == 0:
                        params.fading6[u_id, bs_id] = np.random.normal(0, 6)
                    pl = pl1 + 40 * np.log10(distance_3d / bp) + rain + params.fading6[u_id, bs_id]
                else:
                    # TODO: Look at this - what happens if RMA > 10 km?
                    pl1 = pathloss_rma_los_pl1(bp, avg_building_height, frequency)
                    if params.fading6[u_id, bs_id] == 0:
                        params.fading6[u_id, bs_id] = np.random.normal(0, 6)
                    pl = pl1 + 40 * np.log10(distance_3d / bp) + rain + params.fading6[u_id, bs_id]
            else:  # NLoS
                if distance_2d < 10:
                    distance_3d = util.distance_3d(bs_height, ue_height, d2d=10)
                    nlos_pl = 161.04 - 7.1 * np.log10(avg_street_width) + 7.5 * np.log10(avg_building_height) \
                              - (24.37 - 3.7 * (avg_building_height / max(1, bs_height)) ** 2) * np.log10(
                        bs_height) + (43.42 - 3.1 * np.log10(bs_height)) * (np.log10(distance_3d) - 3) \
                              + 20 * np.log10(frequency / 1e9) - (3.2 * np.log10(11.75 * ue_height) - 4.97)

                    los_pl = pathloss_urban_los(10, distance_3d, frequency, ue_height, bs_height, 28, 22, 9)
                    if params.fading8[u_id, bs_id] == 0:
                        params.fading8[u_id, bs_id] = np.random.normal(0, 8)
                    pl = max(los_pl, nlos_pl) + rain_attenuation(frequency, 10, params.rain) + params.fading8[
                        u_id, bs_id]
                elif distance_2d <= 5000:
                    nlos_pl = 161.04 - 7.1 * np.log10(avg_street_width) + 7.5 * np.log10(avg_building_height) \
                              - (24.37 - 3.7 * (avg_building_height / max(1, bs_height)) ** 2) * np.log10(
                        bs_height) + (43.42 - 3.1 * np.log10(bs_height)) * (np.log10(distance_3d) - 3) \
                              + 20 * np.log10(frequency / 1e9) - (3.2 * np.log10(11.75 * ue_height) - 4.97)

                    los_pl = pathloss_urban_los(distance_2d, distance_3d, frequency, ue_height, bs_height, 28, 22, 9)
                    if params.fading8[u_id, bs_id] == 0:
                        params.fading8[u_id, bs_id] = np.random.normal(0, 8)
                    pl = max(los_pl, nlos_pl) + rain + params.fading8[u_id, bs_id]
                else:
                    # TODO: Look at this - what happens if RMA > 10 km?
                    nlos_pl = 161.04 - 7.1 * np.log10(avg_street_width) + 7.5 * np.log10(avg_building_height) \
                              - (24.37 - 3.7 * (avg_building_height / max(1, bs_height)) ** 2) * np.log10(
                        bs_height) + (43.42 - 3.1 * np.log10(bs_height)) * (np.log10(distance_3d) - 3) \
                              + 20 * np.log10(frequency) - (3.2 * np.log10(11.75 * ue_height) - 4.97)

                    # los_pl = pathloss(params, u_id, bs_id, util.AreaType.UMA, distance_2d, distance_3d, frequency,
                                      # bs_height, ue_height=settings.UE_HEIGHT)

                    los_pl = pathloss_urban_los(distance_2d, distance_3d, frequency, ue_height,
                                                bs_height, 28, 22, 9) #TODO check whether this is correctc

                    if params.fading8[u_id, bs_id] == 0:
                        params.fading8[u_id, bs_id] = np.random.normal(0, 8)
                    pl = max(los_pl, nlos_pl) + rain + params.fading8[u_id, bs_id]
        else:
            raise ValueError("Unknown area type")
        if save:
            params.path_loss[frequency][u_id, bs_id] = pl
        return pl, params


def pathloss_rma_los_pl1(distance, avg_building_height, frequency):
    freq = frequency / 1e9
    a = 40 * math.pi * distance * freq / 3
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
    breakpoint = breakpoint_distance(freq, bs_height, ue_height, type='urban')

    if d_2d < 10:
        return a + b * np.log10(util.distance_3d(bs_height, ue_height, d2d=10)) + 20 * np.log10(freq / 1e9)
    elif d_2d <= breakpoint:
        return a + b * np.log10(d_3d) + 20 * np.log10(freq / 1e9)
    elif d_2d <= 5000:
        return a + 40 * np.log10(d_3d) + 20 * np.log10(freq / 1e9) \
               - c * np.log10(breakpoint ** 2 + (bs_height - ue_height) ** 2)
    else:
        return a + 40 * np.log10(d_3d) + 20 * np.log10(freq / 1e9) \
               - c * np.log10(breakpoint ** 2 + (bs_height - ue_height) ** 2)


def pathloss_urban_nlos(d_3d, freq, ue_height, a, b, c, d):
    return a + b * np.log10(d_3d) + c * np.log10(freq / 1e9) - d * (ue_height - 1.5)


def breakpoint_distance(frequency, bs_height, ue_height=settings.UE_HEIGHT, type=None):
    c = 3.0 * 10 ** 8
    if type == 'urban':
        effective_height = 1
        return 4 * (bs_height - effective_height) * (ue_height - effective_height) * frequency / c
    else:
        return 2 * math.pi * bs_height * ue_height * frequency / c


def rain_attenuation(frequency, distance, rain):
    if rain:
        if 1e9 < frequency < 20e9:
            frequency = frequency / 1e9
            logfreq = np.log(frequency)
            kH = 3.8794e-5 * frequency ** (
                    2.7474 - 1.794 * logfreq + 1.1805 * logfreq ** 2 - 0.2022 * logfreq ** 3)  # TODO: I assume only horizontal attenuation
            alphaH = ((1.0564 * logfreq - 1.9256) ** 2 + 0.9437) / ((1.1141 * logfreq - 2.0940) ** 2 + 0.7181)
            gamma = kH * rain ** alphaH
            return gamma * distance / 1e3  # gamma is in dB/km
        else:
            return 0.0  # TODO: no expression given for frequencies above 20GHz as it is not in the dataset (yet)
    else:
        return 0.0


def los_probability(d_2d, area, ue_h=settings.UE_HEIGHT):
    if area == util.AreaType.RMA:
        if d_2d <= 10:
            return 1
        else:
            return np.exp(-((d_2d - 10) / 1000))
    elif area == util.AreaType.UMI:
        if d_2d <= 18:
            return 1
        else:
            return (18 / d_2d + np.exp(-d_2d / 36) * (1 - 18 / d_2d))
    elif area == util.AreaType.UMA:
        if d_2d <= 18:
            return 1
        else:
            c = 0 if ue_h <= 13 else ((ue_h - 13) / 10) ** 1.5
            return (18 / d_2d + np.exp(-d_2d / 63) * (1 - 18 / d_2d)) * (
                    1 + c * (5 / 4) * (d_2d / 100) ** 3 * np.exp(-d_2d / 150))
    else:
        raise TypeError("Unknown area type")
