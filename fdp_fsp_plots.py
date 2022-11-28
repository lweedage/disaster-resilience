import geopandas as gpd
import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
import numpy as np

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

#
provinces = list(reversed(['Drenthe', 'Flevoland', 'Friesland', 'Gelderland', 'Groningen', 'Limburg', 'Noord-Brabant',
                           'Noord-Holland', 'Overijssel', 'Utrecht', 'Zeeland', 'Zuid-Holland']))
municipalities = ['Middelburg', 'Maastricht', 'Groningen', 'Enschede', 'Emmen', 'Elburg',
                  'Eindhoven', "'s-Gravenhage", 'Amsterdam', 'Almere']
municipalities2 = ['Middelburg', 'Maastricht', 'Groningen', 'Enschede', 'Emmen', 'Elburg',
                   'Eindhoven', "Den Haag", 'Amsterdam', 'Almere']

MNOs = ['KPN', 'T-Mobile', 'Vodafone', 'all_MNOs']
name_MNO = ['MNO-1', 'MNO-2', 'MNO-3', 'National roaming']
#

Disaster = False
Random = False
User = False

radii = [0, 500, 1000, 2500]
increases = [0, 50, 100, 200]
random = [0, 0.05, 0.1, 0.25, 0.5]

province = 'Drenthe'


def find_name(filename, radius):
    if radius == 0:
        return filename
    if Disaster:
        filename += 'disaster' + str(radius)
    elif User:
        filename += 'user_increase' + str(radius)
    elif Random:
        filename += 'random' + str(radius)
    return filename


FSP, FDP, SAT = {MNO: [] for MNO in MNOs}, {MNO: [] for MNO in MNOs}, {MNO: [] for MNO in MNOs}
users = {MNO: [] for MNO in MNOs}

if Disaster:
    measures = radii
elif User:
    measures = increases
elif Random:
    measures = random
else:
    measures = [0]

for measure in measures:
    for FDPFSP in ['FDP', 'FSP']:
        fig, ax = plt.subplots()
        for x in range(len(provinces)):
            if FDPFSP == 'FDP':
                plt.plot([-0.001, 0.25], [x, x], ':', color='gray', alpha = 0.5, zorder=1)
            elif FDPFSP == 'FSP':
                plt.plot([0, 1.01], [x, x], ':', color='gray', alpha = 0.5, zorder=1)

        for i, MNO in zip(range(len(MNOs)), MNOs):
            filename = f'{MNO}'
            filename = find_name(filename, measure)
            df = gpd.read_file(f'converted_data/{filename}_provinces.shp')
            print(min(list(reversed(df[FDPFSP].astype('float')))), max(list(reversed(df[FDPFSP].astype('float')))), MNO)
            plt.scatter(list(reversed(df[FDPFSP].astype('float'))), range(len(provinces)), label=name_MNO[i],
                        color=util.get_color(i), alpha=0.5, marker=markers[i])
        plt.xlabel(FDPFSP)
        plt.yticks(range(len(provinces)), provinces)
        if FDPFSP == 'FSP':
            plt.legend(loc='center left')
        if FDPFSP == 'FDP':
            plt.legend(loc='lower right')
        # plt.legend()
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
        # for pos in ['right', 'top', 'left', 'bottom']:
        #     ax.spines[pos].set_color('white')
        # ax.xaxis.label.set_color('white')
        # ax.yaxis.label.set_color('white')
        # ax.tick_params(colors='white')

        plt.savefig(f'Figures/{FDPFSP}provinces.pdf', dpi=1000, transparent=True)
        plt.show()

        fig, ax = plt.subplots()
        for x in range(len(municipalities)):
            if FDPFSP == 'FDP':
                plt.plot([-0.001, 0.3], [x, x], ':', color='gray', alpha = 0.5, zorder=1)
            elif FDPFSP == 'FSP':
                plt.plot([0.25, 1.01], [x, x], ':', color='gray', alpha = 0.5, zorder=1)

        for i, MNO in zip(range(len(MNOs)), MNOs):
            filename = f'{MNO}'
            filename = find_name(filename, measure)
            print(filename)
            df = util.from_data(f'converted_data/{filename}_municipalities.p')
            df = df[df['area'].isin(municipalities)]
            plt.scatter(list(df[FDPFSP].astype('float')), range(len(municipalities)), label=name_MNO[i],
                        color=util.get_color(i), alpha=0.5, marker=markers[i])
        plt.xlabel(FDPFSP)
        plt.yticks(range(len(municipalities)), municipalities2)
        if FDPFSP == 'FSP':
            plt.legend(loc='lower left')
        if FDPFSP == 'FDP':
            plt.legend(loc='lower right')  # plt.legend()
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
        # for pos in ['right', 'top', 'left', 'bottom']:
        #     ax.spines[pos].set_color('white')
        # ax.xaxis.label.set_color('white')
        # ax.yaxis.label.set_color('white')
        # ax.tick_params(colors='white')

        plt.savefig(f'Figures/{FDPFSP}municipalities.pdf', dpi=1000, transparent=True)
        plt.show()

    dataFDP, dataFSP = [], []
    filename = find_name('all_MNOs', measure)
    df = util.from_data(f'converted_data/{filename}_municipalities.p')
    nationalroaming_FDP = df['FDP'].astype('float')
    nationalroaming_FSP = df['FSP'].astype('float')

    for MNO in MNOs[:-1]:
        filename = f'{MNO}'
        filename = find_name(filename, measure)
        df = util.from_data(f'converted_data/{filename}_municipalities.p')

        dataFDP.append(df['FDP'].astype('float') - nationalroaming_FDP)
        dataFSP.append(nationalroaming_FSP - df['FSP'].astype('float'))

    x = np.array([1, 2, 3])

    fig, ax = plt.subplots()
    fdplot = ax.boxplot(dataFDP, positions=x - 0.17, widths=0.3, patch_artist=True, showfliers=False)
    fsplot = ax.boxplot(dataFSP, positions=x + 0.17, widths=0.3, patch_artist=True, showfliers=False)
    print([min(lijst) for lijst in dataFSP])
    print([max(lijst) for lijst in dataFSP])

    for patch in fdplot['boxes']:
        patch.set_facecolor((0.2549019607843137, 0.4117647058823529, 0.8823529411764706, 0.5))
    for patch in fsplot['boxes']:
        patch.set_facecolor((1.0, 0.4980392156862745, 0.3137254901960784, 0.5))

    ax.legend([fdplot["boxes"][0], fsplot["boxes"][0]], ['$\Delta$ FDP', '$\Delta$ FSP'])
    plt.xticks(x, name_MNO[:-1])
    # plt.yticks([0.0, 0.25, 0.50, 0.75, 1.0])
    plt.ylabel('Difference with national roaming')
    plt.savefig('Figures/municipality_difference.pdf', dpi=1000)
    plt.show()

    dataFDP, dataFSP = [], []
    filename = find_name('all_MNOs', measure)
    df = gpd.read_file(f'converted_data/{filename}_provinces.shp')

    nationalroaming_FDP = df['FDP'].astype('float')
    nationalroaming_FSP = df['FSP'].astype('float')

    for MNO in MNOs[:-1]:
        filename = f'{MNO}'
        filename = find_name(filename, measure)

        df = gpd.read_file(f'converted_data/{filename}_provinces.shp')

        dataFDP.append(df['FDP'].astype('float') - nationalroaming_FDP)
        dataFSP.append(nationalroaming_FSP - df['FSP'].astype('float'))

    x = np.array([1, 2, 3])

    fig, ax = plt.subplots()
    fdplot = ax.boxplot(dataFDP, positions=x - 0.17, widths=0.3, patch_artist=True, showfliers=False)
    fsplot = ax.boxplot(dataFSP, positions=x + 0.17, widths=0.3, patch_artist=True, showfliers=False)

    for patch in fdplot['boxes']:
        patch.set_facecolor((0.2549019607843137, 0.4117647058823529, 0.8823529411764706, 0.5))
    for patch in fsplot['boxes']:
        patch.set_facecolor((1.0, 0.4980392156862745, 0.3137254901960784, 0.5))

    ax.legend([fdplot["boxes"][0], fsplot["boxes"][0]], ['$\Delta$ FDP', '$\Delta$ FSP'])
    plt.xticks(x, name_MNO[:-1])
    # plt.yticks([0.0, 0.25, 0.50, 0.75, 1.0])
    plt.ylabel('Difference with national roaming')
    plt.savefig('Figures/province_difference.pdf', dpi=1000)
    plt.show()
