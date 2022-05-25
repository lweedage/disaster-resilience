import random
from shapely.geometry import Point
import objects.UE as UE
import settings
import util
import numpy as np

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

def generate_users(params):
    all_users = util.from_data(f'data/users/{params.filename}{params.seed}_all_users.p')
    xs = util.from_data(f'data/users/{params.filename}{params.seed}_xs.p')
    ys = util.from_data(f'data/users/{params.filename}{params.seed}_ys.p')

    if all_users is None:
        print('Users are not stored in memory')
        np.random.seed(params.seed)
        all_users = list()
        xs, ys = get_population(params.zip_code_region, params.percentage_plus_MNO)
        for i in range(len(xs)):
            if i < int(len(xs)*settings.FRACTION[1]):
                new_user = UE.UserEquipment(i, xs[i], ys[i], rate_requirement = settings.RATE_REQUIREMENT[1])
            elif i < int(len(xs) * (settings.FRACTION[1] + settings.FRACTION[2])):
                new_user = UE.UserEquipment(i, xs[i], ys[i], rate_requirement = settings.RATE_REQUIREMENT[2])
            else:
                new_user = UE.UserEquipment(i, xs[i], ys[i], rate_requirement = settings.RATE_REQUIREMENT[3])
            all_users.append(new_user)

        util.to_data(all_users, f'data/users/{params.filename}{params.seed}_all_users.p')
        util.to_data(xs, f'data/users/{params.filename}{params.seed}_xs.p')
        util.to_data(ys, f'data/users/{params.filename}{params.seed}_ys.p')

    params.users = all_users
    params.x_user = xs
    params.y_user = ys
    params.number_of_users = len(all_users)
    return params