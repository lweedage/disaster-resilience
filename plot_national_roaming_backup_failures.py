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

NR_fallback_failure_fdp = {'Middelburg': [0.00026246719160104987, 0.0, 0.0],
                           'Enschede': [0.0005903187721369539, 0.0005312868949232586, 0.0008854781582054309],
                           'Amsterdam': [0.0013696808510638297, 0.0011303191489361701, 0.0014228723404255319]
                           }

NR_fallback_failure_fsp = {'Middelburg': [0.8139107611548556, 0.8094488188976378, 0.8918635170603675],
                           'Enschede': [0.7276269185360095, 0.6527744982290437, 0.7966942148760331],
                           'Amsterdam': [0.6911436170212766, 0.6697606382978724, 0.7645079787234043]}

NR_full_failure_fdp = {'Middelburg': [0.00026246719160104987, 0.0, 0.0],
                       'Enschede': [0.0005903187721369539, 0.0005312868949232586, 0.0008854781582054309],
                       'Amsterdam': [0.0013696808510638297, 0.0011303191489361701, 0.0014228723404255319]}

NR_full_failure_fsp = {'Middelburg': [0.9595800524934384, 0.9729658792650918, 0.9666666666666667],
                       'Enschede': [0.8946871310507674, 0.925383707201889, 0.9127508854781582],
                       'Amsterdam': [0.8720345744680851, 0.9118617021276596, 0.9051462765957446]}

no_cooperation_failure_fdp = {'Middelburg': [0.0005249343832020997, 0.0007874015748031496, 0.013385826771653543],
                              'Enschede': [0.005608028335301062, 0.004545454545454545, 0.02066115702479339],
                              'Amsterdam': [0.0398936170212766, 0.013829787234042552, 0.06502659574468085]}

no_cooperation_failure_fsp = {'Middelburg': [0.8711286089238846, 0.9553805774278216, 0.8564304461942257],
                              'Enschede': [0.7604486422668241, 0.8615702479338843, 0.626741440377804],
                              'Amsterdam': [0.6914095744680852, 0.8105186170212766, 0.6179654255319149]}

# cities = ['Overijssel', 'Friesland', 'Utrecht']
cities = ['Middelburg', 'Enschede', 'Amsterdam']
MNOs = ['KPN', 'T-Mobile', 'Vodafone']

positions = [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20]

delta = 0.1

pos = {'KPN': [1, 8, 15], 'T-Mobile': [3, 10, 17], 'Vodafone': [5, 12, 19]}
pos_NR = {'KPN': [2 - delta, 9 - delta, 16 - delta], 'T-Mobile': [4 - delta, 11 - delta, 18 - delta],
          'Vodafone': [6 - delta, 13 - delta, 20 - delta]}

xticks = [3.5, 10.5, 17.5]

patterns = ["///", "O", "|", "-", "+", "x", "o", "O", ".", "*"]

FDPFSP = 'FDP'
labels = ['no cooperation', 'NR-full', 'NR-fallback', 'NR-fallback-QOS']

max_x = 0.2

fig, ax = plt.subplots()
for x in range(len(cities)):
    plt.plot([-0.001, max_x], [x - 0.2, x - 0.2], ':', color='gray', alpha=0.5, zorder=1)
    plt.plot([-0.001, max_x], [x, x], ':', color='gray', alpha=0.5, zorder=1)
    plt.plot([-0.001, max_x], [x + 0.2, x + 0.2], ':', color='gray', alpha=0.5, zorder=1)

y_axes = {'KPN': [i + 0.2 for i in range(len(cities))], 'T-Mobile': [i for i in range(len(cities))],
          'Vodafone': [i - 0.2 for i in range(len(cities))]}

for i, data in zip(range(3), [no_cooperation_failure_fdp, NR_full_failure_fdp, NR_fallback_failure_fdp]):
    for j in range(len(MNOs)):
        vals = [v[j] for k, v in data.items() if k in cities]
        if j == 0:
            plt.scatter(vals, y_axes[MNOs[j]], color=util.get_color(i), alpha=0.5, marker=markers[i], label=labels[i])
        else:
            plt.scatter(vals, y_axes[MNOs[j]], color=util.get_color(i), alpha=0.5, marker=markers[i])

plt.xlabel(FDPFSP)
plt.yticks(range(len(cities)), cities)

ax2 = ax.twinx()
ax2.set_yticks(sorted(y_axes['KPN'] + y_axes['T-Mobile'] + y_axes['Vodafone']), ['$MNO_3$', '$MNO_2$', '$MNO_1$'] * 3)

if FDPFSP == 'FSP':
    ax.legend(loc='lower left')
if FDPFSP == 'FDP':
    ax.legend(loc='lower right')

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

ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax2.spines['bottom'].set_visible(False)

ax.set_ylim([0 - 0.3, 2 + 0.3])
ax2.set_ylim([0 - 0.3, 2 + 0.3])

if 'Enschede' in cities:
    plt.savefig(f'Figures/{FDPFSP}with_fallback_failure_cities.pdf', dpi=1000, transparent=True)
else:
    plt.savefig(f'Figures/{FDPFSP}with_fallback_failure_provinces.pdf', dpi=1000, transparent=True)
plt.show()

FDPFSP = 'FSP'
fig, ax = plt.subplots()
min_x = 0.

for x in range(len(cities)):
    plt.plot([min_x, 1.0], [x - 0.2, x - 0.2], ':', color='gray', alpha=0.5, zorder=1)
    plt.plot([min_x, 1.0], [x, x], ':', color='gray', alpha=0.5, zorder=1)
    plt.plot([min_x, 1.0], [x + 0.2, x + 0.2], ':', color='gray', alpha=0.5, zorder=1)

y_axes = {'KPN': [i + 0.2 for i in range(len(cities))], 'T-Mobile': [i for i in range(len(cities))],
          'Vodafone': [i - 0.2 for i in range(len(cities))]}

for i, data in zip(range(3), [no_cooperation_failure_fsp, NR_full_failure_fsp, NR_fallback_failure_fsp]):
    for j in range(len(MNOs)):
        vals = [v[j] for k, v in data.items() if k in cities]
        if j == 0:
            plt.scatter(vals, y_axes[MNOs[j]], color=util.get_color(i), alpha=0.5, marker=markers[i], label=labels[i])
        else:
            plt.scatter(vals, y_axes[MNOs[j]], color=util.get_color(i), alpha=0.5, marker=markers[i])

plt.xlabel(FDPFSP)
plt.yticks(range(len(cities)), cities)

ax2 = ax.twinx()
ax2.set_yticks(sorted(y_axes['KPN'] + y_axes['T-Mobile'] + y_axes['Vodafone']), ['$MNO_3$', '$MNO_2$', '$MNO_1$'] * 3)

print(sorted(y_axes['KPN'] + y_axes['T-Mobile'] + y_axes['Vodafone']))

if FDPFSP == 'FSP':
    ax.legend(loc='upper left')
if FDPFSP == 'FDP':
    ax.legend(loc='lower right')

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

ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax2.spines['bottom'].set_visible(False)

ax.set_ylim([0 - 0.3, 2 + 0.3])
ax2.set_ylim([0 - 0.3, 2 + 0.3])

if 'Enschede' in cities:
    plt.savefig(f'Figures/{FDPFSP}with_fallback_failure_cities.pdf', dpi=1000, transparent=True)
else:
    plt.savefig(f'Figures/{FDPFSP}with_fallback_failure_provinces.pdf', dpi=1000, transparent=True)

plt.show()
