import settings
import util
import objects.Params as p

import numpy as np
import math
import matplotlib.pyplot as plt


def pathloss(params, u_id, bs_id, area_type, distance_2d, distance_3d, frequency, bs_height,
             ue_height=settings.UE_HEIGHT, save=True):
    if save and params.path_loss[frequency][u_id, bs_id] != 0:
        return params.path_loss[frequency][u_id, bs_id], params
    else:
        avg_building_height = settings.AVG_BUILDING_HEIGHT
        avg_street_width = settings.AVG_STREET_WIDTH

        # p = 0
        if params.los_probabilities[u_id, bs_id] == 0:
            params.los_probabilities[u_id, bs_id] = np.random.uniform(0, 1)
        p = params.los_probabilities[u_id, bs_id]
        los = (p <= los_probability(distance_2d, area_type))


        rain = 0

        if area_type == util.AreaType.UMA and distance_2d <= 5000:
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


        elif area_type == util.AreaType.UMI and distance_2d <= 5000:
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
        elif area_type == util.AreaType.RMA and distance_2d <= 10000:
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
                    # print(bp)
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
                    pl = max(los_pl, nlos_pl) + rain + params.fading8[
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
                    pl = math.inf
        else:
            pl = math.inf
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


def pathloss_urban_nlos(d_3d, freq, ue_height, a, b, c, d):
    return a + b * np.log10(d_3d) + c * np.log10(freq / 1e9) - d * (ue_height - 1.5)


def breakpoint_distance(frequency, bs_height, ue_height=settings.UE_HEIGHT, type=None):
    c = 3.0 * 10 ** 8
    if type == 'urban':
        effective_height = 1
        return max(1, 4 * (bs_height - effective_height) * (ue_height - effective_height) * frequency / c)
    else:
        return max(1, 2 * math.pi * bs_height * ue_height * frequency / c)


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

if __name__ == '__main__':
    d2d = np.arange(0, 11000, 10)
    frequency = 1.835e9
    params = p.Parameters(1, 0, 'KPN', 0)
    params.number_of_bs = 1
    params.number_of_users = 1
    params.initialize()
    y = [pathloss(params, 0, 0, util.AreaType.RMA, d, d, frequency, 10,
             ue_height=settings.UE_HEIGHT, save=False)[0] for d in d2d]
    y1 = [pathloss(params, 0, 0, util.AreaType.UMA, d, d, frequency, 10,
             ue_height=settings.UE_HEIGHT, save=False)[0] for d in d2d]
    plt.plot(d2d, y)
    plt.plot(d2d, y1)
    plt.show()
