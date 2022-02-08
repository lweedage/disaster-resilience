import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import csv
import generate_users as f
import find_base_stations as antenna

# Retrieve zip code population + area data and make a region with specified zip codes
zip_codes = gpd.read_file('zip_codes.shp')
zip_codes = zip_codes[~zip_codes['geometry'].isnull()] # Remove rows with empty geometry

# region that we want to investigate:
zip_code_min, zip_code_max = min(zip_codes['postcode']), max(zip_codes['postcode']) # Enschede is 7511 - 7548
print(zip_code_min, zip_code_max)

region, zip_code_region = antenna.find_zip_code_region(zip_code_min, zip_code_max, zip_codes)
base_stations = antenna.load_bs(region)

xbs, ybs = [], []
for BS in base_stations:
    xbs.append(BS.lat)
    ybs.append(BS.lon)

fig, ax = plt.subplots()
plt.scatter(xbs, ybs)
p = zip_code_region.plot(column='popdensity')
# plt.colorbar(p)
plt.show()