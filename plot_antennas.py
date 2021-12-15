import csv

import matplotlib.pyplot as plt
import networkx as nx

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

lat = []
lon = []
labels = []

with open('antennes.csv') as csvfile:
    csvReader = csv.reader(csvfile, delimiter=',')
    # next(csvReader)
    for row in csvReader:
        lat.append(float(row[3]))
        lon.append(float(row[4]))
        labels.append(row[1])

pointsBS = len(lon)
xbs, ybs = [], []

colorlist, nodesize, G = make_graph(lat, lon, labels)
fig, ax = plt.subplots()
draw_graph(G, ax, colorlist, nodesize)
plt.show()