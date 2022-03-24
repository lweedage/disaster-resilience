import random

from shapely.geometry import Point

import objects.UE as UE


def generate_random(number, polygon):  # to generate users per zip code
    points = []
    minx, miny, maxx, maxy = polygon.bounds
    while len(points) < number:
        pnt = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if polygon.contains(pnt):
            points.append(pnt)
    return points


# find all users in the specific zip codes
def get_population(zip_codes_region, percentage):
    users = []
    division_parameter = percentage / 100  # 1/5th of the population uses the network (assumption)
    for index, row in zip_codes_region.iterrows():
        polygon = row['geometry']
        number_of_users = row['aantal_inw']
        points = generate_random(number_of_users * division_parameter, polygon)
        users += points
    xs = [point.x for point in users]
    ys = [point.y for point in users]
    return xs, ys


def generate_users(zip_codes_region, percentage):
    all_users = list()
    xs, ys = get_population(zip_codes_region, percentage)
    for i in range(len(xs)):
        new_user = UE.UserEquipment(i, xs[i], ys[i], rate_requirement=5)
        all_users.append(new_user)
    return all_users, xs, ys
