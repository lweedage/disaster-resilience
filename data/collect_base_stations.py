import json
import sys
import geopandas as gpd
from shapely.geometry import Point
from shapely.ops import unary_union
import objects.BaseStation as BSO
import util
from settings import *

sys.setrecursionlimit(10000)

# code adapted from Bart Meyers: https://github.com/BartJM/ResilSimulator

def find_zip_code_region(params):
    zip_codes = params.zip_codes
    zip_code_region_data = None
    if zip_code_region_data is None:
        if isinstance(params.cities[0], int):
            zip_code_region_data = zip_codes[zip_codes['postcode'].isin(params.cities)]
        else:
            zip_code_region_data = zip_codes[zip_codes['municipali'].isin(params.cities)]
        region = gpd.GeoSeries(unary_union(zip_code_region_data['geometry']))

    params.region = region
    params.zip_code_region = zip_code_region_data
    return params


def load_bs(params):
    all_basestations = list()
    id = 0
    xs, ys = [], []

    with open(BS_PATH) as f:
        bss = json.load(f)
        # Loop over base stations
        for key in bss.keys():
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
                    for key in bs.get("antennas").keys():
                        antenna = bs.get("antennas").get(key)
                        frequency = antenna.get("frequency")
                        main_direction = antenna.get('angle')
                        power = antenna.get("power") + 30  # We convert ERP power in dBW to dBm
                        height = bs.get('antennas')[str(0)].get("height")
                        provider, bandwidth = util.find_provider(frequency / 1e6)
                        if provider in params.providers:
                            new_bs.add_channel(key, new_bs.id, height, frequency, power, main_direction, bandwidth)
                            new_bs.frequencies.add(frequency)

                    new_bs.provider = provider

                    if new_bs.provider in params.providers:
                        all_basestations.append(new_bs)
                        xs.append(x)
                        ys.append(y)
                        id += 1
    params.xbs = xs
    params.ybs = ys
    params.BaseStations = all_basestations
    params.number_of_bs = len(all_basestations)
    return params
