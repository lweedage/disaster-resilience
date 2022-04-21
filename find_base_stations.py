import json
import geopandas as gpd
from shapely.geometry import Point
from shapely.ops import unary_union
import objects.BaseStation as BSO
import util
from settings import *
import sys

sys.setrecursionlimit(10000)

# code adapted from Bart Meyers

def find_zip_code_region(params):
    # zip_code_region_data = util.from_data(f'data/BSs/{params.filename}zip_code_region_data.p')
    # region = util.from_data(f'data/BSs/{params.filename}region.p')
    zip_codes = params.zip_codes
    zip_code_region_data = None
    if zip_code_region_data is None:
        if isinstance(params.cities[0], int):
            zip_code_region_data = zip_codes[zip_codes['postcode'].isin(params.cities)]
        else:
            zip_code_region_data = zip_codes[zip_codes['municipali'].isin(params.cities)]
        region = gpd.GeoSeries(unary_union(zip_code_region_data['geometry']))

        # util.to_data(zip_code_region_data, f'data/BSs/{params.filename}zip_code_region_data.p')
        # util.to_data(region, f'data/BSs/{params.filename}region.p')
    params.region = region
    params.zip_code_region = zip_code_region_data
    return params

def load_bs(params):
    # all_basestations = util.from_data(f'data/BSs/{params.filename}_all_basestations.p')
    # xs = util.from_data(f'data/BSs/{params.filename}_xs.p')
    # ys = util.from_data(f'data/BSs/{params.filename}_ys.p')

    all_basestations = None
    if all_basestations is None:
        all_basestations = list()
        id = 0
        xs, ys = [], []

        with open(BS_PATH) as f:
            bss = json.load(f)
            # Loop over base stations
            for key in bss.keys():
                small_cell = False
                bs = bss[key]
                x = float(bs.get('x'))
                y = float(bs.get('y'))

                if params.region.contains(Point(x, y)).bool():
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

                        freq_dict = dict()
                        for key in bs.get("antennas").keys():
                            antenna = bs.get("antennas").get(key)
                            frequency = antenna.get("frequency")
                            main_direction = antenna.get('angle')

                            power = antenna.get("power") + 30  # We convert ERP power in dBW to dBm
                            height = bs.get('antennas')[str(0)].get("height")
                            provider, bandwidth = util.find_provider(frequency / 1e6)
                            # if main_direction != 'Omnidirectional':
                            #     if frequency in freq_dict.keys():
                            #         freq_dict[frequency].append(main_direction)
                            #     else:
                            #         freq_dict[frequency] = [main_direction]
                            if provider in params.providers:
                                new_bs.add_channel(key, new_bs.id, height, frequency, power, main_direction, bandwidth)
                                new_bs.frequencies.add(frequency)

                        if provider in params.providers:
                            powers = [channel.power for channel in new_bs.channels]
                            if max(powers) <= 17.8 + 30:  # 17.8 dBW is 60 W, that is the maximum power of a small cell.
                                small_cell = True

                        # TODO this was to find beamwidth, but I now assume that beamwidth is just constant
                        # for channel in new_bs.channels:
                        #     if channel.frequency in freq_dict.keys():
                        #         angle_list = sorted(freq_dict[channel.frequency])
                        #         if len(angle_list) > 1:
                        #             index = angle_list.index(channel.main_direction)
                        #             length = len(angle_list)
                            #         beamwidth = ((angle_list[(index + 1) % length] - angle_list[index]) % 360) / 2 + (
                            #                     (angle_list[index] - angle_list[(index - 1) % length]) % 360) / 2
                            #         if beamwidth == 0:
                            #             beamwidth = 360
                            #     else:
                            #         beamwidth = 360
                            #
                            # channel.beamwidth = beamwidth

                        new_bs.provider = provider

                        # if gpd.GeoSeries(unary_union(params.zip_code_region[params.zip_code_region['scenario'] == 'UMa'].geometry)).contains(
                        #         Point(x, y)).bool():
                        #     area_type = util.AreaType.UMA
                        # elif gpd.GeoSeries(
                        #         unary_union(params.zip_code_region[params.zip_code_region['scenario'] == 'RMa'].geometry)).contains(
                        #         Point(x, y)).bool():
                        #     area_type = util.AreaType.RMA
                        # else:
                        #     print('No type', x, y)
                        # if small_cell:
                        #     area_type = util.AreaType.UMI
                        #
                        # new_bs.area_type = area_type

                        if new_bs.provider in params.providers:
                            all_basestations.append(new_bs)
                            xs.append(x)
                            ys.append(y)
                            id += 1

        params.xbs = xs
        params.ybs = ys
        params.BaseStations = all_basestations
        params.number_of_bs = len(all_basestations)

        # params.initialize()

        # print('Adding interferers ...')
        # for bs in all_basestations:
        #     for channel in bs.channels:
        #         channel.find_interferers(params)
                # TODO this is not an optimal algorithm yet.

        # print('Saving data ...')
        # util.to_data(all_basestations, f'data/BSs/{params.filename}_all_basestations.p')
        # util.to_data(xs, f'data/BSs/{params.filename}_xs.p')
        # util.to_data(ys, f'data/BSs/{params.filename}_ys.p')
    else:
        params.xbs = xs
        params.ybs = ys
        params.BaseStations = all_basestations
        params.number_of_bs = len(all_basestations)

        params.initialize()
    return params

