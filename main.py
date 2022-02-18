import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import util
import find_base_stations as antenna
from settings import *
import generate_users

# Retrieve zip code population + area data and make a region with specified zip codes
# Columns are: aantal_inw (population), stedelijkh (urbanity), postcode (zip code), geometry, popdensity (population density), municipali(city), GSM_BS, UMTS_BS, LTE_BS, NR_BS, BSs, scenario
zip_codes = gpd.read_file('data/zip_codes_with_scenarios.shp')

# region that we want to investigate:
# municipality = 'Overijssel'  # 'Gelderland', 'Overijssel', 'Noord-Holland', 'Zuid-Holland', 'Groningen', 'Utrecht', 'Limburg', 'Noord-Brabant', 'Friesland', 'Zeeland', 'Flevoland', 'Drenthe'
# cities = util.find_cities(municipality)  # has to be a list of cities
cities = ['Enschede']

region, zip_code_region = antenna.find_zip_code_region(zip_codes, cities)
base_stations = antenna.load_bs(region)
users = generate_users.generate_users(zip_code_region)

for bs in base_stations:
    print(bs.channels)
