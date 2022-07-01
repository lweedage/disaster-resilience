import math
import matplotlib.pyplot as plt
import numpy as np
import settings
import util
import progressbar
from shapely.geometry import Point
from model_3GPP import *
from scipy.sparse import lil_matrix
# code from Bart Meyers

def snr(user, base_station, channel, params):
    user_coords = (user.x, user.y)
    bs_coords = (base_station.x, base_station.y)
    power = channel.power

    d2d = util.distance_2d(base_station.x, base_station.y, user_coords[0], user_coords[1])
    d3d = util.distance_3d(h1=channel.height, h2=settings.UE_HEIGHT, d2d=d2d)

    if channel.main_direction != 'Omnidirectional':
        antenna_gain = find_antenna_gain(channel.main_direction, util.find_geo(bs_coords, user_coords), channel.height,
                                         d2d)
    else:
        antenna_gain = 0
    pl, params = pathloss(params, user.id, base_station.id, base_station.area_type, d2d, d3d, channel.frequency,
                         channel.height)

    bandwidth = channel.bandwidth
    radio = base_station.radio
    noise = find_noise(bandwidth, radio)
    return power - pl + antenna_gain - noise, params  # in dB

def snr_interf(bs, base_station, channel, params):
    user_coords = (bs.x, bs.y)
    bs_coords = (base_station.x, base_station.y)
    power = channel.power

    d2d = util.distance_2d(base_station.x, base_station.y, user_coords[0], user_coords[1])
    d3d = util.distance_3d(h1=channel.height, h2=settings.UE_HEIGHT, d2d=d2d)

    if channel.main_direction != 'Omnidirectional':
        antenna_gain = find_antenna_gain(channel.main_direction, util.find_geo(bs_coords, user_coords), channel.height,
                                         d2d)
    else:
        antenna_gain = 0
    path_loss, _ = pathloss(params, bs.id, base_station.id, base_station.area_type, d2d, d3d, channel.frequency,
                         channel.height, save = False)

    bandwidth = channel.bandwidth
    radio = base_station.radio
    noise = find_noise(bandwidth, radio)
    return power - path_loss + antenna_gain - noise  # in dB

def sinr(user, base_station, channel, params):
    user_coords = (user.x, user.y)
    bs_coords = (base_station.x, base_station.y)
    power = channel.power

    d2d = util.distance_2d(base_station.x, base_station.y, user_coords[0], user_coords[1])
    d3d = util.distance_3d(h1=channel.height, h2=settings.UE_HEIGHT, d2d=d2d)

    antenna_gain = find_antenna_gain(channel.main_direction, util.find_geo(bs_coords, user_coords), channel.height,
                                         d2d)
    path_loss, params = pathloss(params, user.id, base_station.id, base_station.area_type, d2d, d3d, channel.frequency,
                         channel.height)

    bandwidth = channel.bandwidth
    radio = base_station.radio
    noise = find_noise(bandwidth, radio)
    interf, params = interference(params, user.id, base_station.id, channel.frequency, user_coords, channel.bs_interferers, user_height=settings.UE_HEIGHT)
    return util.to_db((util.to_pwr(power) * util.to_pwr(antenna_gain)/util.to_pwr(path_loss))/(util.to_pwr(noise) + interf)), params


def highest_snr(bs, base_station, channels, params):
    snrs = list()
    for channel in channels:
        snrs.append(snr_interf(bs, base_station, channel, params))
    return max(snrs)


def find_antenna_gain(bore, geo, height_bs, d2d):
    A_vertical = vertical_gain(settings.UE_HEIGHT, height_bs, d2d)
    # A_vertical = 30
    A_horizontal = horizontal_gain(bore, geo)
    return - min(-(A_horizontal + A_vertical), 30)


def vertical_gain(height_user, height_bs, distance2d):
    vertical_angle = math.atan((height_bs - height_user) / distance2d) - settings.VERTICAL_BORE  # in radians
    return - min(util.to_db(12 * (vertical_angle / settings.VERTICAL_BEAMWIDTH3DB) ** 2), 30)  # I suspect that the 90 - is wrong


def horizontal_gain(bore, geo):
    horizontal_angle = bore - geo  # in degrees
    return - min(util.to_db(12 * (horizontal_angle / settings.HORIZONTAL_BEAMWIDTH3DB) ** 2), 30)


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


def find_closest_angle(bs_coords,user_coords, directions, id_s):
    geo = util.find_geo(bs_coords, user_coords)
    if geo < 0:
        geo += 360
    dirs = [min(abs(bore - geo), abs(bore - geo - 360)) for bore in directions]
    return int(id_s[np.argmin(dirs)])


def interference(params, user_id, bs_id, freq, user_coords, bs_interferers, user_height):
    interf = []
    if params.interference[freq][user_id, bs_id] != 0:
        return params.interference[freq][user_id, bs_id], params
    else:
        for base_station in bs_interferers:
            # find the channel with the direction closest to the BS, as sectorized antenna's will not all interfere with a user (when on the same freq)
            bs_coords = (base_station.x, base_station.y)
            directions = list()
            ids = list()

            for channel in base_station.channels:
                if channel.frequency == freq:
                    directions.append(channel.main_direction)
                    ids.append(channel.id)

            channel_id = find_closest_angle(bs_coords, user_coords, directions, ids)

            for c in base_station.channels:
                if int(c.id) == channel_id:
                    interfering_channel = c

            power = interfering_channel.power

            d2d = util.distance_2d(bs_coords[0], bs_coords[1], user_coords[0], user_coords[1])
            d3d = util.distance_3d(h1=interfering_channel.height, h2=user_height, d2d=d2d)

            antenna_gain = find_antenna_gain(interfering_channel.main_direction, util.find_geo(bs_coords, user_coords),
                                                 interfering_channel.height, d2d)

            path_loss, params = pathloss(params, user_id, base_station.id, base_station.area_type, d2d, d3d, interfering_channel.frequency,
                                 interfering_channel.height)
            interf.append(util.to_pwr(power + antenna_gain - path_loss))

        if len(interf) > 0:
            params.interference[freq][user_id, bs_id] = sum(interf)
            return sum(interf), params
        else:
            params.interference[freq][user_id, bs_id] = 0
            return 0, params


def find_links(p):
    links = util.from_data(f'data/Realisations/{p.filename}{p.seed}_links.p')
    snrs = util.from_data(f'data/Realisations/{p.filename}{p.seed}_snrs.p')
    sinrs = util.from_data(f'data/Realisations/{p.filename}{p.seed}_sinrs.p')
    capacities = util.from_data(f'data/Realisations/{p.filename}{p.seed}_capacities.p')
    FDP = util.from_data(f'data/Realisations/{p.filename}{p.seed}_FDP.p')
    FSP = util.from_data(f'data/Realisations/{p.filename}{p.seed}_FSP.p')
    satisfaction_level = util.from_data(f'data/Realisations/{p.filename}{p.seed}_satisfaction_level.p')
    channel_link = util.from_data(f'data/Realisations/{p.filename}{p.seed}_channel_link.p')

    if links is None:
        links = lil_matrix((p.number_of_users, p.number_of_bs))
        snrs = lil_matrix((p.number_of_users, p.number_of_bs))
        sinrs = lil_matrix((p.number_of_users, p.number_of_bs))
        channel_link = lil_matrix((p.number_of_users, p.number_of_bs))
        capacities = np.zeros(p.number_of_users)
        FDP = np.zeros(p.number_of_users)
        FSP = np.zeros(p.number_of_users)
        satisfaction_level = np.zeros(p.number_of_users)

        bar = progressbar.ProgressBar(maxval=p.number_of_users, widgets=[
            progressbar.Bar('=', f'Finding links {p.filename} [', ']'), ' ',
            progressbar.Percentage(), ' ', progressbar.ETA()])
        bar.start()
        for user in p.users:
            bar.update(int(user.id))
            user_coords = (user.x, user.y)
            BSs = util.find_closest_BS(user_coords, p.xbs, p.ybs)
            best_SINR = - math.inf
            measure = -math.inf

            for bs in BSs[:10]:  # assuming that the highest SNR BS will be within the closest 10 BSs
                base_station = p.BaseStations[bs]
                for channel in base_station.channels:
                    SINR, p = sinr(user, base_station, channel, p)
                    if SINR / max(1, channel.connected_users) > measure:
                        best_bs = bs
                        channel_id = int(channel.id)
                        best_SINR = SINR
                        measure = SINR/(max(1, channel.connected_users))
                        SNR, p = snr(user, base_station, channel, p)
            if best_SINR >= settings.MINIMUM_SNR:
                sinrs[user.id, best_bs] = best_SINR
                channel_link[user.id, best_bs] = channel_id
                for c in p.BaseStations[best_bs].channels:
                    if int(c.id) == channel_id:
                        c.add_user(user.id)
                links[user.id, best_bs] = 1
                snrs[user.id, best_bs] = SNR
            else:
                FDP[user.id] = 1
            # p.path_loss[user.id, :] = 0
            # print(best_SINR, SNR)
        bar.finish()

        # for now, we share the bandwidth equally over the users. water-filling algorithm would also be possible? Or proportionally fair allocation
        print('Now, we find the capacities')
        for bs in p.BaseStations:
            for c in bs.channels:
                if len(c.users) > 0:
                    # first, find the spectral efficiency of all users in this channel
                    SE = [math.log2(1 + util.to_pwr(sinrs[user, bs.id])) for user in c.users]
                    # then, we find the required bandwidth per user
                    BW = [p.users[user].rate_requirement/SE[i] for i, user in zip(range(len(SE)), c.users)]
                    # if there is more BW required than the channel has, we decrease the BW with that percentage for everyone
                    BW = np.multiply(min(len(c.users), 8) * c.bandwidth/sum(BW), BW) #TODO I assume a BS has 8 channels?
                    for i, user in zip(range(len(c.users)), c.users):
                        capacity = shannon_capacity(sinrs[user, bs.id], BW[i])
                        capacities[user] += capacity
                        if capacities[user] > p.users[user].rate_requirement:
                            FSP[user] = 1
                            satisfaction_level[user] = 1
                        else:
                            satisfaction_level[user] = capacities[user] / p.users[user].rate_requirement


        util.to_data(links, f'data/Realisations/{p.filename}{p.seed}_links.p')
        util.to_data(snrs, f'data/Realisations/{p.filename}{p.seed}_snrs.p')
        util.to_data(sinrs, f'data/Realisations/{p.filename}{p.seed}_sinrs.p')
        util.to_data(capacities, f'data/Realisations/{p.filename}{p.seed}_capacities.p')
        util.to_data(FDP, f'data/Realisations/{p.filename}{p.seed}_FDP.p')
        util.to_data(FSP, f'data/Realisations/{p.filename}{p.seed}_FSP.p')
        util.to_data(satisfaction_level, f'data/Realisations/{p.filename}{p.seed}_satisfaction_level.p')

    return links, channel_link, snrs, sinrs, capacities, FDP, FSP, satisfaction_level

def proportional_bandwidth(bandwidth, SE, index):
    return bandwidth / (SE[index] * sum(1/x for x in SE))

# def find_capacity(p, SNR, links):
#     capacity = np.zeros((p.number_of_users, p.number_of_bs))
#     for bs in p.base_stations:
#         bs_id = bs.id
#         for user in p.users:
#             user_id = user.id
#             if links[user_id, bs_id] > 0:
#                 bandwidth = bs.channels[int(links[user_id, bs_id])].bandwidth
#                 capacity[user_id, bs_id] = shannon_capacity(SNR[user.id, bs.id], bandwidth)
#     return capacity

def specify_measures(p, fsp, fdp, satisfaction_level, cap):
    FDP = util.from_data(f'data/Realisations/FDP_per_region{p.filename}.p')
    if FDP is None:
        FDP = dict()
        FSP = dict()
        satisfaction = dict()
        capacity = dict()

        bar = progressbar.ProgressBar(maxval=p.number_of_users, widgets=[
            progressbar.Bar('=', f'Finding FDP/FSP/sat {p.filename} [', ']'), ' ',
            progressbar.Percentage(), ' ', progressbar.ETA()])
        bar.start()

        for i, x, y in zip(range(p.number_of_users), p.x_user, p.y_user):
            bar.update(i)
            point = Point(x, y)
            condition = p.zip_code_region['geometry'].contains(point)
            zipcode = p.zip_code_region.loc[condition]['postcode'].item()

            if zipcode in FDP.keys():
                FDP[zipcode].append(fdp[i])
                FSP[zipcode].append(fsp[i])
                satisfaction[zipcode].append(satisfaction_level[i])
                capacity[zipcode].append(cap[i])

            else:
                FDP[zipcode] = [fdp[i]]
                FSP[zipcode] = [fsp[i]]
                satisfaction[zipcode] = [satisfaction_level[i]]
                capacity[zipcode] = [cap[i]]

        bar.finish()

        util.to_data(FDP, f'data/Realisations/FDP_per_region{p.filename}.p')
        util.to_data(FSP, f'data/Realisations/FSP_per_region{p.filename}.p')
        util.to_data(satisfaction, f'data/Realisations/satisfaction_per_region{p.filename}.p')
        util.to_data(capacity, f'data/Realisations/capacity_per_region{p.filename}.p')

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
    plt.plot(d2d, RMA, color=settings.colors[0], label='Rural')
    plt.plot(d2d, UMA, color=settings.colors[1], label='Urban')
    plt.plot(d2d, UMI, color=settings.colors[2], label='Small cell')

    plt.xlabel('Distance (m)')
    plt.ylabel('LoS probability')
    # plt.title('Path loss in non line-of-sight')
    plt.legend()
    plt.show()


