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

NR_full_fdp = {'Overijssel': [0.0034429563144239535, 0.003015216324240937, 0.003421919921464133],
               'Friesland': [0.004220077776177445, 0.003965624849968793, 0.004220077776177445],
               'Utrecht': [0.0035023297435739192, 0.003252383744252785, 0.003505415496651958],
               'Middelburg': [0.0, 0.0, 0.0],
               'Enschede': [0.004722550177095631, 0.004722550177095631, 0.005726092089728453],
               'Amsterdam': [0.0025, 0.002792553191489362, 0.0025930851063829786]}

NR_full_fsp = {'Overijssel': [0.7853797068929248, 0.8439730734170114, 0.8288899796648201],
               'Friesland': [0.7759277929809401, 0.8373805751596332, 0.8228815593643478],
               'Utrecht': [0.836442743851637, 0.8818835436788348, 0.8721017064214521],

               'Middelburg': [0.9661417322834646, 0.9753280839895013, 0.9750656167979003],
               'Enschede': [0.8706021251475797, 0.9028335301062573, 0.8999409681227863],
               'Amsterdam': [0.8898803191489362, 0.9166489361702128, 0.9163563829787233]
               }

NR_fallback_fdp = {'Middelburg': [0.0, 0.0005249343832020997, 0.0],
                   'Enschede': [0.0018890200708382527, 0.0010625737898465172, 0.001652892561983471],
                   'Amsterdam': [0.004462753175420529, 0.004085135599038792, 0.003913491246138002],

                   'Overijssel': [0.0017810812705981347, 0.0016688871748124256, 0.0016969356987588528],
                   'Friesland': [0.002592539248163618, 0.0026501512314561428, 0.002582937250948197],
                   'Utrecht': [0.0019532816983984943, 0.002008825253803191, 0.0018977381429937977]}

NR_fallback_fsp = {'Middelburg': [0.8083989501312336, 0.8288713910761155, 0.9002624671916011],
                   'Enschede': [0.7212514757969304, 0.6762691853600945, 0.8208972845336482],
                   'Amsterdam': [0.672605561277034, 0.720871953312736, 0.7412289735667696],

                   'Overijssel': [0.6250473318841596, 0.5747142556622957, 0.6852394642731926],
                   'Friesland': [0.5889144942147967, 0.5883815833693409, 0.6792692880119064],
                   'Utrecht': [0.7226586848520381, 0.7258246675101059, 0.7840651711050082]}

no_cooperation_fdp = {'Middelburg': [0.002362204724409449, 0.001837270341207349, 0.01889763779527559],
                      'Enschede': [0.01576151121605667, 0.01357733175914994, 0.03524203069657615],
                      'Amsterdam': [0.021023936170212768, 0.011888297872340426, 0.05227393617021277],

                      'Overijssel': [0.014276698688731505, 0.011836477105392328, 0.05137087160788163],
                      'Friesland': [0.020874741946324837, 0.015243170579480532, 0.06814057323923375],
                      'Utrecht': [0.017255531212392386, 0.011861634831980744, 0.053719875335575644]}
no_cooperation_fsp = {'Middelburg': [0.9102362204724409, 0.973753280839895, 0.9136482939632546],
                      'Enschede': [0.7530106257378985, 0.8533648170011806, 0.6585596221959858],
                      'Amsterdam': [0.742061170212766, 0.8501994680851064, 0.6776994680851064],
                      'Overijssel': [0.70194236028329, 0.7646448355655283, 0.6060374447794685],
                      'Friesland': [0.6588842479235681, 0.7576215852897402, 0.6048009986077104],
                      'Utrecht': [0.7367358903940506, 0.8143950381090506, 0.6777794920850434]}

two_NR_fallback_fdp = {'Middelburg': [0.002047244094488189, 0.00010532136180520814, 5.2401289071711164e-05],
                       'Enschede': [0.015572609208972845, 0.001871195433335702, 0.0017327039021199102],
                       'Amsterdam': [0.04600531914893617, 0.0009222014322815877, 0.000866684540099755],

                       'Overijssel': [0.013843348993759204, 0.001734099992987869, 0.0017691606479209032],
                       'Friesland': [0.020011042296797735, 0.002187815065533631, 0.0022151807575975803],
                       'Utrecht': [0.016668003826333818, 0.001676798222606227, 0.0017064214521553985]}

two_NR_fallback_fsp = {'Middelburg': [0.916246719160105, 0.9928644777376971, 0.9914585898813111],
                       'Enschede': [0.7574557260920898, 0.9536050119614392, 0.9437224844852278],
                       'Amsterdam': [0.6666582446808511, 0.9607190235074617, 0.9570400533017628],

                       'Overijssel': [0.7011548979734942, 0.5994733889629058, 0.7087427249141014],
                       'Friesland': [0.6585572999183831, 0.697985020884344, 0.7657520764318978],
                       'Utrecht': [0.7354383312247353, 0.8008609251087728, 0.8434208658623137]}

cities = ['Overijssel', 'Friesland', 'Utrecht']
cities = ['Middelburg', 'Enschede', 'Amsterdam']  # , 'Utrecht', 'Overijssel', 'Friesland']
MNOs = ['KPN', 'T-Mobile', 'Vodafone']

positions = [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20]

delta = 0.1

pos = {'KPN': [1, 8, 15], 'T-Mobile': [3, 10, 17], 'Vodafone': [5, 12, 19]}
pos_NR = {'KPN': [2 - delta, 9 - delta, 16 - delta], 'T-Mobile': [4 - delta, 11 - delta, 18 - delta],
          'Vodafone': [6 - delta, 13 - delta, 20 - delta]}

xticks = [3.5, 10.5, 17.5]

patterns = ["///", "O", "|", "-", "+", "x", "o", "O", ".", "*"]

# fig, ax = plt.subplots()
# First = True
# for MNO, i in zip(MNOs, range(len(MNOs))):
#     vals = [v[i] for k, v in no_cooperation_fdp.items() if k in cities]
#     if First:
#         plt.bar(pos[MNO], vals, color=util.get_bar_color(i), edgecolor=util.get_bar_color(i), alpha=0.5,
#                 hatch=patterns[0], label='Normal')
#         First = False
#     else:
#         plt.bar(pos[MNO], vals, color=util.get_bar_color(i), edgecolor=util.get_bar_color(i), alpha=0.5,
#                 hatch=patterns[0])
#
# First = True
# for MNO, i in zip(MNOs, range(len(MNOs))):
#     vals = [v[i] for k, v in NR_full_fdp.items() if k in cities]
#     if First:
#         plt.bar(pos_NR[MNO], vals, color=util.get_bar_color(i), edgecolor=util.get_bar_color(i), alpha=0.5,
#                 hatch=patterns[1], label='Back-up')
#         First = False
#     else:
#         plt.bar(pos_NR[MNO], vals, color=util.get_bar_color(i), edgecolor=util.get_bar_color(i), alpha=0.5,
#                 hatch=patterns[1])
#
# legend = ax.legend()
# handles = legend.legendHandles
#
# # There are many more hatches available in matplotlib
# for i, handle in enumerate(handles):
#     handle.set_edgecolor("gray")
#     handle.set_facecolor('gray')
#     handle.set_hatch(patterns[i])
#
# plt.xticks(xticks, cities)
# plt.ylabel('FDP')
# plt.savefig('Figures/improvement_fdp_full_backup.pdf', dpi=1000)
# plt.show()

# fig, ax = plt.subplots()
# First = True
# for MNO, i in zip(MNOs, range(len(MNOs))):
#     vals = [v[i] for k, v in no_cooperation_fsp.items() if k in cities]
#     if First:
#         plt.bar(pos[MNO], vals, color=util.get_bar_color(i), edgecolor=util.get_bar_color(i), alpha=0.5,
#                 hatch=patterns[0], label='Normal')
#         First = False
#     else:
#         plt.bar(pos[MNO], vals, color=util.get_bar_color(i), edgecolor=util.get_bar_color(i), alpha=0.5,
#                 hatch=patterns[0])
#
# First = True
# for MNO, i in zip(MNOs, range(len(MNOs))):
#     vals = [v[i] for k, v in NR_full_fsp.items() if k in cities]
#     if First:
#         plt.bar(pos_NR[MNO], vals, color=util.get_bar_color(i), edgecolor=util.get_bar_color(i), alpha=0.5,
#                 hatch=patterns[1], label='Back-up')
#         First = False
#     else:
#         plt.bar(pos_NR[MNO], vals, color=util.get_bar_color(i), edgecolor=util.get_bar_color(i), alpha=0.5,
#                 hatch=patterns[1])
#
# legend = ax.legend()
# handles = legend.legendHandles
#
# # There are many more hatches available in matplotlib
# for i, handle in enumerate(handles):
#     handle.set_edgecolor("gray")
#     handle.set_facecolor('gray')
#     handle.set_hatch(patterns[i])
#
# plt.xticks(xticks, cities)
# plt.ylabel('FSP')
# plt.savefig('Figures/improvement_fsp_full_backup.pdf', dpi=1000)
# plt.show()

FDPFSP = 'FDP'
labels = ['no cooperation', 'NR-full', 'NR-fallback']

fig, ax = plt.subplots()
for x in range(len(cities)):
    if FDPFSP == 'FDP':
        plt.plot([-0.001, 0.12], [x - 0.2, x - 0.2], ':', color='gray', alpha=0.5, zorder=1)
        plt.plot([-0.001, 0.12], [x, x], ':', color='gray', alpha=0.5, zorder=1)
        plt.plot([-0.001, 0.12], [x + 0.2, x + 0.2], ':', color='gray', alpha=0.5, zorder=1)
    elif FDPFSP == 'FSP':
        plt.plot([0.5, 1.01], [x - 0.2, x - 0.2], ':', color='gray', alpha=0.5, zorder=1)
        plt.plot([0.5, 1.01], [x, x], ':', color='gray', alpha=0.5, zorder=1)
        plt.plot([0.5, 1.01], [x + 0.2, x + 0.2], ':', color='gray', alpha=0.5, zorder=1)

y_axes = {'KPN': [i + 0.2 for i in range(len(cities))], 'T-Mobile': [i for i in range(len(cities))],
          'Vodafone': [i - 0.2 for i in range(len(cities))]}

for i, data in zip(range(3), [no_cooperation_fdp, NR_full_fdp, NR_fallback_fdp]):
    for j in range(len(MNOs)):
        vals = [v[j] for k, v in data.items() if k in cities]
        if j == 0:
            print(j)
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
    plt.savefig(f'Figures/{FDPFSP}with_fallback_cities.pdf', dpi=1000, transparent=True)
else:
    plt.savefig(f'Figures/{FDPFSP}with_fallback_provinces.pdf', dpi=1000, transparent=True)
plt.show()

FDPFSP = 'FSP'
fig, ax = plt.subplots()
for x in range(len(cities)):
    if FDPFSP == 'FDP':
        plt.plot([-0.001, 0.05], [x - 0.2, x - 0.2], ':', color='gray', alpha=0.5, zorder=1)
        plt.plot([-0.001, 0.05], [x, x], ':', color='gray', alpha=0.5, zorder=1)
        plt.plot([-0.001, 0.05], [x + 0.2, x + 0.2], ':', color='gray', alpha=0.5, zorder=1)
    elif FDPFSP == 'FSP':
        plt.plot([0.5, 1.0], [x - 0.2, x - 0.2], ':', color='gray', alpha=0.5, zorder=1)
        plt.plot([0.5, 1.0], [x, x], ':', color='gray', alpha=0.5, zorder=1)
        plt.plot([0.5, 1.0], [x + 0.2, x + 0.2], ':', color='gray', alpha=0.5, zorder=1)

y_axes = {'KPN': [i + 0.2 for i in range(len(cities))], 'T-Mobile': [i for i in range(len(cities))],
          'Vodafone': [i - 0.2 for i in range(len(cities))]}

for i, data in zip(range(3), [no_cooperation_fsp, NR_full_fsp, NR_fallback_fsp]):
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
    plt.savefig(f'Figures/{FDPFSP}with_fallback_cities.pdf', dpi=1000, transparent=True)
else:
    plt.savefig(f'Figures/{FDPFSP}with_fallback_provinces.pdf', dpi=1000, transparent=True)

plt.show()
