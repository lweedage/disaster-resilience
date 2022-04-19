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

# Retrieve zip code population + area data and make a region with specified zip codes
# Columns are: aantal_inw (population), stedelijkh (urbanity), postcode (zip code), geometry,
# popdensity (population density), municipali(city), GSM_BS, UMTS_BS, LTE_BS, NR_BS, BSs, scenario
zip_codes = gpd.read_file('data/zip_codes_with_scenarios.shp')

# Region that we want to investigate:
# province = 'Overijssel'  # 'Gelderland', 'Overijssel', 'Noord-Holland', 'Zuid-Holland', 'Groningen', 'Utrecht', 'Limburg', 'Noord-Brabant', 'Friesland', 'Zeeland', 'Flevoland', 'Drenthe'
# cities = util.find_cities(province)  # has to be a list of cities

cities = ['Enschede']
city = cities[0]

region, zip_code_region = antenna.find_zip_code_region(zip_codes, cities)

print('Finding BSs...')
base_stations, x_bs, y_bs = antenna.load_bs(region, zip_code_region, city)

print('Finding users...')
users, x_user, y_user = generate_users.generate_users(zip_code_region, percentage=1, city = city)
print('There are', len(x_user), 'users')

links, link_channel, snr, sinr, capacity = models.find_links(users, base_stations, x_bs, y_bs)

fig, ax = plt.subplots()
zip_code_region.plot(column='popdensity', ax=ax, cmap='OrRd')
g.draw_graph(x_bs, y_bs, x_user, y_user, links, base_stations, ax)
bound = 1000

plt.xlim((min(x_user) - bound, max(x_user) + bound))
plt.ylim((min(y_user) - bound, max(y_user) + bound))
plt.savefig(f'Figures/{city}graph.png', dpi=1000)
plt.show()

capacity = np.divide(capacity, 1e6)

analyse_UA.histogram_snr(snr, city)
analyse_UA.histogram_snr(sinr, city)
analyse_UA.capacity(capacity, city)
analyse_UA.fairness(capacity)

# analyse_UA.degree_user(links, city)


# util.save_object(base_stations, 'data/' + cities[0] + '_all_base_stations.pkl')
