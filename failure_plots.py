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
percentage_MNO = {'Vodafone': 0.16, 'KPN': 0.42, 'T-Mobile': 0.42, 'All': 1}
provinces = ['Drenthe', 'Flevoland', 'Friesland', 'Gelderland', 'Groningen', 'Limburg', 'Noord-Brabant',
             'Noord-Holland', 'Overijssel', 'Utrecht', 'Zeeland', 'Zuid-Holland']
MNOs = ['KPN', 'Vodafone', 'T-Mobile', 'All']
#
normal = pd.read_pickle('Results/Normal.p')
Disaster1000 = pd.read_pickle('Results/Disaster1000.0.p')
Disaster5000 = pd.read_pickle('Results/Disaster5000.0.p')
Disaster10000 = pd.read_pickle('Results/Disaster10000.0.p')
Disaster50000 = pd.read_pickle('Results/Disaster50000.0.p')
Rain2_5 = pd.read_pickle('Results/Rain2.5.p')
Rain25 = pd.read_pickle('Results/Rain25.p')
Rain150 = pd.read_pickle('Results/Rain150.p')
Random01 = pd.read_pickle('Results/Random0.1.p')
Random05 = pd.read_pickle('Results/Random0.5.p')
Random09 = pd.read_pickle('Results/Random0.9.p')

disasters = [Disaster1000, Disaster5000, Disaster10000, Disaster50000, normal]
rain = [Rain2_5, Rain25, Rain150, normal]
random = [Random01, Random05, Random09, normal]

disaster_name = ['1.000km', '5.000km', '10.000km', '50.000km', 'Normal']
rain_name = ['2.5 mm/h', '25 mm/h', '150 mm/h', 'Normal']
random_name = ['$p=0.1$', '$p=0.5$', '$p=0.9$', 'Normal']

zip_codes = gpd.read_file('data/zip_codes_with_scenarios.shp')

MNO = 'KPN'

fig, ax = plt.subplots()
for x, dis in zip(range(len(disasters)), disasters):
    dataFDP = []
    for province in provinces:
        dataFDP.append(dis.loc[(dis['Provider']==MNO) & (dis['Province']==province), 'FDP'])

    plt.scatter(dataFDP, range(len(provinces)), label = disaster_name[x], color=colors[x], marker=markers[x], zorder = 2)

for x in range(len(provinces)):
    plt.plot([0.0, 1], [x, x], ':', color='gray', zorder=1)

plt.xlabel('FDP')
plt.yticks(range(len(provinces)), provinces)
plt.legend(loc='center')
ax.tick_params(top=False,
               bottom=False,
               left=False,
               right=False,
               labelleft=True,
               labelbottom=True)
ax.spines.right.set_visible(False)
ax.spines.top.set_visible(False)
ax.spines.left.set_visible(False)
ax.spines.bottom.set_visible(False)
plt.savefig(f'Figures/FDP{MNO}_disasters.png')
plt.show()

fig, ax = plt.subplots()
for x, dis in zip(range(len(disasters)), disasters):
    dataFSP = []
    for province in provinces:
        dataFSP.append(dis.loc[(dis['Provider']==MNO) & (dis['Province']==province), 'FSP'])

    plt.scatter(dataFSP, range(len(provinces)), label = disaster_name[x], color=colors[x], marker=markers[x], zorder = 2)

for x in range(len(provinces)):
    plt.plot([0.0, 1], [x, x], ':', color='gray', zorder=1)

plt.xlabel('FSP')
plt.yticks(range(len(provinces)), provinces)
plt.legend(loc='center')
ax.tick_params(top=False,
               bottom=False,
               left=False,
               right=False,
               labelleft=True,
               labelbottom=True)
ax.spines.right.set_visible(False)
ax.spines.top.set_visible(False)
ax.spines.left.set_visible(False)
ax.spines.bottom.set_visible(False)
plt.savefig(f'Figures/FSP{MNO}_disasters.png')
plt.show()

fig, ax = plt.subplots()
for x, dis in zip(range(len(rain)), rain):
    dataFDP = []
    for province in provinces:
        dataFDP.append(dis.loc[(dis['Provider']==MNO) & (dis['Province']==province), 'FDP'])

    plt.scatter(dataFDP, range(len(provinces)), label = rain_name[x], color=colors[x], marker=markers[x], zorder = 2)

for x in range(len(provinces)):
    plt.plot([0.0, 0.2], [x, x], ':', color='gray', zorder=1)

plt.xlabel('FDP')
plt.yticks(range(len(provinces)), provinces)
plt.legend(loc='center right')
ax.tick_params(top=False,
               bottom=False,
               left=False,
               right=False,
               labelleft=True,
               labelbottom=True)
ax.spines.right.set_visible(False)
ax.spines.top.set_visible(False)
ax.spines.left.set_visible(False)
ax.spines.bottom.set_visible(False)
plt.savefig(f'Figures/FDP{MNO}_rain.png')
plt.show()

fig, ax = plt.subplots()
for x, dis in zip(range(len(rain)), rain):
    dataFSP = []
    for province in provinces:
        dataFSP.append(dis.loc[(dis['Provider']==MNO) & (dis['Province']==province), 'FSP'])

    plt.scatter(dataFSP, range(len(provinces)), label = rain_name[x], color=colors[x], marker=markers[x], zorder = 2)

for x in range(len(provinces)):
    plt.plot([0.8, 1], [x, x], ':', color='gray', zorder=1)

plt.xlabel('FSP')
plt.yticks(range(len(provinces)), provinces)
plt.legend(loc='center left')
ax.tick_params(top=False,
               bottom=False,
               left=False,
               right=False,
               labelleft=True,
               labelbottom=True)
ax.spines.right.set_visible(False)
ax.spines.top.set_visible(False)
ax.spines.left.set_visible(False)
ax.spines.bottom.set_visible(False)
plt.savefig(f'Figures/FSP{MNO}_rain.png')
plt.show()

fig, ax = plt.subplots()
for x, dis in zip(range(len(random)), random):
    dataFDP = []
    for province in provinces:
        dataFDP.append(dis.loc[(dis['Provider']==MNO) & (dis['Province']==province), 'FDP'])

    plt.scatter(dataFDP, range(len(provinces)), label = random_name[x], color=colors[x], marker=markers[x], zorder = 2)

for x in range(len(provinces)):
    plt.plot([0.0, 0.5], [x, x], ':', color='gray', zorder=1)

plt.xlabel('FDP')
plt.yticks(range(len(provinces)), provinces)
plt.legend(loc='center right')
ax.tick_params(top=False,
               bottom=False,
               left=False,
               right=False,
               labelleft=True,
               labelbottom=True)
ax.spines.right.set_visible(False)
ax.spines.top.set_visible(False)
ax.spines.left.set_visible(False)
ax.spines.bottom.set_visible(False)
plt.savefig(f'Figures/FDP{MNO}_random.png')
plt.show()

fig, ax = plt.subplots()
for x, dis in zip(range(len(random)), random):
    dataFSP = []
    for province in provinces:
        dataFSP.append(dis.loc[(dis['Provider']==MNO) & (dis['Province']==province), 'FSP'])

    plt.scatter(dataFSP, range(len(provinces)), label = random_name[x], color=colors[x], marker=markers[x], zorder = 2)

for x in range(len(provinces)):
    plt.plot([0.0, 1], [x, x], ':', color='gray', zorder=1)

plt.xlabel('FSP')
plt.yticks(range(len(provinces)), provinces)
plt.legend(loc='center left')
ax.tick_params(top=False,
               bottom=False,
               left=False,
               right=False,
               labelleft=True,
               labelbottom=True)
ax.spines.right.set_visible(False)
ax.spines.top.set_visible(False)
ax.spines.left.set_visible(False)
ax.spines.bottom.set_visible(False)
plt.savefig(f'Figures/FSP{MNO}_random.png')
plt.show()


