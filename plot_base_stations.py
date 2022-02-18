import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import util
import find_base_stations as antenna
from settings import *

# Retrieve zip code population + area data and make a region with specified zip codes
# Columns are: aantal_inw (population), stedelijkh (urbanity), postcode (zip code), geometry, popdensity (population density), municipali(city), GSM_BS, UMTS_BS, LTE_BS, NR_BS, BSs, scenario
zip_codes = gpd.read_file('data/zip_codes_with_scenarios.shp')

# region that we want to investigate:
municipality = 'Overijssel'  # 'Gelderland', 'Overijssel', 'Noord-Holland', 'Zuid-Holland', 'Groningen', 'Utrecht', 'Limburg', 'Noord-Brabant', 'Friesland', 'Zeeland', 'Flevoland', 'Drenthe'
cities = util.find_cities(municipality)  # has to be a list of cities
cities = ['Enschede']

region, zip_code_region = antenna.find_zip_code_region(zip_codes, cities)
base_stations = antenna.load_bs(region)

xbs_UMTS, ybs_UMTS = [], []
xbs_GSM, ybs_GSM = [], []
xbs_LTE, ybs_LTE = [], []
xbs_NR, ybs_NR = [], []

for BS in base_stations:
    if BS.radio == util.BaseStationRadioType.UMTS:
        xbs_UMTS.append(BS.x)
        ybs_UMTS.append(BS.y)
    elif BS.radio == util.BaseStationRadioType.GSM:
        xbs_GSM.append(BS.x)
        ybs_GSM.append(BS.y)
    elif BS.radio == util.BaseStationRadioType.LTE:
        xbs_LTE.append(BS.x)
        ybs_LTE.append(BS.y)
    elif BS.radio == util.BaseStationRadioType.NR:
        xbs_NR.append(BS.x)
        ybs_NR.append(BS.y)

fig, ax = plt.subplots()
p = zip_code_region.plot(column='scenario', ax=ax, legend=True)
ax.scatter(xbs_UMTS, ybs_UMTS, color=colors[0], marker='+', label='UMTS')
ax.scatter(xbs_GSM, ybs_GSM, color=colors[1], marker='+', label='GSM')
ax.scatter(xbs_LTE, ybs_LTE, color=colors[2], marker='+', label='LTE')
ax.scatter(xbs_NR, ybs_NR, color=colors[3], marker='+', label='NR')
plt.legend()
plt.title(cities[0])
plt.show()
