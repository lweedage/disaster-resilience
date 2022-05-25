import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import util
import find_base_stations as antenna
from settings import *
import analyse_UA

city_name = 'Overijssel'
percentage = '89'

SNR_boxplot = []
SINR_boxplot = []
capacity_boxplot = []

FSP_bar = [0, 0, 0]
FDP_bar = [0, 0, 0]

MNOs = ['KPN', 'T-Mobile', 'Vodafone']

for provider, i in zip(MNOs, range(3)):
    filename = f'{city_name}{provider}{percentage}'

    links = util.from_data(f'data/Realisations/{filename}_links.p')
    snr = util.from_data(f'data/Realisations/{filename}_snrs.p')
    sinr = util.from_data(f'data/Realisations/{filename}_sinrs.p')
    capacity = util.from_data(f'data/Realisations/{filename}_capacities.p')
    FDP = util.from_data(f'data/Realisations/{filename}_FDP.p')
    FSP = util.from_data(f'data/Realisations/{filename}_FSP.p')

    fraction_satisified_pop = sum(FSP)/len(FSP)
    fraction_disconnected_pop = sum(FDP)/len(FSP)

    print(f'FDP = {fraction_disconnected_pop}')
    print(f'FSP = {fraction_satisified_pop}')

    capacity = np.divide(capacity, 1e6)
    # analyse_UA.histogram_snr(snr, filename)
    # analyse_UA.histogram_sinr(sinr, filename)
    # analyse_UA.capacity(capacity, filename)
    # analyse_UA.fairness(capacity)
    SNR_boxplot.append(np.extract(snr > 0, snr))
    SINR_boxplot.append(np.extract(sinr > 0, sinr))
    capacity_boxplot.append(np.extract(capacity > 0, capacity))

    FSP_bar[i] = fraction_satisified_pop
    FDP_bar[i] = fraction_disconnected_pop

fig, ax = plt.subplots()
bplot = plt.boxplot(SINR_boxplot,  patch_artist=True,  notch=True,labels = MNOs, showfliers = False)
for patch, color in zip(bplot['boxes'], colors[:3]):
    patch.set_facecolor(color)
plt.ylabel('SINR (dB)')
plt.title('Overijssel')
plt.savefig('SINR.png')
# plt.show()

fig, ax = plt.subplots()
bplot = plt.boxplot(SNR_boxplot,  patch_artist=True,  notch=True,labels = MNOs, showfliers = False)
for patch, color in zip(bplot['boxes'], colors[:3]):
    patch.set_facecolor(color)
plt.ylabel('SNR (dB)')
plt.title('Overijssel')
plt.savefig('SNR.png')
# plt.show()

fig, ax = plt.subplots()
bplot = plt.boxplot(capacity_boxplot,  patch_artist=True,  notch=True,labels = MNOs, showfliers = False)
for patch, color in zip(bplot['boxes'], colors[:3]):
    patch.set_facecolor(color)
plt.ylabel('Per-user capacity (Mbps)')
plt.title('Overijssel')
plt.savefig('capacity.png')

# plt.show()

index = np.arange(3)
width = 0.35

fig, ax = plt.subplots()
plt.bar(index, FSP_bar, width = width, label = 'FSP', color = colors[0])
plt.bar(index + width, FDP_bar, width = width, label = 'FDP', color = colors[1])
plt.ylabel('Fraction')
ax.set_xticks(index + width/2)
ax.set_xticklabels(MNOs)
plt.legend()
plt.title('Overijssel')
plt.savefig(f'fdpfsp.png')
# plt.show()