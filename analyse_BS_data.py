import find_base_stations as antenna
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from cycler import cycler

import util

matplotlib.rcParams['axes.prop_cycle'] = cycler('color',
                                                ['DeepSkyBlue', 'DarkMagenta', 'Orange', 'LimeGreen', 'OrangeRed',
                                                 'LightPink'])
colors = ['DeepSkyBlue', 'DarkMagenta', 'Orange', 'LimeGreen', 'OrangeRed', 'LightPink']





zip_codes = gpd.read_file('data/zip_codes.shp')
# # zip_codes['BS_density'] = zip_codes['BSs']/zip_codes['geometry'].area
#
# # municipality = 'Noord-Brabant'  # 'Gelderland', 'Overijssel', 'Noord-Holland', 'Zuid-Holland', 'Groningen', 'Utrecht', 'Limburg', 'Noord-Brabant', 'Friesland', 'Zeeland', 'Flevoland', 'Drenthe'
# # cities = util.find_cities(municipality)
cities = ['Amsterdam']
region, zip_codes = antenna.find_zip_code_region(zip_codes, cities)
params = antenna.load_bs(params)

small_cells, macro_cells = 0, 0
for bs in base_stations:
    if bs.small_cell:
        small_cells += 1
    else:
        macro_cells += 1

print(f'There are {small_cells} small cells and {macro_cells} larger cells.')

#
# #
# # BS_type = 'BSs'
# #
# # urb_1 = zip_codes[zip_codes.stedelijkh == str(1)][BS_type] / zip_codes[zip_codes.stedelijkh == str(1)][
# #     'geometry'].area * 10**(6)
# # urb_2 = zip_codes[zip_codes.stedelijkh == str(2)][BS_type] / zip_codes[zip_codes.stedelijkh == str(2)][
# #     'geometry'].area * 10**(6)
# # urb_3 = zip_codes[zip_codes.stedelijkh == str(3)][BS_type] / zip_codes[zip_codes.stedelijkh == str(3)][
# #     'geometry'].area * 10**(6)
# # urb_4 = zip_codes[zip_codes.stedelijkh == str(4)][BS_type] / zip_codes[zip_codes.stedelijkh == str(4)][
# #     'geometry'].area * 10**(6)
# # urb_5 = zip_codes[zip_codes.stedelijkh == str(5)][BS_type] / zip_codes[zip_codes.stedelijkh == str(5)][
# #     'geometry'].area * 10**(6)
# #
# # # print('Stedelijkheid 1:', '(', min(urb_1), '-', max(urb_1), '), average =', average(urb_1))
# # print('Stedelijkheid 2:', '(', min(urb_2), '-', max(urb_2), '), average =', average(urb_2))
# # print('Stedelijkheid 3:', '(', min(urb_3), '-', max(urb_3), '), average =', average(urb_3))
# # print('Stedelijkheid 4:', '(', min(urb_4), '-', max(urb_4), '), average =', average(urb_4))
# # print('Stedelijkheid 5:', '(', min(urb_5), '-', max(urb_5), '), average =', average(urb_5))
# #
# # boxplot_data = [urb_1, urb_2, urb_3, urb_4, urb_5]
# # fig, ax = plt.subplots()
# # plt.boxplot(boxplot_data)
# # plt.xlabel('Urbanity')
# # plt.ylabel('Number of ' + BS_type)
# # plt.show()
#
#
# city_list = ['Enschede', 'Amsterdam', 'Assen', 'Middelburg', 'Utrecht', "Netherlands"]
# city_dict = {}
# #
# # for city in city_list:
# #     if city == 'Netherlands':
# #         zip_codes_region = zip_codes
# #     else:
# #         region, zip_codes_region = antenna.find_zip_code_region(zip_codes, [city])
# #     city_dict[city] = []
# #     city_dict[city].append(zip_codes_region['GSM_BS'] / zip_codes_region['geometry'].area)
# #     city_dict[city].append(zip_codes_region['UMTS_BS'] / zip_codes_region['geometry'].area)
# #     city_dict[city].append(zip_codes_region['LTE_BS'] / zip_codes_region['geometry'].area)
# #     city_dict[city].append(zip_codes_region['NR_BS'] / zip_codes_region['geometry'].area)
#
# # fig, ax = plt.subplots()
# # ax.boxplot(city_dict['Enschede'], patch_artist=True, showfliers=False, medianprops={'color': 'black'})
# # ax.boxplot(city_dict['Amsterdam'], patch_artist=True, showfliers=False, medianprops={'color': 'black'})
# # plt.xticks([1, 2, 3, 4], ['GSM', 'UMTS', 'LTE', 'NR'])
# # plt.title('Enschede')
# # plt.show()
#
#
# cities = ['Amsterdam', 'Utrecht', 'Enschede', 'Zwolle', 'Assen', 'Middelburg', 'Elburg']
# KPN = [1147, 500, 207, 168, 104, 57, 32]
# Vodafone = [389, 157, 66, 55, 40, 24, 13]
# TMobile = [852, 366, 159, 111, 62, 36, 23]
# area = [195.02, 99.27, 142.64, 119.24, 78.58, 50.92, 56.75]
# population = [872340, 357355, 159650, 128825, 68600, 48815, 23155]
#
# providers = ['KPN', 'Vodafone', 'T-Mobile']
# LTE, GSM, UMTS, NR = dict(), dict(), dict(), dict()
#
# GSM['KPN'] = [231, 104, 39, 34, 23, 11, 6]
# UMTS['KPN'] = [234, 104, 38, 32, 22, 12, 6]
# LTE['KPN'] = [375, 151, 75, 54, 39, 16, 10]
# NR['KPN'] = [307, 141, 55, 48, 20, 18, 10]
#
# GSM['Vodafone'] = [223, 92, 40, 31, 19, 13, 7]
# UMTS['Vodafone'] = [0, 0, 0, 0, 0, 0, 0]
# LTE['Vodafone'] = [166, 65, 26, 24, 21, 11, 6]
# NR['Vodafone'] = [0, 0, 0, 0, 0, 0, 0]
#
# GSM['T-Mobile'] = [221, 90, 49, 30, 23, 11, 7]
# UMTS['T-Mobile'] = [221, 88, 49, 30, 22, 10, 7]
# LTE['T-Mobile'] = [206, 84, 27, 20, 5, 8, 4]
# NR['T-Mobile'] = [214, 104, 34, 31, 12, 7, 5]
#
# GSM_total = [675, 286, 128,  95,  65,  35,  20]
# UMTS_total = [455, 192, 87, 62, 22, 13]
# LTE_total = [747, 300, 128,  98,  65,  35,  20]
# NR_total = [521, 245,  89,  79,  32,  25,  15]
#
# total_prov = dict()
#
# for prov in providers:
#     total_prov[prov] = np.add(np.add(GSM[prov], UMTS[prov]), np.add(NR[prov], LTE[prov]))
#
# total_BS = np.add(np.add(KPN, Vodafone), TMobile)
# print(total_BS, np.divide(KPN, total_BS))
#
# x_bar = [2 * i for i in range(len(cities))]
# width = 1.5
#
# # fig, ax = plt.subplots()
# # plt.bar(x_bar, KPN, width=width, label='KPN')
# # plt.bar(x_bar, Vodafone, label='Vodafone', width=width, bottom=KPN)
# # plt.bar(x_bar, TMobile, label='T-Mobile', width=width, bottom=np.add(KPN, Vodafone))
# # plt.xticks(x_bar, cities)
# # plt.legend()
# # plt.ylabel("Number of BSs")
# # plt.show()
# #
# # fig, ax = plt.subplots()
# # plt.bar(x_bar, np.divide(KPN, total_BS), width=width, label='KPN')
# # plt.bar(x_bar, np.divide(Vodafone, total_BS), label='Vodafone', width=width, bottom=np.divide(KPN, total_BS))
# # plt.bar(x_bar, np.divide(TMobile, total_BS), label='T-Mobile', width=width, bottom=np.add(np.divide(KPN, total_BS), np.divide(Vodafone, total_BS)))
# # plt.xticks(x_bar, cities)
# # plt.legend()
# # plt.ylabel('Percentage of BSs')
# # plt.show()
# #
# # fig, ax = plt.subplots()
# # plt.bar(x_bar, np.divide(KPN, area), width=width, label='KPN')
# # plt.bar(x_bar, np.divide(Vodafone, area), label='Vodafone', width=width, bottom=np.divide(KPN, area))
# # plt.bar(x_bar, np.divide(TMobile, area), label='T-Mobile', width=width, bottom=np.add(np.divide(KPN, area), np.divide(Vodafone, area)))
# # plt.xticks(x_bar, cities)
# # plt.legend()
# # plt.ylabel('BS per km^2')
# # plt.show()
# #
# # fig, ax = plt.subplots()
# # plt.bar(x_bar, np.divide(KPN, population), width=width, label='KPN')
# # plt.bar(x_bar, np.divide(Vodafone, population), label='Vodafone', width=width, bottom=np.divide(KPN, population))
# # plt.bar(x_bar, np.divide(TMobile, population), label='T-Mobile', width=width, bottom=np.add(np.divide(KPN, population), np.divide(Vodafone, population)))
# # plt.xticks(x_bar, cities)
# # plt.legend()
# # plt.ylabel('BS per person')
# # plt.show()
#
# x_bar = [5 * i for i in range(len(cities))]
# width = 1.5
#
# population = [1 for i in range(len(cities))]
# population = total_BS
#
# fig, ax = plt.subplots()
# for prov in providers:
#     if prov == 'KPN':
#         shift = -width
#     elif prov == 'Vodafone':
#         shift = 0
#     else:
#         shift = width
#     population = total_prov[prov]
#     if prov == 'KPN':
#         plt.bar(np.add(x_bar, shift), np.divide(GSM[prov], population), width=width, color=colors[0], label='GSM')
#         plt.bar(np.add(x_bar, shift), np.divide(UMTS[prov], population), width=width, color=colors[1], label='UMTS',
#                 bottom=np.divide(GSM[prov], population))
#         plt.bar(np.add(x_bar, shift), np.divide(LTE[prov], population), width=width, color=colors[2], label='LTE',
#                 bottom=np.divide(np.add(GSM[prov], UMTS[prov]), population))
#         plt.bar(np.add(x_bar, shift), np.divide(NR[prov], population), width=width, color=colors[3], label='NR',
#                 bottom=np.divide(np.add(LTE[prov], np.add(GSM[prov], UMTS[prov])), population))
#     else:
#         plt.bar(np.add(x_bar, shift), np.divide(GSM[prov], population), width=width, color=colors[0])
#         plt.bar(np.add(x_bar, shift), np.divide(UMTS[prov], population), width=width, color=colors[1], bottom=np.divide(GSM[prov], population))
#         plt.bar(np.add(x_bar, shift), np.divide(LTE[prov], population), width=width, color=colors[2],
#                 bottom=np.divide(np.add(GSM[prov], UMTS[prov]), population))
#         plt.bar(np.add(x_bar, shift), np.divide(NR[prov], population), width=width, color=colors[3],
#                 bottom=np.divide(np.add(LTE[prov], np.add(GSM[prov], UMTS[prov])), population))
#
#     for bar in x_bar:
#         # ax.annotate("", xy=(bar - shift, total_BS[j]), xytext=(bar - shift, total_BS[j] + 5),
#         #             arrowprops=dict(arrowstyle="->"))
#         ax.annotate(prov, xy=(bar + shift - 0.2, 0.08), fontsize=8, rotation = 90)
#
# # plt.bar(x_bar, np.divide(Vodafone, population), label='Vodafone', width=width, bottom=np.divide(KPN, population))
# # plt.bar(x_bar, np.divide(TMobile, population), label='T-Mobile', width=width, bottom=np.add(np.divide(KPN, population), np.divide(Vodafone, population)))
# plt.xticks(x_bar, cities)
# plt.legend()
# plt.ylabel('Percentage of total BSs per provider')
# plt.show()
#
# # providers = ['KPN', 'Vodafone', 'T-Mobile']
# # LTE, GSM, UMTS, NR = dict(), dict(), dict(), dict()
# # for prov in providers:
# #     LTE[prov] = 0
# #     GSM[prov] = 0
# #     UMTS[prov] = 0
# #     NR[prov] = 0
# #
# # for bs in base_stations:
# #     provider = bs.provider
# #     if bs.radio == util.BaseStationRadioType.LTE:
# #         LTE[provider] += 1
# #     elif bs.radio == util.BaseStationRadioType.GSM:
# #         GSM[provider] += 1
# #     elif bs.radio == util.BaseStationRadioType.UMTS:
# #         UMTS[provider] += 1
# #     elif bs.radio == util.BaseStationRadioType.NR:
# #         NR[provider] += 1
#
# # print(f'Number of KPN BS: {len(x_KPN)}')
# # print(f'Number of Vodafone BS: {len(x_Vodafone)}')
# # print(f'Number of T-Mobile BS: {len(x_TMobile)}')
# # print(f'Total number of BSs: {len(x_KPN) + len(x_Vodafone) + len(x_TMobile)}')
# # print(f'Area of {cities[0]}: {sum(zip_code_region.area)/1e6} km^2')
# # print(f'Total population: {sum(zip_code_region.aantal_inw)} ')
# # for prov in providers:
# #     print(f'{prov}: {GSM[prov]}, {UMTS[prov]}, {LTE[prov]}, {NR[prov]}')
#
# # fig, ax = plt.subplots()
# # zip_code_region.plot(column='popdensity', ax=ax)
# # plt.scatter(x_KPN, y_KPN, marker='+', s=10, label='KPN')
# # plt.scatter(x_Vodafone, y_Vodafone, marker='+', s=10, label='Vodafone')
# # plt.scatter(x_TMobile, y_TMobile, marker='+', s=10, label='T-Mobile')
# # plt.legend()
# # plt.show()