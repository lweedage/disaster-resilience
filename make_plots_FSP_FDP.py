import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import pandas as pd
import geopandas as gpd
from shapely import wkt
from shapely.ops import unary_union

import util

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
# provinces = ['Drenthe', 'Flevoland', 'Friesland', 'Gelderland', 'Groningen', 'Limburg', 'Noord-Brabant',
#              'Noord-Holland', 'Overijssel', 'Utrecht', 'Zeeland', 'Zuid-Holland']
MNOs = ['KPN', 'Vodafone', 'T-Mobile', 'all_MNOs']
#
# results = pd.read_pickle('Results/Normal.p')
#
# FSP, FDP, SAT, DEG = {MNO: [] for MNO in MNOs}, {MNO: [] for MNO in MNOs}, {MNO: [] for MNO in MNOs}, {MNO: [] for MNO
#                                                                                                        in MNOs}
#
# for province in provinces:
#     for MNO in MNOs:
#         FSP[MNO].append(results[(results['Provider'] == MNO) & (results['Province'] == province)]['FSP'].tolist()[0])
#         FDP[MNO].append(results[(results['Provider'] == MNO) & (results['Province'] == province)]['FDP'].tolist()[0])
#         SAT[MNO].append(
#             results[(results['Provider'] == MNO) & (results['Province'] == province)]['Satisfaction'].tolist()[0])
#         DEG[MNO].append(
#             results[(results['Provider'] == MNO) & (results['Province'] == province)]['Degree BS'].tolist()[0])
#
# fig, ax = plt.subplots()
# for x in range(len(provinces)):
#     plt.plot([0.7, 1.01], [x, x], ':', color='gray', zorder=1)
#
# for i, MNO in zip(range(len(MNOs)), MNOs):
#     plt.scatter(FSP[MNO], range(len(provinces)), label=MNO, color=colors[i], marker=markers[i])
# plt.xlabel('FSP')
# plt.yticks(range(len(provinces)), provinces)
# plt.legend(loc='center left')
# ax.tick_params(top=False,
#                bottom=False,
#                left=False,
#                right=False,
#                labelleft=True,
#                labelbottom=True)
# ax.spines.right.set_visible(False)
# ax.spines.top.set_visible(False)
# ax.spines.left.set_visible(False)
# ax.spines.bottom.set_visible(False)
# plt.savefig('Figures/FSP.png')
# plt.show()
#
# fig, ax = plt.subplots()
# for x in range(len(provinces)):
#     plt.plot([0, 0.15], [x, x], ':', color='gray', zorder=1)
# for i, MNO in zip(range(len(MNOs)), MNOs):
#     plt.scatter(FDP[MNO], range(len(provinces)), label=MNO, color=colors[i], marker=markers[i])
# plt.xlabel('FDP')
# plt.yticks(range(len(provinces)), provinces)
# plt.legend(loc='center right')
# ax.tick_params(top=False,
#                bottom=False,
#                left=False,
#                right=False,
#                labelleft=True,
#                labelbottom=True)
# ax.spines.right.set_visible(False)
# ax.spines.top.set_visible(False)
# ax.spines.left.set_visible(False)
# ax.spines.bottom.set_visible(False)
# plt.savefig('Figures/FDP.png')
# plt.show()

# zip_codes = gpd.read_file('data/zip_codes_with_scenarios.shp')
#
# provinces = ['Drenthe', 'Flevoland', 'Friesland', 'Gelderland', 'Groningen', 'Limburg', 'Noord-Brabant',
#              'Noord-Holland', 'Overijssel', 'Utrecht', 'Zeeland', 'Zuid-Holland']
#
# MNO = 'T-Mobile'
# percentage_MNO = 0.42
#
# fdp, fsp, geom = [], [], []
# df = gpd.GeoDataFrame()
#
# for province in provinces:
#     FDP = util.from_data(f'data/Realisations/{province}{MNO}2{percentage_MNO}1_FDP.p')
#     FSP = util.from_data(f'data/Realisations/{province}{MNO}2{percentage_MNO}1_FSP.p')
#     fdp.append(sum(FDP) / len(FDP))
#     fsp.append(sum(FSP) / len(FSP))
#     cities = util.find_cities(province)
#     zip_codes.loc[zip_codes['municipali'].isin(cities), ['FDP']] = sum(FDP) / len(FDP)
#     zip_codes.loc[zip_codes['municipali'].isin(cities), ['FSP']] = sum(FSP) / len(FSP)
#
# fig, ax = plt.subplots(1, 2)
# zip_codes.plot(column='FDP', legend=False, cmap='magma_r', ax=ax[0], vmin=0, vmax=1)
# zip_codes.plot(column='FSP', legend=True, cmap='magma_r', ax=ax[1], vmin=0, vmax=1)
# ax[0].set_axis_off()
# ax[1].set_axis_off()
#
# plt.savefig(f'Figures/{MNO}_Netherlands_FDPFSP.png')
# plt.show()

province = 'Overijssel'
percentage_MNO = {'Vodafone': 0.16, 'KPN': 0.42, 'T-Mobile': 0.42, 'all_MNOs': 1}
percentage_MNO = {'Vodafone': 1/3, 'KPN': 1/3, 'T-Mobile': 1/3, 'all_MNOs': 1}

fig, ax = plt.subplots()

for x, MNO in zip(range(4), MNOs):
    print(MNO, x)
    FDP = util.from_data(f'data/Realisations/FDP_per_region{province}{MNO}3{percentage_MNO[MNO]}.p')
    zipcodes = FDP.keys()
    municipality_dict = util.municipality_dict()

    FDP_city = dict()

    cities = util.find_cities(province)
    j = 0
    cities = ['Almelo', 'Borne', 'Enschede', 'Hengelo', 'Losser', 'Rijssen-Holten', 'Zwolle']
    for city in cities:
        FDP_city[city] = []
        plt.plot([0, 0.21], [j, j], ':', color='gray', zorder=1)
        j += 1
        for zipcode in municipality_dict[city]:
            for i in FDP[zipcode]:
                FDP_city[city].append(i)
        FDP_city[city] = sum(FDP_city[city]) / len(FDP_city[city])
    plt.scatter(FDP_city.values(), range(len(cities)), label = MNO, color=colors[x], marker=markers[x])

plt.xlabel('Disconnected users')
plt.yticks(range(len(cities)), cities)
plt.legend(loc='center left')
ax.tick_params(top=False,
               bottom=False,
               left=False,
               right=False,
               labelleft=True,
               labelbottom=True)
# ax.spines.right.set_visible(False)
# ax.spines.top.set_visible(False)
# ax.spines.left.set_visible(False)
# ax.spines.bottom.set_visible(False)
plt.savefig(f'Figures/FDP_per_region{province}.png')
plt.show()

fig, ax = plt.subplots()
for x, MNO in zip(range(4), MNOs):
    print(MNO, x)
    FSP = util.from_data(f'data/Realisations/FSP_per_region{province}{MNO}3{percentage_MNO[MNO]}.p')

    zipcodes = FSP.keys()
    municipality_dict = util.municipality_dict()

    FSP_city = dict()

    cities = util.find_cities(province)
    j = 0
    cities = ['Almelo', 'Borne', 'Enschede', 'Hengelo', 'Losser', 'Rijssen-Holten', 'Zwolle']
    for city in cities:
        FSP_city[city] = []
        plt.plot([0.55, 1.01], [j, j], ':', color='gray', zorder=1)
        j += 1
        for zipcode in municipality_dict[city]:
            for i in FSP[zipcode]:
                FSP_city[city].append(i)
        FSP_city[city] = sum(FSP_city[city]) / len(FSP_city[city])
    plt.scatter(FSP_city.values(), range(len(cities)), label = MNO, color=colors[x], marker=markers[x], zorder = 2)

plt.xlabel('Satisfaction')
plt.yticks(range(len(cities)), cities)
plt.legend(loc='upper right')
ax.tick_params(top=False,
               bottom=False,
               left=False,
               right=False,
               labelleft=True,
               labelbottom=True)
# ax.spines.right.set_visible(False)
# ax.spines.top.set_visible(False)
# ax.spines.left.set_visible(False)
# ax.spines.bottom.set_visible(False)
plt.savefig(f'Figures/FSP_per_region{province}.png')
plt.show()

