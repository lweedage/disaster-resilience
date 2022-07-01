import math
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import analyse_UA
import settings
import util
import find_base_stations as antenna
from settings import *
import generate_users
import pickle
import models
import numpy as np
import graph_functions as g
import objects.Params as p
from shapely.errors import ShapelyDeprecationWarning
import warnings
import model_3GPP
import openpyxl

warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)

provinces = ['Drenthe', 'Flevoland', 'Friesland', 'Groningen', 'Limburg', 'Overijssel', 'Utrecht', 'Zeeland',
             'Zuid-Holland', 'Gelderland', 'Noord-Brabant', 'Noord-Holland']
# provinces = ['Drenthe', 'Flevoland', 'Friesland', 'Groningen', 'Limburg', 'Overijssel', 'Utrecht', 'Zeeland', 'Gelderland', 'Noord-Brabant']
# cities, province = [3412], None #if both none, then entire Netherlands - is too big to save however.
provinces = ['Overijssel']

rain = 0 # 2.5, 25 or 150 or None
radius_disaster = 0 # 0, or a value #there is a disaster in the center of the region with radius
random_failure = 0 # BSs randomly fail with this probability
user_increase = 0

for mno in [['KPN']]:  # [['Vodafone'], ['KPN'], ['T-Mobile'], ['Vodafone', 'KPN', 'T-Mobile']]:
    for province in provinces:
        print(province, mno[0])
        # Retrieve zip code population + area data and make a region with specified zip codes
        # Columns are: aantal_inw (population), stedelijkh (urbanity), postcode (zip code), geometry,
        # popdensity (population density), municipali(city), GSM_BS, UMTS_BS, LTE_BS, NR_BS, BSs, scenario
        zip_codes = gpd.read_file('data/zip_codes_with_scenarios.shp')

        # Region that we want to investigate:
        cities = util.find_cities(province)
        cities = ['Zwolle']
        province = None
        percentage = 3  # Three user density levels - still tbd
        seed = 1

        params = p.Parameters(seed, zip_codes, mno, percentage, city_list=cities, province=province, rain=rain,
                              radius_disaster=radius_disaster, random_failure=random_failure, user_increase = user_increase)
        params = antenna.find_zip_code_region(params)

        # FINDING USERS
        params = generate_users.generate_users(params)
        # FINDING BSS
        params = antenna.load_bs(params)
        # FINDING LINKS
        links, link_channel, snr, sinr, capacity, FDP, FSP, satisfaction_level = models.find_links(params)
        #
        fraction_satisified_pop = sum(FSP) / params.number_of_users
        fraction_disconnected_pop = sum(FDP) / params.number_of_users
        satisfaction = sum(satisfaction_level) / len(satisfaction_level)
        print(f'There are {params.number_of_bs} BSs and {params.number_of_users} users.')
        print(f'FDP = {fraction_disconnected_pop}')
        print(f'FSP = {fraction_satisified_pop}')
        print(f'Satisfaction level = {sum(satisfaction_level) / len(satisfaction_level)}')
        capacity = np.divide(capacity, 1e6)

        models.specify_measures(params, FSP, FDP, satisfaction_level, capacity)

        params.zip_code_region['postcode_string'] = params.zip_code_region['postcode'].map(str)

        fig, ax = plt.subplots()
        params.zip_code_region.plot(ax=ax, column='postcode_string', cmap='Pastel2')
        g.draw_graph(params, links, ax)
        plt.scatter(params.x_user, params.y_user, s=0.01, color='k')
        circle = plt.Circle((params.center.x, params.center.y), params.radius_disaster, color='r', zorder = 2, alpha = 0.5)
        ax.add_patch(circle)
        plt.axis('off')
        plt.savefig(f'Figures/{params.filename}{seed}graph.png', dpi=1000)
        plt.show()

        # new_region = params.zip_codes[params.zip_codes['municipali'] =='Enschede']
        # new_region['postcode_string'] = new_region['postcode'].map(str)
        #
        # # TODO: Make it such that you can plot a smaller part of the province
        # fig, ax = plt.subplots()
        # new_region.plot(ax=ax, column='postcode_string', cmap='Pastel2')
        # g.draw_graph(params, links, ax)
        # plt.scatter(params.x_user, params.y_user, s=0.01, color='k')
        # circle = plt.Circle((params.center.x, params.center.y), params.radius_disaster, color='r')
        # ax.add_patch(circle)
        # plt.axis('off')
        # plt.savefig(f'Figures/{params.filename}{seed}ENSCHEDEgraph.png', dpi=1000)
        # plt.show()
        # # # #
        # analyse_UA.histogram_snr(snr.toarray(), params.filename)
        # analyse_UA.histogram_sinr(sinr.toarray(), params.filename)
        # analyse_UA.capacity(capacity, params.filename)
        # analyse_UA.fairness(capacity)
        # analyse_UA.degree_bs(np.array(links), params.filename, params)

        # if radius_disaster > 0:
        #     sheet_name = f'Disaster{radius_disaster}'
        # elif random_failure > 0:
        #     sheet_name = f'Random{random_failure}'
        # elif rain:
        #     sheet_name = f'Rain{rain}'
        # else:
        #     sheet_name = 'Normal'
        #
        # results = pd.read_pickle(f'Results/{sheet_name}.p')
        # results.loc[(results['Province'] == province) & (results['Provider'] == params.provider),
        #             'Users'] = params.number_of_users
        # results.loc[(results['Province'] == province) & (results['Provider'] == params.provider),
        #             'Base Stations'] = params.number_of_bs
        # results.loc[(results['Province'] == province) & (results['Provider'] == params.provider),
        #             'Channels'] = params.number_of_channels
        #
        # results.loc[(results['Province'] == province) & (
        #         results['Provider'] == params.provider), 'FDP'] = fraction_disconnected_pop
        # results.loc[(results['Province'] == province) & (results['Provider'] == params.provider),
        #             'FSP'] = fraction_satisified_pop
        # results.loc[(results['Province'] == province) & (results['Provider'] == params.provider),
        #             'Degree BS'] = links.sum() / params.number_of_bs
        # results.loc[(results['Province'] == province) & (results['Provider'] == params.provider),
        #             'Satisfaction'] = satisfaction
        # results.loc[(results['Province'] == province) & (results['Provider'] == params.provider),
        #             'Average capacity'] = sum(capacity) / len(capacity)
        #
        # results.to_pickle(f'Results/{sheet_name}.p')

