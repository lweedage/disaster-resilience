import math
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import analyse_UA
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
warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)

# Retrieve zip code population + area data and make a region with specified zip codes
# Columns are: aantal_inw (population), stedelijkh (urbanity), postcode (zip code), geometry,
# popdensity (population density), municipali(city), GSM_BS, UMTS_BS, LTE_BS, NR_BS, BSs, scenario
zip_codes = gpd.read_file('data/zip_codes_with_scenarios.shp')

# Region that we want to investigate:
# province = 'Noord-Holland'  # 'Gelderland', 'Overijssel', 'Noord-Holland', 'Zuid-Holland', 'Groningen', 'Utrecht', 'Limburg', 'Noord-Brabant', 'Friesland', 'Zeeland', 'Flevoland', 'Drenthe'
province = str(input('Province?'))
cities = util.find_cities(province)
# cities, province = [7543], None
# cities, province = None, None

mno = ['T-Mobile'] #'T-Mobile, Vodafone, KPN
percentage = 1 # Three user density levels - still tbd
seed = 1

params = p.Parameters(seed, zip_codes, mno, percentage, city_list = cities, province = province)

params = antenna.find_zip_code_region(params)

print('Finding users...')
params = generate_users.generate_users(params)
print('There are', params.number_of_users, 'users')

print('Finding BSs...')
params = antenna.load_bs(params)
print('There are', params.number_of_bs, 'BSs')

links, link_channel, snr, sinr, capacity, FDP, FSP, satisfaction_level = models.find_links(params)

fraction_satisified_pop = sum(FSP)/params.number_of_users
fraction_disconnected_pop = sum(FDP)/params.number_of_users

print(f'FDP = {fraction_disconnected_pop}')
print(f'FSP = {fraction_satisified_pop}')
print(f'Satisfaction level = {sum(satisfaction_level)/len(satisfaction_level)}')

# params = models.specify_measures(params, FSP, FDP, satisfaction_level)

fig, ax = plt.subplots()
plt.hist(satisfaction_level)
plt.xlabel('satisfaction level')
plt.savefig(f'Figures/{params.filename}_satisfaction_level.png')
plt.show()

fig, ax = plt.subplots()
params.zip_code_region.plot(column='aantal_inw', ax=ax, cmap='OrRd', legend = True)
g.draw_graph(params, links, ax)
bound = 1000
# plt.xlim((min(params.x_user) - bound, max(params.x_user) + bound))
# plt.ylim((min(params.y_user) - bound, max(params.y_user) + bound))
plt.savefig(f'Figures/{params.filename}{seed}graph.png', dpi=1000)
plt.show()
#
capacity = np.divide(capacity, 1e6)

analyse_UA.histogram_snr(snr, params.filename)
analyse_UA.histogram_sinr(sinr, params.filename)
analyse_UA.capacity(capacity, params.filename)
analyse_UA.fairness(capacity)
analyse_UA.degree_bs(links, params.filename, params)
