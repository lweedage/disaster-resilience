import numpy as np
import math

pi = math.pi
propagation_velocity = 3e8
avg_street_width = 20 #from 3GPP
avg_building_height = 5 #from 3GPP

# Scenario's:
RMa = 1
UMa = 2
UMi = 3

def find_gain(bore_1, bore_2, geo_1, geo_2, beamwidth_ml):
    bore = find_bore(bore_1, bore_2, beamwidth_ml)
    geo = find_geo(geo_1, geo_2)
    alpha = math.degrees(abs(bore-geo))
    if alpha > 180:
        alpha = alpha - 360
    beamwidth_ml = math.degrees(beamwidth_ml)
    w = beamwidth_ml / 2.58
    G0 = 20 * math.log10(1.62 / math.sin(math.radians(w / 2)))

    if 0 <= abs(alpha) <= beamwidth_ml / 2:
        return 10 ** ((G0 - 3.01 * (2 * alpha / w) ** 2)/10)
    else:
        return 10**((-0.4111 * math.log(math.degrees(w)) - 10.579)/10)

def find_bore(coord_1, coord_2, beamwidth):
    radians = find_geo(coord_1, coord_2)
    angle = find_beam(radians, beamwidth)
    return angle

def find_geo(coord_1, coord_2):
    dy = coord_2[1] - coord_1[1]
    dx = coord_2[0] - coord_1[0]
    radians = math.atan2(dy, dx)
    return radians

def find_beam(radians, beamwidth):
    angles = [beamwidth * i for i in range(int(-pi/beamwidth), int(pi/beamwidth))]
    minimum = math.inf
    for angle in angles:
        if abs(radians - angle) <= minimum:
            minimum = abs(radians - angle)      # NOTE THAT WE NOW JUST CHOOSE THE FIRST ONE IF TWO ARE EVEN CLOSE
            preferred_angle = angle
    return preferred_angle

def find_3D_distance(distance_2D, height_BS, height_user):
    return math.sqrt(distance_2D**2 - (height_BS - height_user)**2)


# all the following functions come from the 3GPP TR.38.9xx standard.

def pathloss_RMa_LOS(distance_2D, distance_3D, height_BS, height_user, centre_frequency): # works between 10 m and 10 km
    breakpoint_distance = 2 * pi * height_BS * height_user * centre_frequency / propagation_velocity
    PL1 = 20 * math.log10(40 * pi * min(breakpoint_distance, distance_3D) * centre_frequency / 3) + min(0.03 * avg_building_height ** 1.72, 10) * math.log10(
        min(breakpoint_distance, distance_3D)) - min(0.044 * avg_building_height ** 1.72, 14.77) + 0.002 * math.log10(avg_building_height) * min(breakpoint_distance, distance_3D)

    if 10 <= distance_2D <= breakpoint_distance:
        PL = PL1
        sigma_SF = 4
    elif breakpoint_distance < distance_2D <= 10e3:
        PL = PL1 + 40 * math.log10(distance_3D / breakpoint_distance)
        sigma_SF = 6

    return PL, sigma_SF

def pathloss_RMa_NLOS(distance_2D, distance_3D, height_BS, height_user, centre_frequency): # works between 10 m and 5 km
    PL_NLOS = 161.04 - 7.1*math.log10(avg_street_width) + 7.5*math.log10(avg_building_height) - (24.37 - 3.7*(avg_building_height/height_BS)**2)*math.log10(height_BS) + (43.42 - 3.1*math.log10(height_BS))*(math.log10(distance_3D) - 3) + 20*math.log10(centre_frequency) - (3.2* (math.log10(11.75*height_user))**2 - 4.97)
    PL_LOS, sigma = pathloss_RMa_LOS()
    sigma_SF = 8
    return max(PL_LOS, PL_NLOS), sigma_SF

def pathloss_UMa_LOS(distance_2D, distance_3D, height_BS, height_user, centre_frequency):
    breakpoint_distance = find_d_BP_prime(distance_2D, height_BS, height_user, centre_frequency)
    if 10 <= distance_2D <= breakpoint_distance:
        PL = 28 + 22 * math.log10(distance_3D) + 20 * math.log10(centre_frequency)
    elif breakpoint_distance < distance_2D <= 5e3:
        PL = 28 + 40*math.log10(distance_3D) + 20*math.log10(centre_frequency) - 9*math.log10(
            breakpoint_distance ** 2 + (height_BS - height_user) ** 2)
    sigma_SF = 4
    return PL, sigma_SF

def find_d_BP_prime(distance_2D, height_BS, height_user, centre_frequency): # works only between height_user between 13 m and 23 m
    # find g(distance_2D)
    if distance_2D <= 18:
        g = 0
    else:
        g = 5/4 * (distance_2D/100)**3 * math.exp(-distance_2D/150)

    # find C(distance_2D, height_user)
    if height_user < 13:
        C = 0
    elif 13 <= height_user <= 23:
        C = ((height_user - 13)/10) ** 1.5 * g

    p = 1/(1 + C)
    if np.random.uniform(0, 1) > p:
        effective_height = 12 + 3 * np.random.random_integers(0, math.floor((height_user - 1.5 - 12)/3))
    else:
        effective_height = 1

    breakpoint_distance = 4 * (height_BS - effective_height) * (height_user - effective_height) * centre_frequency / propagation_velocity

    return breakpoint_distance

def pathloss_UMa_NLOS(distance_2D, distance_3D, height_BS, height_user, centre_frequency):
    PL_LOS, sigma = pathloss_UMa_LOS(distance_2D, distance_3D, height_BS, height_user, centre_frequency)
    PL_NLOS = 13.54 + 39.08*math.log10(distance_3D) + 20 * math.log10(centre_frequency) - 0.6*(height_user - 1.5)

    sigma_SF = 6
    return max(PL_LOS, PL_NLOS), sigma_SF

def pathloss_UMi_LOS(distance_2D, distance_3D, height_BS, height_user, centre_frequency):
    breakpoint_distance = find_d_BP_prime(distance_2D, height_BS, height_user, centre_frequency)
    if 10 <= distance_2D <= breakpoint_distance:
        PL = 32.4 + 21 *math.log10(distance_3D) + 20 *math.log10(centre_frequency)
    elif breakpoint_distance < distance_2D <= 5e3:
        PL = 32.4 + 4*math.log10(distance_3D) + 20*math.log10(centre_frequency) - 9.5*math.log10(
            breakpoint_distance ** 2 - (height_BS - height_user) ** 2)

    sigma_SF = 4
    return PL, sigma_SF

def pathloss_UMi_NLOS(distance_2D, distance_3D, height_BS, height_user, centre_frequency):
    PL_LOS, sigma = pathloss_UMi_LOS(distance_2D, distance_3D, height_BS, height_user, centre_frequency)
    PL_NLOS = 35.3 * math.log10(distance_3D) + 22.4 + 21.3*math.log(centre_frequency) - 0.3*(height_user - 1.5)

    sigma_SF = 7.82
    return max(PL_LOS, PL_NLOS), sigma_SF

def LOS_probability_RMa(distance_2D):
    if distance_2D <= 10:
        p_LOS = 1
    else:
        p_LOS = math.exp(-(distance_2D - 10)/1000)
    return p_LOS

def LOS_probability_UMi(distance_2D):
    if distance_2D <= 18:
        p_LOS = 1
    else:
        p_LOS = 18/distance_2D + math.exp(-distance_2D/36) * (1 - 18/distance_2D)
    return p_LOS

def LOS_probability_UMa(distance_2D, height_user):
    if distance_2D <= 18:
        p_LOS = 1
    else:
        if height_user <= 13:
            C = 0
        elif 13 <= height_user <= 23:
            C = ((height_user - 13)/10)**1.5
        p_LOS = (18/distance_2D + math.exp(-distance_2D/63) * (1 - 18/distance_2D)) * (1 + C * 5/4*(distance_2D/100)**3 * math.exp(- distance_2D/150))
    return p_LOS

def find_path_loss(distance_2D, distance_3D, height_BS, height_user, centre_frequency, scenario):
    rain_attenuation = 0 # we can add this later
    p = np.random.uniform(0, 1)
    if scenario == RMa:
        if p <= LOS_probability_RMa(distance_2D):
            PL, sigma_SF = pathloss_RMa_LOS(distance_2D, distance_3D, height_BS, height_user, centre_frequency)
        else:
            PL, sigma_SF = pathloss_RMa_NLOS(distance_2D, distance_3D, height_BS, height_user, centre_frequency)
    elif scenario == UMa:
        if p <= LOS_probability_UMa(distance_2D, height_user):
            PL, sigma_SF = pathloss_UMa_LOS(distance_2D, distance_3D, height_BS, height_user, centre_frequency)
        else:
            PL, sigma_SF = pathloss_UMa_NLOS(distance_2D, distance_3D, height_BS, height_user, centre_frequency)
    elif scenario == UMi:
        if p <= LOS_probability_UMi(distance_2D):
            PL, sigma_SF = pathloss_UMi_LOS(distance_2D, distance_3D, height_BS, height_user, centre_frequency)
        else:
            PL, sigma_SF = pathloss_UMi_NLOS(distance_2D, distance_3D, height_BS, height_user, centre_frequency)
    return PL + np.random.normal(0, sigma_SF) + rain_attenuation

def find_SNR(coord_1, coord_2):
    distance_2D = find_distance(coord_1[0], coord_1[1], coord_2[0], coord_2[1])
    distance_3D = find_3D_distance(distance_2D, height_BS=, height_user=)
    transmitting_power = find_transmitting_power()
    gain = find_gain()
    path_loss = find_path_loss(distance_2D, distance_3D, height_BS, height_user, centre_frequency, scenario)
    return transmitting_power + gain - path_loss - noise

def find_squared_distance(x_user, y_user, x_bs, y_bs):
    return (x_bs - x_user)**2 + (y_bs - y_user)**2

def find_distance(x_user, y_user, x_bs, y_bs):
    return np.sqrt(find_squared_distance(x_user, y_user, x_bs, y_bs))