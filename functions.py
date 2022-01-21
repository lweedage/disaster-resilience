import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import csv
import networkx as nx
from shapely.ops import unary_union
from shapely.geometry import Point
import random

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22',
          '#17becf']
color_dict = {'LTE': colors[0], 'GSM 900': colors[1], 'GSM 1800': colors[2], 'UMTS': colors[3]}


def make_BS_graph(xbs, ybs, labels, height):
    G = nx.Graph()
    colorlist, nodesize = [], []
    for node in range(len(xbs)):
        node_name = str('BS' + str(node))
        G.add_node(node_name, pos=(xbs[node], ybs[node]), height=height[node], network_type = labels[node], type = 'BS')
        colorlist.append(color_dict[labels[node]]) # not in use now, but might be useful
    return G

def make_UE_graph(x_user, y_user):
    G = nx.Graph()
    for node in range(len(x_user)):
        node_name = str('U'+str(node))
        G.add_node(node_name, pos=(x_user[node], y_user[node]), type = 'UE')
    return G

def draw_graph(G, ax):
    UE_nodes = [n for n, v in G.nodes(data=True) if v['type'] == 'UE']
    BS_nodes = [n for n, v in G.nodes(data=True) if v['type'] == 'BS']
    UE_graph = G.subgraph(UE_nodes)
    BS_graph = G.subgraph(BS_nodes)
    nx.draw_networkx_nodes(UE_graph, nx.get_node_attributes(UE_graph, 'pos'), nodelist = UE_graph.nodes(), ax=ax, node_size=0.1, node_color='r', node_shape='o')
    nx.draw_networkx_nodes(BS_graph, nx.get_node_attributes(BS_graph, 'pos'), nodelist = BS_graph.nodes(), ax=ax, node_size=10, node_color='k', node_shape='+')
    nx.draw_networkx_edges(G, nx.get_node_attributes(G, 'pos'), edge_color='gray')

def find_data_region(G, zip_codes, zip_code_min, zip_code_max):
    # Find population + antenna data of specific region (Enschede)
    zip_codes_region = zip_codes[(zip_codes['postcode'].astype(int) >= zip_code_min) & (zip_codes['postcode'].astype(int) <= zip_code_max)] #has to be 7511 - 7548 for Enschede
    boundary = gpd.GeoSeries(unary_union(zip_codes_region['geometry']))

    x_users, y_users = get_population(zip_codes_region)

    positions = nx.get_node_attributes(G, 'pos')
    subgraph_nodes = []

    for node in G.nodes():
        x, y = positions[node]
        if boundary.contains(Point(x,y)).bool():
            subgraph_nodes.append(node)

    BS_graph = nx.subgraph(G, subgraph_nodes)       # only BSs of a certain region
    UE_graph = make_UE_graph(x_users, y_users)      # the simulated users of that region

    total_network = nx.compose(BS_graph, UE_graph)
    return total_network

def generate_random(number, polygon):   # to generate users per zip code
    points = []
    minx, miny, maxx, maxy = polygon.bounds
    while len(points) < number:
        pnt = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if polygon.contains(pnt):
            points.append(pnt)
    return points


# find all users in the specific zip codes
def get_population(zip_codes_region):
    users = []
    division_parameter = 5  # 1/5th of the population uses the network

    for index, row in zip_codes_region.iterrows():
        polygon = row['geometry']
        number_of_users = row['aantal_inw']
        points = generate_random(number_of_users / division_parameter, polygon)
        users += points
    xs = [point.x for point in users]
    ys = [point.y for point in users]
    return xs, ys
