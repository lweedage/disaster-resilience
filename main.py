import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import csv
import generate_users as f
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
import find_base_stations as antenna

# pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Retrieve zip code population + area data and make a region with specified zip codes
zip_codes = gpd.read_file('data/zip_codes.shp')

# region that we want to investigate:
zip_code_min, zip_code_max = min(zip_codes['postcode']), max(zip_codes['postcode']) # Enschede is 7511 - 7548
zip_code_min, zip_code_max = 7511, 7548

region, zip_code_region = antenna.find_zip_code_region(zip_code_min, zip_code_max, zip_codes)
# base_stations = antenna.load_bs(region)
#
# xbs, ybs = [], []
# for BS in base_stations:
#     xbs.append(BS.lat)
#     ybs.append(BS.lon)

fig, ax = plt.subplots()
# plt.scatter(xbs, ybs)
p = zip_code_region.plot(column='popdensity', ax = ax, legend = True)
plt.show()



