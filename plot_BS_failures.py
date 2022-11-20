import geopandas as gpd
import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
from shapely.geometry import Point
from shapely.ops import cascaded_union

import util

colors = ['#904C77', '#E49AB0', '#ECB8A5', '#96ACB7', '#957D95'] * 100

params = {'legend.fontsize': 'x-large',
          'axes.labelsize': 'x-large',
          'axes.titlesize': 'x-large',
          'xtick.labelsize': 'x-large',
          'ytick.labelsize': 'x-large',
          'lines.markersize': 8,
          'figure.autolayout': True}
pylab.rcParams.update(params)

data = []
color = {'KPN': 0, 'T-Mobile': 1, 'Vodafone': 2, 'all_MNOs': 3}
for MNO in ['KPN', 'T-Mobile', 'Vodafone']:
    filename = f'Enschede{MNO}20.33'

    seed = 1
    print(filename)

    xbs = util.from_data(f'data/BSs/Enschede{MNO}_xs.p')
    ybs = util.from_data(f'data/BSs/Enschede{MNO}_ys.p')
    region = util.from_data(f'data/Regions/Enschederegion.p')

    x_user = util.from_data(f'data/users/{filename}1_xs.p')
    y_user = util.from_data(f'data/users/{filename}1_ys.p')

    indices = list()
    xs, ys =  [], []

    for bs in range(len(xbs)):
        point = Point(xbs[bs], ybs[bs])
        if region[0].contains(point):
            indices.append(bs)
            xs.append(xbs[bs])
            ys.append(ybs[bs])

    fig, ax = plt.subplots()
    region2 = gpd.GeoSeries(cascaded_union(region[0].buffer(100)))
    region2.plot(color='None', ax=ax)

    sc = ax.scatter(xs, ys, marker="2", s = 150, color=util.get_color(color[MNO]))
    ax.tick_params(top=False,
                   bottom=False,
                   left=False,
                   right=False,
                   labelleft=False,
                   labelbottom=False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    plt.savefig(f'Figures/Enschede{MNO}_BSs.png', dpi=500)
    plt.show()



# for measure in ['FDP', 'FSP']:
#     fig, ax = plt.subplots()
#     data = []
#     color = {'KPN': 0, 'T-Mobile': 1, 'Vodafone': 2, 'all_MNOs': 3}
#     for MNO in ['KPN', 'T-Mobile', 'Vodafone', 'all_MNOs']:
#         if MNO == 'all_MNOs':
#             filename = f'Enschede{MNO}21'
#         else:
#             filename = f'Enschede{MNO}20.33'
#
#         if measure == 'FDP':
#             fdp_all = util.from_data(f'data/BSfailures/failed_fdp_{filename}geographic_failure.p')
#         else:
#             fdp_all = util.from_data(f'data/BSfailures/failed_fsp_{filename}geographic_failure.p')
#
#         seed = 1
#         number_of_bs = len(fdp_all)
#
#         xbs = util.from_data(f'data/BSs/Enschede{MNO}_xs.p')
#         ybs = util.from_data(f'data/BSs/Enschede{MNO}_ys.p')
#         region = util.from_data(f'data/Regions/Enschederegion.p')
#
#         x_user = util.from_data(f'data/users/{filename}1_xs.p')
#         y_user = util.from_data(f'data/users/{filename}1_ys.p')
#
#         indices = list()
#         xs, ys, fdp, fsp = [], [], [], []
#
#         for bs in range(len(xbs)):
#             point = Point(xbs[bs], ybs[bs])
#             if region[0].contains(point):
#                 indices.append(bs)
#                 fdp.append(fdp_all[bs])
#
#
#         data.append(fdp)
#     data = [d[0] for v, d in data.items()]
#     print(data)
#
#     fsplot = ax.boxplot(data, patch_artist = True)
#
#     i = 0
#     for patch in fsplot['boxes']:
#         patch.set_facecolor(util.get_boxplot_color(i))
#         i += 1
#
#     plt.ylabel(f'$\Delta${measure}')
#
#     plt.xticks([1, 2, 3, 4], ['MNO-1', 'MNO-2', 'MNO-3', 'National roaming'])
#     plt.savefig(f'Figures/{measure}_improvement.png')
#     plt.show()
