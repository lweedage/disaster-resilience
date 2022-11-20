import shapely.ops

import util
import geopandas as gpd
from shapely.ops import unary_union
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import cm

norm = matplotlib.colors.Normalize(vmin=0, vmax=1)

# colormap possible values = viridis, jet, spectral
fig, ax = plt.subplots()

city_name = 'Overijssel'
# cities = [city_name]
# for municipality in ['Almere', 'Amsterdam', 'Enschede', "'s-Gravenhage", 'Elburg', 'Emmen', 'Groningen', 'Maastricht',
#                   'Eindhoven', 'Middelburg']:

provinces = ['Drenthe', 'Flevoland', 'Friesland', 'Gelderland', 'Groningen', 'Limburg', 'Noord-Brabant',
             'Noord-Holland', 'Overijssel', 'Utrecht', 'Zeeland', 'Zuid-Holland']

# for province in ['Groningen']:
#     cities = util.find_cities(province)
#     # city_name = municipality
#     # cities = [municipality]
#     city_name = province
#     filename_noMNO = f'{city_name}'
#
#     zip_codes = gpd.read_file('/home/lotte/PycharmProjects/Disaster Resilience/data/zip_codes.shp')
#
#     zip_code_region_data = zip_codes[zip_codes['municipali'].isin(cities)]
#     # zip_code_region_data = zip_codes[zip_codes['postcode'].isin([zip_code])]
#
#     region = gpd.GeoSeries(shapely.ops.unary_union(zip_code_region_data['geometry'].buffer(50)))
#     region = region.simplify(tolerance=200)
#     region.plot()
#     plt.show()
#     # util.to_data(region, f'/home/lotte/PycharmProjects/Disaster Resilience/data/Regions/{filename_noMNO}region.p')
#
#     print(province, region.area*1e-6)
#     for MNO in ['KPN', 'T-Mobile', 'Vodafone']:
#         bs = util.from_data(f'data/BSs/{province}{MNO}_xs.p')
#         print(MNO, len(bs))
#
#     users = util.from_data(f'data/users/{province}{MNO}20.330_xs.p')
#     print('users=', len(users))
#     print('urb=', sum(zip_code_region_data['stedelijkh'].astype('int'))/len(zip_code_region_data['stedelijkh']))
fig, ax = plt.subplots()
zip_codes = gpd.read_file('/home/lotte/PycharmProjects/Disaster Resilience/data/zip_codes.shp')
zip_codes.plot(column = 'aantal_inw', ax = ax, cmap = 'viridis')
fig.set_size_inches((12,10))
ax.set_axis_off()
plt.savefig('the_netherlands.png', dpi=1000, transparent=True)

mnos = ['KPN', 'T-Mobile', 'Vodafone']

colors = {'KPN': '#00c300', 'T-Mobile': '#e20074', 'Vodafone': '#e93f3f'}
fig, ax = plt.subplots()

nederland = gpd.GeoSeries(unary_union(zip_codes.geometry))
nederland.plot(ax=ax, color = 'white')

for province in provinces:
    for mno in mnos:
        filename = f'{province}{mno}'
        x, y = util.from_data(f'data/BSs/{filename}_xs.p'), util.from_data(f'data/BSs/{filename}_ys.p')
        plt.scatter(x, y, color = colors[mno], marker = '2', s = 1)
ax.set_axis_off()
plt.savefig('BSSthe_netherlands.png', dpi=1000, transparent=True)

