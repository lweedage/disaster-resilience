import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import csv
import networkx as nx
from shapely.ops import unary_union
from shapely.geometry import Point
from shapely.geometry import Polygon
import random
import graph_functions as gf
import plot_population as p

def find_data_region(zip_codes, zip_code_min, zip_code_max):
    # Find population + antenna data of specific region (Enschede)
    zip_codes_region = zip_codes[(zip_codes['postcode'].astype(int) >= zip_code_min) & (zip_codes['postcode'].astype(int) <= zip_code_max)] #has to be 7511 - 7548 for Enschede
    boundary = gpd.GeoSeries(unary_union(zip_codes_region['geometry']))

    lat_region, lon_region, labels_region = [], [], []
    G = gf.make_graph(lat, lon, labels)

    positions = nx.get_node_attributes(G, 'pos')
    for node in G.nodes():
        x, y = positions[node]
        if boundary.contains(Point(x,y)).bool():
            lat_region.append(x)
            lon_region.append(y)
            labels_region.append(labels[node])

    antenna_graph_region = gf.make_graph(lat_region, lon_region, labels_region)
    return zip_codes_region, antenna_graph_region

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

# open the zip_code population data
zip_codes = gpd.read_file('zip_codes.shp')

zip_codes_twente, antenna_graph_twente = find_data_region(zip_codes, 7000, 8100)
users = p.get_population(zip_codes_twente)

xs = [point.x for point in users]
ys = [point.y for point in users]

number_of_users = len(xs)

fig, ax = plt.subplots()
gf.draw_graph(antenna_graph_twente, ax)
# zip_codes_twente.plot('aantal_inw', ax = ax, legend = True, vmin = 0)
plt.scatter(xs, ys, s = 0.1, label = 'Users')

plt.legend()
plt.show()