import matplotlib.pylab as pylab
import matplotlib.pyplot as plt

import util

params = {'legend.fontsize': 'x-large',
          'axes.labelsize': 'x-large',
          'axes.titlesize': 'x-large',
          'xtick.labelsize': 'x-large',
          'ytick.labelsize': 'x-large',
          'lines.markersize': 8,
          'figure.autolayout': True}
pylab.rcParams.update(params)

markers = ['o', 'X', 'v', 's', '*', 'P', '1', '+']

with_backup_fdp = {'Overijssel': [0.001212, 0.001276, 0.001299], 'Friesland': [0.0027824, 0.0030606, 0.0033200],
                   'Utrecht': [0.0002984, 0.0002984, 0.0006124], 'Amsterdam': [0.0002859, 0.0004289, 0.0005488],
                   'Middelburg': [0.0002687, 0.0004031, 0.0005123], 'Enschede': [0.0003346, 0.0006692, 0.0006232]}
with_backup_fsp = {'Overijssel': [0.617367, 0.683787, 0.622218], 'Friesland': [0.824708, 0.867696, 0.832534],
                   'Utrecht': [0.971501, 0.975082, 0.973546], 'Amsterdam': [0.933095, 0.939242, 0.938529],
                   'Middelburg': [0.936584, 0.942631, 0.941855], 'Enschede': [0.928508, 0.938546, 0.935812]}

fdp = {'Overijssel': [0.0128884, 0.0116123, 0.0614772], 'Friesland': [0.0178907, 0.0148287, 0.0809027],
       'Utrecht': [0.0148628, 0.0111954, 0.0643698], 'Amsterdam': [0.0224446, 0.0107219, 0.0622942],
       'Middelburg': [0.0210936, 0.0100766, 0.0601947], 'Enschede': [0.0206335, 0.0105956, 0.0558787]}
fsp = {'Overijssel': [0.693102, 0.760225, 0.629319], 'Friesland': [0.647172, 0.753685, 0.624300],
       'Utrecht': [0.720640, 0.807114, 0.706517], 'Amsterdam': [0.701644, 0.828449, 0.807903],
       'Middelburg': [0.713691, 0.838372, 0.815830], 'Enschede': [0.709458, 0.827013, 0.802243]}

cities = ['Overijssel', 'Friesland', 'Utrecht']
# cities = ['Amsterdam', 'Middelburg', 'Enschede']
MNOs = ['KPN', 'T-Mobile', 'Vodafone']

positions = [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20]

delta = 0.1

pos = {'KPN': [1, 8, 15], 'T-Mobile': [3, 10, 17], 'Vodafone': [5, 12, 19]}
pos_NR = {'KPN': [2 - delta, 9 - delta, 16 - delta], 'T-Mobile': [4 - delta, 11 - delta, 18 - delta],
          'Vodafone': [6 - delta, 13 - delta, 20 - delta]}

xticks = [3.5, 10.5, 17.5]

patterns = ["///", "O", "|", "-", "+", "x", "o", "O", ".", "*"]

fig, ax = plt.subplots()
First = True
for MNO, i in zip(MNOs, range(len(MNOs))):
    vals = [v[i] for k, v in fdp.items() if k in cities]
    if First:
        plt.bar(pos[MNO], vals, color=util.get_bar_color(i), edgecolor=util.get_bar_color(i), alpha=0.5,
                hatch=patterns[0], label='Normal')
        First = False
    else:
        plt.bar(pos[MNO], vals, color=util.get_bar_color(i), edgecolor=util.get_bar_color(i), alpha=0.5,
                hatch=patterns[0])

First = True
for MNO, i in zip(MNOs, range(len(MNOs))):
    vals = [v[i] for k, v in with_backup_fdp.items() if k in cities]
    if First:
        plt.bar(pos_NR[MNO], vals, color=util.get_bar_color(i), edgecolor=util.get_bar_color(i), alpha=0.5,
                hatch=patterns[1], label='Back-up')
        First = False
    else:
        plt.bar(pos_NR[MNO], vals, color=util.get_bar_color(i), edgecolor=util.get_bar_color(i), alpha=0.5,
                hatch=patterns[1])

legend = ax.legend()
handles = legend.legendHandles

# There are many more hatches available in matplotlib
for i, handle in enumerate(handles):
    handle.set_edgecolor("gray")
    handle.set_facecolor('gray')
    handle.set_hatch(patterns[i])

plt.xticks(xticks, cities)
plt.ylabel('FDP')
plt.savefig('Figures/improvement_fdp_full_backup.pdf', dpi=1000)
plt.show()

fig, ax = plt.subplots()
First = True
for MNO, i in zip(MNOs, range(len(MNOs))):
    vals = [v[i] for k, v in fsp.items() if k in cities]
    if First:
        plt.bar(pos[MNO], vals, color=util.get_bar_color(i), edgecolor=util.get_bar_color(i), alpha=0.5,
                hatch=patterns[0], label='Normal')
        First = False
    else:
        plt.bar(pos[MNO], vals, color=util.get_bar_color(i), edgecolor=util.get_bar_color(i), alpha=0.5,
                hatch=patterns[0])

First = True
for MNO, i in zip(MNOs, range(len(MNOs))):
    vals = [v[i] for k, v in with_backup_fsp.items() if k in cities]
    if First:
        plt.bar(pos_NR[MNO], vals, color=util.get_bar_color(i), edgecolor=util.get_bar_color(i), alpha=0.5,
                hatch=patterns[1], label='Back-up')
        First = False
    else:
        plt.bar(pos_NR[MNO], vals, color=util.get_bar_color(i), edgecolor=util.get_bar_color(i), alpha=0.5,
                hatch=patterns[1])

legend = ax.legend()
handles = legend.legendHandles

# There are many more hatches available in matplotlib
for i, handle in enumerate(handles):
    handle.set_edgecolor("gray")
    handle.set_facecolor('gray')
    handle.set_hatch(patterns[i])

plt.xticks(xticks, cities)
plt.ylabel('FSP')
plt.savefig('Figures/improvement_fsp_full_backup.pdf', dpi=1000)
plt.show()
