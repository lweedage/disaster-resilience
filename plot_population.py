import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import numpy as np
import csv
import networkx as nx
from shapely.ops import unary_union
from shapely.geometry import Point
import pointpats

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22',
          '#17becf']
color_dict = {'LTE': colors[0], 'GSM 900': colors[1], 'GSM 1800': colors[2], 'UMTS': colors[3]}


lat, lon, labels = [], [], []
def make_graph(xbs, ybs, labels):
    G = nx.Graph()
    colorlist, nodesize = [], []
    for node in range(len(xbs)):
        G.add_node(node, pos=(xbs[node], ybs[node]))
        colorlist.append(color_dict[labels[node]])
        nodesize.append(20)
    return colorlist, nodesize, G

def draw_graph(G, ax, colorlist, nodesize):
    nx.draw_networkx_nodes(G, nx.get_node_attributes(G, 'pos'), nodelist = G.nodes(), ax=ax, node_size=nodesize, node_color=colorlist, node_shape='+')
    nx.draw_networkx_edges(G, nx.get_node_attributes(G, 'pos'), edge_color='gray')

def find_specific_city(min_zipcode, max_zipcode, zip_codes, G):
    zip_codes_city = zip_codes[(zip_codes['postcode'].astype(int) >= min_zipcode) & (zip_codes['postcode'].astype(int) <= max_zipcode)]
    boundary = gpd.GeoSeries(unary_union(zip_codes_city['geometry']))
    positions = nx.get_node_attributes(G, 'pos')
    lat_city, lon_city, labels_city = [], [], []
    for node in G.nodes():
        x, y = positions[node]
        if boundary.contains(Point(x, y)).bool():
            lat_city.append(x)
            lon_city.append(y)
            labels_city.append(labels[node])
    return zip_codes_city, lat_city, lon_city, labels_city

def simulate_user_coordinates(densities, zip_codes):


with open('antennas.csv') as csvfile:
    csvReader = csv.reader(csvfile, delimiter=',')
    # next(csvReader)
    for row in csvReader:
        longitude, latitude = float(row[4]), float(row[3])
        lat.append(latitude)
        lon.append(longitude)
        labels.append(row[1])



zip_codes = gpd.read_file('zip_codes.shp')
user_density = (zip_codes['aantal_inw'] / zip_codes['geometry'].area)
zip_codes['user_density'] = user_density

colorlist, nodesize, graph = make_graph(lat, lon, labels)

zip_codes_enschede, lat_enschede, lon_enschede, labels_enschede = find_specific_city(7511, 7548, zip_codes, graph)
colorlist_enschede, nodesize_enschede, G_enschede = make_graph(lat_enschede, lon_enschede, labels_enschede)


# fig, ax = plt.subplots()
# draw_graph(G_enschede, ax, ['k']*len(nodesize_enschede), nodesize_enschede)
# zip_codes_enschede.plot('aantal_inw', ax = ax, legend = True, vmin = 0)
# plt.show()


fig, ax = plt.subplots()
draw_graph(G_enschede, ax, ['k']*len(nodesize_enschede), nodesize_enschede)
zip_codes_enschede.plot('user_density', ax = ax, legend = True, vmin = 0)
plt.show()

x_user, y_user = simulate_user_coordinates(zip_codes['user_density'].tolist(), zip_codes)