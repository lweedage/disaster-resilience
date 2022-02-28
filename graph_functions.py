import networkx as nx
from settings import *
import pydot

def make_graph(xbs, ybs, xu, yu, base_stations, links):
    G = nx.Graph()
    colorlist = list()
    nodesize = list()
    edgesize = list()
    edgecolor = list()
    labels = {}
    number_of_bs = len(xbs)
    number_of_users = len(xu)
    for node in range(number_of_bs):
        G.add_node(node, x = xbs[node], y = ybs[node])
        if base_stations[node].small_cell:
            colorlist.append(colors[2])
        else:
            colorlist.append(colors[1])
        nodesize.append(1)
        # labels[node] = f'BS{node}'
    for node in range(number_of_users):
        G.add_node(node + number_of_bs, x = xu[node], y = yu[node])
        colorlist.append('k')
        nodesize.append(0.1)
        # labels[node + number_of_bs] = f'{node}'
    for bs in range(number_of_bs):
        for user in range(number_of_users):
            if links[user, bs] > 0.1:
                G.add_edge(user + number_of_bs, bs)
                edgesize.append(0.1)
                edgecolor.append('gray')
    return G, colorlist, nodesize, edgesize, labels, edgecolor


def draw_graph(xbs, ybs, xu, yu, links, base_stations, ax):
    G, colorlist, nodesize, edgesize, labels, edgecolor = make_graph(xbs, ybs, xu, yu, base_stations, links)
    pos = dict()
    for node in G.nodes():
        pos[node] = (nx.get_node_attributes(G, 'x')[node], nx.get_node_attributes(G, 'y')[node])
    nx.draw_networkx_nodes(G, pos, nodelist=G.nodes(), node_size=nodesize,
                           node_color=colorlist, ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color=edgecolor, alpha=0.5, width=edgesize)
    nx.draw_networkx_labels(G, pos, labels, font_size=10)
