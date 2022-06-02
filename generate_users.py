import random
from shapely.geometry import Point
import objects.UE as UE
import settings
import util
import numpy as np
import geopandas as gpd
from shapely.ops import unary_union


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
    division_parameter = percentage / 100
    for index, row in zip_codes_region.iterrows():
        polygon = row['geometry']
        number_of_users = row['aantal_inw']
        points = generate_random(np.ceil(number_of_users * division_parameter), polygon)
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
                new_user = UE.UserEquipment(i, xs[i], ys[i], rate_requirement = settings.RATE_REQUIREMENT[1], type = 1)
            elif i < int(len(xs) * (settings.FRACTION[1] + settings.FRACTION[2])):
                new_user = UE.UserEquipment(i, xs[i], ys[i], rate_requirement = settings.RATE_REQUIREMENT[2], type = 2)
            else:
                new_user = UE.UserEquipment(i, xs[i], ys[i], rate_requirement = settings.RATE_REQUIREMENT[3], type = 3)
            all_users.append(new_user)

        util.to_data(all_users, f'data/users/{params.filename}{params.seed}_all_users.p')
        util.to_data(xs, f'data/users/{params.filename}{params.seed}_xs.p')
        util.to_data(ys, f'data/users/{params.filename}{params.seed}_ys.p')

    params.users = all_users
    params.x_user = xs
    params.y_user = ys
    params.number_of_users = len(all_users)
    return params

def generate_users_grid(params, delta):
    all_users = util.from_data(f'data/users/{params.filename}{params.seed}_all_users_grid.p')
    x_user = util.from_data(f'data/users/{params.filename}{params.seed}_xs_grid.p')
    y_user = util.from_data(f'data/users/{params.filename}{params.seed}_ys_grid.p')

    if all_users is None:
        print('Users are not stored in memory')
        all_users = list()

        [xmin, ymin, xmax, ymax] = gpd.GeoSeries(params.zip_code_region['geometry']).total_bounds
        xmin, xmax = np.floor(xmin), np.ceil(xmax)
        ymin, ymax = np.floor(ymin), np.ceil(ymax)
        xdelta, ydelta = int(xmax - xmin), int(ymax - ymin)

        xL = np.linspace(xmin, xmax, num=int(xdelta/delta))
        yL = np.linspace(ymin, ymax, num=int(ydelta/delta))

        xs, ys = np.meshgrid(xL, yL)
        xs = xs.flatten()
        ys = ys.flatten()
        x_user = []
        y_user = []

        polygon = gpd.GeoSeries(unary_union(params.zip_code_region['geometry']))

        i = 0
        for j in range(len(xs)):
            pnt = Point(xs[j], ys[j])
            if polygon.contains(pnt).bool():
                if i < int(len(xs)*settings.FRACTION[1]):
                    new_user = UE.UserEquipment(i, xs[j], ys[j], rate_requirement = settings.RATE_REQUIREMENT[1], type = 1)
                elif i < int(len(xs) * (settings.FRACTION[1] + settings.FRACTION[2])):
                    new_user = UE.UserEquipment(i, xs[j], ys[j], rate_requirement = settings.RATE_REQUIREMENT[2], type = 2)
                else:
                    new_user = UE.UserEquipment(i, xs[j], ys[j], rate_requirement = settings.RATE_REQUIREMENT[3], type = 3)
                all_users.append(new_user)
                i += 1
                x_user.append(xs[j])
                y_user.append(ys[j])

        util.to_data(all_users, f'data/users/{params.filename}{params.seed}_all_users_grid.p')
        util.to_data(x_user, f'data/users/{params.filename}{params.seed}_xs_grid.p')
        util.to_data(y_user, f'data/users/{params.filename}{params.seed}_ys_grid.p')

    params.users = all_users
    params.x_user = x_user
    params.y_user = y_user
    params.number_of_users = len(all_users)
    return params