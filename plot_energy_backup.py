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

markers = ['o', 'X', 'v', 's', '*', 'P', '1', '+']



max_iterations = 20
#municipalities = ['Middelburg', 'Enschede', 'Amsterdam']
#MNOs = ['KPN', 'T-Mobile', 'Vodafone'] # p.providers

#p_per_mno_fp = util.from_data(f'data/Realisations/{p.filename}{max_iterations}_totalpower_per_mno_fp.p')
#p_per_mno = util.from_data(f'data/Realisations/{p.filename}{max_iterations}_totalpower_per_mno.p')
# fallback
p_per_mno_fp_Middelburg = util.from_data(f'data/Realisations/Middelburgall_MNOs0.021backup{max_iterations}_totalpower_per_mno_fp.p')
p_per_mno_Middelburg = util.from_data(f'data/Realisations/Middelburgall_MNOs0.021backup{max_iterations}_totalpower_per_mno.p')
p_per_mno_fp_Enschede = util.from_data(f'data/Realisations/Enschedeall_MNOs0.021backup{max_iterations}_totalpower_per_mno_fp.p')
p_per_mno_Enschede = util.from_data(f'data/Realisations/Enschedeall_MNOs0.021backup{max_iterations}_totalpower_per_mno.p')
p_per_mno_fp_Amsterdam = util.from_data(f'data/Realisations/Amsterdamall_MNOs0.021backup{max_iterations}_totalpower_per_mno_fp.p')
p_per_mno_Amsterdam = util.from_data(f'data/Realisations/Amsterdamall_MNOs0.021backup{max_iterations}_totalpower_per_mno.p')

fdp_per_mno_Middelburg = util.from_data(f'data/Realisations/Middelburgall_MNOs0.021backup{max_iterations}_fdp_per_MNO.p')
fdp_per_mno_Enschede = util.from_data(f'data/Realisations/Enschedeall_MNOs0.021backup{max_iterations}_fdp_per_MNO.p')
fdp_per_mno_Amsterdam = util.from_data(f'data/Realisations/Amsterdamall_MNOs0.021backup{max_iterations}_fdp_per_MNO.p')
fsp_per_mno_Middelburg = util.from_data(f'data/Realisations/Middelburgall_MNOs0.021backup{max_iterations}_fsp_per_MNO.p')
fsp_per_mno_Enschede = util.from_data(f'data/Realisations/Enschedeall_MNOs0.021backup{max_iterations}_fsp_per_MNO.p')
fsp_per_mno_Amsterdam = util.from_data(f'data/Realisations/Amsterdamall_MNOs0.021backup{max_iterations}_fsp_per_MNO.p')

total_fsp_Middelburg = util.from_data(f'data/Realisations/Middelburgall_MNOs0.021backup{max_iterations}_totalfsp.p')
total_fdp_Middelburg = util.from_data(f'data/Realisations/Middelburgall_MNOs0.021backup{max_iterations}_totalfdp.p')
total_fsp_Enschede = util.from_data(f'data/Realisations/Enschedeall_MNOs0.021backup{max_iterations}_totalfsp.p')
total_fdp_Enschede = util.from_data(f'data/Realisations/Enschedeall_MNOs0.021backup{max_iterations}_totalfdp.p')
total_fsp_Amsterdam = util.from_data(f'data/Realisations/Amsterdamall_MNOs0.021backup{max_iterations}_totalfsp.p')
total_fdp_Amsterdam = util.from_data(f'data/Realisations/Amsterdamall_MNOs0.021backup{max_iterations}_totalfdp.p')

# National Roaming
p_per_mno_fp_Middelburg_NR = util.from_data(f'data/Realisations/Middelburgall_MNOs0.021{max_iterations}_totalpower_per_mno_fp.p')
p_per_mno_Middelburg_NR = util.from_data(f'data/Realisations/Middelburgall_MNOs0.021{max_iterations}_totalpower_per_mno.p')
p_per_mno_fp_Enschede_NR = util.from_data(f'data/Realisations/Enschedeall_MNOs0.021{max_iterations}_totalpower_per_mno_fp.p')
p_per_mno_Enschede_NR = util.from_data(f'data/Realisations/Enschedeall_MNOs0.021{max_iterations}_totalpower_per_mno.p')
p_per_mno_Amsterdam_NR = util.from_data(f'data/Realisations/Amsterdamall_MNOs0.021{max_iterations}_totalpower_per_mno.p')

fdp_per_mno_Middelburg_NR = util.from_data(f'data/Realisations/Middelburgall_MNOs0.021{max_iterations}_fdp_per_MNO.p')
fdp_per_mno_Enschede_NR = util.from_data(f'data/Realisations/Enschedeall_MNOs0.021{max_iterations}_fdp_per_MNO.p')
fdp_per_mno_Amsterdam_NR = util.from_data(f'data/Realisations/Amsterdamall_MNOs0.021{max_iterations}_fdp_per_MNO.p')
fsp_per_mno_Middelburg_NR = util.from_data(f'data/Realisations/Middelburgall_MNOs0.021{max_iterations}_fsp_per_MNO.p')
fsp_per_mno_Enschede_NR = util.from_data(f'data/Realisations/Enschedeall_MNOs0.021{max_iterations}_fsp_per_MNO.p')
fsp_per_mno_Amsterdam_NR = util.from_data(f'data/Realisations/Amsterdamall_MNOs0.021{max_iterations}_fsp_per_MNO.p')

total_fdp_Middelburg_NR = util.from_data(f'data/Realisations/Middelburgall_MNOs0.021{max_iterations}_totalfdp.p')
total_fdp_Enschede_NR = util.from_data(f'data/Realisations/Enschedeall_MNOs0.021{max_iterations}_totalfdp.p')
total_fdp_Amsterdam_NR = util.from_data(f'data/Realisations/Amsterdamall_MNOs0.021{max_iterations}_totalfdp.p')
total_fsp_Middelburg_NR = util.from_data(f'data/Realisations/Middelburgall_MNOs0.021{max_iterations}_totalfsp.p')
total_fsp_Enschede_NR = util.from_data(f'data/Realisations/Enschedeall_MNOs0.021{max_iterations}_totalfsp.p')
total_fsp_Amsterdam_NR = util.from_data(f'data/Realisations/Amsterdamall_MNOs0.021{max_iterations}_totalfsp.p')

# No coop
p_KPN_fp_Middelburg_nc = util.from_data(f'data/Realisations/MiddelburgKPN0.020.33{max_iterations}_totalpower_per_mno_fp.p')
p_KPN_Middelburg_nc = util.from_data(f'data/Realisations/MiddelburgKPN0.020.33{max_iterations}_totalpower_per_mno.p')
p_T_Mobile_fp_Middelburg_nc = util.from_data(f'data/Realisations/MiddelburgT-Mobile0.020.33{max_iterations}_totalpower_per_mno_fp.p')
p_T_Mobile_Middelburg_nc = util.from_data(f'data/Realisations/MiddelburgT-Mobile0.020.33{max_iterations}_totalpower_per_mno.p')
p_Vodafone_fp_Middelburg_nc = util.from_data(f'data/Realisations/MiddelburgVodafone0.020.33{max_iterations}_totalpower_per_mno_fp.p')
p_Vodafone_Middelburg_nc = util.from_data(f'data/Realisations/MiddelburgVodafone0.020.33{max_iterations}_totalpower_per_mno.p')

fdp_KPN_Middelburg_nc = util.from_data(f'data/Realisations/MiddelburgKPN0.020.33{max_iterations}_fdp_per_MNO.p')
fdp_T_Mobile_Middelburg_nc = util.from_data(f'data/Realisations/MiddelburgT-Mobile0.020.33{max_iterations}_fdp_per_MNO.p')
fdp_Vodafone_Middelburg_nc = util.from_data(f'data/Realisations/MiddelburgVodafone0.020.33{max_iterations}_fdp_per_MNO.p')
fsp_KPN_Middelburg_nc = util.from_data(f'data/Realisations/MiddelburgKPN0.020.33{max_iterations}_fsp_per_MNO.p')
fsp_T_Mobile_Middelburg_nc = util.from_data(f'data/Realisations/MiddelburgT-Mobile0.020.33{max_iterations}_fsp_per_MNO.p')
fsp_Vodafone_Middelburg_nc = util.from_data(f'data/Realisations/MiddelburgVodafone0.020.33{max_iterations}_fsp_per_MNO.p')

p_KPN_fp_Enschede_nc = util.from_data(f'data/Realisations/EnschedeKPN0.020.33{max_iterations}_totalpower_per_mno_fp.p')
p_KPN_Enschede_nc = util.from_data(f'data/Realisations/EnschedeKPN0.020.33{max_iterations}_totalpower_per_mno.p')
p_T_Mobile_fp_Enschede_nc = util.from_data(f'data/Realisations/EnschedeT-Mobile0.020.33{max_iterations}_totalpower_per_mno_fp.p')
p_T_Mobile_Enschede_nc = util.from_data(f'data/Realisations/EnschedeT-Mobile0.020.33{max_iterations}_totalpower_per_mno.p')
p_Vodafone_fp_Enschede_nc = util.from_data(f'data/Realisations/EnschedeVodafone0.020.33{max_iterations}_totalpower_per_mno_fp.p')
p_Vodafone_Enschede_nc = util.from_data(f'data/Realisations/EnschedeVodafone0.020.33{max_iterations}_totalpower_per_mno.p')

fdp_KPN_Enschede_nc = util.from_data(f'data/Realisations/EnschedeKPN0.020.33{max_iterations}_fdp_per_MNO.p')
fdp_T_Mobile_Enschede_nc = util.from_data(f'data/Realisations/EnschedeT-Mobile0.020.33{max_iterations}_fdp_per_MNO.p')
fdp_Vodafone_Enschede_nc = util.from_data(f'data/Realisations/EnschedeVodafone0.020.33{max_iterations}_fdp_per_MNO.p')
fsp_KPN_Enschede_nc = util.from_data(f'data/Realisations/EnschedeKPN0.020.33{max_iterations}_fsp_per_MNO.p')
fsp_T_Mobile_Enschede_nc = util.from_data(f'data/Realisations/EnschedeT-Mobile0.020.33{max_iterations}_fsp_per_MNO.p')
fsp_Vodafone_Enschede_nc = util.from_data(f'data/Realisations/EnschedeVodafone0.020.33{max_iterations}_fsp_per_MNO.p')

p_KPN_Amsterdam_nc = util.from_data(f'data/Realisations/AmsterdamKPN0.020.33{max_iterations}_totalpower_per_mno.p')
p_T_Mobile_Amsterdam_nc = util.from_data(f'data/Realisations/AmsterdamT-Mobile0.020.33{max_iterations}_totalpower_per_mno.p')
p_Vodafone_Amsterdam_nc = util.from_data(f'data/Realisations/AmsterdamVodafone0.020.33{max_iterations}_totalpower_per_mno.p')

fdp_KPN_Amsterdam_nc = util.from_data(f'data/Realisations/AmsterdamKPN0.020.33{max_iterations}_fdp_per_MNO.p')
fdp_T_Mobile_Amsterdam_nc = util.from_data(f'data/Realisations/AmsterdamT-Mobile0.020.33{max_iterations}_fdp_per_MNO.p')
fdp_Vodafone_Amsterdam_nc = util.from_data(f'data/Realisations/AmsterdamVodafone0.020.33{max_iterations}_fdp_per_MNO.p')
fsp_KPN_Amsterdam_nc = util.from_data(f'data/Realisations/AmsterdamKPN0.020.33{max_iterations}_fsp_per_MNO.p')
fsp_T_Mobile_Amsterdam_nc = util.from_data(f'data/Realisations/AmsterdamT-Mobile0.020.33{max_iterations}_fsp_per_MNO.p')
fsp_Vodafone_Amsterdam_nc = util.from_data(f'data/Realisations/AmsterdamVodafone0.020.33{max_iterations}_fsp_per_MNO.p')

#KPN_total_fsp_Enschede_NC = util.from_data(f'data/Realisations/EnschedeKPN0.020.33{max_iterations}_totalfsp.p') # Same as fsp_KPN_Enschede_nc['KPN']
#KPN_total_fdp_Enschede_NC = util.from_data(f'data/Realisations/EnschedeKPN0.020.33{max_iterations}_totalfdp.p')

# Middelburg
p_KPN_Middelburg, p_T_Mobile_Middelburg, p_Vodafone_Middelburg  = [], [], []
for samp in p_per_mno_Middelburg:
    p_KPN_Middelburg.append(samp["KPN"])
    p_T_Mobile_Middelburg.append(samp["T-Mobile"])
    p_Vodafone_Middelburg.append(samp["Vodafone"])

p_KPN_Middelburg_NR, p_T_Mobile_Middelburg_NR, p_Vodafone_Middelburg_NR  = [], [], []
for samp in p_per_mno_Middelburg_NR:
    p_KPN_Middelburg_NR.append(samp["KPN"])
    p_T_Mobile_Middelburg_NR.append(samp["T-Mobile"])
    p_Vodafone_Middelburg_NR.append(samp["Vodafone"])

p_KPN_Middelburg_NC, p_T_Mobile_Middelburg_NC, p_Vodafone_Middelburg_NC  = [], [], []
for samp in p_KPN_Middelburg_nc:
    p_KPN_Middelburg_NC.append(samp["KPN"])
for samp in p_T_Mobile_Middelburg_nc:
    p_T_Mobile_Middelburg_NC.append(samp["T-Mobile"])
for samp in p_Vodafone_Middelburg_nc:
    p_Vodafone_Middelburg_NC.append(samp["Vodafone"])


MNOs = ['KPN', 'T-Mobile', 'Vodafone']
name_MNO = ['MNO-1', 'MNO-2', 'MNO-3', 'Total']

#x = np.array([1, 2, 3])
x = np.array([2, 4, 6, 8])
fig, ax = plt.subplots()
#fbplot = ax.boxplot(dataFDP, positions=x - 0.17, widths=0.3, patch_artist=True, showfliers=False)
#nrplot = ax.boxplot(dataFSP, positions=x + 0.17, widths=0.3, patch_artist=True, showfliers=False)
box_width = 0.25
fbplot = ax.boxplot([p_KPN_Middelburg, p_T_Mobile_Middelburg, p_Vodafone_Middelburg, np.add(np.add(p_KPN_Middelburg, p_T_Mobile_Middelburg), p_Vodafone_Middelburg)], positions=x - 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)
nrplot = ax.boxplot([p_KPN_Middelburg_NR, p_T_Mobile_Middelburg_NR, p_Vodafone_Middelburg_NR, np.add(np.add(p_KPN_Middelburg_NR, p_T_Mobile_Middelburg_NR), p_Vodafone_Middelburg_NR)], positions=x, widths=box_width, patch_artist=True, showfliers=False)
ncplot = ax.boxplot([p_KPN_Middelburg_NC, p_T_Mobile_Middelburg_NC, p_Vodafone_Middelburg_NC, np.add(np.add(p_KPN_Middelburg_NC, p_T_Mobile_Middelburg_NC), p_Vodafone_Middelburg_NC)], positions=x + 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)

for patch in fbplot['boxes']:
    patch.set_facecolor((0.2549019607843137, 0.4117647058823529, 0.8823529411764706, 0.5))
for patch in nrplot['boxes']:
    patch.set_facecolor((1.0, 0.4980392156862745, 0.3137254901960784, 0.5))
for patch in ncplot['boxes']:
    patch.set_facecolor('#1f77b4')

ax.legend([fbplot["boxes"][0], nrplot["boxes"][0], ncplot["boxes"][0]], ['NR-fallback', 'NR-full', 'no cooperation'])
plt.xticks(x, name_MNO)
# plt.yticks([0.0, 0.25, 0.50, 0.75, 1.0])
plt.ylabel('Total power consumption (W)')
plt.savefig('Figures/powerperMNO_middelburg.pdf', dpi=1000)
#plt.show()


# fsp Middelburg
fsp_KPN_Middelburg, fsp_T_Mobile_Middelburg, fsp_Vodafone_Middelburg  = [], [], []
for samp in fsp_per_mno_Middelburg:
    fsp_KPN_Middelburg.append(samp["KPN"])
    fsp_T_Mobile_Middelburg.append(samp["T-Mobile"])
    fsp_Vodafone_Middelburg.append(samp["Vodafone"])

fsp_KPN_Middelburg_NR, fsp_T_Mobile_Middelburg_NR, fsp_Vodafone_Middelburg_NR  = [], [], []
for samp in fsp_per_mno_Middelburg_NR:
    fsp_KPN_Middelburg_NR.append(samp["KPN"])
    fsp_T_Mobile_Middelburg_NR.append(samp["T-Mobile"])
    fsp_Vodafone_Middelburg_NR.append(samp["Vodafone"])

fsp_KPN_Middelburg_NC, fsp_T_Mobile_Middelburg_NC, fsp_Vodafone_Middelburg_NC  = [], [], []
for samp in fsp_KPN_Middelburg_nc:
    fsp_KPN_Middelburg_NC.append(samp["KPN"])
for samp in fsp_T_Mobile_Middelburg_nc:
    fsp_T_Mobile_Middelburg_NC.append(samp["T-Mobile"])
for samp in fsp_Vodafone_Middelburg_nc:
    fsp_Vodafone_Middelburg_NC.append(samp["Vodafone"])


fig, ax = plt.subplots()

#fbplot = ax.boxplot(dataFDP, positions=x - 0.17, widths=0.3, patch_artist=True, showfliers=False)
#nrplot = ax.boxplot(dataFSP, positions=x + 0.17, widths=0.3, patch_artist=True, showfliers=False)
box_width = 0.25
fbplot = ax.boxplot([fsp_KPN_Middelburg, fsp_T_Mobile_Middelburg, fsp_Vodafone_Middelburg, total_fsp_Middelburg], positions=x - 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)
nrplot = ax.boxplot([fsp_KPN_Middelburg_NR, fsp_T_Mobile_Middelburg_NR, fsp_Vodafone_Middelburg_NR, total_fsp_Middelburg_NR], positions=x, widths=box_width, patch_artist=True, showfliers=False)
total_fsp_Middelburg_NC = np.add(np.add(fsp_KPN_Middelburg_NC, fsp_T_Mobile_Middelburg_NC), fsp_Vodafone_Middelburg_NC)/3 # only possible because all the scenarios uses the same number of users.
ncplot = ax.boxplot([fsp_KPN_Middelburg_NC, fsp_T_Mobile_Middelburg_NC, fsp_Vodafone_Middelburg_NC, total_fsp_Middelburg_NC], positions=x + 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)

for patch in fbplot['boxes']:
    patch.set_facecolor((0.2549019607843137, 0.4117647058823529, 0.8823529411764706, 0.5))
for patch in nrplot['boxes']:
    patch.set_facecolor((1.0, 0.4980392156862745, 0.3137254901960784, 0.5))
for patch in ncplot['boxes']:
    patch.set_facecolor('#1f77b4')

ax.legend([fbplot["boxes"][0], nrplot["boxes"][0], ncplot["boxes"][0]], ['NR-fallback', 'NR-full', 'no cooperation'])
plt.xticks(x, name_MNO)
# plt.yticks([0.0, 0.25, 0.50, 0.75, 1.0])
plt.ylabel('FSP')
plt.savefig('Figures/FSPperMNO_middelburg.pdf', dpi=1000)
#plt.show()

# fdp Middelburg
fdp_KPN_Middelburg, fdp_T_Mobile_Middelburg, fdp_Vodafone_Middelburg  = [], [], []
for samp in fdp_per_mno_Middelburg:
    fdp_KPN_Middelburg.append(samp["KPN"])
    fdp_T_Mobile_Middelburg.append(samp["T-Mobile"])
    fdp_Vodafone_Middelburg.append(samp["Vodafone"])

fdp_KPN_Middelburg_NR, fdp_T_Mobile_Middelburg_NR, fdp_Vodafone_Middelburg_NR  = [], [], []
for samp in fdp_per_mno_Middelburg_NR:
    fdp_KPN_Middelburg_NR.append(samp["KPN"])
    fdp_T_Mobile_Middelburg_NR.append(samp["T-Mobile"])
    fdp_Vodafone_Middelburg_NR.append(samp["Vodafone"])

fdp_KPN_Middelburg_NC, fdp_T_Mobile_Middelburg_NC, fdp_Vodafone_Middelburg_NC  = [], [], []
for samp in fdp_KPN_Middelburg_nc:
    fdp_KPN_Middelburg_NC.append(samp["KPN"])
for samp in fdp_T_Mobile_Middelburg_nc:
    fdp_T_Mobile_Middelburg_NC.append(samp["T-Mobile"])
for samp in fdp_Vodafone_Middelburg_nc:
    fdp_Vodafone_Middelburg_NC.append(samp["Vodafone"])


fig, ax = plt.subplots()
box_width = 0.25
fbplot = ax.boxplot([fdp_KPN_Middelburg, fdp_T_Mobile_Middelburg, fdp_Vodafone_Middelburg, total_fdp_Middelburg], positions=x - 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)
nrplot = ax.boxplot([fdp_KPN_Middelburg_NR, fdp_T_Mobile_Middelburg_NR, fdp_Vodafone_Middelburg_NR, total_fdp_Middelburg_NR], positions=x, widths=box_width, patch_artist=True, showfliers=False)
total_fdp_Middelburg_NC = np.add(np.add(fdp_KPN_Middelburg_NC, fdp_T_Mobile_Middelburg_NC), fdp_Vodafone_Middelburg_NC)/3 # only possible because all the scenarios uses the same number of users.
ncplot = ax.boxplot([fdp_KPN_Middelburg_NC, fdp_T_Mobile_Middelburg_NC, fdp_Vodafone_Middelburg_NC, total_fdp_Middelburg_NC], positions=x + 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)

for patch in fbplot['boxes']:
    patch.set_facecolor((0.2549019607843137, 0.4117647058823529, 0.8823529411764706, 0.5))
for patch in nrplot['boxes']:
    patch.set_facecolor((1.0, 0.4980392156862745, 0.3137254901960784, 0.5))
for patch in ncplot['boxes']:
    patch.set_facecolor('#1f77b4')

ax.legend([fbplot["boxes"][0], nrplot["boxes"][0], ncplot["boxes"][0]], ['NR-fallback', 'NR-full', 'no cooperation'])
plt.xticks(x, name_MNO)
# plt.yticks([0.0, 0.25, 0.50, 0.75, 1.0])
plt.ylabel('FDP')
plt.savefig('Figures/FDPperMNO_middelburg.pdf', dpi=1000)
#plt.show()



# Enschede
p_KPN_Enschede, p_T_Mobile_Enschede, p_Vodafone_Enschede  = [], [], []
for samp in p_per_mno_Enschede:
    p_KPN_Enschede.append(samp["KPN"])
    p_T_Mobile_Enschede.append(samp["T-Mobile"])
    p_Vodafone_Enschede.append(samp["Vodafone"])

p_KPN_Enschede_NR, p_T_Mobile_Enschede_NR, p_Vodafone_Enschede_NR  = [], [], []
for samp in p_per_mno_Enschede_NR:
    p_KPN_Enschede_NR.append(samp["KPN"])
    p_T_Mobile_Enschede_NR.append(samp["T-Mobile"])
    p_Vodafone_Enschede_NR.append(samp["Vodafone"])

p_KPN_Enschede_NC, p_T_Mobile_Enschede_NC, p_Vodafone_Enschede_NC  = [], [], []
for samp in p_KPN_Enschede_nc:
    p_KPN_Enschede_NC.append(samp["KPN"])
for samp in p_T_Mobile_Enschede_nc:
    p_T_Mobile_Enschede_NC.append(samp["T-Mobile"])
for samp in p_Vodafone_Enschede_nc:
    p_Vodafone_Enschede_NC.append(samp["Vodafone"])

MNOs = ['KPN', 'T-Mobile', 'Vodafone']
name_MNO = ['MNO-1', 'MNO-2', 'MNO-3', 'Total']

#x = np.array([1, 2, 3])
fig, ax = plt.subplots()
fbplot = ax.boxplot([p_KPN_Enschede, p_T_Mobile_Enschede, p_Vodafone_Enschede, np.add(np.add(p_KPN_Enschede, p_T_Mobile_Enschede), p_Vodafone_Enschede)], positions=x - 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)
nrplot = ax.boxplot([p_KPN_Enschede_NR, p_T_Mobile_Enschede_NR, p_Vodafone_Enschede_NR, np.add(np.add(p_KPN_Enschede_NR, p_T_Mobile_Enschede_NR), p_Vodafone_Enschede_NR)], positions=x, widths=box_width, patch_artist=True, showfliers=False)
ncplot = ax.boxplot([p_KPN_Enschede_NC, p_T_Mobile_Enschede_NC, p_Vodafone_Enschede_NC, np.add(np.add(p_KPN_Enschede_NC, p_T_Mobile_Enschede_NC), p_Vodafone_Enschede_NC)], positions=x + 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)

for patch in fbplot['boxes']:
    patch.set_facecolor((0.2549019607843137, 0.4117647058823529, 0.8823529411764706, 0.5))
for patch in nrplot['boxes']:
    patch.set_facecolor((1.0, 0.4980392156862745, 0.3137254901960784, 0.5))
for patch in ncplot['boxes']:
    patch.set_facecolor('#1f77b4')

ax.legend([fbplot["boxes"][0], nrplot["boxes"][0], ncplot["boxes"][0]], ['NR-fallback', 'NR-full', 'no cooperation'])
plt.xticks(x, name_MNO)
plt.ylabel('Total power consumption (W)')
plt.savefig('Figures/powerperMNO_enschede.pdf', dpi=1000)
#plt.show()


# fsp Enschede
fsp_KPN_Enschede, fsp_T_Mobile_Enschede, fsp_Vodafone_Enschede  = [], [], []
for samp in fsp_per_mno_Enschede:
    fsp_KPN_Enschede.append(samp["KPN"])
    fsp_T_Mobile_Enschede.append(samp["T-Mobile"])
    fsp_Vodafone_Enschede.append(samp["Vodafone"])

fsp_KPN_Enschede_NR, fsp_T_Mobile_Enschede_NR, fsp_Vodafone_Enschede_NR  = [], [], []
for samp in fsp_per_mno_Enschede_NR:
    fsp_KPN_Enschede_NR.append(samp["KPN"])
    fsp_T_Mobile_Enschede_NR.append(samp["T-Mobile"])
    fsp_Vodafone_Enschede_NR.append(samp["Vodafone"])

fsp_KPN_Enschede_NC, fsp_T_Mobile_Enschede_NC, fsp_Vodafone_Enschede_NC  = [], [], []
for samp in fsp_KPN_Enschede_nc:
    fsp_KPN_Enschede_NC.append(samp["KPN"])
for samp in fsp_T_Mobile_Enschede_nc:
    fsp_T_Mobile_Enschede_NC.append(samp["T-Mobile"])
for samp in fsp_Vodafone_Enschede_nc:
    fsp_Vodafone_Enschede_NC.append(samp["Vodafone"])


fig, ax = plt.subplots()
fbplot = ax.boxplot([fsp_KPN_Enschede, fsp_T_Mobile_Enschede, fsp_Vodafone_Enschede, total_fsp_Enschede], positions=x - 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)
nrplot = ax.boxplot([fsp_KPN_Enschede_NR, fsp_T_Mobile_Enschede_NR, fsp_Vodafone_Enschede_NR, total_fsp_Enschede_NR], positions=x, widths=box_width, patch_artist=True, showfliers=False)
total_fsp_Enschede_NC = np.add(np.add(fsp_KPN_Enschede_NC, fsp_T_Mobile_Enschede_NC), fsp_Vodafone_Enschede_NC)/3 # only possible because all the scenarios uses the same number of users.
ncplot = ax.boxplot([fsp_KPN_Enschede_NC, fsp_T_Mobile_Enschede_NC, fsp_Vodafone_Enschede_NC, total_fsp_Enschede_NC], positions=x + 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)

for patch in fbplot['boxes']:
    patch.set_facecolor((0.2549019607843137, 0.4117647058823529, 0.8823529411764706, 0.5))
for patch in nrplot['boxes']:
    patch.set_facecolor((1.0, 0.4980392156862745, 0.3137254901960784, 0.5))
for patch in ncplot['boxes']:
    patch.set_facecolor('#1f77b4')

ax.legend([fbplot["boxes"][0], nrplot["boxes"][0], ncplot["boxes"][0]], ['NR-fallback', 'NR-full', 'no cooperation'])
plt.xticks(x, name_MNO)
plt.ylabel('FSP')
plt.savefig('Figures/FSPperMNO_enschede.pdf', dpi=1000)
#plt.show()


# fsp Enschede
fdp_KPN_Enschede, fdp_T_Mobile_Enschede, fdp_Vodafone_Enschede  = [], [], []
for samp in fdp_per_mno_Enschede:
    fdp_KPN_Enschede.append(samp["KPN"])
    fdp_T_Mobile_Enschede.append(samp["T-Mobile"])
    fdp_Vodafone_Enschede.append(samp["Vodafone"])

fdp_KPN_Enschede_NR, fdp_T_Mobile_Enschede_NR, fdp_Vodafone_Enschede_NR  = [], [], []
for samp in fdp_per_mno_Enschede_NR:
    fdp_KPN_Enschede_NR.append(samp["KPN"])
    fdp_T_Mobile_Enschede_NR.append(samp["T-Mobile"])
    fdp_Vodafone_Enschede_NR.append(samp["Vodafone"])

fdp_KPN_Enschede_NC, fdp_T_Mobile_Enschede_NC, fdp_Vodafone_Enschede_NC  = [], [], []
for samp in fdp_KPN_Enschede_nc:
    fdp_KPN_Enschede_NC.append(samp["KPN"])
for samp in fdp_T_Mobile_Enschede_nc:
    fdp_T_Mobile_Enschede_NC.append(samp["T-Mobile"])
for samp in fdp_Vodafone_Enschede_nc:
    fdp_Vodafone_Enschede_NC.append(samp["Vodafone"])


fig, ax = plt.subplots()
fbplot = ax.boxplot([fdp_KPN_Enschede, fdp_T_Mobile_Enschede, fdp_Vodafone_Enschede, total_fdp_Enschede], positions=x - 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)
nrplot = ax.boxplot([fdp_KPN_Enschede_NR, fdp_T_Mobile_Enschede_NR, fdp_Vodafone_Enschede_NR, total_fdp_Enschede_NR], positions=x, widths=box_width, patch_artist=True, showfliers=False)
total_fdp_Enschede_NC = np.add(np.add(fdp_KPN_Enschede_NC, fdp_T_Mobile_Enschede_NC), fdp_Vodafone_Enschede_NC)/3 # only possible because all the scenarios uses the same number of users.
ncplot = ax.boxplot([fdp_KPN_Enschede_NC, fdp_T_Mobile_Enschede_NC, fdp_Vodafone_Enschede_NC, total_fdp_Enschede_NC], positions=x + 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)

for patch in fbplot['boxes']:
    patch.set_facecolor((0.2549019607843137, 0.4117647058823529, 0.8823529411764706, 0.5))
for patch in nrplot['boxes']:
    patch.set_facecolor((1.0, 0.4980392156862745, 0.3137254901960784, 0.5))
for patch in ncplot['boxes']:
    patch.set_facecolor('#1f77b4')

ax.legend([fbplot["boxes"][0], nrplot["boxes"][0], ncplot["boxes"][0]], ['NR-fallback', 'NR-full', 'no cooperation'])
plt.xticks(x, name_MNO)
plt.ylabel('FDP')
plt.savefig('Figures/FDPperMNO_enschede.pdf', dpi=1000)
#plt.show()




# Amsterdam
p_KPN_Amsterdam, p_T_Mobile_Amsterdam, p_Vodafone_Amsterdam  = [], [], []
for samp in p_per_mno_Amsterdam:
    p_KPN_Amsterdam.append(samp["KPN"])
    p_T_Mobile_Amsterdam.append(samp["T-Mobile"])
    p_Vodafone_Amsterdam.append(samp["Vodafone"])

p_KPN_Amsterdam_NR, p_T_Mobile_Amsterdam_NR, p_Vodafone_Amsterdam_NR  = [], [], []
for samp in p_per_mno_Amsterdam_NR:
    p_KPN_Amsterdam_NR.append(samp["KPN"])
    p_T_Mobile_Amsterdam_NR.append(samp["T-Mobile"])
    p_Vodafone_Amsterdam_NR.append(samp["Vodafone"])

p_KPN_Amsterdam_NC, p_T_Mobile_Amsterdam_NC, p_Vodafone_Amsterdam_NC  = [], [], []
for samp in p_KPN_Amsterdam_nc:
    p_KPN_Amsterdam_NC.append(samp["KPN"])
for samp in p_T_Mobile_Amsterdam_nc:
    p_T_Mobile_Amsterdam_NC.append(samp["T-Mobile"])
for samp in p_Vodafone_Amsterdam_nc:
    p_Vodafone_Amsterdam_NC.append(samp["Vodafone"])

MNOs = ['KPN', 'T-Mobile', 'Vodafone']
name_MNO = ['MNO-1', 'MNO-2', 'MNO-3', 'Total']

#x = np.array([1, 2, 3])
fig, ax = plt.subplots()
fbplot = ax.boxplot([p_KPN_Amsterdam, p_T_Mobile_Amsterdam, p_Vodafone_Amsterdam, np.add(np.add(p_KPN_Amsterdam, p_T_Mobile_Amsterdam), p_Vodafone_Amsterdam)], positions=x - 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)
nrplot = ax.boxplot([p_KPN_Amsterdam_NR, p_T_Mobile_Amsterdam_NR, p_Vodafone_Amsterdam_NR, np.add(np.add(p_KPN_Amsterdam_NR, p_T_Mobile_Amsterdam_NR), p_Vodafone_Amsterdam_NR)], positions=x, widths=box_width, patch_artist=True, showfliers=False)
ncplot = ax.boxplot([p_KPN_Amsterdam_NC, p_T_Mobile_Amsterdam_NC, p_Vodafone_Amsterdam_NC, np.add(np.add(p_KPN_Amsterdam_NC, p_T_Mobile_Amsterdam_NC), p_Vodafone_Amsterdam_NC)], positions=x + 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)

for patch in fbplot['boxes']:
    patch.set_facecolor((0.2549019607843137, 0.4117647058823529, 0.8823529411764706, 0.5))
for patch in nrplot['boxes']:
    patch.set_facecolor((1.0, 0.4980392156862745, 0.3137254901960784, 0.5))
for patch in ncplot['boxes']:
    patch.set_facecolor('#1f77b4')

ax.legend([fbplot["boxes"][0], nrplot["boxes"][0], ncplot["boxes"][0]], ['NR-fallback', 'NR-full', 'no cooperation'])
plt.xticks(x, name_MNO)
plt.ylabel('Total power consumption (W)')
plt.savefig('Figures/powerperMNO_amsterdam.pdf', dpi=1000)
#plt.show()


# fsp Amsterdam
fsp_KPN_Amsterdam, fsp_T_Mobile_Amsterdam, fsp_Vodafone_Amsterdam  = [], [], []
for samp in fsp_per_mno_Amsterdam:
    fsp_KPN_Amsterdam.append(samp["KPN"])
    fsp_T_Mobile_Amsterdam.append(samp["T-Mobile"])
    fsp_Vodafone_Amsterdam.append(samp["Vodafone"])

fsp_KPN_Amsterdam_NR, fsp_T_Mobile_Amsterdam_NR, fsp_Vodafone_Amsterdam_NR  = [], [], []
for samp in fsp_per_mno_Amsterdam_NR:
    fsp_KPN_Amsterdam_NR.append(samp["KPN"])
    fsp_T_Mobile_Amsterdam_NR.append(samp["T-Mobile"])
    fsp_Vodafone_Amsterdam_NR.append(samp["Vodafone"])

fsp_KPN_Amsterdam_NC, fsp_T_Mobile_Amsterdam_NC, fsp_Vodafone_Amsterdam_NC  = [], [], []
for samp in fsp_KPN_Amsterdam_nc:
    fsp_KPN_Amsterdam_NC.append(samp["KPN"])
for samp in fsp_T_Mobile_Amsterdam_nc:
    fsp_T_Mobile_Amsterdam_NC.append(samp["T-Mobile"])
for samp in fsp_Vodafone_Amsterdam_nc:
    fsp_Vodafone_Amsterdam_NC.append(samp["Vodafone"])


fig, ax = plt.subplots()
fbplot = ax.boxplot([fsp_KPN_Amsterdam, fsp_T_Mobile_Amsterdam, fsp_Vodafone_Amsterdam, total_fsp_Amsterdam], positions=x - 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)
nrplot = ax.boxplot([fsp_KPN_Amsterdam_NR, fsp_T_Mobile_Amsterdam_NR, fsp_Vodafone_Amsterdam_NR, total_fsp_Amsterdam_NR], positions=x, widths=box_width, patch_artist=True, showfliers=False)
total_fsp_Amsterdam_NC = np.add(np.add(fsp_KPN_Amsterdam_NC, fsp_T_Mobile_Amsterdam_NC), fsp_Vodafone_Amsterdam_NC)/3 # only possible because all the scenarios uses the same number of users.
ncplot = ax.boxplot([fsp_KPN_Amsterdam_NC, fsp_T_Mobile_Amsterdam_NC, fsp_Vodafone_Amsterdam_NC, total_fsp_Amsterdam_NC], positions=x + 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)

for patch in fbplot['boxes']:
    patch.set_facecolor((0.2549019607843137, 0.4117647058823529, 0.8823529411764706, 0.5))
for patch in nrplot['boxes']:
    patch.set_facecolor((1.0, 0.4980392156862745, 0.3137254901960784, 0.5))
for patch in ncplot['boxes']:
    patch.set_facecolor('#1f77b4')

ax.legend([fbplot["boxes"][0], nrplot["boxes"][0], ncplot["boxes"][0]], ['NR-fallback', 'NR-full', 'no cooperation'])
plt.xticks(x, name_MNO)
plt.ylabel('FSP')
plt.savefig('Figures/FSPperMNO_amsterdam.pdf', dpi=1000)
#plt.show()


# fsp Amsterdam
fdp_KPN_Amsterdam, fdp_T_Mobile_Amsterdam, fdp_Vodafone_Amsterdam  = [], [], []
for samp in fdp_per_mno_Amsterdam:
    fdp_KPN_Amsterdam.append(samp["KPN"])
    fdp_T_Mobile_Amsterdam.append(samp["T-Mobile"])
    fdp_Vodafone_Amsterdam.append(samp["Vodafone"])

fdp_KPN_Amsterdam_NR, fdp_T_Mobile_Amsterdam_NR, fdp_Vodafone_Amsterdam_NR  = [], [], []
for samp in fdp_per_mno_Amsterdam_NR:
    fdp_KPN_Amsterdam_NR.append(samp["KPN"])
    fdp_T_Mobile_Amsterdam_NR.append(samp["T-Mobile"])
    fdp_Vodafone_Amsterdam_NR.append(samp["Vodafone"])

fdp_KPN_Amsterdam_NC, fdp_T_Mobile_Amsterdam_NC, fdp_Vodafone_Amsterdam_NC  = [], [], []
for samp in fdp_KPN_Amsterdam_nc:
    fdp_KPN_Amsterdam_NC.append(samp["KPN"])
for samp in fdp_T_Mobile_Amsterdam_nc:
    fdp_T_Mobile_Amsterdam_NC.append(samp["T-Mobile"])
for samp in fdp_Vodafone_Amsterdam_nc:
    fdp_Vodafone_Amsterdam_NC.append(samp["Vodafone"])


fig, ax = plt.subplots()
fbplot = ax.boxplot([fdp_KPN_Amsterdam, fdp_T_Mobile_Amsterdam, fdp_Vodafone_Amsterdam, total_fdp_Amsterdam], positions=x - 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)
nrplot = ax.boxplot([fdp_KPN_Amsterdam_NR, fdp_T_Mobile_Amsterdam_NR, fdp_Vodafone_Amsterdam_NR, total_fdp_Amsterdam_NR], positions=x, widths=box_width, patch_artist=True, showfliers=False)
total_fdp_Amsterdam_NC = np.add(np.add(fdp_KPN_Amsterdam_NC, fdp_T_Mobile_Amsterdam_NC), fdp_Vodafone_Amsterdam_NC)/3 # only possible because all the scenarios uses the same number of users.
ncplot = ax.boxplot([fdp_KPN_Amsterdam_NC, fdp_T_Mobile_Amsterdam_NC, fdp_Vodafone_Amsterdam_NC, total_fdp_Amsterdam_NC], positions=x + 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)

for patch in fbplot['boxes']:
    patch.set_facecolor((0.2549019607843137, 0.4117647058823529, 0.8823529411764706, 0.5))
for patch in nrplot['boxes']:
    patch.set_facecolor((1.0, 0.4980392156862745, 0.3137254901960784, 0.5))
for patch in ncplot['boxes']:
    patch.set_facecolor('#1f77b4')

ax.legend([fbplot["boxes"][0], nrplot["boxes"][0], ncplot["boxes"][0]], ['NR-fallback', 'NR-full', 'no cooperation'])
plt.xticks(x, name_MNO)
plt.ylabel('FDP')
plt.savefig('Figures/FDPperMNO_amsterdam.pdf', dpi=1000)
#plt.show()
