import csv
import networkx as nx
import matplotlib.pyplot as plt
import math
import numpy as np
import geopy.distance
import pickle
import progressbar
from owslib.wfs import WebFeatureService

wfs = WebFeatureService('https://geo.zaanstad.nl/geoserver/wfs?SERVICE=WFS&singleTile=true', version='1.1.0')
res = wfs.getfeature(typename='geo:antenneregister', sortby=['gemeente'], startindex=10000)
print(res)
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22',
          '#17becf']

color_dict = {'LTE': colors[0], 'GSM 900': colors[1], 'GSM 1800': colors[2], 'UMTS': colors[3]}
print(color_dict)

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

First = True

lon = []
lat = []
labels = []

with open('antenneregister.csv') as csvfile:
    csvReader = csv.reader(csvfile, delimiter=';')
    for row in csvReader:
        if not First:
            lon.append(float(row[4]))
            lat.append(float(row[5]))
            labels.append(row[2])
        else:
            First = False
pointsBS = len(lon)
xbs, ybs = [], []

print(set(labels))


colorlist, nodesize, G = make_graph(lat, lon, labels)

fig, ax = plt.subplots()
draw_graph(G, ax, colorlist, nodesize)
plt.show()