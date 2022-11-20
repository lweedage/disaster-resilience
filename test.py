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
percentage_MNO = {'Vodafone': 1/3, 'KPN': 1/3, 'T-Mobile': 1/3, 'all_MNOs': 1}

fig, ax = plt.subplots()
cities = ['Almelo', 'Borne', 'Enschede', 'Hengelo', 'Losser', 'Rijssen-Holten', 'Zwolle']

MNO = 'KPN'

j = 0
i = 0
city = 'Enschede'

FSP = dict()
FSPdis = dict()
fsp = util.from_data(f'data/Realisations/FSP_per_region{city}{MNO}3{percentage_MNO[MNO]}.p')
fspdis = util.from_data(f'data/Realisations/FSP_per_region{city}{MNO}3{percentage_MNO[MNO]}disaster2500.0.p')

zipcodes = fsp.keys()
for k, v in fsp.items():
    FSP[k] = sum(v)/len(v)

for k, v in fspdis.items():
    FSPdis[k] = sum(v)/len(v)

plt.scatter(FSP.values(), range(len(zipcodes)), label='Normal', color=colors[0], marker=markers[0], zorder=2)
plt.scatter(FSPdis.values(), range(len(zipcodes)), label='With disaster', color=colors[1], marker=markers[1], zorder=2)

for j in range(len(zipcodes)):
    plt.plot([0.0, 1.01], [j, j], ':', color='gray', zorder=1)


plt.xlabel('Satisfaction')
plt.yticks(range(len(zipcodes)), zipcodes)
plt.legend(loc='upper left')
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
plt.savefig(f'Figures/FSP_per_regionEnschede{MNO}_withdisaster.png')
plt.show()

fig, ax = plt.subplots()
cities = ['Almelo', 'Borne', 'Enschede', 'Hengelo', 'Losser', 'Rijssen-Holten', 'Zwolle']

MNO = 'KPN'

j = 0
i = 0
city = 'Enschede'

FDP = dict()
FDPdis = dict()
fsp = util.from_data(f'data/Realisations/FDP_per_region{city}{MNO}3{percentage_MNO[MNO]}.p')
fspdis = util.from_data(f'data/Realisations/FDP_per_region{city}{MNO}3{percentage_MNO[MNO]}disaster2500.0.p')

zipcodes = fsp.keys()
for k, v in fsp.items():
    FDP[k] = sum(v)/len(v)

for k, v in fspdis.items():
    FDPdis[k] = sum(v)/len(v)

plt.scatter(FDP.values(), range(len(zipcodes)), label='Normal', color=colors[0], marker=markers[0], zorder=2)
plt.scatter(FDPdis.values(), range(len(zipcodes)), label='With disaster', color=colors[1], marker=markers[1], zorder=2)

for j in range(len(zipcodes)):
    plt.plot([0.0, 0.9], [j, j], ':', color='gray', zorder=1)


plt.xlabel('Disconnected users')
plt.yticks(range(len(zipcodes)), zipcodes)
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
plt.savefig(f'Figures/FDP_per_regionEnschede{MNO}_withdisaster.png')
plt.show()

