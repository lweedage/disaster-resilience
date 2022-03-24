import json

import geopandas as gpd
from shapely.geometry import Point
from shapely.ops import unary_union

import objects.BaseStation as BSO
import util
from settings import *


# code from Bart Meyers

def find_zip_code_region(zip_codes, city=None):
    if city is None:
        city = list(zip_codes['municipali'])
    zip_code_region_data = zip_codes[zip_codes['municipali'].isin(city)]
    region = gpd.GeoSeries(unary_union(zip_code_region_data['geometry']))
    return region, zip_code_region_data


def load_bs(region, zip_code_region):
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

            if region.contains(Point(x, y)).bool():
                if bs.get("type") == "LTE":
                    radio = util.BaseStationRadioType.LTE
                elif bs.get("type") == "5G NR":
                    radio = util.BaseStationRadioType.NR
                elif bs.get("type") == "GSM":
                    radio = util.BaseStationRadioType.GSM
                elif bs.get("type") == "UMTS":
                    radio = util.BaseStationRadioType.UMTS
                else:
                    print(bs.get("HOOFDSOORT"))  # there are no other kinds of BSs in this data set

                new_bs = BSO.BaseStation(id, radio, x, y)
                xs.append(x)
                ys.append(y)

                freq_dict = dict()
                for key in bs.get("antennas").keys():
                    antenna = bs.get("antennas").get(key)
                    frequency = antenna.get("frequency")
                    main_direction = antenna.get('angle')
                    power = antenna.get("power") + 30 # We convert ERP power in dBW to dBm
                    height = bs.get('antennas')[str(0)].get("height")
                    provider, bandwidth = util.find_provider(frequency / 1e6)
                    if main_direction != 'Omnidirectional':
                        if frequency in freq_dict.keys():
                            freq_dict[frequency].append(main_direction)
                        else:
                            freq_dict[frequency] = [main_direction]
                    new_bs.add_channel(key, height, frequency, power, main_direction, bandwidth)
                powers = [channel.power for channel in new_bs.channels]
                if max(powers) <= 17.8 + 30:  # 17.8 dBW is 60 W, that is the maximum power of a small cell.
                    small_cell = True

                for channel in new_bs.channels:
                    if channel.frequency in freq_dict.keys():
                        angle_list = sorted(freq_dict[channel.frequency])
                        if len(angle_list) > 1:
                            index = angle_list.index(channel.main_direction)
                            length = len(angle_list)
                            beamwidth = ((angle_list[(index + 1) % length] - angle_list[index]) % 360) / 2 + (
                                        (angle_list[index] - angle_list[(index - 1) % length]) % 360) / 2
                            if beamwidth == 0:
                                beamwidth = 360
                        else:
                            beamwidth = 360

                    channel.beamwidth = beamwidth

                new_bs.provider = provider

                if gpd.GeoSeries(unary_union(zip_code_region[zip_code_region['scenario'] == 'UMa'].geometry)).contains(
                        Point(x, y)).bool():
                    area_type = util.AreaType.UMA
                elif gpd.GeoSeries(
                        unary_union(zip_code_region[zip_code_region['scenario'] == 'RMa'].geometry)).contains(
                        Point(x, y)).bool():
                    area_type = util.AreaType.RMA
                else:
                    print('No type', x, y)
                if small_cell:
                    area_type = util.AreaType.UMI

                new_bs.area_type = area_type

                all_basestations.append(new_bs)
                id += 1

    return all_basestations, xs, ys
