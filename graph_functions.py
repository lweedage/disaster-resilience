import networkx as nx

from settings import *


def make_graph(p, links):
    G = nx.Graph()
    colorlist = list()
    nodesize = list()
    edgesize = list()
    edgecolor = list()
    MNOcolor = {'KPN': 0, 'T-Mobile': 1, 'Vodafone': 2, 'all_MNOs':3}
    labels = {}
    number_of_bs = p.number_of_bs
    number_of_users = p.number_of_users
    xbs = p.xbs
    ybs = p.ybs
    i = 0
    for node in range(number_of_bs):
        G.add_node(node, x=xbs[node], y=ybs[node])
        # if base_stations[node].small_cell:
        #     colorlist.append(colors[2])
        # else:
        #     colorlist.append(colors[1])
        MNO = p.BaseStations[node].provider

        colorlist.append(colors[MNOcolor[MNO]])
        nodesize.append(2)
        labels[node] = f'{MNO}'
    for node in range(number_of_users):
        G.add_node(node + number_of_bs, x=p.x_user[node], y=p.y_user[node])
        MNO = p.users[node].provider
        colorlist.append(colors[MNOcolor[MNO]])
        nodesize.append(0.1)
        # labels[node + number_of_bs] = f'{node}'
    for bs in range(number_of_bs):
        for user in range(number_of_users):
            if links[user, bs] > 0.1:
                G.add_edge(user + number_of_bs, bs)
                edgesize.append(0.1)
                edgecolor.append('gray')
    return G, colorlist, nodesize, edgesize, labels, edgecolor


def draw_graph(params, links, ax):
    G, colorlist, nodesize, edgesize, labels, edgecolor = make_graph(params, links)
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
