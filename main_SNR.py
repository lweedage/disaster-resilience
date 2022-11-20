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

municipalities = ['Enschede', 'Amsterdam']
name_MNOs = ['MNO-1', 'MNO-2', 'MNO-3', 'National roaming']
i = 0
minimum = 100
random_failure = 0.5
radius_disaster = 0

for municipality in municipalities:
    i = 0
    fig, ax = plt.subplots()
    for mno in [['KPN'], ['T-Mobile'], ['Vodafone'], ['Vodafone', 'KPN', 'T-Mobile']]:
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

        delta = 50
        params = p.Parameters(seed, zip_codes, mno, percentage, buffer_size=2000, city_list=cities, province=province, delta=delta, radius_disaster=radius_disaster, random_failure=random_failure)

        params = antenna.find_zip_code_region(params)
        print('Finding users...')
        params = generate_users.generate_users_grid(params, delta)
        print('There are', params.number_of_users, 'users')

        print('Finding BSs...')
        params = antenna.load_bs(params)
        print('There are', params.number_of_bs, 'BSs')

        sinrs = models.find_links_heatmap(params)

        data = list(sinrs)
        minimum = min(min(sinrs), minimum)

        ecdf = sm.distributions.ECDF(data)
        plt.step(ecdf.x, ecdf.y, label = name_MNOs[i], color = util.get_color(i), alpha = 0.8)

        # add some markers to the ecdf, to give the 25, 50 and 75 percentile
        points = []
        First25, First50, First75 = True, True, True
        First = True
        for j in range(len(ecdf.x)):
            if ecdf.x[j] > 5 and First:
                print(ecdf.y[j])
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

    plt.xticks(list(plt.xticks()[0]) + [5])
    if minimum == -100:
        plt.xlim((-10, 100))
    plt.xlabel('SINR (dB)')
    plt.ylabel('ECDF')
    plt.vlines(5, 0, 1, color = 'gray', linestyles='dashed')
    plt.savefig(f'Figures/sinr_distribution{params.filename}.png', dpi=1000)
    plt.show()