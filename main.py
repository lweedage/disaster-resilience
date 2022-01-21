import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import csv

import functions as f
import plot_population as p

# region that we want to investigate:
zip_code_min, zip_code_max = 7511, 7512

# open the antenna data
lat, lon, labels, height = [], [], [], []

with open('antennas.csv') as csvfile:
    csvReader = csv.reader(csvfile, delimiter=',')
    # next(csvReader)
    for row in csvReader:
        longitude, latitude = float(row[4]), float(row[3])
        lat.append(latitude)
        lon.append(longitude)
        labels.append(row[1])
        height.append(row[2])

G = f.make_BS_graph(lat, lon, labels, height)

# open the zip_code population data
zip_codes = gpd.read_file('zip_codes.shp')

# get region-specific data (users included)
network_twente = f.find_data_region(G, zip_codes, zip_code_min, zip_code_max)


fig, ax = plt.subplots()
f.draw_graph(network_twente, ax)
plt.legend()
plt.show()