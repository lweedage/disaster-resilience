import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import util
import find_base_stations as antenna
from settings import *

# Retrieve zip code population + area data and make a region with specified zip codes
# Columns are: aantal_inw (population), stedelijkh (urbanity), postcode (zip code), geometry, popdensity (population density), municipali(city)
zip_codes = gpd.read_file('data/zip_codes.shp')
print(zip_codes.columns)

# region that we want to investigate:
city = ['Enschede', 'Hengelo', 'Haaksbergen', 'Almelo', 'Borne'] #has to be a list of municipalities - if None, it does the Netherlands


region, zip_code_region = antenna.find_zip_code_region(zip_codes, city)
# base_stations = antenna.load_bs(region)
#
# xbs, ybs = [], []
# for BS in base_stations:
#     xbs.append(BS.lat)
#     ybs.append(BS.lon)
# print(zip_code_region)


fig, ax = plt.subplots()
p = zip_code_region.plot(column='popdensity', ax = ax, legend = True)
# k = ax.scatter(xbs, ybs, color = 'k', marker = '+')

plt.title(city)
plt.show()

