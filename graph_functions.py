import networkx as nx
from settings import *
from matplotlib.lines import Line2D


def make_graph(xbs, ybs, xu, yu, base_stations, links):
    G = nx.Graph()
    colorlist = list()
    nodesize = list()
    edgesize = list()
    edgecolor = list()
    freq_color = dict()
    labels = {}
    number_of_bs = len(xbs)
    number_of_users = len(xu)
    i = 0
    for node in range(number_of_bs):
        G.add_node(node, x = xbs[node], y = ybs[node])
        # if base_stations[node].small_cell:
        #     colorlist.append(colors[2])
        # else:
        #     colorlist.append(colors[1])
        freq = base_stations[node].channels[0].frequency
        if freq not in freq_color:
            freq_color[freq] = i
            i +=1
        colorlist.append(colors[freq_color[freq]])
        nodesize.append(1)
        labels[node] = f'{freq_color[freq]}'
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
    return G, colorlist, nodesize, edgesize, labels, edgecolor, freq_color


def draw_graph(xbs, ybs, xu, yu, links, base_stations, ax):
    G, colorlist, nodesize, edgesize, labels, edgecolor, freq_color = make_graph(xbs, ybs, xu, yu, base_stations, links)
    pos = dict()
    for node in G.nodes():
        pos[node] = (nx.get_node_attributes(G, 'x')[node], nx.get_node_attributes(G, 'y')[node])
    nx.draw_networkx_nodes(G, pos, nodelist=G.nodes(), node_size=nodesize,
                           node_color=colorlist, ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color=edgecolor, alpha=0.5, width=edgesize)
    # nx.draw_networkx_labels(G, pos, labels, font_size=2)


    # legend_elements = []
    # i = 0
    # for key, value in freq_color.items():
    #     legend_elements.append(Line2D([0], [0], marker = f'${i}$', color = 'w', markerfacecolor= colors[value], markeredgecolor= colors[value], markersize = 10, label = f'{key/1e6} MHz'))
    #     i += 1
    # ax.legend(handles=legend_elements, bbox_to_anchor=(1.1, 0.9))

