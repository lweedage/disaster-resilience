import progressbar
from scipy.sparse import lil_matrix

from model_3GPP import *
import cvxpy as cp


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

    if d2d <= 5_000 and util.to_pwr(power) != 0:
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


def find_links_new(p):
    links = util.from_data(f'data/Realisations/{p.filename}{p.seed}_links.p')
    snrs = util.from_data(f'data/Realisations/{p.filename}{p.seed}_snrs.p')
    sinrs = util.from_data(f'data/Realisations/{p.filename}{p.seed}_sinrs.p')
    capacities = util.from_data(f'data/Realisations/{p.filename}{p.seed}_capacities.p')
    FDP = util.from_data(f'data/Realisations/{p.filename}{p.seed}_FDP.p')
    FSP = util.from_data(f'data/Realisations/{p.filename}{p.seed}_FSP.p')
    channel_link = util.from_data(f'data/Realisations/{p.filename}{p.seed}_channel_link.p')
    total_p = util.from_data(f'data/Realisations/{p.filename}{p.seed}_total_power.p')
    power_per_MNO = util.from_data(f'data/Realisations/{p.filename}{p.seed}_power_per_MNO.p')
    connections = util.from_data(f'data/Realisations/{p.filename}{p.seed}_connections.p')

    links_fp = util.from_data(f'data/Realisations/{p.filename}{p.seed}_links_fp.p')
    snrs_fp = util.from_data(f'data/Realisations/{p.filename}{p.seed}_snrs_fp.p')
    sinrs_fp = util.from_data(f'data/Realisations/{p.filename}{p.seed}_sinrs_fp.p')
    capacities_fp = util.from_data(f'data/Realisations/{p.filename}{p.seed}_capacities_fp.p')
    FDP_fp = util.from_data(f'data/Realisations/{p.filename}{p.seed}_FDP_fp.p')
    FSP_fp = util.from_data(f'data/Realisations/{p.filename}{p.seed}_FSP_fp.p')
    channel_link_fp = util.from_data(f'data/Realisations/{p.filename}{p.seed}_channel_link_fp.p')
    power_per_MNO_fp = util.from_data(f'data/Realisations/{p.filename}{p.seed}_power_per_MNO_fp.p')
    connections_fp = util.from_data(f'data/Realisations/{p.filename}{p.seed}_connections_fp.p')

    # FDP = None
    if FDP_fp is None:
        connections = None
        connections_fp = None
        links_fp = lil_matrix((p.number_of_users, p.number_of_bs))
        snrs_fp = lil_matrix((p.number_of_users, p.number_of_bs))
        sinrs_fp = lil_matrix((p.number_of_users, p.number_of_bs))
        channel_link_fp = lil_matrix((p.number_of_users, p.number_of_bs))
        FDP_fp = np.zeros(p.number_of_users)

        maximum = 20

        bar = progressbar.ProgressBar(maxval=p.number_of_users, widgets=[
            progressbar.Bar('=', f'Finding links {p.filename} [', ']'), ' ',
            progressbar.Percentage(), ' ', progressbar.ETA()])
        bar.start()

        connections_fp = {'KPN': {'KPN': 0, 'T-Mobile': 0, 'Vodafone': 0},
                       'T-Mobile': {'KPN': 0, 'T-Mobile': 0, 'Vodafone': 0},
                       'Vodafone': {'KPN': 0, 'T-Mobile': 0, 'Vodafone': 0}, 'no': {'KPN': 0, 'T-Mobile': 0, 'Vodafone': 0}}

        disconnected_users = []
        for user in p.users:

            bar.update(int(user.id))
            user_coords = (user.x, user.y)
            BSs = util.find_closest_BS(user_coords, p.xbs, p.ybs)
            best_SINR = - math.inf
            best_measure = -math.inf

            for bs in BSs[:maximum]:  # assuming that the highest SINR BS will be within the closest 20 BSs
                if bs != p.failed_BS:
                    base_station = p.BaseStations[bs]
                    if not p.back_up or (user.provider == base_station.provider and p.back_up):
                        if not p.geographic_failure or (
                                p.geographic_failure and (base_station.x, base_station.y) != p.failed_BS_coords):
                            for channel in base_station.channels:
                                SINR, p = sinr(user, base_station, channel, p)
                                # a user connects to the BS with highest SINR/degree
                                if SINR / max(1, len(channel.users)) > best_measure and SINR >= settings.MINIMUM_SNR - settings.PRECISION_MARGIN:
                                    best_bs = bs
                                    channel_id = int(channel.id)
                                    best_SINR = SINR
                                    SNR, p = snr(user, base_station, channel, p)
                                    best_measure = SINR / max(len(channel.users), 1)
            if best_SINR >= settings.MINIMUM_SNR - settings.PRECISION_MARGIN:
                sinrs_fp[user.id, best_bs] = best_SINR
                channel_link_fp[user.id, best_bs] = channel_id
                for c in p.BaseStations[best_bs].channels:
                    if int(c.id) == channel_id:
                        c.add_user(user.id)
                        """ # Teste, remover!
                        bs = p.BaseStations[best_bs]
                        user_coords = (user.x, user.y)
                        bs_coords = (bs.x, bs.y)

                        d2d = util.distance_2d(bs.x, bs.y, user_coords[0], user_coords[1])
                        d3d = util.distance_3d(h1=c.height, h2=settings.UE_HEIGHT, d2d=d2d)
                        # Find gain and losses
                        antenna_gain = find_antenna_gain(c.main_direction, util.find_geo(bs_coords, user_coords))
                        path_loss, p = pathloss(p, user.id, bs.id, bs.area_type, d2d, d3d,
                                                    c.frequency, c.height)
                        noise = find_noise(c.bandwidth, bs.radio)
                        interf, p = interference(p, user.id, bs.id, c.frequency, user_coords,
                                                    c.bs_interferers, user_height=settings.UE_HEIGHT)
                        newPaux = util.to_pwr(path_loss)*(util.to_pwr(noise) + interf)*(settings.MINIMUM_SNR)/util.to_pwr(antenna_gain)
                        newPaux_dBW = util.to_pwr(path_loss)*(util.dbm_to_pwr(noise) + interf/1000)*(settings.MINIMUM_SNR)/util.to_pwr(antenna_gain)
                        maxP_W = util.dbm_to_pwr(c.max_power)
                        SINR, p = sinr(user, bs, c, p)
                        shouldBemaxP = util.to_pwr(path_loss)*(util.to_pwr(noise) + interf)*(util.to_pwr(SINR))/util.to_pwr(antenna_gain)
                        maxP_mW = util.to_pwr(c.max_power)
                        if(newPaux > util.to_pwr(c.max_power)):
                            SINR, p = sinr(user, bs, c, p)
                            bug = 1 """

                links_fp[user.id, best_bs] = 1
                snrs_fp[user.id, best_bs] = SNR
                connections_fp[p.BaseStations[best_bs].provider][user.provider] += 1
            elif p.back_up:
                disconnected_users.append(user)
            else:
                FDP_fp[user.id] = 1
                connections_fp['no'][user.provider] += 1

        # print(connections)
        # # print([p.BaseStations[id].provider for id in range(len(p.BaseStations))])
        # print('Total number of disconnected users:', len(disconnected_users), 'out of', len(p.users))
        # print('Disconnected per MNO:', disconnected)


        for user in disconnected_users:
            best_SINR = - math.inf
            best_measure = -math.inf
            user_coords = (user.x, user.y)
            BSs = util.find_closest_BS(user_coords, p.xbs, p.ybs)
            for bs in BSs[:maximum]:  # assuming that the highest SNR BS will be within the closest 10 BSs
                base_station = p.BaseStations[bs]
                if base_station.provider != user.provider:
                    for channel in base_station.channels:
                        SINR, p = sinr(user, base_station, channel, p)
                        # a user connects to the BS with highest SINR/degree
                        if SINR / max(1, len(channel.users)) > best_measure and SINR >= settings.MINIMUM_SNR - settings.PRECISION_MARGIN:
                            best_bs = bs
                            channel_id = int(channel.id)
                            best_SINR = SINR
                            SNR, p = snr(user, base_station, channel, p)
                            best_measure = SINR / max(len(channel.users), 1)
            if best_SINR >= settings.MINIMUM_SNR - settings.PRECISION_MARGIN:
                sinrs_fp[user.id, best_bs] = best_SINR
                channel_link_fp[user.id, best_bs] = channel_id
                for c in p.BaseStations[best_bs].channels:
                    if int(c.id) == channel_id:
                        c.add_user(user.id)                      
                links_fp[user.id, best_bs] = 1
                snrs_fp[user.id, best_bs] = SNR
                connections_fp[p.BaseStations[best_bs].provider][user.provider] += 1
            else:
                FDP_fp[user.id] = 1
                connections_fp['no'][user.provider] += 1

        # print(connections_disconnected)
        bar.finish()

        print('Now, we find the capacities')


        capacities_fp, FSP_fp = find_capacity(p, sinrs_fp)
        
        # Calculate the total power
        total_p_fp = 0
        power_per_MNO_fp = {MNO: 0 for MNO in ['KPN', 'T-Mobile', 'Vodafone']}
        for bs in p.BaseStations:
            for c in bs.channels:
                # first convert from dBm to dBW (-30)
                total_p_fp += util.to_pwr(c.power -30)
                power_per_MNO_fp[bs.provider] += util.to_pwr(c.power - 30)
        

        # Recalculate the SINRs (and everything that depends on it, e.g FSP) here using only the necessary power to meet the requiremets? Maybe after that, more users cold be conected due to less interference.
        # TODO: 
        # [x] add a new variable to represent the max power per channel and use the channel.power as an adaptative transmit power
        # [x] Solve a power min prob. (for each channel iteratively or globally?) with a constraint on the data rate requirement (assume user association as given and only decide on the power)
        # [x] If outage, use full power.
        # [x] Save links to avoid long simulation for test purposes?
        # [x] Calculate FSP, FDP etc with the old approach (using full power), then compare with the new approach        
        links = lil_matrix((p.number_of_users, p.number_of_bs))
        snrs = lil_matrix((p.number_of_users, p.number_of_bs))
        sinrs = lil_matrix((p.number_of_users, p.number_of_bs))
        channel_link = lil_matrix((p.number_of_users, p.number_of_bs))
        #capacities = np.zeros(p.number_of_users)
        FDP = np.zeros(p.number_of_users)
        #FSP = np.zeros(p.number_of_users)
        #interf_loss = np.zeros(p.number_of_users)



        # TODO: Add a new loop with a fix number of iterations (to allow further power decrease)
        # Set interference to zero to allow recalculation
        number_iterations = 4
        for iter in range(number_iterations):
            # Update the power necessary for each channel of each BS.
            bar = progressbar.ProgressBar(maxval=p.number_of_bs, widgets=[
                progressbar.Bar('=', f'Updating transmit power {iter} {p.filename} [', ']'), ' ',
                progressbar.Percentage(), ' ', progressbar.ETA()])
            bar.start()
            p.clear_interference()
            for bs in p.BaseStations:
                bar.update(int(bs.id))
                for c in bs.channels:
                    if len(c.users) > 0:
                        # first, find the spectral efficiency of all users in this channel
                        #SE = [math.log2(1 + util.to_pwr(sinrs[user, bs.id])) for user in c.users]
                        SE = [math.log2(1 + util.to_pwr(sinr(p.users[user], bs, c, p)[0])) for user in c.users]
                        # then, we find the required bandwidth per user
                        BW = [p.users[user].rate_requirement / SE[i] for i, user in zip(range(len(SE)), c.users)]
                        # Fraction of required BW
                        frac_BW = np.sum([BW[i]/c.bandwidth for i in range(len(BW))])
                        #Nii = [frac_BW*c.bandwidth/BW[i] for i in range(len(BW))]
                        # if there is more BW required than the channel has, we decrease the BW with that percentage for everyone
                        BW = np.multiply(min(len(c.users), 1) * c.bandwidth / sum(BW), BW)
                        Ei = BW/c.bandwidth
                        #Ni = 1/Ei

                        # If there is enough power to serve all the users with QoS guarantee, then optimize the BS power
                        if frac_BW <= 1:
                            # Create variables and parameters.
                            #Pj, Ei = cp.Variable(), cp.Variable(shape = (len(c.users),))
                            """ Pj = cp.Variable()
                            Ni = cp.Variable(shape = (len(c.users),)) # Variable substitution Ni = 1/Ei, where Ei is the fraction of time user i transmits.
                            # Creates the list of constraints and adds the constraints on transmit power and time sharing
                            constraints = list()
                            constraints.append(Ni>=1) # Equivalent to 0 < Ei <= 1
                            constraints.append(cp.harmonic_mean(Ni) >= len(c.users)) # Equivalent to sum(Ei)<=1
                            constraints.append(Pj>=0)
                            constraints.append(Pj<=util.to_pwr(c.max_power))

                            for i, user in zip(range(len(c.users)), c.users):
                                user_obj = p.users[user]
                                user_coords = (user_obj.x, user_obj.y)
                                bs_coords = (bs.x, bs.y)

                                d2d = util.distance_2d(bs.x, bs.y, user_coords[0], user_coords[1])
                                d3d = util.distance_3d(h1=c.height, h2=settings.UE_HEIGHT, d2d=d2d)
                                # Find gain and losses
                                antenna_gain = find_antenna_gain(c.main_direction, util.find_geo(bs_coords, user_coords))
                                path_loss, p = pathloss(p, user_obj.id, bs.id, bs.area_type, d2d, d3d,
                                                            c.frequency, c.height)
                                noise = find_noise(c.bandwidth, bs.radio)
                                interf, p = interference(p, user_obj.id, bs.id, c.frequency, user_coords,
                                                            c.bs_interferers, user_height=settings.UE_HEIGHT)
                                # creates the data rate constraints for each user served by channel c
                                constraints.append(Pj*util.to_pwr(antenna_gain) / util.to_pwr(path_loss) - (util.to_pwr(noise) + interf)*(cp.exp(cp.multiply(np.log(2),((Ni[i]*user_obj.rate_requirement)/(c.bandwidth)))) -1) >= 0)
                                #a**x = cp.exp(cp.multiply(np.log(a), x))
                                #constraints.append(Pj*util.to_pwr(antenna_gain) / util.to_pwr(path_loss) - (util.to_pwr(noise) + interf)*(2**((user_obj.rate_requirement)/(Ei[i]*c.bandwidth)) -1) >= 0)

                            prob1 = cp.Problem(cp.Minimize(Pj), constraints)

                            try:
                                prob1.solve(solver='MOSEK') # TODO: Why it is returning infeasible in some cases?
                            except Exception as e:
                                print(e)
                            #Power_dB = util.to_db(Pj.value)
                            #c.update_power(Pj.value) """

                            #for given Ei
                            newP = -math.inf
                            for i, user in zip(range(len(c.users)), c.users):
                                user_obj = p.users[user]
                                user_coords = (user_obj.x, user_obj.y)
                                bs_coords = (bs.x, bs.y)

                                d2d = util.distance_2d(bs.x, bs.y, user_coords[0], user_coords[1])
                                d3d = util.distance_3d(h1=c.height, h2=settings.UE_HEIGHT, d2d=d2d)
                                # Find gain and losses
                                antenna_gain = find_antenna_gain(c.main_direction, util.find_geo(bs_coords, user_coords))
                                path_loss, p = pathloss(p, user_obj.id, bs.id, bs.area_type, d2d, d3d,
                                                            c.frequency, c.height)
                                noise = find_noise(c.bandwidth, bs.radio)
                                interf, p = interference(p, user_obj.id, bs.id, c.frequency, user_coords,
                                                            c.bs_interferers, user_height=settings.UE_HEIGHT)
                                # Minimum power (im mW) to transmit in the req data rate
                                newPaux = util.to_pwr(path_loss)*(util.to_pwr(noise) + interf)*(2**((user_obj.rate_requirement)/(Ei[i]*c.bandwidth)) -1)/util.to_pwr(antenna_gain)
                                if (newPaux>newP):
                                    newP = newPaux
                                # Minimum power (im mW) to stay connected
                                newPaux = util.to_pwr(path_loss)*(util.to_pwr(noise) + interf)*(util.to_pwr(settings.MINIMUM_SNR))/util.to_pwr(antenna_gain)
                                if (newPaux>newP):
                                    newP = newPaux
                            newP_dBm = util.to_db(newP)
                            c.update_power(newP) # Power in mW
                    else:
                        c.update_power(0)
            bar.finish()
            # Calculate the total power
            total_p = 0
            power_per_MNO = {MNO: 0 for MNO in ['KPN', 'T-Mobile', 'Vodafone']}
            for bs in p.BaseStations:
                for c in bs.channels:
                    # first convert from dBm to dBW (-30)
                    total_p += util.to_pwr(c.power - 30)
                    power_per_MNO[bs.provider] += util.to_pwr(c.power - 30)
            #print(f"Power iteration {iter}: {total_p}")
        

        fraction_power = total_p_fp/total_p


        # Recalculate links, FDP etc.
        bar = progressbar.ProgressBar(maxval=p.number_of_users, widgets=[
            progressbar.Bar('=', f'Recalculating SINR, FSP, etc. {p.filename} [', ']'), ' ',
            progressbar.Percentage(), ' ', progressbar.ETA()])
        bar.start()

        connections = connections_fp
        links = links_fp

        for user in p.users:
            bar.update(int(user.id))

            # Checks if all the connected users can stay connected
            BS_indices = links.getrow(user.id).nonzero()[1] # Gets the BS associated to the user assuming a single link per user 
            if(len(BS_indices) > 0):
                serving_BS_id = BS_indices[0]
                base_station = p.BaseStations[serving_BS_id]
                for channel in base_station.channels:
                    if (user.id in channel.users):
                        SINR, p = sinr(user, base_station, channel, p)
                        SNR, p = snr(user, base_station, channel, p)
                        if SINR >= settings.MINIMUM_SNR - settings.PRECISION_MARGIN:
                            sinrs[user.id, base_station.id] = SINR
                            snrs[user.id, base_station.id] = SNR
                            channel_link[user.id, base_station.id] = int(channel.id)
                        else: # If the user cannot connect anymore
                            FDP[user.id] = 1
                            links[user.id, base_station.id] = 0
                            connections[base_station.provider][user.provider] -= 1
            else:# Checks if any of the disconnected users can now connect to any of the BSs
                # TODO: Do we need to restrict the new conections to certain MNOs here?
                user_coords = (user.x, user.y)
                BSs = util.find_closest_BS(user_coords, p.xbs, p.ybs)
                best_SINR = - math.inf
                best_measure = -math.inf
                for bs in BSs[:maximum]:  
                    base_station = p.BaseStations[bs]
                    for channel in base_station.channels:
                        SINR, p = sinr(user, base_station, channel, p)
                        # a user connects to the BS with highest SINR/degree
                        if SINR / max(1, len(channel.users)) > best_measure and SINR >= settings.MINIMUM_SNR:
                            best_bs = bs
                            channel_id = int(channel.id)
                            best_SINR = SINR
                            SNR, p = snr(user, base_station, channel, p)
                            best_measure = SINR / max(len(channel.users), 1)
                if best_SINR >= settings.MINIMUM_SNR - settings.PRECISION_MARGIN:
                    sinrs[user.id, best_bs] = best_SINR
                    channel_link[user.id, best_bs] = channel_id
                    for c in p.BaseStations[best_bs].channels:
                        if int(c.id) == channel_id:
                            c.add_user(user.id)
                    links[user.id, best_bs] = 1
                    snrs[user.id, best_bs] = SNR
                    connections[p.BaseStations[best_bs].provider][user.provider] += 1
                else:
                    FDP[user.id] = 1
                    # connections['no'][user.provider] += 1 # it already accounted for it

        # print(connections)
        # # print([p.BaseStations[id].provider for id in range(len(p.BaseStations))])
        # print('Total number of disconnected users:', len(disconnected_users), 'out of', len(p.users))
        # print('Disconnected per MNO:', disconnected)

        # print(connections_disconnected)
        bar.finish()

        print('Now, we find the capacities')


        capacities, FSP = find_capacity(p, sinrs)

        FSP_diff = FSP - FSP_fp
        FDP_diff = FDP - FDP_fp


        if p.seed == 1:
            util.to_data(links_fp, f'data/Realisations/{p.filename}{p.seed}_links_fp.p')
            util.to_data(snrs_fp, f'data/Realisations/{p.filename}{p.seed}_snrs_fp.p')
        util.to_data(sinrs_fp, f'data/Realisations/{p.filename}{p.seed}_sinrs_fp.p')
        util.to_data(capacities_fp, f'data/Realisations/{p.filename}{p.seed}_capacities_fp.p')
        util.to_data(FDP_fp, f'data/Realisations/{p.filename}{p.seed}_FDP_fp.p')
        util.to_data(FSP_fp, f'data/Realisations/{p.filename}{p.seed}_FSP_fp.p')
        util.to_data(connections_fp, f'data/Realisations/{p.filename}{p.seed}_connections_fp.p')
        util.to_data(power_per_MNO_fp, f'data/Realisations/{p.filename}{p.seed}_power_per_MNO_fp.p')

        if p.seed == 1:
            util.to_data(links, f'data/Realisations/{p.filename}{p.seed}_links.p')
            util.to_data(snrs, f'data/Realisations/{p.filename}{p.seed}_snrs.p')
        util.to_data(sinrs, f'data/Realisations/{p.filename}{p.seed}_sinrs.p')
        util.to_data(capacities, f'data/Realisations/{p.filename}{p.seed}_capacities.p')
        util.to_data(FDP, f'data/Realisations/{p.filename}{p.seed}_FDP.p')
        util.to_data(FSP, f'data/Realisations/{p.filename}{p.seed}_FSP.p')
        util.to_data(connections, f'data/Realisations/{p.filename}{p.seed}_connections.p')
        util.to_data(power_per_MNO, f'data/Realisations/{p.filename}{p.seed}_power_per_MNO.p')

    #return links, channel_link, snrs, sinrs, capacities, FDP, FSP, connections
    #return links_fp, channel_link_fp, snrs_fp, sinrs_fp, capacities_fp, FDP_fp, FSP_fp, connections_fp, total_p_fp
    return [links, links_fp], [channel_link, channel_link_fp], [snrs, snrs_fp], [sinrs, sinrs_fp], [capacities, capacities_fp], [FDP, FDP_fp], [FSP, FSP_fp], [connections, connections_fp], [power_per_MNO, power_per_MNO_fp]#[total_p, total_p_fp]


def find_links(p):
    links = util.from_data(f'data/Realisations/{p.filename}{p.seed}_links.p')
    snrs = util.from_data(f'data/Realisations/{p.filename}{p.seed}_snrs.p')
    sinrs = util.from_data(f'data/Realisations/{p.filename}{p.seed}_sinrs.p')
    capacities = util.from_data(f'data/Realisations/{p.filename}{p.seed}_capacities.p')
    FDP = util.from_data(f'data/Realisations/{p.filename}{p.seed}_FDP.p')
    FSP = util.from_data(f'data/Realisations/{p.filename}{p.seed}_FSP.p')
    channel_link = util.from_data(f'data/Realisations/{p.filename}{p.seed}_channel_link.p')

    connections = None
    # FDP = None
    if FDP is None:
        links = lil_matrix((p.number_of_users, p.number_of_bs))
        snrs = lil_matrix((p.number_of_users, p.number_of_bs))
        sinrs = lil_matrix((p.number_of_users, p.number_of_bs))
        channel_link = lil_matrix((p.number_of_users, p.number_of_bs))
        FDP = np.zeros(p.number_of_users)

        maximum = 20

        bar = progressbar.ProgressBar(maxval=p.number_of_users, widgets=[
            progressbar.Bar('=', f'Finding links {p.filename} [', ']'), ' ',
            progressbar.Percentage(), ' ', progressbar.ETA()])
        bar.start()

        connections = {'KPN': {'KPN': 0, 'T-Mobile': 0, 'Vodafone': 0},
                       'T-Mobile': {'KPN': 0, 'T-Mobile': 0, 'Vodafone': 0},
                       'Vodafone': {'KPN': 0, 'T-Mobile': 0, 'Vodafone': 0}, 'no': {'KPN': 0, 'T-Mobile': 0, 'Vodafone': 0}}

        disconnected_users = []
        for user in p.users:

            bar.update(int(user.id))
            user_coords = (user.x, user.y)
            BSs = util.find_closest_BS(user_coords, p.xbs, p.ybs)
            best_SINR = - math.inf
            best_measure = -math.inf

            for bs in BSs[:maximum]:  # assuming that the highest SINR BS will be within the closest 20 BSs
                if bs != p.failed_BS:
                    base_station = p.BaseStations[bs]
                    if not p.back_up or (user.provider == base_station.provider and p.back_up):
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
                sinrs[user.id, best_bs] = best_SINR
                channel_link[user.id, best_bs] = channel_id
                for c in p.BaseStations[best_bs].channels:
                    if int(c.id) == channel_id:
                        c.add_user(user.id)
                links[user.id, best_bs] = 1
                snrs[user.id, best_bs] = SNR
                connections[p.BaseStations[best_bs].provider][user.provider] += 1
            elif p.back_up:
                disconnected_users.append(user)
            else:
                FDP[user.id] = 1
                connections['no'][user.provider] += 1

        # print(connections)
        # # print([p.BaseStations[id].provider for id in range(len(p.BaseStations))])
        # print('Total number of disconnected users:', len(disconnected_users), 'out of', len(p.users))
        # print('Disconnected per MNO:', disconnected)


        for user in disconnected_users:
            best_SINR = - math.inf
            best_measure = -math.inf
            user_coords = (user.x, user.y)
            BSs = util.find_closest_BS(user_coords, p.xbs, p.ybs)
            for bs in BSs[:maximum]:  # assuming that the highest SNR BS will be within the closest 10 BSs
                base_station = p.BaseStations[bs]
                if base_station.provider != user.provider:
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
                sinrs[user.id, best_bs] = best_SINR
                channel_link[user.id, best_bs] = channel_id
                for c in p.BaseStations[best_bs].channels:
                    if int(c.id) == channel_id:
                        c.add_user(user.id)
                links[user.id, best_bs] = 1
                snrs[user.id, best_bs] = SNR
                connections[p.BaseStations[best_bs].provider][user.provider] += 1
            else:
                FDP[user.id] = 1
                connections['no'][user.provider] += 1

        # print(connections_disconnected)
        bar.finish()

        print('Now, we find the capacities')


        capacities, FSP = find_capacity(p, sinrs)

        if p.seed == 1:
            util.to_data(links, f'data/Realisations/{p.filename}{p.seed}_links.p')
            util.to_data(snrs, f'data/Realisations/{p.filename}{p.seed}_snrs.p')
        util.to_data(sinrs, f'data/Realisations/{p.filename}{p.seed}_sinrs.p')
        util.to_data(capacities, f'data/Realisations/{p.filename}{p.seed}_capacities.p')
        util.to_data(FDP, f'data/Realisations/{p.filename}{p.seed}_FDP.p')
        util.to_data(FSP, f'data/Realisations/{p.filename}{p.seed}_FSP.p')

    return links, channel_link, snrs, sinrs, capacities, FDP, FSP, connections

def find_capacity(p, sinrs):
    capacities = np.zeros(p.number_of_users)
    FSP = np.zeros(p.number_of_users)
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
                    capacities[user] = capacity
                    # PRECISION_MARGIN is added to avoid errors due to the precision
                    if capacities[user] >= p.users[user].rate_requirement - settings.PRECISION_MARGIN:
                    #if capacities[user] >= p.users[user].rate_requirement:
                        FSP[user] = 1
    return capacities, FSP

def find_links_QoS(p):
    links = util.from_data(f'data/Realisations/{p.filename}{p.seed}_linksQOS.p')
    snrs = util.from_data(f'data/Realisations/{p.filename}{p.seed}_snrsQOS.p')
    sinrs = util.from_data(f'data/Realisations/{p.filename}{p.seed}_sinrsQOS.p')
    capacities = util.from_data(f'data/Realisations/{p.filename}{p.seed}_capacitiesQOS.p')
    FDP = util.from_data(f'data/Realisations/{p.filename}{p.seed}_FDPQOS.p')
    FSP = util.from_data(f'data/Realisations/{p.filename}{p.seed}_FSPQOS.p')
    channel_link = util.from_data(f'data/Realisations/{p.filename}{p.seed}_channel_linkQOS.p')

    FDP = None
    if FDP is None:
        links = lil_matrix((p.number_of_users, p.number_of_bs))
        snrs = lil_matrix((p.number_of_users, p.number_of_bs))
        sinrs = lil_matrix((p.number_of_users, p.number_of_bs))
        channel_link = lil_matrix((p.number_of_users, p.number_of_bs))
        capacities = np.zeros(p.number_of_users)
        FDP = np.zeros(p.number_of_users)
        FSP = np.zeros(p.number_of_users)

        maximum = 20

        bar = progressbar.ProgressBar(maxval=p.number_of_users, widgets=[
            progressbar.Bar('=', f'Finding links {p.filename} [', ']'), ' ',
            progressbar.Percentage(), ' ', progressbar.ETA()])
        bar.start()

        connections = {'KPN': {'KPN': 0, 'T-Mobile': 0, 'Vodafone': 0},
                       'T-Mobile': {'KPN': 0, 'T-Mobile': 0, 'Vodafone': 0},
                       'Vodafone': {'KPN': 0, 'T-Mobile': 0, 'Vodafone': 0},
                       'no': {'KPN': 0, 'T-Mobile': 0, 'Vodafone': 0}}

        disconnected_users = []
        for user in p.users:

            bar.update(int(user.id))
            user_coords = (user.x, user.y)
            BSs = util.find_closest_BS(user_coords, p.xbs, p.ybs)
            best_SINR = - math.inf
            best_measure = -math.inf

            for bs in BSs[:maximum]:  # assuming that the highest SNR BS will be within the closest 10 BSs
                if bs != p.failed_BS:
                    base_station = p.BaseStations[bs]
                    if not p.back_up or (user.provider == base_station.provider and p.back_up):
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
                sinrs[user.id, best_bs] = best_SINR
                channel_link[user.id, best_bs] = channel_id
                for c in p.BaseStations[best_bs].channels:
                    if int(c.id) == channel_id:
                        c.add_user(user.id)
                links[user.id, best_bs] = 1
                snrs[user.id, best_bs] = SNR
                connections[p.BaseStations[best_bs].provider][user.provider] += 1
            else:
                disconnected_users.append(user)
                # connections['no'][user.provider] += 1

        #
        # print(connections)
        # # print([p.BaseStations[id].provider for id in range(len(p.BaseStations))])
        # print('Total number of disconnected users:', len(disconnected_users), 'out of', len(p.users))
        # print('Disconnected per MNO:', disconnected)


        print('Now, we find the capacities in the first round')
        capacites, FSP = find_capacity(p, sinrs)



        connections_disconnected = {'KPN': {'KPN': 0, 'T-Mobile': 0, 'Vodafone': 0},
                                    'T-Mobile': {'KPN': 0, 'T-Mobile': 0, 'Vodafone': 0},
                                    'Vodafone': {'KPN': 0, 'T-Mobile': 0, 'Vodafone': 0}}

        for user in disconnected_users:
            best_SINR = - math.inf
            best_measure = -math.inf
            user_coords = (user.x, user.y)
            BSs = util.find_closest_BS(user_coords, p.xbs, p.ybs)
            for bs in BSs[:maximum]:  # assuming that the highest SNR BS will be within the closest 10 BSs
                base_station = p.BaseStations[bs]
                if base_station.provider != user.provider:
                    for channel in base_station.channels:
                        if sum([FSP[u] for u in channel.users]) == len(channel.users): #ensure that the users that are connected are satisfied. TODO still could happen that after adding a user they are not satisfied any more...
                            SINR, p = sinr(user, base_station, channel, p)
                            # a user connects to the BS with highest SINR/degree
                            if SINR / max(1, len(channel.users)) > best_measure and SINR >= settings.MINIMUM_SNR:
                                best_bs = bs
                                channel_id = int(channel.id)
                                best_SINR = SINR
                                SNR, p = snr(user, base_station, channel, p)
                                best_measure = SINR / max(len(channel.users), 1)
            if best_SINR >= settings.MINIMUM_SNR:
                sinrs[user.id, best_bs] = best_SINR
                channel_link[user.id, best_bs] = channel_id
                for c in p.BaseStations[best_bs].channels:
                    if int(c.id) == channel_id:
                        c.add_user(user.id)
                links[user.id, best_bs] = 1
                snrs[user.id, best_bs] = SNR
                connections[p.BaseStations[best_bs].provider][user.provider] += 1
            else:
                FDP[user.id] = 1
                connections['no'][user.provider] += 1

        # print(connections_disconnected)
        bar.finish()

        print('Now, we find the capacities for the second round')
        FSP, capacties = find_capacity(p, sinrs)

        if p.seed == 1:
            util.to_data(links, f'data/Realisations/{p.filename}{p.seed}_linksQOS.p')
            util.to_data(snrs, f'data/Realisations/{p.filename}{p.seed}_snrsQOS.p')
        util.to_data(sinrs, f'data/Realisations/{p.filename}{p.seed}_sinrsQOS.p')
        util.to_data(capacities, f'data/Realisations/{p.filename}{p.seed}_capacitiesQOS.p')
        util.to_data(FDP, f'data/Realisations/{p.filename}{p.seed}_FDPQOS.p')
        util.to_data(FSP, f'data/Realisations/{p.filename}{p.seed}_FSPQOS.p')

    return links, channel_link, snrs, sinrs, capacities, FDP, FSP, connections