import matplotlib.pyplot as plt
import numpy as np
import util
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import matplotlib.pylab as pylab
params = {'legend.fontsize': 'large',
         'axes.labelsize': 'large',
         'axes.titlesize':'large',
         'xtick.labelsize':'large',
         'ytick.labelsize':'large',
          'figure.autolayout': True}
pylab.rcParams.update(params)

def histogram_snr(SNR, city):
    fig, ax = plt.subplots()
    signal = SNR[np.nonzero(SNR)]
    plt.hist(signal)
    plt.xlabel('SNR (dB)')
    plt.ylabel('Number of users')
    plt.title(f'SNR distribution in {city}')
    plt.savefig(f'Figures/SNR_{city}.png')
    plt.show()
    print(f'SNR:{np.min(signal)}-{np.max(signal)} dB, average is {util.average(signal)} dB')

def histogram_sinr(SNR, city):
    fig, ax = plt.subplots()
    signal = SNR[np.nonzero(SNR)]
    plt.hist(signal)
    plt.xlabel('SINR (dB)')
    plt.ylabel('Number of users')
    plt.title(f'SINR distribution in {city}')
    plt.savefig(f'Figures/SINR_{city}.png')
    plt.show()
    print(f'SINR:{np.min(signal)}-{np.max(signal)} dB, average is {util.average(signal)} dB')

def degree_bs(links, city, params):
    fig, ax = plt.subplots()
    degrees = sum(links)
    plt.hist(degrees)
    plt.xlabel('Number of connections per BS')
    plt.ylabel('Number of BSs')
    plt.title(f'BS degree in {city}')
    plt.savefig(f'Figures/degree_{city}.png')
    plt.show()
    print(f'Number of connections per BS:{np.min(degrees)}-{np.max(degrees)}, average is {util.average(degrees)}')
    #
    # links_per_user = sum(np.transpose(links))
    # color_users = []
    # for user in range(params.number_of_users):
    #     if links_per_user[user] == 0:
    #         color_users.append('r')
    #     else:
    #         color_users.append('g')
    # fig, ax = plt.subplots()
    # plt.scatter(params.x_user, params.y_user, c = color_users, s = 2)
    # plt.scatter(params.xbs, params.ybs, s = np.multiply(2, degrees), c = degrees, cmap = 'magma_r', marker = 's')
    # legend_elements = [Line2D([0], [0], marker='o', color='w', label='Connected user',
    #                           markerfacecolor='g', markersize=5),
    #                    Line2D([0], [0], marker='o', color='w', label='Disconnected user',
    #                           markerfacecolor='r', markersize=5),
    #                    Line2D([0], [0], marker='s', color='w', label='BS',
    #                           markerfacecolor='purple', markersize=10)]
    #
    # ax.legend(handles=legend_elements)
    # plt.xticks([])
    # plt.yticks([])
    # plt.savefig(f'Figures/scatter_degrees_{city}.png', dpi = 300)

def degree_user(links, city):
    fig, ax = plt.subplots()
    degrees = sum(np.transpose(links))
    plt.hist(degrees)
    plt.xlabel('Number of connections per user')
    plt.ylabel('Number of users')
    plt.title(f'User degree in {city}')
    plt.savefig(f'Figures/user_degree_{city}.png')
    plt.show()

def capacity(capacity, city):
    fig, ax = plt.subplots()
    plt.boxplot(capacity, showfliers = False)
    plt.ylabel('Channel capacity per user (Mbps)')
    plt.savefig(f'Figures/capacity_boxplot_{city}.png')
    plt.title(f'User capacity in {city}')
    plt.show()
    fig, ax = plt.subplots()
    plt.hist(capacity)
    plt.ylabel('Channel capacity per user (Mbps)')
    plt.title(f'User capacity in {city}')
    plt.savefig(f'Figures/capacity_{city}.png')
    plt.show()

def fairness(capacity):
    # capacity_per_user = sum(np.transpose(capacity))
    fairness = sum(capacity)**2 /(sum(i**2 for i in capacity) * len(capacity))
    print(f'The fairness is {fairness}')