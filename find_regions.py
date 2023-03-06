import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt
from shapely.ops import unary_union

import util

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
zip_codes = gpd.read_file('/home/lotte/PycharmProjects/Disaster Resilience/data/zip_codes.shp')

# fig, ax = plt.subplots()
# zip_codes.plot(column='aantal_inw', ax=ax, cmap='plasma')
# fig.set_size_inches((20, 24))
# ax.set_axis_off()
# plt.savefig('the_netherlands.png', dpi=500, transparent=True)

mnos = ['KPN', 'T-Mobile', 'Vodafone']

fig, ax = plt.subplots()

markers = ['o', '^', 's']
nederland = gpd.GeoSeries(unary_union(zip_codes.geometry))
nederland.plot(ax=ax, color='yellow', alpha=0.1)
colors = {'KPN': '#00c300', 'T-Mobile': '#e20074', 'Vodafone': '#e93f3f'}

for province in provinces:
    i = 0
    for mno in mnos:
        filename = f'{province}{mno}'
        x, y = util.from_data(f'data/BSs/{filename}_xs.p'), util.from_data(f'data/BSs/{filename}_ys.p')
        plt.scatter(x, y, color=colors[mno], marker=markers[i], s=2)
        i += 1
ax.set_axis_off()
fig.set_size_inches((24, 20))
plt.savefig('BSSthe_netherlands.png', dpi=500, transparent=True)
plt.show()
