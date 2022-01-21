import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import csv
import networkx as nx
from shapely.ops import unary_union
from shapely.geometry import Point
from shapely.geometry import Polygon
import random
import graph_functions as gf

def generate_random(number, polygon):   #to generate users per zip code
    points = []
    minx, miny, maxx, maxy = polygon.bounds
    while len(points) < number:
        pnt = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if polygon.contains(pnt):
            points.append(pnt)
    return points


# find all users in the specific zip codes
def get_population(zip_codes_region):
    users = []
    division_parameter = 5  # 1/5th of the population uses the network

    for index, row in zip_codes_region.iterrows():
        polygon = row['geometry']
        number_of_users = row['aantal_inw']
        points = generate_random(number_of_users / division_parameter, polygon)
        users += points
    return users

