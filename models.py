import progressbar
from scipy.sparse import lil_matrix

from model_3GPP import *


# code adapted from Bart Meyers: https://github.com/BartJM/ResilSimulator

def snr(user, base_station, channel, params):
    user_coords = (user.x, user.y)
    bs_coords = (base_station.x, base_station.y)
    power = channel.power

    d2d = util.distance_2d(base_station.x, base_station.y, user_coords[0], user_coords[1])
    d3d = util.distance_3d(h1=channel.height, h2=settings.UE_HEIGHT, d2d=d2d)

    if channel.main_direction != 'Omnidirectional':
        antenna_gain = find_antenna_gain(channel.main_direction, util.find_geo(bs_coords, user_coords))
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
        antenna_gain = find_antenna_gain(channel.main_direction, util.find_geo(bs_coords, user_coords))
    else:
        antenna_gain = 0
    if d2d <= 10_000:
        path_loss, _ = pathloss(params, bs.id, base_station.id, base_station.area_type, d2d, d3d, channel.frequency,
                                channel.height, save=False)
        bandwidth = channel.bandwidth
        radio = base_station.radio
        noise = find_noise(bandwidth, radio)
        return power - path_loss + antenna_gain - noise  # in dB
    else:
        return 0


def sinr(user, base_station, channel, params):
    user_coords = (user.x, user.y)
    bs_coords = (base_station.x, base_station.y)
    power = channel.power

    d2d = util.distance_2d(base_station.x, base_station.y, user_coords[0], user_coords[1])
    d3d = util.distance_3d(h1=channel.height, h2=settings.UE_HEIGHT, d2d=d2d)

    if d2d <= 5_000:
        antenna_gain = find_antenna_gain(channel.main_direction, util.find_geo(bs_coords, user_coords))
        path_loss, params = pathloss(params, user.id, base_station.id, base_station.area_type, d2d, d3d,
                                     channel.frequency, channel.height)
        if path_loss < math.inf:
            bandwidth = channel.bandwidth
            radio = base_station.radio
            noise = find_noise(bandwidth, radio)
            interf, params = interference(params, user.id, base_station.id, channel.frequency, user_coords,
                                          channel.bs_interferers, user_height=settings.UE_HEIGHT)
            return util.to_db(util.to_pwr(power) * util.to_pwr(antenna_gain) / util.to_pwr(path_loss) / (
                    util.to_pwr(noise) + interf)), params
        else:
            return -math.inf, params
    else:
        return - math.inf, params


def find_antenna_gain(bore, geo):
    A_vertical = 0
    A_horizontal = horizontal_gain(bore, geo)
    return - min(-(A_horizontal + A_vertical), 20)


def horizontal_gain(bore, geo):
    horizontal_angle = bore - geo  # in degrees
    if horizontal_angle > 180:
        horizontal_angle -= 360
    return - min(12 * (horizontal_angle / settings.HORIZONTAL_BEAMWIDTH3DB) ** 2, 20)


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


def find_closest_angle(bs_coords, user_coords, directions, id_s):
    geo = util.find_geo(bs_coords, user_coords)
    if geo < 0:
        geo += 360
    dirs = [min(abs(bore - geo), abs(bore - geo - 360)) for bore in directions]
    return int(id_s[np.argmin(dirs)])


def interference(params, user_id, bs_id, freq, user_coords, bs_interferers, user_height):
    interf = []
    bs_interf_coord = (params.BaseStations[bs_id].x, params.BaseStations[bs_id].y)
    if params.interference[freq][user_id, bs_id] != 0:
        return params.interference[freq][user_id, bs_id], params
    else:
        for base_station in bs_interferers[settings.CUTOFF_VALUE_INTERFERENCE:]:
            # find the channel with the direction closest to the BS, as sectorized antenna's will not all interfere with a user (when on the same freq)
            bs_coords = (base_station.x, base_station.y)

            if bs_coords != bs_interf_coord:
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

                if d2d <= 10_000:
                    antenna_gain = find_antenna_gain(interfering_channel.main_direction,
                                                     util.find_geo(bs_coords, user_coords))

                    path_loss, params = pathloss(params, user_id, base_station.id, base_station.area_type, d2d, d3d,
                                                 interfering_channel.frequency,
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
    channel_link = util.from_data(f'data/Realisations/{p.filename}{p.seed}_channel_link.p')
    interf_loss = util.from_data(f'data/Realisations/{p.filename}{p.seed}_interference_loss.p')

    if interf_loss is None:
        links = lil_matrix((p.number_of_users, p.number_of_bs))
        snrs = lil_matrix((p.number_of_users, p.number_of_bs))
        sinrs = lil_matrix((p.number_of_users, p.number_of_bs))
        channel_link = lil_matrix((p.number_of_users, p.number_of_bs))
        capacities = np.zeros(p.number_of_users)
        FDP = np.zeros(p.number_of_users)
        FSP = np.zeros(p.number_of_users)
        interf_loss = np.zeros(p.number_of_users)

        bar = progressbar.ProgressBar(maxval=p.number_of_users, widgets=[
            progressbar.Bar('=', f'Finding links {p.filename} [', ']'), ' ',
            progressbar.Percentage(), ' ', progressbar.ETA()])
        bar.start()

        for user in p.users:
            bar.update(int(user.id))
            user_coords = (user.x, user.y)
            BSs = util.find_closest_BS(user_coords, p.xbs, p.ybs)
            best_SINR = - math.inf
            best_measure = -math.inf

            for bs in BSs[:10]:  # assuming that the highest SNR BS will be within the closest 10 BSs
                if bs != p.failed_BS:
                    base_station = p.BaseStations[bs]
                    if not p.geographic_failure or (
                            p.geographic_failure and (base_station.x, base_station.y) != p.failed_BS_coords):
                        for channel in base_station.channels:
                            SINR, p = sinr(user, base_station, channel, p)
                            # a user connects to the BS with highest SINR/degree
                            if SINR / max(1, len(channel.users)) > best_measure and SINR >= settings.MINIMUM_SNR:
                                best_bs = bs
                                channel_id = int(channel.id)
                                best_SINR = SINR
                                SNR, p = snr(user, base_station, channel, p)
                                best_measure = SINR / max(len(channel.users), 1)
            if best_SINR >= settings.MINIMUM_SNR:
                interf_loss[user.id] = SNR - best_SINR

                sinrs[user.id, best_bs] = best_SINR
                channel_link[user.id, best_bs] = channel_id
                for c in p.BaseStations[best_bs].channels:
                    if int(c.id) == channel_id:
                        c.add_user(user.id)
                links[user.id, best_bs] = 1
                snrs[user.id, best_bs] = SNR
            else:
                FDP[user.id] = 1

        bar.finish()

        print('Now, we find the capacities')
        for bs in p.BaseStations:
            for c in bs.channels:
                if len(c.users) > 0:
                    # first, find the spectral efficiency of all users in this channel
                    SE = [math.log2(1 + util.to_pwr(sinrs[user, bs.id])) for user in c.users]
                    # then, we find the required bandwidth per user
                    BW = [p.users[user].rate_requirement / SE[i] for i, user in zip(range(len(SE)), c.users)]
                    # if there is more BW required than the channel has, we decrease the BW with that percentage for everyone
                    BW = np.multiply(min(len(c.users), 1) * c.bandwidth / sum(BW), BW)

                    for i, user in zip(range(len(c.users)), c.users):
                        capacity = shannon_capacity(sinrs[user, bs.id], BW[i])
                        capacities[user] += capacity
                        if capacities[user] > p.users[user].rate_requirement:
                            FSP[user] = 1

        if p.seed == 1:
            util.to_data(links, f'data/Realisations/{p.filename}{p.seed}_links.p')
            util.to_data(snrs, f'data/Realisations/{p.filename}{p.seed}_snrs.p')
            util.to_data(sinrs, f'data/Realisations/{p.filename}{p.seed}_sinrs.p')
        util.to_data(capacities, f'data/Realisations/{p.filename}{p.seed}_capacities.p')
        util.to_data(FDP, f'data/Realisations/{p.filename}{p.seed}_FDP.p')
        util.to_data(FSP, f'data/Realisations/{p.filename}{p.seed}_FSP.p')
        util.to_data(FSP, f'data/Realisations/{p.filename}{p.seed}_interference_loss.p')

    return links, channel_link, snrs, sinrs, capacities, FDP, FSP, interf_loss


def find_links_heatmap(p):
    sinrs = util.from_data(f'data/Realisations/{p.filename}{p.seed}_sinrs.p')
    if sinrs is None:
        sinrs = np.zeros(p.number_of_users)
        bar = progressbar.ProgressBar(maxval=p.number_of_users, widgets=[
            progressbar.Bar('=', f'Finding links {p.filename} [', ']'), ' ',
            progressbar.Percentage(), ' ', progressbar.ETA()])
        bar.start()
        for user in p.users:
            bar.update(int(user.id))
            user_coords = (user.x, user.y)
            BSs = util.find_closest_BS(user_coords, p.xbs, p.ybs)
            best_SINR = - 1000
            for bs in BSs[:10]:  # assuming that the highest SINR BS will be within the closest 10 BSs
                if bs != p.failed_BS:
                    base_station = p.BaseStations[bs]
                    if not p.geographic_failure or (
                            p.geographic_failure and (base_station.x, base_station.y) != p.failed_BS_coords):
                        for channel in base_station.channels:
                            SINR, p = sinr(user, base_station, channel, p)
                            if SINR > best_SINR:
                                best_SINR = SINR

            sinrs[int(user.id)] = best_SINR

        bar.finish()
        util.to_data(sinrs, f'data/Realisations/{p.filename}{p.seed}_sinrs.p')
    return sinrs
