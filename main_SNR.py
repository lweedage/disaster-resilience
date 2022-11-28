import matplotlib.pyplot as plt
import geopandas as gpd
import find_base_stations as antenna
import generate_users
import models
import objects.Params as p
from shapely.errors import ShapelyDeprecationWarning
import warnings
import statsmodels.api as sm
import matplotlib.pylab as pylab
import util
import numpy as np
import seaborn as sns
import pandas as pd
from shapely.ops import unary_union


params = {'legend.fontsize': 'x-large',
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large',
        'lines.markersize': 8}#,
          # 'figure.autolayout': True}
pylab.rcParams.update(params)

markers = ['o', 'X', 'v', 's', '*', 'P', '1', '+']

warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)

municipalities = ['Enschede']
name_MNOs = ['MNO-1', 'MNO-2', 'MNO-3', 'National roaming']
MNOs = [['KPN'], ['T-Mobile'], ['Vodafone'], ['KPN', 'Vodafone', 'T-Mobile']]
i = 0
minimum = 100
random_failure = 0
radius_disaster = 1000

for municipality in municipalities:
    i = 0
    fig, ax = plt.subplots()
    for mno in MNOs:
        print(municipality, mno[0])
        # Retrieve zip code population + area data and make a region with specified zip codes
        # Columns are: aantal_inw (population), stedelijkh (urbanity), postcode (zip code), geometry,
        # popdensity (population density), municipali(city), BSs, scenario
        zip_codes = gpd.read_file('data/zip_codes.shp')

        # Region that we want to investigate:
        # cities = util.find_cities(province)
        cities = [municipality]
        province = None

        percentage = 2
        seed = 1

        delta = 100
        params = p.Parameters(seed, zip_codes, mno, percentage, buffer_size=2000, city_list=cities, province=province, delta=delta, radius_disaster=radius_disaster, random_failure=random_failure)

        params = antenna.find_zip_code_region(params)
        print('Finding users...')
        params = generate_users.generate_users_grid(params, delta)
        print('There are', params.number_of_users, 'users')

        print('Finding BSs...')
        params = antenna.load_bs(params)
        print('There are', params.number_of_bs, 'BSs')

        sinrs = models.find_links_heatmap(params)

        # [xmin, ymin, xmax, ymax] = gpd.GeoSeries(params.zip_code_region['geometry']).total_bounds
        # xmin, xmax = np.floor(xmin), np.ceil(xmax)
        # ymin, ymax = np.floor(ymin), np.ceil(ymax)
        # xdelta, ydelta = int(xmax - xmin), int(ymax - ymin)
        #
        # fig, ax = plt.subplots()
        # data1 = pd.DataFrame(data={'x': params.y_user, 'y': params.x_user, 'z': sinrs})
        # data = data1.pivot(index='x', columns='y', values='z')
        # hm = sns.heatmap(data, cmap='magma_r', ax=ax, vmin = 0, vmax = 80)
        # # circle1 = plt.Circle(((xmax + xmin)/2, (ymax + ymin)/2), 2500, color='r')
        # # print(circle1)
        # # ax.add_patch(circle1)
        # ax.scatter(np.divide(np.subtract(params.xbs, xmin), delta), np.divide(np.subtract(params.ybs, ymin), delta),
        #            s=5, color='g')
        # plt.xticks([])
        # plt.yticks([])
        # plt.savefig(f'Figures/heatmap{params.filename}.png', dpi=400)
        # plt.show()

        data = list(sinrs)
        ecdf = sm.distributions.ECDF(data)
        plt.step(ecdf.x, ecdf.y, label = name_MNOs[i], color = util.get_color(i), alpha = 0.8)

        # add some markers to the ecdf, to give the 25, 50 and 75 percentile
        points = []
        First25, First50, First75 = True, True, True
        First = True
        for j in range(len(ecdf.x)):
            if ecdf.x[j] > 5 and First:
                print(ecdf.y[j]*100)
                First = False
            if ecdf.y[j] > .25 and First25:
                points.append(ecdf.x[j])
                First25 = False
            if ecdf.y[j] > .5 and First50:
                points.append(ecdf.x[j])
                First50 = False
            if ecdf.y[j] > .75 and First75:
                points.append(ecdf.x[j])
                First75 = False

        plt.scatter(points, [0.25, 0.5, 0.75], color = util.get_color(i), alpha = 0.8, marker = markers[i] )
        i += 1

    plt.legend()

    plt.xlim((-10, 100))
    plt.xticks(list(plt.xticks()[0]) + [5])
    plt.xlabel('SINR (dB)')
    plt.ylabel('ECDF')
    plt.vlines(5, 0, 1, color = 'gray', linestyles='dashed')
    plt.savefig(f'Figures/sinr_distribution{params.filename}.pdf', dpi=1000)
    plt.show()