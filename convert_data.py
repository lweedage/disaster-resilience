import csv
import pickle
import matplotlib.pyplot as plt
import pandas as pd
import shapely.geometry
from shapely.geometry import MultiPolygon
from shapely.ops import transform
import scipy
import geopandas as gpd
import pyproj
from shapely.ops import unary_union
from shapely.geometry import Point
import matplotlib
import numpy as np
import pylab

# matplotlib.use('TkAgg')

params = {'legend.fontsize': 'x-large',
          'axes.labelsize': 'x-large',
          'axes.titlesize': 'x-large',
          'xtick.labelsize': 'x-large',
          'ytick.labelsize': 'x-large',
          'lines.markersize': 8}  # ,
# 'figure.autolayout': True}
pylab.rcParams.update(params)

colors = ['#904C77', '#E49AB0', '#ECB8A5', '#96ACB7', '#957D95'] * 100

transformer = pyproj.Transformer.from_proj(pyproj.Proj(init="epsg:28992"), pyproj.Proj(init="epsg:4326"))

percentage = 2
max_iterations = 100

disaster = False
user_increase = False
random_failure = False

radius_disaster = 100  # 100, 500, 1000, 2500
percentage_increase = 200  # 50, 100, 200
random_p = 0.5  # 0.05, 0.1, 0.25, 0.5

mnos = ['KPN', 'T-Mobile', 'Vodafone', 'all_MNOs']
providers = ['MNO-1', 'MNO-2', 'MNO-3', 'National roaming']
mnos = ['all_MNOs']


areas = ['Drenthe', 'Flevoland', 'Friesland', 'Gelderland', 'Groningen', 'Limburg', 'Noord-Brabant', 'Noord-Holland',
         'Overijssel', 'Utrecht', 'Zeeland', 'Zuid-Holland']
provinces = ['Drenthe', 'Flevoland', 'Friesland', 'Gelderland', 'Groningen', 'Limburg', 'Noord-Brabant',
             'Noord-Holland', 'Overijssel', 'Utrecht', 'Zeeland', 'Zuid-Holland']

# areas = ['Noord-Holland']
# provinces = areas

data_figureFSP = dict()
data_figureFDP = dict()
# for MNO in mnos:
#     df = gpd.GeoDataFrame(columns=['area', 'FSP', 'FDP'])
#     df['area'] = areas
#     geom = []
#     for area in areas:
#         print(area)
#         region = pickle.load(open(f'data/Regions/{area}region.p', 'rb'))
#         region = region.geometry.values
#         region = transform(transformer.transform, region[0])
#         geom.append(region)
#
#         if MNO == 'all_MNOs':
#             share = 1
#         else:
#             share = 0.33
#
#         # --- add FSP and FDP ---
#         filename = f'{area}{MNO}{percentage}{share}'
#         if disaster:
#             filename += 'disaster' + str(radius_disaster)
#         elif user_increase:
#             filename += 'user_increase' + str(percentage_increase)
#         elif random_failure:
#             filename += 'random' + str(random_p)
#
#         filename += str(max_iterations)
#
#         fsp = pickle.load(open(f'data/Realisations/{filename}_totalfsp.p', 'rb'))
#         fdp = pickle.load(open(f'data/Realisations/{filename}_totalfdp.p', 'rb'))
#
#         print(max(fsp), max(fdp))
#
#         fsp = sum(fsp) / len(fsp)
#         fdp = sum(fdp) / len(fdp)
#
#         condition = df['area'] == area
#         df.loc[condition, 'FSP'] = fsp
#         df.loc[condition, 'FDP'] = fdp
#
#     df = df.set_geometry(geom)
#
#     filename = f'{MNO}'
#     if disaster:
#         filename += 'disaster' + str(radius_disaster)
#     elif user_increase:
#         filename += 'user_increase' + str(percentage_increase)
#     elif random_failure:
#         filename += 'random' + str(random_p)
#     df.to_file(f'converted_data/{filename}_provinces.shp')
#     data_figureFSP[MNO] = df['FSP'].tolist()
#     data_figureFDP[MNO] = df['FDP'].tolist()
#
# boxplot_data = data_figureFSP.values()
#
# fig, ax = plt.subplots()
# bplot = plt.boxplot(boxplot_data, patch_artist=True, showfliers=False)
# for patch, color in zip(bplot['boxes'], colors[:4]):
#     patch.set_facecolor(color)
# plt.xticks(np.arange(1, 5), providers)
# plt.ylabel('FSP')
# if disaster:
#     plt.savefig(f'Figures/boxplotFSPprovincesdisaster{radius_disaster}.png', dpi=1000)
# elif user_increase:
#     plt.savefig(f'Figures/boxplotFSPprovincesuser_increase{percentage_increase}.png', dpi=1000)
# elif random_failure:
#     plt.savefig(f'Figures/boxplotFSPprovincesrandom{random_p}.png', dpi=1000)
# else:
#     plt.savefig(f'Figures/boxplotFSPprovinces.png', dpi=1000)
# boxplot_data = data_figureFDP.values()
#
# fig, ax = plt.subplots()
# bplot = plt.boxplot(boxplot_data, patch_artist=True, showfliers=False)
# for patch, color in zip(bplot['boxes'], colors[:4]):
#     patch.set_facecolor(color)
# plt.xticks(np.arange(1, 5), providers)
# plt.ylabel('FDP')
# if disaster:
#     plt.savefig(f'Figures/boxplotFDPprovincesdisaster{radius_disaster}.png', dpi=1000)
# elif user_increase:
#     plt.savefig(f'Figures/boxplotFDPprovincesuser_increase{percentage_increase}.png', dpi=1000)
# elif random_failure:
#     plt.savefig(f'Figures/boxplotFDPprovincesrandom{random_p}.png', dpi=1000)
# else:
#     plt.savefig(f'Figures/boxplotFDPprovinces.png', dpi=1000)


# --- municipality level ----
def find_municipalities(province):
    with open("data/cities_per_province") as f:
        data = f.read()
        data = data.split('\n')
    if province == 'Netherlands':
        print(province)
        cities = []
        for line in data:
            line = line.split(':')
            for city in line[1].split(','):
                cities.append(city)
        return cities
    else:
        for line in data:
            line = line.split(':')
            if line[0] == province:
                return line[1].split(',')


zip_codes = gpd.read_file('data/zip_codes.shp')

data_figureFSP = dict()
data_figureFDP = dict()
for MNO in mnos:
    if MNO == 'all_MNOs':
        share = 1
    else:
        share = 0.33

    df = pd.DataFrame(columns=['area', 'FSP', 'FDP'])

    areas = []

    for i in provinces:
        for x in find_municipalities(i):
            areas.append(x)

    df['area'] = areas  # find_municipalities('Netherlands')

    geom = []

    for province in provinces:
        areas = find_municipalities(province)
        print(MNO, province)
        for area in areas:
            print(area)
            FSP, FDP = [], []
            zip_code_region_data = zip_codes[zip_codes['municipali'].isin([area])]
            region = gpd.GeoSeries(unary_union(zip_code_region_data['geometry'].buffer(50)))
            region = region.simplify(tolerance=200)
            region = region.geometry.values
            region = transform(transformer.transform, region[0])
            # df[df['area'] == area].set_geometry(gpd.GeoSeries(region))
            geom.append(region)

            for seed in range(max_iterations):
                # --- add FSP and FDP and capacity to df of users ---
                filename = f'{province}{MNO}{percentage}{share}'
                if disaster:
                    filename += 'disaster' + str(radius_disaster)
                elif user_increase:
                    filename += 'user_increase' + str(percentage_increase)
                elif random_failure:
                    filename += 'random' + str(random_p)
                filename += str(seed)

                fsp = pickle.load(open(f'data/Realisations/{filename}_FSP.p', 'rb'))
                fdp = pickle.load(open(f'data/Realisations/{filename}_FDP.p', 'rb'))

                xs = pickle.load(open(f'data/users/{province}{MNO}{percentage}{share}{seed}_xs.p', 'rb'))
                ys = pickle.load(open(f'data/users/{province}{MNO}{percentage}{share}{seed}_ys.p', 'rb'))

                x, y = transformer.transform(xs, ys)
                for i in range(len(x)):
                    user = Point(x[i], y[i])
                    if region.buffer(0).contains(user):
                        FSP.append(fsp[i])
                        FDP.append(fdp[i])

            condition = df['area'] == area
            df.loc[condition, 'FSP'] = sum(FSP) / max(1, len(FSP))
            df.loc[condition, 'FDP'] = sum(FDP) / max(1, len(FDP))
        data_figureFSP[MNO] = df['FSP'].tolist()
        data_figureFDP[MNO] = df['FDP'].tolist()

    filename = MNO
    if disaster:
        filename += 'disaster' + str(radius_disaster)
    elif user_increase:
        filename += 'user_increase' + str(percentage_increase)
    elif random_failure:
        filename += 'random' + str(random_p)

    df.to_pickle(f'converted_data/{filename}_municipalities.p')

boxplot_data = data_figureFSP.values()

fig, ax = plt.subplots()
bplot = plt.boxplot(boxplot_data, patch_artist=True, showfliers=False)
for patch, color in zip(bplot['boxes'], colors[:3]):
    patch.set_facecolor(color)
plt.xticks(np.arange(1, 5), providers)
plt.ylabel('FSP')

if disaster:
    plt.savefig(f'Figures/FSPmunicipalitiesdisaster{radius_disaster}.png', dpi=1000)
elif user_increase:
    plt.savefig(f'Figures/FSPmunicipalitiesuser_increase{percentage_increase}.png', dpi=1000)
elif random_failure:
    plt.savefig(f'Figures/FSPmunicipalitiesrandom{random_p}.png', dpi=1000)
else:
    plt.savefig(f'Figures/FSPmunicipalities.png', dpi=1000)

boxplot_data = data_figureFDP.values()

fig, ax = plt.subplots()
bplot = plt.boxplot(boxplot_data, patch_artist=True, showfliers=False)
for patch, color in zip(bplot['boxes'], colors[:3]):
    patch.set_facecolor(color)
plt.xticks(np.arange(1, 5), providers)
plt.ylabel('FDP')

if disaster:
    plt.savefig(f'Figures/FDPmunicipalitiesdisaster{radius_disaster}.png', dpi=1000)
elif user_increase:
    plt.savefig(f'Figures/FDPmunicipalitiesuser_increase{percentage_increase}.png', dpi=1000)
elif random_failure:
    plt.savefig(f'Figures/FDPmunicipalitiesrandom{random_p}.png', dpi=1000)
else:
    plt.savefig(f'Figures/FDPmunicipalities.png', dpi=1000)
