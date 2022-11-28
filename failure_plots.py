import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import pandas as pd
import geopandas as gpd
from shapely import wkt
from shapely.ops import unary_union
import util
import numpy as np

params = {'legend.fontsize': 'x-large',
          'axes.labelsize': 'x-large',
          'axes.titlesize': 'x-large',
          'xtick.labelsize': 'x-large',
          'ytick.labelsize': 'x-large',
          'lines.markersize': 8,
          'figure.autolayout': True}
pylab.rcParams.update(params)

colors = ['#904C77', '#E49AB0', '#ECB8A5', '#96ACB7', '#957D95'] * 100
markers = ['o', 'X', 'v', 's', '*', 'P', '1', '+']
#
max_iterations = 100
percentage = 2
percentage_MNO = {'Vodafone': 0.33, 'KPN': 0.33, 'T-Mobile': 0.33, 'all_MNOs': 1}

#
provinces = list(reversed(['Drenthe', 'Flevoland', 'Friesland', 'Gelderland', 'Groningen', 'Limburg', 'Noord-Brabant',
             'Noord-Holland', 'Overijssel', 'Utrecht', 'Zeeland', 'Zuid-Holland']))
municipalities = ['Middelburg', 'Maastricht', 'Groningen', 'Enschede', 'Emmen', 'Elburg',
                  'Eindhoven', "'s-Gravenhage", 'Amsterdam', 'Almere']
municipalities2 = ['Middelburg', 'Maastricht', 'Groningen', 'Enschede', 'Emmen', 'Elburg',
                  'Eindhoven', "Den Haag", 'Amsterdam', 'Almere']


MNOs = ['KPN', 'T-Mobile', 'Vodafone', 'all_MNOs']
name_MNO = ['MNO-1', 'MNO-2', 'MNO-3', 'National roaming']
#

Disaster = True
Random = False
User = False

radii = [0, 500, 1000, 2500]
increases = [0, 50, 100, 200]
random = [0, 0.05, 0.1, 0.25, 0.5]

def find_name(filename, radius):
    if MNO != 'all_MNOs':
        filename += str(20.33)
    else:
        filename += str(21)

    if radius == 0:
        return filename + str(5)

    if Disaster:
        filename += 'disaster' + str(radius)
    elif User:
        filename += 'user_increase' + str(radius)
    elif Random:
        filename += 'random' + str(radius)
    return filename + str(5)

FSP, FDP, SAT = {MNO: [] for MNO in MNOs}, {MNO: [] for MNO in MNOs}, {MNO: [] for MNO in MNOs}
users = {MNO: [] for MNO in MNOs}

if Disaster:
    measures = radii
elif User:
    measures = increases
elif Random:
    measures = random
else:
    measures = [0]

MNOs = ['KPN', 'T-Mobile', 'Vodafone', 'all_MNOs']
municipalities = ['Enschede']

for MNO in MNOs:
    for FDPFSP in ['FDP', 'FSP']:
        data = []
        for i, measure in zip(range(len(measures)), measures):
            for municipality in municipalities:
                filename = f'{municipality}{MNO}'
                filename = find_name(filename, measure)
                if FDPFSP == 'FDP':
                    fdpfsp = util.from_data(f'data/Realisations/{filename}_totalfdp.p')
                else:
                    fdpfsp = util.from_data(f'data/Realisations/{filename}_totalfsp.p')

                data.append(sum(fdpfsp)/len(fdpfsp))

        print(MNO, FDPFSP, data)
print(measures)
#
#         if Disaster:
#             label = str('$r_{fail} =$' + str(measure))
#         elif User:
#             label = f'{measure}$\%$'
#         elif Random:
#             label = str('$p_{iso} =$' + str(measure))
#         else:
#             label = 'blub'
#
#         plt.scatter(data, range(len(municipalities)), label=label, color=colors[i], marker=markers[i])
#     plt.xlabel(FDPFSP)
#     plt.yticks(range(len(municipalities)), municipalities2)
#     if FDPFSP == 'FSP':
#         plt.legend(loc='lower left')
#     if FDPFSP == 'FDP':
#         plt.legend(loc='upper right')        # plt.legend()
#     ax.tick_params(top=False,
#                    bottom=False,
#                    left=False,
#                    right=False,
#                    labelleft=True,
#                    labelbottom=True)
#     ax.spines['right'].set_visible(False)
#     ax.spines['top'].set_visible(False)
#     ax.spines['left'].set_visible(False)
#     ax.spines['bottom'].set_visible(False)
#     plt.savefig(f'Figures/{find_name(MNO, measure)}{FDPFSP}municipalities.png')
#     # plt.show()
#
# dataFDP, dataFSP = [], []
# filename = find_name('all_MNOs', measure)
# filename = 'all_MNOs'
# df = util.from_data(f'converted_data/{filename}_municipalities.p')
# print(df)
# print(filename)
# nationalroaming_FDP = df['FDP'].astype('float')
# nationalroaming_FSP = df['FSP'].astype('float')
#
#
# for MNO in MNOs[:-1]:
#     filename = f'{MNO}'
#     # filename = find_name(filename, measure)
#     df = util.from_data(f'converted_data/{filename}_municipalities.p')
#
#     dataFDP.append(df['FDP'].astype('float') - nationalroaming_FDP)
#     dataFSP.append(nationalroaming_FSP - df['FSP'].astype('float'))
#
# x = np.array([1, 2, 3])
#
# print(dataFSP)
#
# fig, ax = plt.subplots()
# fdplot = ax.boxplot(dataFDP, positions=x - 0.17, widths=0.3, patch_artist=True, showfliers = False)
# fsplot = ax.boxplot(dataFSP, positions=x + 0.17, widths=0.3, patch_artist=True, showfliers=False)
#
# for patch in fdplot['boxes']:
#     patch.set_facecolor(colors[0])
# for patch in fsplot['boxes']:
#     patch.set_facecolor(colors[1])
#
# ax.legend([fdplot["boxes"][0], fsplot["boxes"][0]], ['$\Delta FDP$', '$\Delta FSP$'])
# plt.xticks(x, name_MNO[:-1])
# # plt.yticks([0.0, 0.25, 0.50, 0.75, 1.0])
# plt.ylabel('Difference with national roaming')
# plt.savefig('Figures/municipality_difference.png', dpi=1000)
# plt.show()