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

NR_fallback_failure_fdp = {'Middelburg': [0.0026059992406024554, 0.0024414631059359575, 0.0025933426148588784],
                           'Enschede': [0.002525504666811374, 0.002387670935532885, 0.0025189928369871934],
                           'Amsterdam': [0.0027340425531914895, 0.0025638297872340424, 0.0027220744680851064],

                           'Overijssel': [0.0016670952258506899, 0.0014763863889603154, 0.0015620982257649782],
                           'Friesland': [0.001946051544067924, 0.0017074911713877827, 0.0018502517093695995],
                           'Utrecht': [0.0017897367852624433, 0.0015613910574875799, 0.0017002499459993212]}

NR_fallback_failure_fsp = {'Middelburg': [0.7034350082268067, 0.7147563599544361, 0.7855727123148969],
                           'Enschede': [0.7030518775775993, 0.702799001519427, 0.7873789884957673],
                           'Amsterdam': [0.6995066489361702, 0.7091303191489362, 0.7797220744680851],

                           'Overijssel': [0.6530599125739265, 0.6033256192680209, 0.7262813919602297],
                           'Friesland': [0.6349913592305958, 0.6034713351867158, 0.7203490119468029],
                           'Utrecht': [0.6617366618323202, 0.6232634924553337, 0.737396241552751]}

NR_full_failure_fdp = {'Middelburg': [0.0, 0.0, 0.0],
                       'Enschede': [0.0011806375442739079, 0.0005903187721369539, 0.0005903187721369539],
                       'Amsterdam':  [0.0010638297872340426, 0.0007978723404255319, 0.0014627659574468085],

                       'Overijssel': [0.0037194651581383387, 0.0037241793091625955, 0.0037216079540584555],
                       'Friesland': [0.003958787286798407, 0.003961417086182283, 0.003971372755278383],
                       'Utrecht': [0.0040170333569907735, 0.00402629061622489, 0.004021970561915635]}

NR_full_failure_fsp = {'Middelburg': [0.9606299212598425, 0.9816272965879265, 0.963254593175853],
                       'Enschede': [0.885478158205431, 0.9291617473435655, 0.9120425029515938],
                       'Amsterdam': [0.8716755319148937, 0.9128989361702128, 0.9022606382978723],

                       'Overijssel': [0.79113975314991, 0.8504169880860547, 0.8383354761292534],
                       'Friesland': [0.7850052595987678, 0.8460742730483132, 0.8335141633481103],
                       'Utrecht': [0.799202332829327, 0.8570836547659456, 0.8458829882432808]}

no_cooperation_failure_fdp = {'Middelburg': [0.0411213770408809, 0.013821035311985825, 0.06543475509429186],
                              'Enschede': [0.03640112871716952, 0.012426741914477969, 0.05926850444975038],
                              'Amsterdam': [0.04313829787234043, 0.01452127659574468, 0.06809840425531914],

                              'Overijssel': [0.024470729407731207, 0.014249592868775179, 0.05896974372160795],
                              'Friesland': [0.025828386805920804, 0.015741227740626643, 0.06467428056202569],
                              'Utrecht': [0.028080353010152128, 0.01468818465146419, 0.06159163143765236]}

no_cooperation_failure_fsp = {'Middelburg': [0.7053790659410202, 0.8334514618402734, 0.6510694848753322],
                              'Enschede': [0.710418927718689, 0.8359995658780117, 0.641632298675928],
                              'Amsterdam': [0.6964627659574468, 0.8274468085106383, 0.640811170212766],

                              'Overijssel': [0.6540884546155824, 0.7476000685694695, 0.5691051684237594],
                              'Friesland': [0.6350026297993838, 0.7428244045382824, 0.5667969043504395],
                              'Utrecht': [0.6596722930231123, 0.7592804023822014, 0.5866942327274971]}

NR_fallback_QOS_failure_fdp = {'Middelburg': [0.006115681559296292, 0.009527907859764586, 0.005947348436906721],
                               'Enschede': [0.005727154330366833, 0.00916757108747558, 0.005898632515736922],
                               'Amsterdam': [0.006416223404255319, 0.009990691489361702, 0.0062393617021276595],

                               'Overijssel': [0.005374346447244364, 0.01298641467386646, 0.006869160881117682],
                               'Friesland': [0.006213088887219175, 0.015305995942595236, 0.008270343376662409],
                               'Utrecht': [0.005811398771870275, 0.0137559786465887, 0.007262937019779678]}

NR_fallback_QOS_failure_fsp = {
    'Middelburg': [0.7276041007467409, 0.7169687381344134, 0.8247247183900772],
    'Enschede': [0.7266550900803126, 0.7033090948556544, 0.8263848491426091],
    'Amsterdam': [0.7223031914893617, 0.7102353723404256, 0.8197965425531915],

    'Overijssel': [0.6662098225764979, 0.6124674295020143, 0.7469707294077312],
    'Friesland': [0.6485870463596063, 0.6128606582012173, 0.7422888646780375],
    'Utrecht': [0.6750239145863548, 0.6320199339648841, 0.7583031443823866]}

cities = ['Overijssel', 'Friesland', 'Utrecht']
# cities = ['Middelburg', 'Enschede', 'Amsterdam']
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

for i, data in zip(range(4), [no_cooperation_failure_fdp, NR_full_failure_fdp, NR_fallback_failure_fdp,
                              NR_fallback_QOS_failure_fdp]):
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

for i, data in zip(range(4), [no_cooperation_failure_fsp, NR_full_failure_fsp, NR_fallback_failure_fsp,
                              NR_fallback_QOS_failure_fsp]):
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
