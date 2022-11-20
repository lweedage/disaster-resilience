import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import numpy as np
import util
from shapely.geometry import Point

params = {'legend.fontsize': 'x-large',
          'axes.labelsize': 'x-large',
          'axes.titlesize': 'x-large',
          'xtick.labelsize': 'x-large',
          'ytick.labelsize': 'x-large',
          'lines.markersize': 8,
          'figure.autolayout': True}
pylab.rcParams.update(params)

colors = ['#904C77', '#E49AB0', '#ECB8A5', '#96ACB7', '#957D95'] * 100

xbs = util.from_data('data/BSs/EnschedeKPN_xs.p')
ybs = util.from_data('data/BSs/EnschedeKPN_ys.p')
region = util.from_data('data/Regions/Enschederegion.p')

city_name = 'Enschede'
provider = 'KPN'
percentage = 2
percentage_MNO = 1/3

def find_name(city_name, provider, percentage, percentage_MNO, user_increase, seed = 1):
    filename = f'{city_name}{provider}{percentage}{str(percentage_MNO)[:4]}'
    bsfilename = f'{city_name}{provider}'
    userfilename = filename
    if user_increase > 0:
        userfilename += f'user_increase{user_increase}'
        filename += f'user_increase{user_increase}'
    filename += f'{seed}'
    return userfilename, filename, bsfilename

increases = [0, 5, 25, 50, 75, 100]
fsp, fdp = [], []


fig, ax = plt.subplots()
for i, provider in zip(range(4), ['KPN', 'T-Mobile', 'Vodafone', 'all_MNOs']):
    fsp, fdp = [], []
    for user_increase in increases:
        userfilename, filename, bsfilename = find_name(city_name, provider, percentage, percentage_MNO, user_increase)
        print(filename)
        FSP = util.from_data(f'data/Realisations/{filename}_FSP.p')
        fsp.append(np.sum(FSP)/len(FSP))
        fdp.append(util.from_data(f'data/Realisations/{filename}_FDP.p'))
    plt.scatter(increases, fsp, label = provider, color = colors[i])
    print(fsp)
plt.legend()
plt.show()
plt.savefig('user_increases_enschede.png')

