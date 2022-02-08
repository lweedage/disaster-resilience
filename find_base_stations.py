import settings
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

def find_zip_code_region(zip_code_min, zip_code_max, zip_codes):
    zip_code_region_data = zip_codes[(zip_codes['postcode'] >= zip_code_min) & (
           zip_codes['postcode'] <= zip_code_max) ]
    region = gpd.GeoSeries(unary_union(zip_code_region_data['geometry']))
    return region, zip_code_region_data

def load_bs(zip_code_region):
    all_basestations = list()
    with open(settings.BS_PATH) as f:
        bss = json.load(f)
        # Loop over base-stations
        for bs in bss:
            bs_lat = float(bs.get('X'))
            bs_lon = float(bs.get('Y'))
            if zip_code_region.contains(Point(bs_lat, bs_lon)).bool():
                if bs.get("HOOFDSOORT") == "LTE":
                    radio = util.BaseStationRadioType.LTE
                elif bs.get("HOOFDSOORT") == "5G NR":
                    radio = util.BaseStationRadioType.NR
                else:
                    print(bs.get("HOOFDSOORT")) # there are no other kinds of BSs in this data set (yet)

                h = util.str_to_float(bs.get('antennes')[0].get("Hoogte")) # the height of all antenna's is the same for 1 BS.
                new_bs = BSO.BaseStation(bs.get('ID'), radio, bs_lon, bs_lat, h)
                for antenna in bs.get("antennes"):
                    frequency = util.str_to_float(antenna.get("Frequentie"))
                    power = util.str_to_float(antenna.get("Vermogen")) # in dBW?
                    main_direction = util.str_to_float(antenna.get('Hoofdstraalrichting'))
                    new_bs.add_channel(frequency, power, main_direction)
                all_basestations.append(new_bs)

    return all_basestations



