import find_base_stations as antenna
import geopandas as gpd
import matplotlib.pyplot as plt

import util


def average(data):
    if len(data) > 0:
        return (sum(data) / len(data))
    else:
        return None


zip_codes = gpd.read_file('data/zip_codes.shp')
# zip_codes['BS_density'] = zip_codes['BSs']/zip_codes['geometry'].area

# municipality = 'Noord-Brabant'  # 'Gelderland', 'Overijssel', 'Noord-Holland', 'Zuid-Holland', 'Groningen', 'Utrecht', 'Limburg', 'Noord-Brabant', 'Friesland', 'Zeeland', 'Flevoland', 'Drenthe'
# cities = util.find_cities(municipality)
cities = ['Assen']
region, zip_codes = antenna.find_zip_code_region(zip_codes, cities)

BS_type = 'BSs'

urb_1 = zip_codes[zip_codes.stedelijkh == str(1)][BS_type] / zip_codes[zip_codes.stedelijkh == str(1)][
    'geometry'].area * 10**(6)
urb_2 = zip_codes[zip_codes.stedelijkh == str(2)][BS_type] / zip_codes[zip_codes.stedelijkh == str(2)][
    'geometry'].area * 10**(6)
urb_3 = zip_codes[zip_codes.stedelijkh == str(3)][BS_type] / zip_codes[zip_codes.stedelijkh == str(3)][
    'geometry'].area * 10**(6)
urb_4 = zip_codes[zip_codes.stedelijkh == str(4)][BS_type] / zip_codes[zip_codes.stedelijkh == str(4)][
    'geometry'].area * 10**(6)
urb_5 = zip_codes[zip_codes.stedelijkh == str(5)][BS_type] / zip_codes[zip_codes.stedelijkh == str(5)][
    'geometry'].area * 10**(6)

# print('Stedelijkheid 1:', '(', min(urb_1), '-', max(urb_1), '), average =', average(urb_1))
print('Stedelijkheid 2:', '(', min(urb_2), '-', max(urb_2), '), average =', average(urb_2))
print('Stedelijkheid 3:', '(', min(urb_3), '-', max(urb_3), '), average =', average(urb_3))
print('Stedelijkheid 4:', '(', min(urb_4), '-', max(urb_4), '), average =', average(urb_4))
print('Stedelijkheid 5:', '(', min(urb_5), '-', max(urb_5), '), average =', average(urb_5))

# boxplot_data = [urb_1, urb_2, urb_3, urb_4, urb_5]
# fig, ax = plt.subplots()
# plt.boxplot(boxplot_data)
# plt.xlabel('Urbanity')
# plt.ylabel('Number of ' + BS_type)
# plt.show()
#
# fig, ax = plt.subplots()
# plt.scatter(zip_codes['popdensity'], zip_codes['GSM_BS'] / zip_codes['aantal_inw'], marker='+', s=8, label='GSM')
# plt.scatter(zip_codes['popdensity'], zip_codes['UMTS_BS'] / zip_codes['aantal_inw'], marker='d', s=8, label='UMTS')
# plt.scatter(zip_codes['popdensity'], zip_codes['LTE_BS'] / zip_codes['aantal_inw'], marker='*', s=8, label='LTE')
# plt.scatter(zip_codes['popdensity'], zip_codes['NR_BS'] / zip_codes['aantal_inw'], s=8, label='NR')
# plt.xlabel('Number of residents')
# plt.ylabel('Number of BSs per user')
# plt.xscale('log')
# plt.title('Residents and BSs per zip code')
# plt.legend()
# plt.show()
#
# data = [zip_codes['GSM_BS'], zip_codes['UMTS_BS'], zip_codes['LTE_BS'], zip_codes['NR_BS']]
# fig, ax = plt.subplots()
# plt.hist(data, bins=25, histtype='bar', label=['GSM', 'UMTS', 'LTE', 'NR'])
# plt.xlabel('Number of BSs per zip code')
# plt.xlim([0, 30])
# plt.legend()
# plt.show()
#
# city_list = ['Enschede', 'Amsterdam', 'Assen', 'Middelburg', 'Utrecht', "Netherlands"]
# city_dict = {}
#
# for city in city_list:
#     if city == 'Netherlands':
#         zip_codes_region = zip_codes
#     else:
#         region, zip_codes_region = antenna.find_zip_code_region(zip_codes, [city])
#     city_dict[city] = []
#     city_dict[city].append(zip_codes_region['GSM_BS'] / zip_codes_region['geometry'].area)
#     city_dict[city].append(zip_codes_region['UMTS_BS'] / zip_codes_region['geometry'].area)
#     city_dict[city].append(zip_codes_region['LTE_BS'] / zip_codes_region['geometry'].area)
#     city_dict[city].append(zip_codes_region['NR_BS'] / zip_codes_region['geometry'].area)
#
# colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22',
#           '#17becf']
#
# fig, ax = plt.subplots()
# bplot = ax.boxplot(city_dict['Enschede'], patch_artist=True, showfliers=False, medianprops={'color': 'black'})
# for patch, color in zip(bplot['boxes'], colors[:4]):
#     patch.set_facecolor(color)
# plt.xticks([1, 2, 3, 4], ['GSM', 'UMTS', 'LTE', 'NR'])
# plt.title('Enschede')
# plt.show()
#
# fig, ax = plt.subplots()
# bplot = ax.boxplot(city_dict['Amsterdam'], patch_artist=True, showfliers=False, medianprops={'color': 'black'})
# for patch, color in zip(bplot['boxes'], colors[:4]):
#     patch.set_facecolor(color)
# plt.xticks([1, 2, 3, 4], ['GSM', 'UMTS', 'LTE', 'NR'])
# plt.title('Amsterdam')
# plt.show()
#
# fig, ax = plt.subplots()
# bplot = ax.boxplot(city_dict['Assen'], patch_artist=True, showfliers=False, medianprops={'color': 'black'})
# for patch, color in zip(bplot['boxes'], colors[:4]):
#     patch.set_facecolor(color)
# plt.xticks([1, 2, 3, 4], ['GSM', 'UMTS', 'LTE', 'NR'])
# plt.title('Assen')
# plt.show()
#
# fig, ax = plt.subplots()
# bplot = ax.boxplot(city_dict['Netherlands'], patch_artist=True, showfliers=False, medianprops={'color': 'black'})
# for patch, color in zip(bplot['boxes'], colors[:4]):
#     patch.set_facecolor(color)
# plt.xticks([1, 2, 3, 4], ['GSM', 'UMTS', 'LTE', 'NR'])
# plt.title('The Netherlands')
# plt.show()
