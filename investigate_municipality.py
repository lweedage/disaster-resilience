import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
import statsmodels.api as sm
import util

params = {'legend.fontsize': 'x-large',
          'axes.labelsize': 'x-large',
          'axes.titlesize': 'x-large',
          'xtick.labelsize': 'x-large',
          'ytick.labelsize': 'x-large',
          'lines.markersize': 8,
          'figure.autolayout': True}
pylab.rcParams.update(params)

colors = ['#904C77', '#E49AB0', '#ECB8A5', '#96ACB7', '#957D95'] * 100
markers = ['o', 'X', 'v', 's', '*', 'P', '1', '+']
#
max_iterations = 5
percentage = 2
percentage_MNO = {'Vodafone': 0.33, 'KPN': 0.33, 'T-Mobile': 0.33, 'all_MNOs': 1}

municipalities = ['Middelburg', 'Maastricht', 'Groningen', 'Enschede', 'Emmen', 'Elburg',
                  'Eindhoven', "'s-Gravenhage", 'Amsterdam', 'Almere']
municipalities2 = ['Middelburg', 'Maastricht', 'Groningen', 'Enschede', 'Emmen', 'Elburg',
                   'Eindhoven', "Den Haag", 'Amsterdam', 'Almere']

MNOs = ['KPN', 'T-Mobile', 'Vodafone', 'all_MNOs']
name_MNO = ['MNO-1', 'MNO-2', 'MNO-3', 'National roaming']
#

Disaster = True
Random = False
User = False

radii = [0, 500, 1000, 2500, 5000]  # , 2500]
increases = [0, 50, 100, 200]
random = [0, 0.05, 0.1, 0.25, 0.5]

province = 'Drenthe'


def find_name(filename, radius):
    if MNO != 'all_MNOs':
        filename += str(20.33)
    else:
        filename += str(21)

    if radius == 0:
        return filename + str(5)

    if Disaster:
        filename += 'disaster' + str(radius)
    elif User:
        filename += 'user_increase' + str(radius)
    elif Random:
        filename += 'random' + str(radius)
    return filename + str(5)


if Disaster:
    measures = radii
elif User:
    measures = increases
elif Random:
    measures = random
else:
    measures = [0]

MNO = 'KPN'
municipality = 'Enschede'

seed = 1

i = 0
baseline = util.from_data(f'data/Realisations/{municipality}{MNO}2{percentage_MNO[MNO]}{seed}_sinrs.p')
baseline_snr = baseline.sum(axis=1)
baseline_snr = [float(i[0]) for i in baseline_snr]
ecdf = sm.distributions.ECDF(baseline_snr)
plt.step(ecdf.x, ecdf.y, label=str('no failure'), color=colors[i])
points = []
First25, First50, First75 = True, True, True
for j in range(len(ecdf.x)):
    if ecdf.y[j] > .25 and First25:
        points.append(ecdf.x[j])
        First25 = False
    if ecdf.y[j] > .5 and First50:
        points.append(ecdf.x[j])
        First50 = False
    if ecdf.y[j] > .75 and First75:
        points.append(ecdf.x[j])
        First75 = False

plt.scatter(points, [0.25, 0.5, 0.75], color=colors[i], marker=markers[i])
i = 1
for measure in [0.05, 0.1, 0.25, 0.5]:
    snr = util.from_data(f'data/Realisations/{municipality}{MNO}2{percentage_MNO[MNO]}random{measure}{seed}_sinrs.p')
    snr = snr.sum(axis=1)
    snr = [float(i[0]) for i in snr]
    ecdf = sm.distributions.ECDF(snr)
    plt.step(ecdf.x, ecdf.y, label=str('$p_{iso} = $' + str(measure)), color=colors[i])
    points = []
    First25, First50, First75 = True, True, True
    for j in range(len(ecdf.x)):
        if ecdf.y[j] > .25 and First25:
            points.append(ecdf.x[j])
            First25 = False
        if ecdf.y[j] > .5 and First50:
            points.append(ecdf.x[j])
            First50 = False
        if ecdf.y[j] > .75 and First75:
            points.append(ecdf.x[j])
            First75 = False

    plt.scatter(points, [0.25, 0.5, 0.75], color=colors[i], marker=markers[i])
    i += 1
# plt.xlim([5,20])
plt.xlabel('SINR (dB)')
plt.ylabel('ECDF')
plt.legend()
plt.show()

i = 0
baseline = util.from_data(f'data/Realisations/{municipality}{MNO}2{percentage_MNO[MNO]}{seed}_capacities.p')
ecdf = sm.distributions.ECDF(baseline)
plt.step(ecdf.x, ecdf.y, label=str('no failure'), color=colors[i])
points = []
First25, First50, First75 = True, True, True
for j in range(len(ecdf.x)):
    if ecdf.y[j] > .25 and First25:
        points.append(ecdf.x[j])
        First25 = False
    if ecdf.y[j] > .5 and First50:
        points.append(ecdf.x[j])
        First50 = False
    if ecdf.y[j] > .75 and First75:
        points.append(ecdf.x[j])
        First75 = False

plt.scatter(points, [0.25, 0.5, 0.75], color=colors[i], marker=markers[i])
i = 1
for measure in [0.05, 0.1, 0.25, 0.5]:
    capacities = util.from_data(
        f'data/Realisations/{municipality}{MNO}2{percentage_MNO[MNO]}random{measure}{seed}_capacities.p')
    # snr = snr.sum(axis = 1)
    # snr = [float(i[0]) for i in snr]
    ecdf = sm.distributions.ECDF(capacities)
    plt.step(ecdf.x, ecdf.y, label=str('$p_{iso} = $' + str(measure)), color=colors[i])
    points = []
    First25, First50, First75 = True, True, True
    for j in range(len(ecdf.x)):
        if ecdf.y[j] > .25 and First25:
            points.append(ecdf.x[j])
            First25 = False
        if ecdf.y[j] > .5 and First50:
            points.append(ecdf.x[j])
            First50 = False
        if ecdf.y[j] > .75 and First75:
            points.append(ecdf.x[j])
            First75 = False

    plt.scatter(points, [0.25, 0.5, 0.75], color=colors[i], marker=markers[i])
    i += 1
plt.xlim([-0.5e7, 1e8])
plt.xlabel('Capacity')
plt.ylabel('ECDF')
plt.legend()
plt.show()



for FDPFSP in ['FDP', 'FSP']:
    fig, ax = plt.subplots()
    for x in range(len(measures)):
        if FDPFSP == 'FDP':
            plt.plot([-0.001, 0.6], [x, x], ':', color='gray', zorder=1)
        elif FDPFSP == 'FSP':
            plt.plot([-0.01, 1], [x, x], ':', color='gray', zorder=1)

    for i, MNO in zip(range(len(MNOs)), MNOs):
        data = []

        for measure in measures:
            filename = f'{municipality}{MNO}'
            filename = find_name(filename, measure)
            if FDPFSP == 'FDP':
                fdpfsp = util.from_data(f'data/Realisations/{filename}_totalfdp.p')
            else:
                fdpfsp = util.from_data(f'data/Realisations/{filename}_totalfsp.p')
            data.append(sum(fdpfsp)/len(fdpfsp))
        plt.scatter(data, range(len(measures)), label=name_MNO[i], color=colors[i], marker=markers[i])
    plt.xlabel(FDPFSP)
    # plt.yticks(range(len(measures)), [str('$p_{iso} = $' + str(measure)) for measure in measures])
    plt.yticks(range(len(measures)), [str('$r_{fail} = $' + str(measure)) for measure in measures])
    # plt.yticks(range(len(measures)), [str(str(measure) + '%') for measure in measures])

    if FDPFSP == 'FSP':
        plt.legend(loc='lower left')
    if FDPFSP == 'FDP':
        plt.legend(loc='lower right')        # plt.legend()
    ax.tick_params(top=False,
                   bottom=False,
                   left=False,
                   right=False,
                   labelleft=True,
                   labelbottom=True)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    plt.savefig(f'Figures/national_roaming{find_name(MNO, measure)}{FDPFSP}municipalities.png')
    plt.show()

