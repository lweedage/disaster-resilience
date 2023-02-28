import warnings

import geopandas as gpd
from shapely.errors import ShapelyDeprecationWarning
import numpy as np
import find_base_stations as antenna
import generate_users
import models
import objects.Params as p
import util

warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)

provinces = ['Drenthe', 'Flevoland', 'Friesland', 'Groningen', 'Limburg', 'Overijssel', 'Utrecht', 'Zeeland',
             'Zuid-Holland', 'Gelderland', 'Noord-Brabant', 'Noord-Holland']
municipalities = ['Middelburg', 'Maastricht', 'Groningen', 'Enschede', 'Emmen', 'Elburg',
                  'Eindhoven', "'s-Gravenhage", 'Amsterdam', 'Almere']

provinces = ['Overijssel', 'Friesland', 'Utrecht']
municipalities = ['Middelburg', 'Enschede', 'Amsterdam']

# provinces = ['Friesland']
# municipalities = ['Emmen']

# MNOS = [['KPN'], ['T-Mobile'], ['Vodafone'], ['KPN', 'Vodafone', 'T-Mobile']]
# MNOS = [['KPN'], ['T-Mobile'], ['Vodafone']]
# MNOS = [['KPN', 'Vodafone', 'T-Mobile']]
MNOS = [['Vodafone', 'T-Mobile']]

fdp_per_MNO = {MNO: list() for MNO in ['KPN', 'T-Mobile', 'Vodafone']}
fsp_per_MNO = {MNO: list() for MNO in ['KPN', 'T-Mobile', 'Vodafone']}

radius_disaster = 0  # 0, or a value if there is a disaster in the center of the region with radius
random_failure = 0  # BSs randomly fail with this probability
user_increase = 0  # an increase in number of users
back_up = True
# back_up = False

# sharing = ['T-Mobile', 'Vodafone']
sharing = MNOS[0]

radii = [500, 1000, 2500]
increases = [50, 100, 200]
random = [0.05, 0.1, 0.25, 0.5]

max_iterations = 1

# fig, ax = plt.subplots()

zip_codes = gpd.read_file('data/square_statistics.shp')
for random in [0, 0.1]:
    print('Failure:', random)
    # for province in provinces:
    for municipality in municipalities:
        #     fig, ax = plt.subplots()
        j = 0
        extraticks = [0, 0.4, 0.6, 0.8, 1.0]
        for mno in MNOS:
            data = []
            fdp, fsp, sat = [], [], []
            for iteration in range(max_iterations):
                # Retrieve zip code population + area data and make a region with specified zip codes
                # Columns are: aantal_inw (population), stedelijkh (urbanity), postcode (zip code), geometry,
                # popdensity (population density), municipali(city), scenario

                # Region that we want to investigate:
                # cities = util.find_cities(province)
                cities = [municipality]
                province = None

                percentage = 2/100  # percentage of active users
                seed = iteration

                params = p.Parameters(seed, zip_codes, mno, percentage, buffer_size=2000, city_list=cities,
                                      province=province, radius_disaster=radius_disaster, random_failure=random_failure,
                                      user_increase=user_increase, capacity_distribution=False, back_up=back_up,
                                      sharing=sharing)
                params = antenna.find_zip_code_region(params)

        #         # FINDING USERS
                params = generate_users.generate_users(params)
        #         # FINDING BSS
                params = antenna.load_bs(params)
        #         # FINDING LINKS
                links, link_channel, snr, sinr, capacity, FDP, FSP, interference_loss = models.find_links(params)
        #         links, link_channel, snr, sinr, capacity, FDP, FSP, interference_loss = models.find_links_QoS(params)

                fraction_satisified_pop = sum(FSP) / params.number_of_users
                fraction_disconnected_pop = sum(FDP) / params.number_of_users
                # print(f'There are {params.number_of_bs} BSs and {params.number_of_users} users.')
                #
                # print(f'FDP = {fraction_disconnected_pop}')
                # print(f'FSP = {fraction_satisified_pop}')
                fdp.append(fraction_disconnected_pop)
                fsp.append(fraction_satisified_pop)

                # graph_functions.draw_graph(params, links, ax)
                for user in params.users:
                    MNO = user.provider
                    id = user.id
                    fdp_per_MNO[MNO].append(FDP[id])
                    fsp_per_MNO[MNO].append(FSP[id])

            # util.to_data(fdp, f'data/Realisations/{params.filename}{max_iterations}_totalfdp.p')
            # util.to_data(fsp, f'data/Realisations/{params.filename}{max_iterations}_totalfsp.p')

        if type(MNOS[0]) == list and len(MNOS[0]) == 1:
            lijst = [MNOS[i][0] for i in range(len(MNOS))]
        elif len(MNOS[0]) > 1:
            lijst = MNOS[0]
        else:
            lijst = MNOS

        if province:
            print(province, ':', [sum(fdp_per_MNO[MNO]) / len(fdp_per_MNO[MNO]) for MNO in lijst])
            print(province, ':', [sum(fsp_per_MNO[MNO]) / len(fsp_per_MNO[MNO]) for MNO in lijst])
        else:
            print(municipality, ':', [sum(fdp_per_MNO[MNO]) / len(fdp_per_MNO[MNO]) for MNO in lijst])
            print(municipality, ':', [sum(fsp_per_MNO[MNO]) / len(fsp_per_MNO[MNO]) for MNO in lijst])

        # util.to_data(fdp_per_MNO, f'data/Realisations/{params.filename}{max_iterations}_fdp_per_MNO.p')
        # util.to_data(fsp_per_MNO, f'data/Realisations/{params.filename}{max_iterations}_fsp_per_MNO.p')

# plt.savefig(f'{params.filename}.pdf', dpi=1000)
# plt.show()
