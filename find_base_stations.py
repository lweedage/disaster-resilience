from settings import *
import util
import json
import objects.BaseStation as BSO
import geopandas as gpd
from shapely.geometry import Point
from shapely.ops import unary_union
import pandas
import numpy as np
import matplotlib.pyplot as plt

# code from Bart Meyers

def find_zip_code_region(zip_codes, city=['Netherlands']):
    if city == ['Netherlands']:
        city = list(zip_codes['municipali'])
    zip_code_region_data = zip_codes[zip_codes['municipali'].isin(city)]
    region = gpd.GeoSeries(unary_union(zip_code_region_data['geometry']))
    return region, zip_code_region_data

def load_bs(zip_code_region):
    all_basestations = list()
    with open(BS_PATH) as f:
        bss = json.load(f)
        # Loop over base-stations
        for key in bss.keys():
            small_cell = False

            bs = bss[key]
            x = float(bs.get('x'))
            y = float(bs.get('y'))
            if zip_code_region.contains(Point(x, y)).bool():
                if bs.get("type") == "LTE":
                    radio = util.BaseStationRadioType.LTE
                elif bs.get("type") == "5G NR":
                    radio = util.BaseStationRadioType.NR
                elif bs.get("type") == "GSM":
                    radio = util.BaseStationRadioType.GSM
                elif bs.get("type") == "UMTS":
                    radio = util.BaseStationRadioType.UMTS
                else:
                    print(bs.get("HOOFDSOORT")) # there are no other kinds of BSs in this data set (yet)

                new_bs = BSO.BaseStation(bs.get('ID'), radio, x, y)
                for key in bs.get("antennas").keys():
                    height = bs.get('antennas')[str(0)].get("height")
                    antenna = bs.get("antennas").get(key)
                    frequency = antenna.get("frequency")
                    angle = antenna.get('angle')
                    power = antenna.get("power") # in dBW?
                    provider, bandwidth = util.find_provider(frequency/1e6)


                    new_bs.add_channel(height, frequency, power, angle, bandwidth)
                new_bs.provider = provider
                new_bs.small_cell = small_cell
                all_basestations.append(new_bs)

    return all_basestations



