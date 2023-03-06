import json
import geopandas as gpd
import seaborn
from shapely.geometry import Point
from shapely.ops import unary_union
import objects.BaseStation as BSO
import settings
import util
from settings import *
import sys
import progressbar
import matplotlib.pyplot as plt
import objects.Params as p
import matplotlib.pylab as pylab

params = {'legend.fontsize': 'x-large',
          'axes.labelsize': 'x-large',
          'axes.titlesize': 'x-large',
          'xtick.labelsize': 'x-large',
          'ytick.labelsize': 'x-large',
          'lines.markersize': 8,
          'figure.autolayout': True}
pylab.rcParams.update(params)

sys.setrecursionlimit(100000)


# code adapted from Bart Meyers

def find_zip_code_region(params):
    zip_code_region_data = util.from_data(f'data/BSs/{params.filename_noMNO}_zip_code_region_data.p')
    region = util.from_data(f'data/BSs/{params.filename_noMNO}_region.p')
    zip_codes = params.zip_codes
    # zip_code_region_data = None
    if zip_code_region_data is None:
        if isinstance(params.cities[0], int):
            zip_code_region_data = zip_codes[zip_codes['postcode'].isin(params.cities)]
        else:
            zip_code_region_data = zip_codes[zip_codes['municipali'].isin(params.cities)]

        region = gpd.GeoSeries(unary_union(zip_code_region_data['geometry']))

        util.to_data(zip_code_region_data, f'data/BSs/{params.filename_noMNO}zip_code_region_data.p')
        util.to_data(region, f'data/BSs/{params.filename_noMNO}region.p')
    params.region = region
    params.zip_code_region = zip_code_region_data
    params.center = region.centroid[0]
    return params


def load_bs(params):
    UMA = util.from_data('data/UMA.p')
    RMA = util.from_data('data/RMA.p')
    if UMA is None:
        UMA = unary_union(params.zip_codes[params.zip_codes['scenario'] == 'UMA'].geometry)
        RMA = unary_union(params.zip_codes[params.zip_codes['scenario'] == 'RMA'].geometry)

        util.to_data(UMA, 'data/UMA.p')
        util.to_data(RMA, 'data/RMA.p')

    all_basestations = util.from_data(f'data/BSs/{params.bsfilename}_all_basestations.p')
    xs = util.from_data(f'data/BSs/{params.bsfilename}_xs.p')
    ys = util.from_data(f'data/BSs/{params.bsfilename}_ys.p')
    channel_count = util.from_data(f'data/BSs/{params.bsfilename}_channels.p')
    all_freqs = util.from_data(f'data/BSs/{params.bsfilename}_all_freqs.p')
    radios = util.from_data(f'data/BSs/{params.bsfilename}_radios.p')

    if params.buffer_size:
        new_region = params.region.buffer(params.buffer_size, join_style=3)
    else:
        new_region = params.region

    # radios = None
    if radios is None or all_basestations[0].provider == '':
        print('BSs are not stored in memory')
        all_basestations = list()
        id = 0
        xs, ys = [], []
        radios = []
        all_freqs = set()
        omnidirection = 0

        with open(BS_PATH) as f:
            bss = json.load(f)
            bar = progressbar.ProgressBar(maxval=len(bss),
                                          widgets=[progressbar.Bar('=', f'Finding BSs {params.bsfilename} [', ']'), ' ',
                                                   progressbar.Percentage(), ' ', progressbar.ETA()])
            bar.start()

            # Loop over base stations
            for key, index in zip(bss.keys(), range(len(bss))):
                bar.update(index)

                bs = bss[key]
                x = float(bs.get('x'))
                y = float(bs.get('y'))
                if new_region.contains(Point(x, y)).bool() and Point(x, y).distance(
                        params.center) > params.radius_disaster:
                    Continue = True
                    if bs.get("type") == "LTE":
                        radio = util.BaseStationRadioType.LTE
                    elif bs.get("type") == "5G NR":
                        radio = util.BaseStationRadioType.NR
                    elif bs.get("type") == "UMTS":
                        radio = util.BaseStationRadioType.UMTS
                    elif bs.get("type") == "GSM":
                        radio = util.BaseStationRadioType.GSM
                        Continue = False
                    else:
                        print(bs.get("HOOFDSOORT"))  # there are no other kinds of BSs in this data set

                    if Continue:
                        new_bs = BSO.BaseStation(id, radio, x, y)
                        channel = 0
                        for key in bs.get("antennas").keys():
                            antenna = bs.get("antennas").get(key)
                            frequency = antenna.get("frequency")
                            provider, bandwidth = util.find_provider(frequency / 1e6)
                            new_bs.provider = provider
                            if provider in params.providers:
                                all_freqs.add(frequency)
                                main_direction = antenna.get('angle')
                                if main_direction != 'Omnidirectional':  # we only consider three-sectorized antenna's
                                    power = POWER_PERCENTAGE * (
                                            antenna.get("power") + 30)  # We convert ERP power in dBW to dBm
                                    height = bs.get('antennas')[str(0)].get("height")

                                    new_bs.add_channel(key, new_bs.id, height, frequency, power, main_direction,
                                                       bandwidth)
                                    new_bs.frequencies.add(frequency)
                                    channel += 1
                                else:
                                    omnidirection += 1

                        if channel > 0:
                            if UMA.contains(Point(x, y)):
                                area_type = util.AreaType.UMA
                            elif RMA.contains(Point(x, y)):
                                area_type = util.AreaType.RMA
                            else:
                                area_type = util.AreaType.RMA  # TODO: there are still some BSs that have no zip code? I assume this is RMA
                                # print('No type', x, y)

                            new_bs.area_type = area_type

                            p = np.random.uniform(0, 1)
                            if p >= params.random_failure:
                                all_basestations.append(new_bs)
                                xs.append(x)
                                ys.append(y)
                                id += 1
                                radios.append(bs.get("type"))


            # bar.finish()
        params.xbs = xs
        params.ybs = ys
        params.BaseStations = all_basestations
        params.number_of_bs = len(all_basestations)

        freq_channels = dict()
        channel_count = 0
        for bs in all_basestations:
            for channel in bs.channels:
                channel_count += 1
                if channel.frequency in freq_channels.keys():
                    freq_channels[channel.frequency].add(channel.BS_id)
                else:
                    freq_channels[channel.frequency] = {channel.BS_id}
        for bs in all_basestations:
            for channel in bs.channels:
                bs_interferers = [params.BaseStations[i] for i in freq_channels[channel.frequency] if
                                  i != channel.BS_id and 1 < util.distance_2d(params.BaseStations[i].x,
                                                                              params.BaseStations[i].y, bs.x,
                                                                              bs.y) <= 5_000]
                distances = np.array([util.distance_2d(i.x, i.y, bs.x, bs.y) for i in
                             bs_interferers])
                indices = np.array(distances).argsort()
                channel.bs_interferers = [bs_interferers[i] for i in indices[settings.CUTOFF_VALUE_INTERFERENCE:]]

        util.to_data(all_basestations, f'data/BSs/{params.bsfilename}_all_basestations.p')
        util.to_data(xs, f'data/BSs/{params.bsfilename}_xs.p')
        util.to_data(ys, f'data/BSs/{params.bsfilename}_ys.p')
        util.to_data(channel_count, f'data/BSs/{params.bsfilename}_channels.p')
        util.to_data(all_freqs, f'data/BSs/{params.bsfilename}_all_freqs.p')
        util.to_data(radios, f'data/BSs/{params.bsfilename}_radios.p')


        params.all_freqs = list(all_freqs)
        params.number_of_channels = channel_count
        params.initialize()
    else:
        params.xbs = xs
        params.ybs = ys
        params.BaseStations = all_basestations
        params.number_of_bs = len(all_basestations)
        params.number_of_channels = channel_count
        params.all_freqs = list(all_freqs)
        params.initialize()
    return params


# if __name__ == '__main__':
#     percentage = 2  # Three user density levels - still tbd
#     seed = 1
#     power3G, power4G, power5G = dict(), dict(), dict()
#     freq3G, freq4G, freq5G = dict(), dict(), dict()
#     for mno in ['KPN', 'T-Mobile', 'Vodafone']:
#         freq3G[mno], freq4G[mno], freq5G[mno] = set(), set(), set()
#         power3G[mno], power4G[mno], power5G[mno] = [], [], []
#
#     for province in ['Drenthe', 'Flevoland', 'Friesland', 'Groningen', 'Limburg', 'Overijssel', 'Utrecht', 'Zeeland',
#                      'Zuid-Holland', 'Gelderland', 'Noord-Brabant', 'Noord-Holland']:
#         # for city in ['Almere', 'Amsterdam', 'Enschede', "'s-Gravenhage", 'Elburg', 'Emmen', 'Groningen', 'Maastricht', 'Eindhoven', 'Middelburg']:
#         for mno in [['KPN'], ['T-Mobile'], ['Vodafone']]:
#             zip_codes = gpd.read_file('data/zip_codes_with_scenarios.shp')
#             cities = util.find_cities(province)
#             # province = None
#             # cities = [city]
#             print(province)
#
#             params = p.Parameters(seed, zip_codes, mno, percentage, buffer_size=None, city_list=cities,
#                                   province=province)
#
#             params = find_zip_code_region(params)
#             print(len(params.zip_code_region['postcode']), sum(params.zip_code_region['geometry'].area))
#             params = load_bs(params)
#             mno = mno[0]
#
#             for bs in params.BaseStations:
#                 for channel in bs.channels:
#                     if bs.radio == util.BaseStationRadioType.UMTS:
#                         power3G[mno].append(channel.power)
#                         freq3G[mno].add(channel.frequency / 1e6)
#                     elif bs.radio == util.BaseStationRadioType.LTE:
#                         power4G[mno].append(channel.power)
#                         freq4G[mno].add(channel.frequency / 1e6)
#                     elif bs.radio == util.BaseStationRadioType.NR:
#                         power5G[mno].append(channel.power)
#                         freq5G[mno].add(channel.frequency / 1e6)
#
#     x = np.array([1, 2, 3])
#
#     fig, ax = plt.subplots()
#     data = [power3G, power4G, power5G]
#
#     # print(power3G, power4G, power5G)
#     with open("power3G.txt", "w") as output:
#         output.write(str(power3G))
#     with open("power4G.txt", "w") as output:
#         output.write(str(power4G))
#     with open("power5G.txt", "w") as output:
#         output.write(str(power5G))
#
#     plt.hist(data, density=True, histtype='bar', color=colors[:3], label=['3G', '4G', '5G'])
#
#     plt.xlabel('Power (dBW)')
#     plt.legend()
#
#     plt.savefig('power.png', dpi=1000)
#     # plt.show()
#
#     # print('3G', freq3G)
#     # print('4G', freq4G)
#     # print('5G', freq5G)

markers = ['o', '^', 's']
colors = seaborn.color_palette('Magma')



