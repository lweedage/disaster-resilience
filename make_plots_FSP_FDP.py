import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import pandas as pd

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

provinces = ['Drenthe', 'Flevoland', 'Friesland', 'Gelderland', 'Groningen', 'Limburg', 'Noord-Brabant',
             # 'Noord-Holland',
             'Overijssel', 'Utrecht', 'Zeeland', 'Zuid-Holland']
MNOs = ['KPN', 'Vodafone', 'T-Mobile', 'All']

results = pd.read_excel('Data_per_province.xls', sheet_name='Sheet1')

FSP, FDP, SAT, DEG = {MNO: [] for MNO in MNOs}, {MNO: [] for MNO in MNOs}, {MNO: [] for MNO in MNOs}, {MNO: [] for MNO
                                                                                                       in MNOs}

for province in provinces:
    for MNO in MNOs:
        FSP[MNO].append(results[(results['Provider'] == MNO) & (results['Province'] == province)]['FSP'].tolist()[0])
        FDP[MNO].append(results[(results['Provider'] == MNO) & (results['Province'] == province)]['FDP'].tolist()[0])
        SAT[MNO].append(
            results[(results['Provider'] == MNO) & (results['Province'] == province)]['Satisfaction'].tolist()[0])
        DEG[MNO].append(
            results[(results['Provider'] == MNO) & (results['Province'] == province)]['Degree BS'].tolist()[0])

fig, ax = plt.subplots(1, 2)
for i, MNO in zip(range(len(MNOs)), MNOs):
    ax[0].scatter(FSP[MNO], range(len(provinces)), label=MNO, color=colors[i], marker=markers[i])
    ax[1].scatter(FDP[MNO], range(len(provinces)), label=MNO, color=colors[i], marker=markers[i])


ax[0].set_title('FSP')
ax[1].set_title('FDP')
ax[0].set_yticks(range(len(provinces)), provinces)
ax[1].set_yticks([], [])

plt.legend(bbox_to_anchor=(1,0.5) , loc='center left')
plt.show()
