import warnings
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.errors import ShapelyDeprecationWarning
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

provinces = ['Drenthe']
MNOS = [['KPN'], ['T-Mobile'], ['Vodafone'], ['KPN', 'Vodafone', 'T-Mobile']]
MNOS = [['KPN']]

radius_disaster = 0  # 0, or a value if there is a disaster in the center of the region with radius
random_failure = 0  # BSs randomly fail with this probability
user_increase = 0  # an increase in number of users

radii = [500, 1000, 2500]
increases = [50, 100, 200]
random = [0.05, 0.1, 0.25, 0.5]

max_iterations = 100

zip_codes = gpd.read_file('data/square_statistics.shp')
for user_increase in [0]:
    for province in provinces:
        # for municipality in municipalities:
        fig, ax = plt.subplots()
        j = 0
        extraticks = [0, 0.4, 0.6, 0.8, 1.0]
        for mno in MNOS:
            data = []
            fdp, fsp, sat = [], [], []
            for iteration in range(max_iterations):
                print(iteration)
                # Retrieve zip code population + area data and make a region with specified zip codes
                # Columns are: aantal_inw (population), stedelijkh (urbanity), postcode (zip code), geometry,
                # popdensity (population density), municipali(city), scenario

                # Region that we want to investigate:
                cities = util.find_cities(province)
                # cities = [municipality]
                # province = None

                percentage = 2  # Three user density levels - still tbd
                seed = iteration  # iteration

                params = p.Parameters(seed, zip_codes, mno, percentage, buffer_size=2000, city_list=cities,
                                      province=province, radius_disaster=radius_disaster, random_failure=random_failure,
                                      user_increase=user_increase, capacity_distribution=False)
                params = antenna.find_zip_code_region(params)

                # FINDING USERS
                params = generate_users.generate_users(params)
                # FINDING BSS
                params = antenna.load_bs(params)
                # FINDING LINKS
                links, link_channel, snr, sinr, capacity, FDP, FSP, interference_loss = models.find_links(params)

                # print(interference_loss)
                # print('average loss: ', sum(interference_loss)/len(interference_loss))

                for i in capacity:
                    data.append(i)

                fraction_satisified_pop = sum(FSP) / params.number_of_users
                fraction_disconnected_pop = sum(FDP) / params.number_of_users
                print(f'There are {params.number_of_bs} BSs and {params.number_of_users} users.')

                print(f'FDP = {fraction_disconnected_pop}')
                print(f'FSP = {fraction_satisified_pop}')

                fdp.append(fraction_disconnected_pop)
                fsp.append(fraction_satisified_pop)
            #
            util.to_data(fdp, f'data/Realisations/{params.filename}{max_iterations}_totalfdp.p')
            util.to_data(fsp, f'data/Realisations/{params.filename}{max_iterations}_totalfsp.p')
