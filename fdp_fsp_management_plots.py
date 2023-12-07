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
          'figure.autolayout': True,
          'figure.figsize': [9,4]}
pylab.rcParams.update(params)

markers = ['o', 'X', 'v', 's', '*', 'P', '1', '+']

max_iterations = 20
# municipalities = ['Middelburg', 'Enschede', 'Amsterdam']
municipalities = ['Amsterdam']
areas = ['AreaType.RMA', 'AreaType.UMA', 'AreaType.UMI']
technologies = ['BaseStationRadioType.NR', 'BaseStationRadioType.LTE', 'BaseStationRadioType.UMTS']
MNOs = ['KPN', 'T-Mobile', 'Vodafone']
MNOsplus = ['KPN', 'T-Mobile', 'Vodafone', 'total']

fsp = dict()
fdp = dict()

max_iterations = 20

for municipality in municipalities:
    fsp[municipality] = dict()
    fdp[municipality] = dict()
    i = util.from_data(f'data/Realisations/{municipality}all_MNOs0.021{max_iterations}_fdp_per_MNO.p')
    j = util.from_data(f'data/Realisations/{municipality}all_MNOs0.021{max_iterations}_fsp_per_MNO.p')
    area = 'full'
    fsp[municipality][area] = dict()
    fdp[municipality][area] = dict()
    for mno in MNOs:
        fdp[municipality][area][mno] = []
        fsp[municipality][area][mno] = []
        size = int(np.size(i[mno]) / max_iterations)
        for iter in range(max_iterations):
            fdp[municipality][area][mno].append(sum(i[mno][iter * size:(iter + 1) * size]) / size)
            fsp[municipality][area][mno].append(sum(j[mno][iter * size:(iter + 1) * size]) / size)
    fdp[municipality][area]['total'] = util.from_data(
        f'data/Realisations/{municipality}all_MNOs0.021{max_iterations}_totalfdp.p')
    fsp[municipality][area]['total'] = util.from_data(
        f'data/Realisations/{municipality}all_MNOs0.021{max_iterations}_totalfsp.p')

    for area in areas + technologies:
        fsp[municipality][area] = dict()
        fdp[municipality][area] = dict()
        i = util.from_data(f'data/Realisations/{municipality}all_MNOs0.021{area}{max_iterations}_fdp_per_MNO.p')
        j = util.from_data(f'data/Realisations/{municipality}all_MNOs0.021{area}{max_iterations}_fsp_per_MNO.p')
        for mno in MNOs:
            fdp[municipality][area][mno] = []
            fsp[municipality][area][mno] = []
            size = int(np.size(i[mno]) / max_iterations)
            for iter in range(max_iterations):
                fdp[municipality][area][mno].append(sum(i[mno][iter * size:(iter + 1) * size]) / size)
                fsp[municipality][area][mno].append(sum(j[mno][iter * size:(iter + 1) * size]) / size)

        fdp[municipality][area]['total'] = util.from_data(
            f'data/Realisations/{municipality}all_MNOs0.021{area}{max_iterations}_totalfdp.p')
        fsp[municipality][area]['total'] = util.from_data(
            f'data/Realisations/{municipality}all_MNOs0.021{area}{max_iterations}_totalfsp.p')

data_fsp, data_fdp = dict(), dict()

for area in areas + technologies + ['full']:
    data_fsp[area] = [fsp[municipality][area][mno] for mno in MNOsplus]
    data_fdp[area] = [fdp[municipality][area][mno] for mno in MNOsplus]

util.to_data(data_fsp, f'{municipality}management_data-fsp.p')
util.to_data(data_fdp, f'{municipality}management_data-fdp.p')
print(municipality)

# data_fsp = util.from_data(f'{municipality}management_data-fsp.p')
# data_fdp = util.from_data(f'{municipality}management_data-fdp.p')

name_MNO = ['MNO-1', 'MNO-2', 'MNO-3', 'total']

x = np.array([2, 4, 6, 8])
box_width = 0.25

fig, ax = plt.subplots()

x_aux = np.array([x[0] + 1.5 * box_width, x[1] + 3 * box_width, x[2] + 4.5 * box_width, x[3] + 6 * box_width])
pos1 = [x_aux[0] - 2.25 * box_width, x_aux[1] - 2.25 * box_width, x_aux[2] - 2.25 * box_width,
        x_aux[3] - 2.25 * box_width]
pos2 = [x_aux[0] - 0 * box_width, x_aux[1] - 0 * box_width, x_aux[2] - 0 * box_width,
        x_aux[3] - 0 * box_width]
pos3 = [x_aux[0] + 0.75 * box_width, x_aux[1] + 0.75 * box_width, x_aux[2] + 0.75 * box_width,
        x_aux[3] + 0.75 * box_width]
pos4 = [x_aux[0] + 2.25 * box_width, x_aux[1] + 2.25 * box_width, x_aux[2] + 2.25 * box_width,
        x_aux[3] + 2.25 * box_width]

plot1 = ax.boxplot(data_fsp['AreaType.RMA'], positions=pos1, widths=box_width, patch_artist=True, showfliers=False)
plot2 = ax.boxplot(data_fsp['AreaType.UMA'], positions=pos2, widths=box_width, patch_artist=True, showfliers=False)
plot4 = ax.boxplot(data_fsp['full'], positions=pos4, widths=box_width, patch_artist=True, showfliers=False)

ax.axvspan((x_aux[0] + x_aux[1]) / 2, (x_aux[1] + x_aux[2]) / 2, color='#CCC', alpha=0.2, lw=0)
ax.axvspan((x_aux[2] + x_aux[3]) / 2, x_aux[3] + 1 + 0.75 * box_width, color='#CCC', alpha=0.2, lw=0)

for patch in plot1['boxes'] + plot1['whiskers'] + plot1['caps']:
    patch.set(color=util.get_boxplot_color(0))
for patch in plot2['boxes'] + plot2['whiskers'] + plot2['caps']:
    patch.set(color=util.get_boxplot_color(1))
for patch in plot4['boxes'] + plot4['whiskers'] + plot4['caps']:
    patch.set(color=util.get_boxplot_color(3))

ax.legend([plot1["boxes"][0], plot2["boxes"][0], plot4["boxes"][0]], ['Only RMa', 'Only UMa',  'RMa and UMa'])
plt.xticks(x_aux, name_MNO)
plt.ylabel('FSP')
plt.savefig(f'Figures/FSP_areas_{municipality}.pdf', dpi=1000)
plt.show()

fig, ax = plt.subplots()

plot1 = ax.boxplot(data_fdp['AreaType.RMA'], positions=pos1, widths=box_width, patch_artist=True, showfliers=False)
plot2 = ax.boxplot(data_fdp['AreaType.UMA'], positions=pos2, widths=box_width, patch_artist=True, showfliers=False)
plot4 = ax.boxplot(data_fdp['full'], positions=pos4, widths=box_width, patch_artist=True, showfliers=False)

ax.axvspan((x_aux[0] + x_aux[1]) / 2, (x_aux[1] + x_aux[2]) / 2, color='#CCC', alpha=0.2, lw=0)
ax.axvspan((x_aux[2] + x_aux[3]) / 2, x_aux[3] + 1 + 0.75 * box_width, color='#CCC', alpha=0.2, lw=0)

for patch in plot1['boxes'] + plot1['whiskers'] + plot1['caps']:
    patch.set(color=util.get_boxplot_color(0))
for patch in plot2['boxes'] + plot2['whiskers'] + plot2['caps']:
    patch.set(color=util.get_boxplot_color(1))

for patch in plot4['boxes'] + plot4['whiskers'] + plot4['caps']:
    patch.set(color=util.get_boxplot_color(3))

ax.legend([plot1["boxes"][0], plot2["boxes"][0], plot4["boxes"][0]], ['Only RMa', 'Only UMa',  'RMa and UMa'])
plt.xticks(x_aux, name_MNO)
plt.ylabel('FDP')
plt.savefig(f'Figures/FDP_areas_{municipality}.pdf', dpi=1000)
plt.show()

fig, ax = plt.subplots()
pos1 = [x_aux[0] - 2.25 * box_width, x_aux[1] - 2.25 * box_width, x_aux[2] - 2.25 * box_width,
        x_aux[3] - 2.25 * box_width]
pos2 = [x_aux[0] - 0.75 * box_width, x_aux[1] - 0.75 * box_width, x_aux[2] - 0.75 * box_width,
        x_aux[3] - 0.75 * box_width]
pos3 = [x_aux[0] + 0.75 * box_width, x_aux[1] + 0.75 * box_width, x_aux[2] + 0.75 * box_width,
        x_aux[3] + 0.75 * box_width]
pos4 = [x_aux[0] + 2.25 * box_width, x_aux[1] + 2.25 * box_width, x_aux[2] + 2.25 * box_width,
        x_aux[3] + 2.25 * box_width]


plot1 = ax.boxplot(data_fsp['BaseStationRadioType.NR'], positions=pos1, widths=box_width, patch_artist=True,
                   showfliers=False)
plot2 = ax.boxplot(data_fsp['BaseStationRadioType.LTE'], positions=pos2, widths=box_width, patch_artist=True,
                   showfliers=False)
plot3 = ax.boxplot(data_fsp['BaseStationRadioType.UMTS'], positions=pos3, widths=box_width, patch_artist=True,
                   showfliers=False)
plot4 = ax.boxplot(data_fsp['full'], positions=pos4, widths=box_width, patch_artist=True, showfliers=False)

ax.axvspan((x_aux[0] + x_aux[1]) / 2, (x_aux[1] + x_aux[2]) / 2, color='#CCC', alpha=0.2, lw=0)
ax.axvspan((x_aux[2] + x_aux[3]) / 2, x_aux[3] + 1 + 0.75 * box_width, color='#CCC', alpha=0.2, lw=0)

for patch in plot1['boxes'] + plot1['whiskers'] + plot1['caps']:
    patch.set(color=util.get_boxplot_color(0))
for patch in plot2['boxes'] + plot2['whiskers'] + plot2['caps']:
    patch.set(color=util.get_boxplot_color(1))
for patch in plot3['boxes'] + plot3['whiskers'] + plot3['caps']:
    patch.set(color=util.get_boxplot_color(2))
for patch in plot4['boxes'] + plot4['whiskers'] + plot4['caps']:
    patch.set(color=util.get_boxplot_color(3))

ax.legend([plot3["boxes"][0], plot2["boxes"][0], plot1["boxes"][0], plot4["boxes"][0]], ['Only 3G', 'Only 4G', 'Only 5G', '3G, 4G and 5G'])
plt.xticks(x_aux, name_MNO)
plt.ylabel('FSP')
plt.savefig(f'Figures/FSP_technologies_{municipality}.pdf', dpi=1000)
plt.show()

fig, ax = plt.subplots()

plot1 = ax.boxplot(data_fdp['BaseStationRadioType.NR'], positions=pos1, widths=box_width, patch_artist=True,
                   showfliers=False)
plot2 = ax.boxplot(data_fdp['BaseStationRadioType.LTE'], positions=pos2, widths=box_width, patch_artist=True,
                   showfliers=False)
plot3 = ax.boxplot(data_fdp['BaseStationRadioType.UMTS'], positions=pos3, widths=box_width, patch_artist=True,
                   showfliers=False)
plot4 = ax.boxplot(data_fdp['full'], positions=pos4, widths=box_width, patch_artist=True, showfliers=False)

ax.axvspan((x_aux[0] + x_aux[1]) / 2, (x_aux[1] + x_aux[2]) / 2, color='#CCC', alpha=0.2, lw=0)
ax.axvspan((x_aux[2] + x_aux[3]) / 2, x_aux[3] + 1 + 0.75 * box_width, color='#CCC', alpha=0.2, lw=0)

for patch in plot1['boxes'] + plot1['whiskers'] + plot1['caps']:
    patch.set(color=util.get_boxplot_color(0))
for patch in plot2['boxes'] + plot2['whiskers'] + plot2['caps']:
    patch.set(color=util.get_boxplot_color(1))
for patch in plot3['boxes'] + plot3['whiskers'] + plot3['caps']:
    patch.set(color=util.get_boxplot_color(2))
for patch in plot4['boxes'] + plot4['whiskers'] + plot4['caps']:
    patch.set(color=util.get_boxplot_color(3))

ax.legend([plot3["boxes"][0], plot2["boxes"][0], plot1["boxes"][0], plot4["boxes"][0]], ['Only 3G', 'Only 4G', 'Only 5G', '3G, 4G and 5G'])
plt.xticks(x_aux, name_MNO)
plt.ylabel('FDP')
plt.savefig(f'Figures/FDP_technologies_{municipality}.pdf', dpi=1000)
plt.show()
