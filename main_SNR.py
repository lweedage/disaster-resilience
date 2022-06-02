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
import objects.UE as User
warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)

# Retrieve zip code population + area data and make a region with specified zip codes
# Columns are: aantal_inw (population), stedelijkh (urbanity), postcode (zip code), geometry,
# popdensity (population density), municipali(city), GSM_BS, UMTS_BS, LTE_BS, NR_BS, BSs, scenario
zip_codes = gpd.read_file('data/zip_codes_with_scenarios.shp')

# Region that we want to investigate:
province = 'Noord-Holland'  # 'Gelderland', 'Overijssel', 'Noord-Holland', 'Zuid-Holland', 'Groningen', 'Utrecht', 'Limburg', 'Noord-Brabant', 'Friesland', 'Zeeland', 'Flevoland', 'Drenthe'
cities = util.find_cities(province)
# cities, province = ['Hengelo'], None
# cities, province = None, None

mno = ['KPN'] #'T-Mobile, Vodafone, KPN
percentage = 1 # Three user density levels - still tbd
seed = 1

delta = 500
params = p.Parameters(seed, zip_codes, mno, percentage, city_list = cities, province = province, delta = delta)

params = antenna.find_zip_code_region(params)



print('Finding users...')
params = generate_users.generate_users_grid(params, delta)
print('There are', params.number_of_users, 'users')

print('Finding BSs...')
params = antenna.load_bs(params)
print('There are', params.number_of_bs, 'BSs')


links, link_channel, snr, sinr, capacity, FDP, FSP, satisfaction_level = models.find_links(params)

fraction_disconnected_pop = sum(FDP)/params.number_of_users

print(f'FDP = {fraction_disconnected_pop}')

# analyse_UA.SE(spectral_efficiency, params.filename)

[xmin, ymin, xmax, ymax] = gpd.GeoSeries(params.zip_code_region['geometry']).total_bounds
xmin, xmax = np.floor(xmin), np.ceil(xmax)
ymin, ymax = np.floor(ymin), np.ceil(ymax)
xdelta, ydelta = int(xmax - xmin), int(ymax - ymin)

fig, ax = plt.subplots()
data = pd.DataFrame(data={'x':params.y_user, 'y':params.x_user, 'z':sum(np.transpose(snr))})
data = data.pivot(index='x', columns='y', values='z')
hm = sns.heatmap(data, cmap ='magma_r', ax = ax)
ax.scatter(np.divide(np.subtract(params.xbs, xmin), delta), np.divide(np.subtract(params.ybs, ymin), delta), s = 5, color = 'g')
plt.xticks([])
plt.yticks([])
plt.savefig(f'Figures/heatmap{params.filename}.png', dpi=1000)
plt.show()