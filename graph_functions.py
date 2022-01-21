import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import csv
import networkx as nx

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22',
          '#17becf']
color_dict = {'LTE': colors[0], 'GSM 900': colors[1], 'GSM 1800': colors[2], 'UMTS': colors[3]}


def make_graph(xbs, ybs, labels):
    G = nx.Graph()
    colorlist, nodesize = [], []
    for node in range(len(xbs)):
        G.add_node(node, pos=(xbs[node], ybs[node]))
        colorlist.append(color_dict[labels[node]])
        nodesize.append(20)
    return G

def draw_graph(G, ax,  colorlist = 'k', nodesize=5):
    nx.draw_networkx_nodes(G, nx.get_node_attributes(G, 'pos'), nodelist = G.nodes(), ax=ax, node_size=nodesize, node_color=colorlist, node_shape='+')
    nx.draw_networkx_edges(G, nx.get_node_attributes(G, 'pos'), edge_color='gray')
