import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import util
import find_base_stations as antenna
from settings import *

# Retrieve zip code population + area data and make a region with specified zip codes
# Columns are: aantal_inw (population), stedelijkh (urbanity), postcode (zip code), geometry, popdensity (population density), municipali(city), BS_GSM, BS_UMTS, BS_LTE, BS_NR, BSs
zip_codes = gpd.read_file('data/zip_codes.shp')


# region that we want to investigate:
municipality = 'Groningen'  # 'Gelderland', 'Overijssel', 'Noord-Holland', 'Zuid-Holland', 'Groningen', 'Utrecht', 'Limburg', 'Noord-Brabant', 'Friesland', 'Zeeland', 'Flevoland', 'Drenthe'
cities = util.find_cities(municipality)  # has to be a list of cities
cities = ['Groningen']

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
p = zip_code_region.plot(column='popdensity', ax=ax, legend=True)
ax.scatter(xbs_UMTS, ybs_UMTS, color=colors[0], marker='+', label='UMTS')
ax.scatter(xbs_GSM, ybs_GSM, color=colors[1], marker='+', label='GSM')
ax.scatter(xbs_LTE, ybs_LTE, color=colors[2], marker='+', label='LTE')
ax.scatter(xbs_NR, ybs_NR, color=colors[3], marker='+', label='NR')
plt.legend()
plt.title(cities[0])
plt.show()

# fig, ax = plt.subplots()
# plt.hist(zip_codes['BSs'], alpha = 0.3, density = True, label = 'Total BSs per zip code')
# plt.hist(zip_codes['GSM_BS'], alpha = 0.3, density = True, label = 'GSM BSs per zip code')
# plt.hist(zip_codes['LTE_BS'], alpha = 0.3, density = True, label = 'LTE BSs per zip code')
# plt.hist(zip_codes['UMTS_BS'], alpha = 0.3, density = True, label = 'UMTS BSs per zip code')
# plt.hist(zip_codes['NR_BS'], alpha = 0.3, density = True, label = 'NR BSs per zip code')
# plt.legend()
# plt.show()