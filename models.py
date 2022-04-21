import math
import numpy as np
import settings
import util
import matplotlib.pyplot as plt



# code from Bart Meyers
def pathloss(params, u_id, bs_id, area_type, distance_2d, distance_3d, frequency, bs_height, ue_height=settings.UE_HEIGHT):
    avg_building_height = settings.AVG_BUILDING_HEIGHT
    avg_street_width = settings.AVG_STREET_WIDTH

    p = params.los_probabilities[u_id, bs_id]
    print(area_type, los_probability(distance_2d, area_type))
    los = (p <= los_probability(distance_2d, area_type))

    if area_type == util.AreaType.UMA:
        pl_los = pathloss_urban_los(distance_2d, distance_3d, frequency, ue_height,
                                    bs_height, 28, 22, 9)
        if los:
            return pl_los + atmospheric_attenuation(frequency, distance_2d) + params.fading4[u_id, bs_id]
        else:
            pl_nlos = pathloss_urban_nlos(distance_3d, frequency, ue_height,
                                          13.54, 39.08, 20, 0.6)
            return max(pl_los, pl_nlos) + atmospheric_attenuation(frequency, distance_2d) + params.fading6[u_id, bs_id]
    elif area_type == util.AreaType.UMI:
        pl_los = pathloss_urban_los(distance_2d, distance_3d, frequency, ue_height,
                                    bs_height, 32.4, 21, 9.5)
        if los:
            return pl_los + atmospheric_attenuation(frequency, distance_2d) + params.fading4[u_id, bs_id]
        else:
            pl_nlos = pathloss_urban_nlos(distance_3d, frequency, ue_height,
                                          22.4, 35.3, 21.3, 0.3)
            return max(pl_los, pl_nlos) + atmospheric_attenuation(frequency, distance_2d) + params.fading78[u_id, bs_id]
    elif area_type == util.AreaType.RMA:
        if los:
            bp = breakpoint_distance(frequency, bs_height)
            if distance_2d < 10:
                return settings.MCL
            elif distance_2d <= bp:
                return pathloss_rma_los_pl1(distance_3d, avg_building_height, frequency) + \
                       atmospheric_attenuation(frequency, distance_2d) + params.fading4[u_id, bs_id]
            elif distance_2d <= 10000:
                pl1 = pathloss_rma_los_pl1(bp, avg_building_height, frequency)
                return pl1 + 40 * np.log10(distance_3d / bp) + atmospheric_attenuation(frequency,
                                                                                       distance_2d) + params.fading6[u_id, bs_id]
            else:  # TODO This is not correct yet
                pl1 = pathloss_rma_los_pl1(bp, avg_building_height, frequency)
                return pl1 + 40 * np.log10(distance_3d / bp) + atmospheric_attenuation(frequency,
                                                                                       distance_2d) + params.fading6[u_id, bs_id]
        else:  # NLoS
            if distance_2d < 10:
                return settings.MCL
            elif distance_2d <= 5000:
                nlos_pl = 161.04 - 7.1 * np.log10(avg_street_width) + 7.5 * np.log10(avg_building_height) \
                          - (24.37 - 3.7 * (avg_building_height / bs_height) ** 2) * np.log10(
                    bs_height) \
                          + (43.42 - 3.1 * np.log10(bs_height)) * (np.log10(distance_3d) - 3) \
                          + 20 * np.log10(frequency / 1e9) - (3.2 * np.log10(11.75 * ue_height) - 4.97)

                los_pl = pathloss(util.AreaType.UMA, distance_2d, distance_3d, frequency, bs_height,
                                  ue_height=settings.UE_HEIGHT)  # todo THIS IS WRONG!
                return max(los_pl, nlos_pl) + atmospheric_attenuation(frequency,
                                                                      distance_2d) + params.fading8[u_id, bs_id]
            else:  # TODO This is not correct
                nlos_pl = 161.04 - 7.1 * np.log10(avg_street_width) + 7.5 * np.log10(avg_building_height) \
                          - (24.37 - 3.7 * (avg_building_height / bs_height) ** 2) * np.log10(
                    bs_height) \
                          + (43.42 - 3.1 * np.log10(bs_height)) * (np.log10(distance_3d) - 3) \
                          + 20 * np.log10(frequency) - (3.2 * np.log10(11.75 * ue_height) - 4.97)

                los_pl = pathloss(util.AreaType.UMA, distance_2d, distance_3d, frequency, bs_height,
                                  ue_height=settings.UE_HEIGHT)  # todo THIS IS WRONG!
                return max(los_pl, nlos_pl) + atmospheric_attenuation(frequency,
                                                                      distance_2d) + params.fading8[u_id, bs_id]
    else:
        return math.inf

        # raise ValueError("Unknown area type")


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
    breakpoint = breakpoint_distance(freq, bs_height, ue_height, type = 'urban')

    if d_2d < 10:
        return settings.MCL
    elif d_2d <= breakpoint:
        return a + b * np.log10(d_3d) + 20 * np.log10(freq / 1e9)
    elif d_2d <= 5000:
        return a + 40 * np.log10(d_3d) + 20 * np.log10(freq / 1e9) \
               - c * np.log10(breakpoint ** 2 + (bs_height - ue_height) ** 2)
    else:  # TODO this is not correct
        return a + 40 * np.log10(d_3d) + 20 * np.log10(freq / 1e9) \
               - c * np.log10(breakpoint ** 2 + (bs_height - ue_height) ** 2)


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


def breakpoint_distance(frequency, bs_height, ue_height=settings.UE_HEIGHT, type = None):
    c = 3.0 * 10 ** 8
    if type == 'urban':
        effective_height = 1
        return 4 * (bs_height - effective_height) * (ue_height - effective_height) * frequency / c
    else:
        return 2 * math.pi * bs_height * ue_height * frequency / c


# TODO
def atmospheric_attenuation(frequency, distance):
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
                    1 + c * (5 / 4) * (d_2d / 100)**3 * np.exp(-d_2d / 150))
    else:
        raise TypeError("Unknown area type")


def snr(user, base_station, channel, params):
    user_coords = (user.x, user.y)
    bs_coords = (base_station.x, base_station.y)
    power = channel.power

    # power = 10 * math.log10(10**(power/10) / 3 )  #first convert to ratio, divide by 3 (sectorized antenna's) and then back to db
    # todo Not all antenna's have three sectors.

    d2d = util.distance_2d(base_station.x, base_station.y, user_coords[0], user_coords[1])
    d3d = util.distance_3d(h1=channel.height, h2=settings.UE_HEIGHT, d2d=d2d)

    if channel.main_direction != 'Omnidirectional':
        antenna_gain = find_antenna_gain(channel.main_direction, util.find_geo(bs_coords, user_coords), channel.height,
                                         d2d)
    else:
        antenna_gain = 0

    path_loss = pathloss(params, user.id, base_station.id, base_station.area_type, d2d, d3d, channel.frequency, channel.height)

    bandwidth = channel.bandwidth
    radio = base_station.radio
    noise = find_noise(bandwidth, radio)
    return power - path_loss + antenna_gain - noise  # in dB

def highest_snr(bs, base_station, channels, params):
    snrs = list()
    for channel in channels:
        snrs.append(snr(bs, base_station, channel, params))
    return max(snrs)


def find_antenna_gain(bore, geo, height_bs, d2d):
    A_vertical = vertical_gain(settings.UE_HEIGHT, height_bs, d2d)
    A_horizontal = horizontal_gain(bore, geo)
    return - min(-(A_horizontal + A_vertical), 30)


def vertical_gain(height_user, height_bs, distance2d):
    vertical_angle = np.degrees(math.atan((height_bs - height_user) / distance2d)) - settings.VERTICAL_BORE  # in degrees
    return - min(12 * ((vertical_angle) / settings.VERTICAL_BEAMWIDTH3DB) ** 2, 30) #I suspect that the 90 - is wrong


def horizontal_gain(bore, geo):
    horizontal_angle = bore - geo  # in degrees
    return - min(12 * (horizontal_angle / settings.HORIZONTAL_BEAMWIDTH3DB) ** 2, 30)


def shannon_capacity(snr, bandwidth):
    snr = util.to_pwr(snr)
    return bandwidth * math.log2(1 + snr)


def thermal_noise(bandwidth):
    thermal_noise = settings.BOLTZMANN * settings.TEMPERATURE * bandwidth
    return 10 * math.log10(thermal_noise) + 30  # 30 is to go from dBW to dBm


def find_noise(bandwidth, radio):
    if radio == util.BaseStationRadioType.NR:
        noise_figure = 7.8
    else:
        noise_figure = 5
    return thermal_noise(bandwidth) + noise_figure


def find_closest_angle(user_coords, bs_coords, directions, id_s):
    geo = util.find_geo(user_coords, bs_coords)
    if geo < 0:
        geo += 360
    directions = [min(abs(bore - geo), abs(bore - geo - 360)) for bore in directions]
    return int(id_s[np.argmin(directions)])


def interference(freq, user_coords, bs_interferers, base_stations, user_height):
    interf = 0
    for base_station in bs_interferers:
        OMNI = False
        # find the channel with the direction closest to the BS, as sectorized antenna's will not all interfere with a user (when on the same freq)
        bs_coords = (base_station.x, base_station.y)
        directions = list()
        ids = list()
        for channel in base_station.channels:
            if freq == channel.frequency:
                if channel.main_direction != 'Omnidirectional':
                    directions.append(channel.main_direction)
                    ids.append(channel.id)
                else:
                    OMNI = True
                    channel_id = int(channel.id)

        if not OMNI:
            channel_id = find_closest_angle(user_coords, bs_coords, directions, ids)

        for c in base_station.channels:
            if c.id == channel_id:
                channel = c

        power = channel.power

        d2d = util.distance_2d(bs_coords[0], bs_coords[1], user_coords[0], user_coords[1])
        d3d = util.distance_3d(h1=channel.height, h2=user_height, d2d=d2d)

        if channel.main_direction != 'Omnidirectional':
            antenna_gain = find_antenna_gain(channel.main_direction, util.find_geo(bs_coords, user_coords),
                                             channel.height, d2d)
        else:
            antenna_gain = 0  # TODO this is not true yet

        path_loss = pathloss(base_station.area_type, d2d, d3d, channel.frequency, channel.height)
        interf += util.to_pwr(power + antenna_gain - path_loss)
    if interf > 0:
        return util.to_db(interf)
    else:
        return 0


def find_links(p):
    links = np.zeros((p.number_of_users, p.number_of_bs))
    snrs = np.zeros((p.number_of_users, p.number_of_bs))
    sinrs = np.zeros((p.number_of_users, p.number_of_bs))
    channel_link = np.zeros((p.number_of_users, p.number_of_bs))
    capacities = np.zeros((p.number_of_users, p.number_of_bs))
    FDP = np.zeros(p.number_of_users)
    FSP = np.zeros(p.number_of_users)

    for user in p.users:
        user_coords = (user.x, user.y)
        BSs = util.find_closest_BS(user_coords, p.xbs, p.ybs)
        best_SNR = - math.inf
        for bs in BSs[:10]:  #TODO assuming that the highest SNR BS will be within the closest 10 BSs
            base_station = p.BaseStations[bs]
            for channel in base_station.channels:
                SNR = snr(user, base_station, channel, p)
                if SNR > best_SNR:
                    best_bs = bs
                    channel_id = int(channel.id)
                    best_SNR = SNR
                    SINR = SNR + interference(channel.frequency, user_coords, channel.bs_interferers, p.BaseStations,
                                          user_height=settings.UE_HEIGHT)
                    capacity = shannon_capacity(SINR, channel.bandwidth / max(1, channel.connected_users))


        if best_SNR >= settings.MINIMUM_SNR:
            snrs[user.id, best_bs] = best_SNR
            channel_link[user.id, best_bs] = channel_id
            for c in p.BaseStations[best_bs].channels:
                if c.id == channel_id:
                    c.users.append(user.id)
            links[user.id, best_bs] = 1
            capacities[user.id, best_bs] = capacity
            sinrs[user.id, best_bs] = SINR
        else:
            FDP[user.id] = 1

        if capacity > settings.RATE_REQUIREMENT:
            FSP[user.id] = 1

    return links, channel_link, snrs, sinrs, capacities, FDP, FSP


def find_capacity(p, SNR, links):
    capacity = np.zeros((p.number_of_users, p.number_of_bs))
    for bs in p.base_stations:
        bs_id = bs.id
        for user in p.users:
            user_id = user.id
            if links[user_id, bs_id] > 0:
                bandwidth = bs.channels[int(links[user_id, bs_id])].bandwidth
                capacity[user_id, bs_id] = shannon_capacity(SNR[user.id, bs.id], bandwidth)
    return capacity


if __name__ == '__main__':
    angles = np.arange(-180, 180, 1)
    gain = [find_antenna_gain(0, angle, 7, 25) for angle in angles]

    fig, ax = plt.subplots()
    plt.plot(angles, gain)
    plt.show()


    # x1, y1 = (0,0)
    # x2, y2 = (100, 10)
    # d2d = util.distance_2d(x1, y1, x2, y2)
    # d3d = util.distance_3d(h1=30, h2=settings.UE_HEIGHT, d2d=d2d)
    # print(d2d, pathloss(util.AreaType.RMA, d2d, d3d, 1850 * 1e6, 30))
    #
    # print(find_noise(1850 * 1e6, util.AreaType.RMA))
    #
    # d2d = np.arange(10, 2000, 10)
    # d3d = [util.distance_3d(h1=30, h2=settings.UE_HEIGHT, d2d = i) for i in d2d]
    # RMA = [pathloss(util.AreaType.RMA, i, j, 1850 * 1e6, 30) for i, j in zip(d2d, d3d)]
    # UMA = [pathloss(util.AreaType.UMA, i, j, 1850 * 1e6, 30) for i, j in zip(d2d, d3d)]
    # UMI = [pathloss(util.AreaType.UMI, i, j, 1850 * 1e6, 30) for i, j in zip(d2d, d3d)]
    #
    #
    # fig, ax = plt.subplots()
    # plt.plot(d2d, RMA, color = settings.colors[0], label = 'Rural')
    # plt.plot(d2d, UMA, color = settings.colors[1], label = 'Urban'  )
    # plt.plot(d2d, UMI, color = settings.colors[2], label = 'Small cell')
    #
    # plt.xlabel('Distance (m)')
    # plt.ylabel('Path loss (dB)')
    # plt.title('Path loss in non line-of-sight')
    # plt.legend()
    # plt.show()

    d2d = np.arange(10, 250, 10)
    RMA = [los_probability(i, util.AreaType.RMA) for i in d2d]
    UMA = [los_probability(i, util.AreaType.UMA) for i in d2d]
    UMI = [los_probability(i, util.AreaType.UMI) for i in d2d]

    fig, ax = plt.subplots()
    plt.plot(d2d, RMA, color = settings.colors[0], label = 'Rural')
    plt.plot(d2d, UMA, color = settings.colors[1], label = 'Urban'  )
    plt.plot(d2d, UMI, color = settings.colors[2], label = 'Small cell')

    plt.xlabel('Distance (m)')
    plt.ylabel('LoS probability')
    # plt.title('Path loss in non line-of-sight')
    plt.legend()
    plt.show()