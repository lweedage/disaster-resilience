import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import util
import find_base_stations as antenna
from settings import *
import generate_users
import pickle

# Retrieve zip code population + area data and make a region with specified zip codes
# Columns are: aantal_inw (population), stedelijkh (urbanity), postcode (zip code), geometry, popdensity (population density), municipali(city), GSM_BS, UMTS_BS, LTE_BS, NR_BS, BSs, scenario
zip_codes = gpd.read_file('data/zip_codes_with_scenarios.shp')

# region that we want to investigate:
# province = 'Overijssel'  # 'Gelderland', 'Overijssel', 'Noord-Holland', 'Zuid-Holland', 'Groningen', 'Utrecht', 'Limburg', 'Noord-Brabant', 'Friesland', 'Zeeland', 'Flevoland', 'Drenthe'
# cities = util.find_cities(province)  # has to be a list of cities
cities = ['Assen']

region, zip_code_region = antenna.find_zip_code_region(zip_codes, cities)
print('Finding BSs...')
base_stations = antenna.load_bs(region)
users = generate_users.generate_users(zip_code_region)

def save_object(obj, filename):
    with open(filename, 'wb') as outp:
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)

save_object(base_stations, 'Data/all_base_stations.pkl')

x_KPN, y_KPN = [], []
x_Vodafone, y_Vodafone = [], []
x_TMobile, y_TMobile = [], []

providers = ['KPN', 'Vodafone', 'T-Mobile']
LTE, GSM, UMTS, NR = dict(), dict(), dict(), dict()
for prov in providers:
    LTE[prov] = 0
    GSM[prov] = 0
    UMTS[prov] = 0
    NR[prov] = 0

for bs in base_stations:
    # if bs.provider == 'KPN':
    #     x_KPN.append(bs.x)
    #     y_KPN.append(bs.y)
    # elif bs.provider == 'Vodafone':
    #     x_Vodafone.append(bs.x)
    #     y_Vodafone.append(bs.y)
    # elif bs.provider == 'T-Mobile':
    #     x_TMobile.append(bs.x)
    #     y_TMobile.append(bs.y)
    provider = bs.provider
    if bs.radio == util.BaseStationRadioType.LTE:
        LTE[provider] += 1
    elif bs.radio == util.BaseStationRadioType.GSM:
        GSM[provider] += 1
    elif bs.radio == util.BaseStationRadioType.UMTS:
        UMTS[provider] += 1
    elif bs.radio == util.BaseStationRadioType.NR:
        NR[provider] += 1

# print(f'Number of KPN BS: {len(x_KPN)}')
# print(f'Number of Vodafone BS: {len(x_Vodafone)}')
# print(f'Number of T-Mobile BS: {len(x_TMobile)}')
# print(f'Total number of BSs: {len(x_KPN) + len(x_Vodafone) + len(x_TMobile)}')
# print(f'Area of {cities[0]}: {sum(zip_code_region.area)/1e6} km^2')
# print(f'Total population: {sum(zip_code_region.aantal_inw)} ')
for prov in providers:
    print(f'{prov}: {GSM[prov]}, {UMTS[prov]}, {LTE[prov]}, {NR[prov]}')

# fig, ax = plt.subplots()
# zip_code_region.plot(column='popdensity', ax=ax)
# plt.scatter(x_KPN, y_KPN, marker='+', s=10, label='KPN')
# plt.scatter(x_Vodafone, y_Vodafone, marker='+', s=10, label='Vodafone')
# plt.scatter(x_TMobile, y_TMobile, marker='+', s=10, label='T-Mobile')
# plt.legend()
# plt.show()

