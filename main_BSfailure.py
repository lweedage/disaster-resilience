import warnings
from copy import deepcopy
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from shapely.errors import ShapelyDeprecationWarning
import find_base_stations as antenna
import generate_users
import models
import objects.Params as parameters
import util

warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)

provinces = ['Drenthe', 'Flevoland', 'Friesland', 'Groningen', 'Limburg', 'Overijssel', 'Utrecht', 'Zeeland',
             'Zuid-Holland', 'Gelderland', 'Noord-Brabant', 'Noord-Holland']
municipalities = ['Almere', 'Amsterdam', 'Enschede', "'s-Gravenhage", 'Elburg', 'Emmen', 'Groningen', 'Maastricht',
                  'Eindhoven', 'Middelburg']

radius_disaster = 0  # 0, or a value if there is a disaster in the center of the region with radius
random_failure = 0  # BSs randomly fail with this probability
user_increase = 0  # an increase in number of users
geographic_failure = True # True - all antennas on the same cell tower will fail - a single MNO/antenna fails.

zip_codes = gpd.read_file('data/square_statistics.shp')

for municipality in municipalities:
    # for province in municipalities:
    fig, ax = plt.subplots()
    j = 0
    for mno in [['KPN'], ['T-Mobile'], ['Vodafone'], ['KPN', 'Vodafone', 'T-Mobile']]:
        data = []
        for iteration in range(1):
            # Retrieve zip code population + area data and make a region with specified zip codes
            # Columns are: aantal_inw (population), stedelijkh (urbanity), postcode (zip code), geometry,
            # popdensity (population density), municipali(city), BSs, scenario

            # Region that we want to investigate:
            # cities = util.find_cities(province)
            cities = [municipality]
            province = None

            percentage = 2  # Three user density levels - still tbd
            seed = 1  # iteration

            params = parameters.Parameters(seed, zip_codes, mno, percentage, buffer_size=2000, city_list=cities,
                                           province=province, radius_disaster=radius_disaster,
                                           random_failure=random_failure,
                                           user_increase=user_increase, capacity_distribution=False,
                                           geographic_failure=geographic_failure)
            params = antenna.find_zip_code_region(params)

            # FINDING USERS
            params = generate_users.generate_users(params)
            # FINDING BSS
            params = antenna.load_bs(params)
            # FINDING LINKS
            links, link_channel, snr, sinr, capacity, FDP, FSP, satisfaction_level = models.find_links(params)

            fraction_satisified_pop = sum(FSP) / params.number_of_users
            fraction_disconnected_pop = sum(FDP) / params.number_of_users
            satisfaction = sum(satisfaction_level) / len(satisfaction_level)
            print(f'There are {params.number_of_bs} BSs and {params.number_of_users} users.')

            print(f'FDP = {fraction_disconnected_pop}')
            print(f'FSP = {fraction_satisified_pop}')
            print(f'Satisfaction level = {sum(satisfaction_level) / len(satisfaction_level)}')
            capacity = np.divide(capacity, 1e6)

            failure_fsp = []
            failure_fdp = []

            # we iterate over all BSs and let them fail one by one.
            for failed_bs in range(params.number_of_bs):
                p = deepcopy(params)
                p.failure_update(failed_bs)

                links, link_channel, snr, sinr, capacity, FDP, FSP, satisfaction_level = models.find_links(p)

                failure_fraction_satisified_pop = sum(FSP) / p.number_of_users
                failure_fraction_disconnected_pop = sum(FDP) / p.number_of_users

                failure_fsp.append(fraction_satisified_pop - failure_fraction_satisified_pop)
                failure_fdp.append(fraction_disconnected_pop - failure_fraction_disconnected_pop)

            util.to_data(failure_fdp, f'data/BSfailures/failed_fdp_{params.filename}.p')
            util.to_data(failure_fsp, f'data/BSfailures/failed_fsp_{params.filename}.p')
