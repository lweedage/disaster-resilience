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

# fallback MNO-2 and MNO-3
p_per_mno_fp_Middelburg_fb23 = util.from_data(f'data/Realisations/Middelburgall_MNOs0.021backupVodafoneT-Mobile{max_iterations}_totalpower_per_mno_fp.p')
p_per_mno_Middelburg_fb23 = util.from_data(f'data/Realisations/Middelburgall_MNOs0.021backupVodafoneT-Mobile{max_iterations}_totalpower_per_mno.p')
p_per_mno_fp_Enschede_fb23 = util.from_data(f'data/Realisations/Enschedeall_MNOs0.021backupVodafoneT-Mobile{max_iterations}_totalpower_per_mno_fp.p')
p_per_mno_Enschede_fb23 = util.from_data(f'data/Realisations/Enschedeall_MNOs0.021backupVodafoneT-Mobile{max_iterations}_totalpower_per_mno.p')
p_per_mno_fp_Amsterdam_fb23 = util.from_data(f'data/Realisations/Amsterdamall_MNOs0.021backupVodafoneT-Mobile{max_iterations}_totalpower_per_mno_fp.p')
p_per_mno_Amsterdam_fb23 = util.from_data(f'data/Realisations/Amsterdamall_MNOs0.021backupVodafoneT-Mobile{max_iterations}_totalpower_per_mno.p')

fdp_per_mno_Middelburg_fb23 = util.from_data(f'data/Realisations/Middelburgall_MNOs0.021backupVodafoneT-Mobile{max_iterations}_fdp_per_MNO.p')
fdp_per_mno_Enschede_fb23 = util.from_data(f'data/Realisations/Enschedeall_MNOs0.021backupVodafoneT-Mobile{max_iterations}_fdp_per_MNO.p')
fdp_per_mno_Amsterdam_fb23 = util.from_data(f'data/Realisations/Amsterdamall_MNOs0.021backupVodafoneT-Mobile{max_iterations}_fdp_per_MNO.p')
fsp_per_mno_Middelburg_fb23 = util.from_data(f'data/Realisations/Middelburgall_MNOs0.021backupVodafoneT-Mobile{max_iterations}_fsp_per_MNO.p')
fsp_per_mno_Enschede_fb23 = util.from_data(f'data/Realisations/Enschedeall_MNOs0.021backupVodafoneT-Mobile{max_iterations}_fsp_per_MNO.p')
fsp_per_mno_Amsterdam_fb23 = util.from_data(f'data/Realisations/Amsterdamall_MNOs0.021backupVodafoneT-Mobile{max_iterations}_fsp_per_MNO.p')

total_fsp_Middelburg_fb23 = util.from_data(f'data/Realisations/Middelburgall_MNOs0.021backupVodafoneT-Mobile{max_iterations}_totalfsp.p')
total_fdp_Middelburg_fb23 = util.from_data(f'data/Realisations/Middelburgall_MNOs0.021backupVodafoneT-Mobile{max_iterations}_totalfdp.p')
total_fsp_Enschede_fb23 = util.from_data(f'data/Realisations/Enschedeall_MNOs0.021backupVodafoneT-Mobile{max_iterations}_totalfsp.p')
total_fdp_Enschede_fb23 = util.from_data(f'data/Realisations/Enschedeall_MNOs0.021backupVodafoneT-Mobile{max_iterations}_totalfdp.p')
total_fsp_Amsterdam_fb23 = util.from_data(f'data/Realisations/Amsterdamall_MNOs0.021backupVodafoneT-Mobile{max_iterations}_totalfsp.p')
total_fdp_Amsterdam_fb23 = util.from_data(f'data/Realisations/Amsterdamall_MNOs0.021backupVodafoneT-Mobile{max_iterations}_totalfdp.p')

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
total_p_Middelburg = np.add(np.add(p_KPN_Middelburg, p_T_Mobile_Middelburg), p_Vodafone_Middelburg)
fbplot = ax.boxplot([p_KPN_Middelburg, p_T_Mobile_Middelburg, p_Vodafone_Middelburg, total_p_Middelburg], positions=x - 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)
total_p_Middelburg_NR = np.add(np.add(p_KPN_Middelburg_NR, p_T_Mobile_Middelburg_NR), p_Vodafone_Middelburg_NR)
nrplot = ax.boxplot([p_KPN_Middelburg_NR, p_T_Mobile_Middelburg_NR, p_Vodafone_Middelburg_NR, total_p_Middelburg_NR], positions=x, widths=box_width, patch_artist=True, showfliers=False)
total_p_Middelburg_NC =np.add(np.add(p_KPN_Middelburg_NC, p_T_Mobile_Middelburg_NC), p_Vodafone_Middelburg_NC)
ncplot = ax.boxplot([p_KPN_Middelburg_NC, p_T_Mobile_Middelburg_NC, p_Vodafone_Middelburg_NC, total_p_Middelburg_NC], positions=x + 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)

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
total_p_Enschede = np.add(np.add(p_KPN_Enschede, p_T_Mobile_Enschede), p_Vodafone_Enschede)
fbplot = ax.boxplot([p_KPN_Enschede, p_T_Mobile_Enschede, p_Vodafone_Enschede, total_p_Enschede], positions=x - 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)
total_p_Enschede_NR = np.add(np.add(p_KPN_Enschede_NR, p_T_Mobile_Enschede_NR), p_Vodafone_Enschede_NR)
nrplot = ax.boxplot([p_KPN_Enschede_NR, p_T_Mobile_Enschede_NR, p_Vodafone_Enschede_NR, total_p_Enschede_NR], positions=x, widths=box_width, patch_artist=True, showfliers=False)
total_p_Enschede_NC = np.add(np.add(p_KPN_Enschede_NC, p_T_Mobile_Enschede_NC), p_Vodafone_Enschede_NC)
ncplot = ax.boxplot([p_KPN_Enschede_NC, p_T_Mobile_Enschede_NC, p_Vodafone_Enschede_NC, total_p_Enschede_NC], positions=x + 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)

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

p_T_Mobile_Amsterdam_FB23, p_Vodafone_Amsterdam_FB23  = [], []
for samp in p_per_mno_Amsterdam_fb23:
    p_T_Mobile_Amsterdam_FB23.append(samp["T-Mobile"])
    p_Vodafone_Amsterdam_FB23.append(samp["Vodafone"])

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
name_MNO = ['MNO$_1$', 'MNO$_2$', 'MNO$_3$', 'Total']

#x = np.array([1, 2, 3])
fig, ax = plt.subplots()
#fbplot = ax.boxplot([p_KPN_Amsterdam, p_T_Mobile_Amsterdam, p_Vodafone_Amsterdam, np.add(np.add(p_KPN_Amsterdam, p_T_Mobile_Amsterdam), p_Vodafone_Amsterdam)], positions=x - 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)
#nrplot = ax.boxplot([p_KPN_Amsterdam_NR, p_T_Mobile_Amsterdam_NR, p_Vodafone_Amsterdam_NR, np.add(np.add(p_KPN_Amsterdam_NR, p_T_Mobile_Amsterdam_NR), p_Vodafone_Amsterdam_NR)], positions=x, widths=box_width, patch_artist=True, showfliers=False)
#ncplot = ax.boxplot([p_KPN_Amsterdam_NC, p_T_Mobile_Amsterdam_NC, p_Vodafone_Amsterdam_NC, np.add(np.add(p_KPN_Amsterdam_NC, p_T_Mobile_Amsterdam_NC), p_Vodafone_Amsterdam_NC)], positions=x + 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)
# TODO: No need for x_aux anymore. only use x and adjust box_width
x_aux = np.array([x[0]+1.5*box_width, x[1]+3*box_width, x[2]+4.5*box_width, x[3]+6*box_width])
posfb = [x_aux[0] - 2.25*box_width, x_aux[1] - 2.25*box_width, x_aux[2] - 2.25*box_width, x_aux[3] - 2.25*box_width] 
posfb23 = np.array([x_aux[0] - 0.75*box_width, x_aux[1] - 0.75*box_width, x_aux[2] - 0.75*box_width, x_aux[3] - 0.75*box_width])
posnr = [x_aux[0]+ 0.75*box_width, x_aux[1] + 0.75*box_width, x_aux[2] + 0.75*box_width, x_aux[3] + 0.75*box_width]
posnc = [x_aux[0] + 2.25*box_width, x_aux[1] + 2.25*box_width, x_aux[2] + 2.25*box_width, x_aux[3] + 2.25*box_width] 

total_p_Amsterdam = np.add(np.add(p_KPN_Amsterdam, p_T_Mobile_Amsterdam), p_Vodafone_Amsterdam)
fbplot = ax.boxplot([p_KPN_Amsterdam, p_T_Mobile_Amsterdam, p_Vodafone_Amsterdam, total_p_Amsterdam], positions=posfb, widths=box_width, patch_artist=True, showfliers=False)
total_p_Amsterdam_NR = np.add(np.add(p_KPN_Amsterdam_NR, p_T_Mobile_Amsterdam_NR), p_Vodafone_Amsterdam_NR)
nrplot = ax.boxplot([p_KPN_Amsterdam_NR, p_T_Mobile_Amsterdam_NR, p_Vodafone_Amsterdam_NR, total_p_Amsterdam_NR], positions=posnr, widths=box_width, patch_artist=True, showfliers=False)
total_p_Amsterdam_NC = np.add(np.add(p_KPN_Amsterdam_NC, p_T_Mobile_Amsterdam_NC), p_Vodafone_Amsterdam_NC)
ncplot = ax.boxplot([p_KPN_Amsterdam_NC, p_T_Mobile_Amsterdam_NC, p_Vodafone_Amsterdam_NC, total_p_Amsterdam_NC], positions=posnc, widths=box_width, patch_artist=True, showfliers=False)
total_p_Amsterdam_FB23 = np.add(np.add(p_T_Mobile_Amsterdam_FB23, p_Vodafone_Amsterdam_FB23),p_KPN_Amsterdam_NC)
fb23plot = ax.boxplot([p_KPN_Amsterdam_NC, p_T_Mobile_Amsterdam_FB23, p_Vodafone_Amsterdam_FB23, total_p_Amsterdam_FB23], positions=posfb23, widths=box_width, patch_artist=True, showfliers=False)

print(np.mean(total_p_Amsterdam_NR)/np.mean(total_p_Amsterdam_NC))

ax.axvspan((x_aux[0]+x_aux[1])/2, (x_aux[1]+x_aux[2])/2, color='#CCC', alpha=0.2, lw=0)
ax.axvspan((x_aux[2]+x_aux[3])/2, x_aux[3] + 1 + 0.75*box_width , color='#CCC', alpha=0.2, lw=0)

for patch in fbplot['boxes'] + fbplot['whiskers'] + fbplot['caps']:
    #patch.set_facecolor(util.get_boxplot_color(0))
    patch.set(color=util.get_boxplot_color(0))
for patch in nrplot['boxes'] + nrplot['whiskers'] + nrplot['caps']:
    #patch.set_facecolor(util.get_boxplot_color(1))
    patch.set(color=util.get_boxplot_color(1))
for patch in ncplot['boxes'] + ncplot['whiskers'] + ncplot['caps']:
    #patch.set_facecolor(util.get_boxplot_color(2))
    patch.set(color=util.get_boxplot_color(2))
for patch in fb23plot['boxes'] + fb23plot['whiskers'] + fb23plot['caps']:
    #patch.set_facecolor(util.get_boxplot_color(3))
    patch.set(color=util.get_boxplot_color(3))

#ax.legend([fbplot["boxes"][0], nrplot["boxes"][0], ncplot["boxes"][0]], ['NR-fallback', 'NR-full', 'no cooperation'])
ax.legend([fbplot["boxes"][0], fb23plot["boxes"][0], nrplot["boxes"][0], ncplot["boxes"][0]], ['NR-fallback', 'NR-fallback 2&3', 'NR-full', 'no cooperation'])
plt.xticks(x_aux, name_MNO)
plt.ylabel('Total power consumption (W)')
plt.savefig('Figures/powerperMNO_amsterdam.pdf', dpi=1000)
# plt.show()



# fsp Amsterdam
fsp_KPN_Amsterdam, fsp_T_Mobile_Amsterdam, fsp_Vodafone_Amsterdam  = [], [], []
for samp in fsp_per_mno_Amsterdam:
    fsp_KPN_Amsterdam.append(samp["KPN"])
    fsp_T_Mobile_Amsterdam.append(samp["T-Mobile"])
    fsp_Vodafone_Amsterdam.append(samp["Vodafone"])

fsp_T_Mobile_Amsterdam_FB23, fsp_Vodafone_Amsterdam_FB23  = [], []
for samp in fsp_per_mno_Amsterdam_fb23:
    fsp_T_Mobile_Amsterdam_FB23.append(samp["T-Mobile"])
    fsp_Vodafone_Amsterdam_FB23.append(samp["Vodafone"])

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
fbplot = ax.boxplot([fsp_KPN_Amsterdam, fsp_T_Mobile_Amsterdam, fsp_Vodafone_Amsterdam, total_fsp_Amsterdam], positions=posfb, widths=box_width, patch_artist=True, showfliers=False)
# For KPN it is equivalent to the non coop case in the total for FB23
total_fsp_Amsterdam_FB23 = np.add(np.add(fsp_T_Mobile_Amsterdam_FB23, fsp_Vodafone_Amsterdam_FB23), fsp_KPN_Amsterdam_NC)/3 # only possible because all the scenarios uses the same number of users.
fb23plot = ax.boxplot([fsp_KPN_Amsterdam_NC, fsp_T_Mobile_Amsterdam_FB23, fsp_Vodafone_Amsterdam_FB23, total_fsp_Amsterdam_FB23], positions=posfb23, widths=box_width, patch_artist=True, showfliers=False)
nrplot = ax.boxplot([fsp_KPN_Amsterdam_NR, fsp_T_Mobile_Amsterdam_NR, fsp_Vodafone_Amsterdam_NR, total_fsp_Amsterdam_NR], positions=posnr, widths=box_width, patch_artist=True, showfliers=False)
total_fsp_Amsterdam_NC = np.add(np.add(fsp_KPN_Amsterdam_NC, fsp_T_Mobile_Amsterdam_NC), fsp_Vodafone_Amsterdam_NC)/3 # only possible because all the scenarios uses the same number of users.
ncplot = ax.boxplot([fsp_KPN_Amsterdam_NC, fsp_T_Mobile_Amsterdam_NC, fsp_Vodafone_Amsterdam_NC, total_fsp_Amsterdam_NC], positions=posnc, widths=box_width, patch_artist=True, showfliers=False)

#print(np.mean(total_fsp_Amsterdam_NR)-np.mean(total_fsp_Amsterdam_NC))

ax.axvspan((x_aux[0]+x_aux[1])/2, (x_aux[1]+x_aux[2])/2, color='#CCC', alpha=0.2, lw=0)
ax.axvspan((x_aux[2]+x_aux[3])/2, x_aux[3] + 1 + 0.75*box_width , color='#CCC', alpha=0.2, lw=0)

""" for patch in fbplot['boxes']:
    patch.set_facecolor(util.get_boxplot_color(0))
for patch in nrplot['boxes']:
    patch.set_facecolor(util.get_boxplot_color(1))
for patch in ncplot['boxes']:
    patch.set_facecolor(util.get_boxplot_color(2))
for patch in fb23plot['boxes']:
    patch.set_facecolor(util.get_boxplot_color(3)) """
for patch in fbplot['boxes'] + fbplot['whiskers'] + fbplot['caps']:
    #patch.set_facecolor(util.get_boxplot_color(0))
    patch.set(color=util.get_boxplot_color(0))
for patch in nrplot['boxes'] + nrplot['whiskers'] + nrplot['caps']:
    #patch.set_facecolor(util.get_boxplot_color(1))
    patch.set(color=util.get_boxplot_color(1))
for patch in ncplot['boxes'] + ncplot['whiskers'] + ncplot['caps']:
    #patch.set_facecolor(util.get_boxplot_color(2))
    patch.set(color=util.get_boxplot_color(2))
for patch in fb23plot['boxes'] + fb23plot['whiskers'] + fb23plot['caps']:
    #patch.set_facecolor(util.get_boxplot_color(3))
    patch.set(color=util.get_boxplot_color(3))

ax.legend([fbplot["boxes"][0], fb23plot["boxes"][0], nrplot["boxes"][0], ncplot["boxes"][0]], ['NR-fallback', 'NR-fallback 2&3', 'NR-full', 'no cooperation'], loc='upper left', bbox_to_anchor=(0.17, 0.35))
plt.xticks(x_aux, name_MNO)
plt.ylabel('FSP')
plt.savefig('Figures/FSPperMNO_amsterdam.pdf', dpi=1000)
# plt.show()


# fdp Amsterdam
fdp_KPN_Amsterdam, fdp_T_Mobile_Amsterdam, fdp_Vodafone_Amsterdam  = [], [], []
for samp in fdp_per_mno_Amsterdam:
    fdp_KPN_Amsterdam.append(samp["KPN"])
    fdp_T_Mobile_Amsterdam.append(samp["T-Mobile"])
    fdp_Vodafone_Amsterdam.append(samp["Vodafone"])

fdp_T_Mobile_Amsterdam_FB23, fdp_Vodafone_Amsterdam_FB23  = [], []
for samp in fdp_per_mno_Amsterdam_fb23:
    fdp_T_Mobile_Amsterdam_FB23.append(samp["T-Mobile"])
    fdp_Vodafone_Amsterdam_FB23.append(samp["Vodafone"])

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
fbplot = ax.boxplot([fdp_KPN_Amsterdam, fdp_T_Mobile_Amsterdam, fdp_Vodafone_Amsterdam, total_fdp_Amsterdam], positions=posfb, widths=box_width, patch_artist=True, showfliers=False)
# For KPN it is equivalent to the non coop case in the total for FB23
total_fdp_Amsterdam_FB23 = np.add(np.add(fdp_T_Mobile_Amsterdam_FB23, fdp_Vodafone_Amsterdam_FB23), fdp_KPN_Amsterdam_NC)/3 # only possible because all the scenarios uses the same number of users.
fb23plot = ax.boxplot([fdp_KPN_Amsterdam_NC, fdp_T_Mobile_Amsterdam_FB23, fdp_Vodafone_Amsterdam_FB23, total_fdp_Amsterdam_FB23], positions=posfb23, widths=box_width, patch_artist=True, showfliers=False)
nrplot = ax.boxplot([fdp_KPN_Amsterdam_NR, fdp_T_Mobile_Amsterdam_NR, fdp_Vodafone_Amsterdam_NR, total_fdp_Amsterdam_NR], positions=posnr, widths=box_width, patch_artist=True, showfliers=False)
total_fdp_Amsterdam_NC = np.add(np.add(fdp_KPN_Amsterdam_NC, fdp_T_Mobile_Amsterdam_NC), fdp_Vodafone_Amsterdam_NC)/3 # only possible because all the scenarios uses the same number of users.
ncplot = ax.boxplot([fdp_KPN_Amsterdam_NC, fdp_T_Mobile_Amsterdam_NC, fdp_Vodafone_Amsterdam_NC, total_fdp_Amsterdam_NC], positions=posnc, widths=box_width, patch_artist=True, showfliers=False)

ax.axvspan((x_aux[0]+x_aux[1])/2, (x_aux[1]+x_aux[2])/2, color='#CCC', alpha=0.2, lw=0)
ax.axvspan((x_aux[2]+x_aux[3])/2, x_aux[3] + 1 + 0.75*box_width , color='#CCC', alpha=0.2, lw=0)

""" for patch in fbplot['boxes']:
    patch.set_facecolor(util.get_boxplot_color(0))
for patch in nrplot['boxes']:
    patch.set_facecolor(util.get_boxplot_color(1))
for patch in ncplot['boxes']:
    patch.set_facecolor(util.get_boxplot_color(2))
for patch in fb23plot['boxes']:
    patch.set_facecolor(util.get_boxplot_color(3)) """
for patch in fbplot['boxes'] + fbplot['whiskers'] + fbplot['caps']:
    #patch.set_facecolor(util.get_boxplot_color(0))
    patch.set(color=util.get_boxplot_color(0))
for patch in nrplot['boxes'] + nrplot['whiskers'] + nrplot['caps']:
    #patch.set_facecolor(util.get_boxplot_color(1))
    patch.set(color=util.get_boxplot_color(1))
for patch in ncplot['boxes'] + ncplot['whiskers'] + ncplot['caps']:
    #patch.set_facecolor(util.get_boxplot_color(2))
    patch.set(color=util.get_boxplot_color(2))
for patch in fb23plot['boxes'] + fb23plot['whiskers'] + fb23plot['caps']:
    #patch.set_facecolor(util.get_boxplot_color(3))
    patch.set(color=util.get_boxplot_color(3))

ax.legend([fbplot["boxes"][0], fb23plot["boxes"][0], nrplot["boxes"][0], ncplot["boxes"][0]], ['NR-fallback', 'NR-fallback 2&3', 'NR-full', 'no cooperation'])
plt.xticks(x_aux, name_MNO)
plt.ylabel('FDP')
plt.savefig('Figures/FDPperMNO_amsterdam.pdf', dpi=1000)
#plt.show()










# ======= Random failure ===========
# fallback
p_per_mno_Middelburg_random10 = util.from_data(f'data/Realisations/Middelburgall_MNOs0.021random0.1backup{max_iterations}_totalpower_per_mno.p')
p_per_mno_Enschede_random10 = util.from_data(f'data/Realisations/Enschedeall_MNOs0.021random0.1backup{max_iterations}_totalpower_per_mno.p')
p_per_mno_Amsterdam_random10 = util.from_data(f'data/Realisations/Amsterdamall_MNOs0.021random0.1backup{max_iterations}_totalpower_per_mno.p')

fdp_per_mno_Middelburg_random10 = util.from_data(f'data/Realisations/Middelburgall_MNOs0.021random0.1backup{max_iterations}_fdp_per_MNO.p')
fdp_per_mno_Enschede_random10 = util.from_data(f'data/Realisations/Enschedeall_MNOs0.021random0.1backup{max_iterations}_fdp_per_MNO.p')
fdp_per_mno_Amsterdam_random10 = util.from_data(f'data/Realisations/Amsterdamall_MNOs0.021random0.1backup{max_iterations}_fdp_per_MNO.p')
fsp_per_mno_Middelburg_random10 = util.from_data(f'data/Realisations/Middelburgall_MNOs0.021random0.1backup{max_iterations}_fsp_per_MNO.p')
fsp_per_mno_Enschede_random10 = util.from_data(f'data/Realisations/Enschedeall_MNOs0.021random0.1backup{max_iterations}_fsp_per_MNO.p')
fsp_per_mno_Amsterdam_random10 = util.from_data(f'data/Realisations/Amsterdamall_MNOs0.021random0.1backup{max_iterations}_fsp_per_MNO.p')

total_fsp_Middelburg_random10 = util.from_data(f'data/Realisations/Middelburgall_MNOs0.021random0.1backup{max_iterations}_totalfsp.p')
total_fdp_Middelburg_random10 = util.from_data(f'data/Realisations/Middelburgall_MNOs0.021random0.1backup{max_iterations}_totalfdp.p')
total_fsp_Enschede_random10 = util.from_data(f'data/Realisations/Enschedeall_MNOs0.021random0.1backup{max_iterations}_totalfsp.p')
total_fdp_Enschede_random10 = util.from_data(f'data/Realisations/Enschedeall_MNOs0.021random0.1backup{max_iterations}_totalfdp.p')
total_fsp_Amsterdam_random10 = util.from_data(f'data/Realisations/Amsterdamall_MNOs0.021random0.1backup{max_iterations}_totalfsp.p')
total_fdp_Amsterdam_random10 = util.from_data(f'data/Realisations/Amsterdamall_MNOs0.021random0.1backup{max_iterations}_totalfdp.p')

# National Roaming
p_per_mno_fp_Middelburg_random10_NR = util.from_data(f'data/Realisations/Middelburgall_MNOs0.021random0.1{max_iterations}_totalpower_per_mno_fp.p')
p_per_mno_Middelburg_random10_NR = util.from_data(f'data/Realisations/Middelburgall_MNOs0.021random0.1{max_iterations}_totalpower_per_mno.p')
p_per_mno_fp_Enschede_random10_NR = util.from_data(f'data/Realisations/Enschedeall_MNOs0.021random0.1{max_iterations}_totalpower_per_mno_fp.p')
p_per_mno_Enschede_random10_NR = util.from_data(f'data/Realisations/Enschedeall_MNOs0.021random0.1{max_iterations}_totalpower_per_mno.p')
p_per_mno_Amsterdam_random10_NR = util.from_data(f'data/Realisations/Amsterdamall_MNOs0.021random0.1{max_iterations}_totalpower_per_mno.p')

fdp_per_mno_Middelburg_random10_NR = util.from_data(f'data/Realisations/Middelburgall_MNOs0.021random0.1{max_iterations}_fdp_per_MNO.p')
fdp_per_mno_Enschede_random10_NR = util.from_data(f'data/Realisations/Enschedeall_MNOs0.021random0.1{max_iterations}_fdp_per_MNO.p')
fdp_per_mno_Amsterdam_random10_NR = util.from_data(f'data/Realisations/Amsterdamall_MNOs0.021random0.1{max_iterations}_fdp_per_MNO.p')
fsp_per_mno_Middelburg_random10_NR = util.from_data(f'data/Realisations/Middelburgall_MNOs0.021random0.1{max_iterations}_fsp_per_MNO.p')
fsp_per_mno_Enschede_random10_NR = util.from_data(f'data/Realisations/Enschedeall_MNOs0.021random0.1{max_iterations}_fsp_per_MNO.p')
fsp_per_mno_Amsterdam_random10_NR = util.from_data(f'data/Realisations/Amsterdamall_MNOs0.021random0.1{max_iterations}_fsp_per_MNO.p')

total_fdp_Middelburg_random10_NR = util.from_data(f'data/Realisations/Middelburgall_MNOs0.021random0.1{max_iterations}_totalfdp.p')
total_fdp_Enschede_random10_NR = util.from_data(f'data/Realisations/Enschedeall_MNOs0.021random0.1{max_iterations}_totalfdp.p')
total_fdp_Amsterdam_random10_NR = util.from_data(f'data/Realisations/Amsterdamall_MNOs0.021random0.1{max_iterations}_totalfdp.p')
total_fsp_Middelburg_random10_NR = util.from_data(f'data/Realisations/Middelburgall_MNOs0.021random0.1{max_iterations}_totalfsp.p')
total_fsp_Enschede_random10_NR = util.from_data(f'data/Realisations/Enschedeall_MNOs0.021random0.1{max_iterations}_totalfsp.p')
total_fsp_Amsterdam_random10_NR = util.from_data(f'data/Realisations/Amsterdamall_MNOs0.021random0.1{max_iterations}_totalfsp.p')

# No coop
p_KPN_fp_Middelburg_random10_nc = util.from_data(f'data/Realisations/MiddelburgKPN0.020.33random0.1{max_iterations}_totalpower_per_mno_fp.p')
p_KPN_Middelburg_random10_nc = util.from_data(f'data/Realisations/MiddelburgKPN0.020.33random0.1{max_iterations}_totalpower_per_mno.p')
p_T_Mobile_fp_Middelburg_random10_nc = util.from_data(f'data/Realisations/MiddelburgT-Mobile0.020.33random0.1{max_iterations}_totalpower_per_mno_fp.p')
p_T_Mobile_Middelburg_random10_nc = util.from_data(f'data/Realisations/MiddelburgT-Mobile0.020.33random0.1{max_iterations}_totalpower_per_mno.p')
p_Vodafone_fp_Middelburg_random10_nc = util.from_data(f'data/Realisations/MiddelburgVodafone0.020.33random0.1{max_iterations}_totalpower_per_mno_fp.p')
p_Vodafone_Middelburg_random10_nc = util.from_data(f'data/Realisations/MiddelburgVodafone0.020.33random0.1{max_iterations}_totalpower_per_mno.p')

fdp_KPN_Middelburg_random10_nc = util.from_data(f'data/Realisations/MiddelburgKPN0.020.33random0.1{max_iterations}_fdp_per_MNO.p')
fdp_T_Mobile_Middelburg_random10_nc = util.from_data(f'data/Realisations/MiddelburgT-Mobile0.020.33random0.1{max_iterations}_fdp_per_MNO.p')
fdp_Vodafone_Middelburg_random10_nc = util.from_data(f'data/Realisations/MiddelburgVodafone0.020.33random0.1{max_iterations}_fdp_per_MNO.p')
fsp_KPN_Middelburg_random10_nc = util.from_data(f'data/Realisations/MiddelburgKPN0.020.33random0.1{max_iterations}_fsp_per_MNO.p')
fsp_T_Mobile_Middelburg_random10_nc = util.from_data(f'data/Realisations/MiddelburgT-Mobile0.020.33random0.1{max_iterations}_fsp_per_MNO.p')
fsp_Vodafone_Middelburg_random10_nc = util.from_data(f'data/Realisations/MiddelburgVodafone0.020.33random0.1{max_iterations}_fsp_per_MNO.p')

p_KPN_Enschede_random10_nc = util.from_data(f'data/Realisations/EnschedeKPN0.020.33random0.1{max_iterations}_totalpower_per_mno.p')
p_T_Mobile_Enschede_random10_nc = util.from_data(f'data/Realisations/EnschedeT-Mobile0.020.33random0.1{max_iterations}_totalpower_per_mno.p')
p_Vodafone_Enschede_random10_nc = util.from_data(f'data/Realisations/EnschedeVodafone0.020.33random0.1{max_iterations}_totalpower_per_mno.p')

fdp_KPN_Enschede_random10_nc = util.from_data(f'data/Realisations/EnschedeKPN0.020.33random0.1{max_iterations}_fdp_per_MNO.p')
fdp_T_Mobile_Enschede_random10_nc = util.from_data(f'data/Realisations/EnschedeT-Mobile0.020.33random0.1{max_iterations}_fdp_per_MNO.p')
fdp_Vodafone_Enschede_random10_nc = util.from_data(f'data/Realisations/EnschedeVodafone0.020.33random0.1{max_iterations}_fdp_per_MNO.p')
fsp_KPN_Enschede_random10_nc = util.from_data(f'data/Realisations/EnschedeKPN0.020.33random0.1{max_iterations}_fsp_per_MNO.p')
fsp_T_Mobile_Enschede_random10_nc = util.from_data(f'data/Realisations/EnschedeT-Mobile0.020.33random0.1{max_iterations}_fsp_per_MNO.p')
fsp_Vodafone_Enschede_random10_nc = util.from_data(f'data/Realisations/EnschedeVodafone0.020.33random0.1{max_iterations}_fsp_per_MNO.p')

p_KPN_Amsterdam_random10_nc = util.from_data(f'data/Realisations/AmsterdamKPN0.020.33random0.1{max_iterations}_totalpower_per_mno.p')
p_T_Mobile_Amsterdam_random10_nc = util.from_data(f'data/Realisations/AmsterdamT-Mobile0.020.33random0.1{max_iterations}_totalpower_per_mno.p')
p_Vodafone_Amsterdam_random10_nc = util.from_data(f'data/Realisations/AmsterdamVodafone0.020.33random0.1{max_iterations}_totalpower_per_mno.p')

fdp_KPN_Amsterdam_random10_nc = util.from_data(f'data/Realisations/AmsterdamKPN0.020.33random0.1{max_iterations}_fdp_per_MNO.p')
fdp_T_Mobile_Amsterdam_random10_nc = util.from_data(f'data/Realisations/AmsterdamT-Mobile0.020.33random0.1{max_iterations}_fdp_per_MNO.p')
fdp_Vodafone_Amsterdam_random10_nc = util.from_data(f'data/Realisations/AmsterdamVodafone0.020.33random0.1{max_iterations}_fdp_per_MNO.p')
fsp_KPN_Amsterdam_random10_nc = util.from_data(f'data/Realisations/AmsterdamKPN0.020.33random0.1{max_iterations}_fsp_per_MNO.p')
fsp_T_Mobile_Amsterdam_random10_nc = util.from_data(f'data/Realisations/AmsterdamT-Mobile0.020.33random0.1{max_iterations}_fsp_per_MNO.p')
fsp_Vodafone_Amsterdam_random10_nc = util.from_data(f'data/Realisations/AmsterdamVodafone0.020.33random0.1{max_iterations}_fsp_per_MNO.p')


# Amsterdam with 10% random failure
p_KPN_Amsterdam_random10, p_T_Mobile_Amsterdam_random10, p_Vodafone_Amsterdam_random10  = [], [], []
for samp in p_per_mno_Amsterdam_random10:
    p_KPN_Amsterdam_random10.append(samp["KPN"])
    p_T_Mobile_Amsterdam_random10.append(samp["T-Mobile"])
    p_Vodafone_Amsterdam_random10.append(samp["Vodafone"])


p_KPN_Amsterdam_random10_NR, p_T_Mobile_Amsterdam_random10_NR, p_Vodafone_Amsterdam_random10_NR  = [], [], []
for samp in p_per_mno_Amsterdam_random10_NR:
    p_KPN_Amsterdam_random10_NR.append(samp["KPN"])
    p_T_Mobile_Amsterdam_random10_NR.append(samp["T-Mobile"])
    p_Vodafone_Amsterdam_random10_NR.append(samp["Vodafone"])

p_KPN_Amsterdam_random10_NC, p_T_Mobile_Amsterdam_random10_NC, p_Vodafone_Amsterdam_random10_NC  = [], [], []
for samp in p_KPN_Amsterdam_random10_nc:
    p_KPN_Amsterdam_random10_NC.append(samp["KPN"])
for samp in p_T_Mobile_Amsterdam_random10_nc:
    p_T_Mobile_Amsterdam_random10_NC.append(samp["T-Mobile"])
for samp in p_Vodafone_Amsterdam_random10_nc:
    p_Vodafone_Amsterdam_random10_NC.append(samp["Vodafone"])


total_p_Amsterdam_random10 = np.add(np.add(p_KPN_Amsterdam_random10, p_T_Mobile_Amsterdam_random10), p_Vodafone_Amsterdam_random10)
total_p_Amsterdam_random10_NR = np.add(np.add(p_KPN_Amsterdam_random10_NR, p_T_Mobile_Amsterdam_random10_NR), p_Vodafone_Amsterdam_random10_NR)
total_p_Amsterdam_random10_NC = np.add(np.add(p_KPN_Amsterdam_random10_NC, p_T_Mobile_Amsterdam_random10_NC), p_Vodafone_Amsterdam_random10_NC)
# Enschede with 10% random failure
p_KPN_Enschede_random10, p_T_Mobile_Enschede_random10, p_Vodafone_Enschede_random10  = [], [], []
for samp in p_per_mno_Enschede_random10:
    p_KPN_Enschede_random10.append(samp["KPN"])
    p_T_Mobile_Enschede_random10.append(samp["T-Mobile"])
    p_Vodafone_Enschede_random10.append(samp["Vodafone"])

p_KPN_Enschede_random10_NR, p_T_Mobile_Enschede_random10_NR, p_Vodafone_Enschede_random10_NR  = [], [], []
for samp in p_per_mno_Enschede_random10_NR:
    p_KPN_Enschede_random10_NR.append(samp["KPN"])
    p_T_Mobile_Enschede_random10_NR.append(samp["T-Mobile"])
    p_Vodafone_Enschede_random10_NR.append(samp["Vodafone"])

p_KPN_Enschede_random10_NC, p_T_Mobile_Enschede_random10_NC, p_Vodafone_Enschede_random10_NC  = [], [], []
for samp in p_KPN_Enschede_random10_nc:
    p_KPN_Enschede_random10_NC.append(samp["KPN"])
for samp in p_T_Mobile_Enschede_random10_nc:
    p_T_Mobile_Enschede_random10_NC.append(samp["T-Mobile"])
for samp in p_Vodafone_Enschede_random10_nc:
    p_Vodafone_Enschede_random10_NC.append(samp["Vodafone"])


total_p_Enschede_random10 = np.add(np.add(p_KPN_Enschede_random10, p_T_Mobile_Enschede_random10), p_Vodafone_Enschede_random10)
total_p_Enschede_random10_NR = np.add(np.add(p_KPN_Enschede_random10_NR, p_T_Mobile_Enschede_random10_NR), p_Vodafone_Enschede_random10_NR)
total_p_Enschede_random10_NC = np.add(np.add(p_KPN_Enschede_random10_NC, p_T_Mobile_Enschede_random10_NC), p_Vodafone_Enschede_random10_NC)


# Middelburg with 10% random failure
p_KPN_Middelburg_random10, p_T_Mobile_Middelburg_random10, p_Vodafone_Middelburg_random10  = [], [], []
for samp in p_per_mno_Middelburg_random10:
    p_KPN_Middelburg_random10.append(samp["KPN"])
    p_T_Mobile_Middelburg_random10.append(samp["T-Mobile"])
    p_Vodafone_Middelburg_random10.append(samp["Vodafone"])

p_KPN_Middelburg_random10_NR, p_T_Mobile_Middelburg_random10_NR, p_Vodafone_Middelburg_random10_NR  = [], [], []
for samp in p_per_mno_Middelburg_random10_NR:
    p_KPN_Middelburg_random10_NR.append(samp["KPN"])
    p_T_Mobile_Middelburg_random10_NR.append(samp["T-Mobile"])
    p_Vodafone_Middelburg_random10_NR.append(samp["Vodafone"])

p_KPN_Middelburg_random10_NC, p_T_Mobile_Middelburg_random10_NC, p_Vodafone_Middelburg_random10_NC  = [], [], []
for samp in p_KPN_Middelburg_random10_nc:
    p_KPN_Middelburg_random10_NC.append(samp["KPN"])
for samp in p_T_Mobile_Middelburg_random10_nc:
    p_T_Mobile_Middelburg_random10_NC.append(samp["T-Mobile"])
for samp in p_Vodafone_Middelburg_random10_nc:
    p_Vodafone_Middelburg_random10_NC.append(samp["Vodafone"])

total_p_Middelburg_random10 = np.add(np.add(p_KPN_Middelburg_random10, p_T_Mobile_Middelburg_random10), p_Vodafone_Middelburg_random10)
total_p_Middelburg_random10_NR = np.add(np.add(p_KPN_Middelburg_random10_NR, p_T_Mobile_Middelburg_random10_NR), p_Vodafone_Middelburg_random10_NR)
total_p_Middelburg_random10_NC = np.add(np.add(p_KPN_Middelburg_random10_NC, p_T_Mobile_Middelburg_random10_NC), p_Vodafone_Middelburg_random10_NC)



MNOs = ['KPN', 'T-Mobile', 'Vodafone']
name_MNO = ['MNO-1', 'MNO-2', 'MNO-3', 'Total']

""" #x = np.array([1, 2, 3])
fig, ax = plt.subplots()
teste = np.mean(p_KPN_Amsterdam_random10) - np.mean(p_KPN_Amsterdam)
teste2 = np.mean(p_KPN_Amsterdam_random10)

fbplot = ax.boxplot([ np.subtract(p_KPN_Amsterdam_random10, p_KPN_Amsterdam), np.subtract(p_T_Mobile_Amsterdam_random10, p_T_Mobile_Amsterdam), np.subtract(p_Vodafone_Amsterdam_random10, p_Vodafone_Amsterdam), np.subtract(np.add(np.add(p_KPN_Amsterdam_random10, p_T_Mobile_Amsterdam_random10), p_Vodafone_Amsterdam_random10), np.add(np.add(p_KPN_Amsterdam, p_T_Mobile_Amsterdam), p_Vodafone_Amsterdam))], positions=x - 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)
nrplot = ax.boxplot([p_KPN_Amsterdam_random10_NR - p_KPN_Amsterdam_NR, p_T_Mobile_Amsterdam_random10_NR - p_T_Mobile_Amsterdam_NR, p_Vodafone_Amsterdam_random10_NR - p_Vodafone_Amsterdam_NR, np.add(np.add(p_KPN_Amsterdam_random10_NR, p_T_Mobile_Amsterdam_random10_NR), p_Vodafone_Amsterdam_random10_NR) - np.add(np.add(p_KPN_Amsterdam_NR, p_T_Mobile_Amsterdam_NR), p_Vodafone_Amsterdam_NR)], positions=x, widths=box_width, patch_artist=True, showfliers=False)
ncplot = ax.boxplot([p_KPN_Amsterdam_random10_NC - p_KPN_Amsterdam_NC, p_T_Mobile_Amsterdam_random10_NC - p_T_Mobile_Amsterdam_NC, p_Vodafone_Amsterdam_random10_NC - p_Vodafone_Amsterdam_NC, np.add(np.add(p_KPN_Amsterdam_random10_NC, p_T_Mobile_Amsterdam_random10_NC), p_Vodafone_Amsterdam_random10_NC) - np.add(np.add(p_KPN_Amsterdam_NC, p_T_Mobile_Amsterdam_NC), p_Vodafone_Amsterdam_NC)], positions=x + 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)

ax.axvspan((x[0]+x[1])/2, (x[1]+x[2])/2, color='#CCC', alpha=0.2, lw=0)
ax.axvspan((x[2]+x[3])/2, (x[3]+x[3]+2)/2, color='#CCC', alpha=0.2, lw=0)

for patch in fbplot['boxes']:
    patch.set_facecolor(util.get_boxplot_color(0))
for patch in nrplot['boxes']:
    patch.set_facecolor(util.get_boxplot_color(1))
for patch in ncplot['boxes']:
    patch.set_facecolor(util.get_boxplot_color(2))

ax.legend([fbplot["boxes"][0], nrplot["boxes"][0], ncplot["boxes"][0]], ['NR-fallback', 'NR-full', 'no cooperation'])
plt.xticks(x, name_MNO)
plt.ylabel('Total power consumption (W)')
plt.savefig('Figures/powerdiffperMNO_amsterdam_10percent_failure.pdf', dpi=1000)
plt.show() """



# fsp Amsterdam
fsp_KPN_Amsterdam_random10, fsp_T_Mobile_Amsterdam_random10, fsp_Vodafone_Amsterdam_random10  = [], [], []
for samp in fsp_per_mno_Amsterdam_random10:
    fsp_KPN_Amsterdam_random10.append(samp["KPN"])
    fsp_T_Mobile_Amsterdam_random10.append(samp["T-Mobile"])
    fsp_Vodafone_Amsterdam_random10.append(samp["Vodafone"])

fsp_KPN_Amsterdam_random10_NR, fsp_T_Mobile_Amsterdam_random10_NR, fsp_Vodafone_Amsterdam_random10_NR  = [], [], []
for samp in fsp_per_mno_Amsterdam_random10_NR:
    fsp_KPN_Amsterdam_random10_NR.append(samp["KPN"])
    fsp_T_Mobile_Amsterdam_random10_NR.append(samp["T-Mobile"])
    fsp_Vodafone_Amsterdam_random10_NR.append(samp["Vodafone"])

fsp_KPN_Amsterdam_random10_NC, fsp_T_Mobile_Amsterdam_random10_NC, fsp_Vodafone_Amsterdam_random10_NC  = [], [], []
for samp in fsp_KPN_Amsterdam_random10_nc:
    fsp_KPN_Amsterdam_random10_NC.append(samp["KPN"])
for samp in fsp_T_Mobile_Amsterdam_random10_nc:
    fsp_T_Mobile_Amsterdam_random10_NC.append(samp["T-Mobile"])
for samp in fsp_Vodafone_Amsterdam_random10_nc:
    fsp_Vodafone_Amsterdam_random10_NC.append(samp["Vodafone"])

# fsp Enschede
fsp_KPN_Enschede_random10, fsp_T_Mobile_Enschede_random10, fsp_Vodafone_Enschede_random10  = [], [], []
for samp in fsp_per_mno_Enschede_random10:
    fsp_KPN_Enschede_random10.append(samp["KPN"])
    fsp_T_Mobile_Enschede_random10.append(samp["T-Mobile"])
    fsp_Vodafone_Enschede_random10.append(samp["Vodafone"])

fsp_KPN_Enschede_random10_NR, fsp_T_Mobile_Enschede_random10_NR, fsp_Vodafone_Enschede_random10_NR  = [], [], []
for samp in fsp_per_mno_Enschede_random10_NR:
    fsp_KPN_Enschede_random10_NR.append(samp["KPN"])
    fsp_T_Mobile_Enschede_random10_NR.append(samp["T-Mobile"])
    fsp_Vodafone_Enschede_random10_NR.append(samp["Vodafone"])

fsp_KPN_Enschede_random10_NC, fsp_T_Mobile_Enschede_random10_NC, fsp_Vodafone_Enschede_random10_NC  = [], [], []
for samp in fsp_KPN_Enschede_random10_nc:
    fsp_KPN_Enschede_random10_NC.append(samp["KPN"])
for samp in fsp_T_Mobile_Enschede_random10_nc:
    fsp_T_Mobile_Enschede_random10_NC.append(samp["T-Mobile"])
for samp in fsp_Vodafone_Enschede_random10_nc:
    fsp_Vodafone_Enschede_random10_NC.append(samp["Vodafone"])

# fsp Middelburg
fsp_KPN_Middelburg_random10, fsp_T_Mobile_Middelburg_random10, fsp_Vodafone_Middelburg_random10  = [], [], []
for samp in fsp_per_mno_Middelburg_random10:
    fsp_KPN_Middelburg_random10.append(samp["KPN"])
    fsp_T_Mobile_Middelburg_random10.append(samp["T-Mobile"])
    fsp_Vodafone_Middelburg_random10.append(samp["Vodafone"])

fsp_KPN_Middelburg_random10_NR, fsp_T_Mobile_Middelburg_random10_NR, fsp_Vodafone_Middelburg_random10_NR  = [], [], []
for samp in fsp_per_mno_Middelburg_random10_NR:
    fsp_KPN_Middelburg_random10_NR.append(samp["KPN"])
    fsp_T_Mobile_Middelburg_random10_NR.append(samp["T-Mobile"])
    fsp_Vodafone_Middelburg_random10_NR.append(samp["Vodafone"])

fsp_KPN_Middelburg_random10_NC, fsp_T_Mobile_Middelburg_random10_NC, fsp_Vodafone_Middelburg_random10_NC  = [], [], []
for samp in fsp_KPN_Middelburg_random10_nc:
    fsp_KPN_Middelburg_random10_NC.append(samp["KPN"])
for samp in fsp_T_Mobile_Middelburg_random10_nc:
    fsp_T_Mobile_Middelburg_random10_NC.append(samp["T-Mobile"])
for samp in fsp_Vodafone_Middelburg_random10_nc:
    fsp_Vodafone_Middelburg_random10_NC.append(samp["Vodafone"])


fig, ax = plt.subplots()
fbplot = ax.boxplot([fsp_KPN_Amsterdam_random10, fsp_T_Mobile_Amsterdam_random10, fsp_Vodafone_Amsterdam_random10, total_fsp_Amsterdam_random10], positions=x - 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)
nrplot = ax.boxplot([fsp_KPN_Amsterdam_random10_NR, fsp_T_Mobile_Amsterdam_random10_NR, fsp_Vodafone_Amsterdam_random10_NR, total_fsp_Amsterdam_random10_NR], positions=x, widths=box_width, patch_artist=True, showfliers=False)
total_fsp_Amsterdam_random10_NC = np.add(np.add(fsp_KPN_Amsterdam_random10_NC, fsp_T_Mobile_Amsterdam_random10_NC), fsp_Vodafone_Amsterdam_random10_NC)/3 # only possible because all the scenarios uses the same number of users.
ncplot = ax.boxplot([fsp_KPN_Amsterdam_random10_NC, fsp_T_Mobile_Amsterdam_random10_NC, fsp_Vodafone_Amsterdam_random10_NC, total_fsp_Amsterdam_random10_NC], positions=x + 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)

ax.axvspan((x[0]+x[1])/2, (x[1]+x[2])/2, color='#CCC', alpha=0.2, lw=0)
ax.axvspan((x[2]+x[3])/2, (x[3]+x[3]+2)/2, color='#CCC', alpha=0.2, lw=0)

for patch in fbplot['boxes']:
    patch.set_facecolor(util.get_boxplot_color(0))
for patch in nrplot['boxes']:
    patch.set_facecolor(util.get_boxplot_color(1))
for patch in ncplot['boxes']:
    patch.set_facecolor(util.get_boxplot_color(2))

ax.legend([fbplot["boxes"][0], nrplot["boxes"][0], ncplot["boxes"][0]], ['NR-fallback', 'NR-full', 'no cooperation'])
plt.xticks(x, name_MNO)
plt.ylabel('FSP')
plt.savefig('Figures/FSPperMNO_amsterdam_10percent_failure.pdf', dpi=1000)
#plt.show()


# fdp Amsterdam
fdp_KPN_Amsterdam_random10, fdp_T_Mobile_Amsterdam_random10, fdp_Vodafone_Amsterdam_random10  = [], [], []
for samp in fdp_per_mno_Amsterdam_random10:
    fdp_KPN_Amsterdam_random10.append(samp["KPN"])
    fdp_T_Mobile_Amsterdam_random10.append(samp["T-Mobile"])
    fdp_Vodafone_Amsterdam_random10.append(samp["Vodafone"])

fdp_KPN_Amsterdam_random10_NR, fdp_T_Mobile_Amsterdam_random10_NR, fdp_Vodafone_Amsterdam_random10_NR  = [], [], []
for samp in fdp_per_mno_Amsterdam_random10_NR:
    fdp_KPN_Amsterdam_random10_NR.append(samp["KPN"])
    fdp_T_Mobile_Amsterdam_random10_NR.append(samp["T-Mobile"])
    fdp_Vodafone_Amsterdam_random10_NR.append(samp["Vodafone"])

fdp_KPN_Amsterdam_random10_NC, fdp_T_Mobile_Amsterdam_random10_NC, fdp_Vodafone_Amsterdam_random10_NC  = [], [], []
for samp in fdp_KPN_Amsterdam_random10_nc:
    fdp_KPN_Amsterdam_random10_NC.append(samp["KPN"])
for samp in fdp_T_Mobile_Amsterdam_random10_nc:
    fdp_T_Mobile_Amsterdam_random10_NC.append(samp["T-Mobile"])
for samp in fdp_Vodafone_Amsterdam_random10_nc:
    fdp_Vodafone_Amsterdam_random10_NC.append(samp["Vodafone"])

# fdp Enschede
fdp_KPN_Enschede_random10, fdp_T_Mobile_Enschede_random10, fdp_Vodafone_Enschede_random10  = [], [], []
for samp in fdp_per_mno_Enschede_random10:
    fdp_KPN_Enschede_random10.append(samp["KPN"])
    fdp_T_Mobile_Enschede_random10.append(samp["T-Mobile"])
    fdp_Vodafone_Enschede_random10.append(samp["Vodafone"])

fdp_KPN_Enschede_random10_NR, fdp_T_Mobile_Enschede_random10_NR, fdp_Vodafone_Enschede_random10_NR  = [], [], []
for samp in fdp_per_mno_Enschede_random10_NR:
    fdp_KPN_Enschede_random10_NR.append(samp["KPN"])
    fdp_T_Mobile_Enschede_random10_NR.append(samp["T-Mobile"])
    fdp_Vodafone_Enschede_random10_NR.append(samp["Vodafone"])

fdp_KPN_Enschede_random10_NC, fdp_T_Mobile_Enschede_random10_NC, fdp_Vodafone_Enschede_random10_NC  = [], [], []
for samp in fdp_KPN_Enschede_random10_nc:
    fdp_KPN_Enschede_random10_NC.append(samp["KPN"])
for samp in fdp_T_Mobile_Enschede_random10_nc:
    fdp_T_Mobile_Enschede_random10_NC.append(samp["T-Mobile"])
for samp in fdp_Vodafone_Enschede_random10_nc:
    fdp_Vodafone_Enschede_random10_NC.append(samp["Vodafone"])

# fdp Middelburg
fdp_KPN_Middelburg_random10, fdp_T_Mobile_Middelburg_random10, fdp_Vodafone_Middelburg_random10  = [], [], []
for samp in fdp_per_mno_Middelburg_random10:
    fdp_KPN_Middelburg_random10.append(samp["KPN"])
    fdp_T_Mobile_Middelburg_random10.append(samp["T-Mobile"])
    fdp_Vodafone_Middelburg_random10.append(samp["Vodafone"])

fdp_KPN_Middelburg_random10_NR, fdp_T_Mobile_Middelburg_random10_NR, fdp_Vodafone_Middelburg_random10_NR  = [], [], []
for samp in fdp_per_mno_Middelburg_random10_NR:
    fdp_KPN_Middelburg_random10_NR.append(samp["KPN"])
    fdp_T_Mobile_Middelburg_random10_NR.append(samp["T-Mobile"])
    fdp_Vodafone_Middelburg_random10_NR.append(samp["Vodafone"])

fdp_KPN_Middelburg_random10_NC, fdp_T_Mobile_Middelburg_random10_NC, fdp_Vodafone_Middelburg_random10_NC  = [], [], []
for samp in fdp_KPN_Middelburg_random10_nc:
    fdp_KPN_Middelburg_random10_NC.append(samp["KPN"])
for samp in fdp_T_Mobile_Middelburg_random10_nc:
    fdp_T_Mobile_Middelburg_random10_NC.append(samp["T-Mobile"])
for samp in fdp_Vodafone_Middelburg_random10_nc:
    fdp_Vodafone_Middelburg_random10_NC.append(samp["Vodafone"])


fig, ax = plt.subplots()
fbplot = ax.boxplot([fdp_KPN_Amsterdam_random10, fdp_T_Mobile_Amsterdam_random10, fdp_Vodafone_Amsterdam_random10, total_fdp_Amsterdam_random10], positions=x - 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)
nrplot = ax.boxplot([fdp_KPN_Amsterdam_random10_NR, fdp_T_Mobile_Amsterdam_random10_NR, fdp_Vodafone_Amsterdam_random10_NR, total_fdp_Amsterdam_random10_NR], positions=x, widths=box_width, patch_artist=True, showfliers=False)
total_fdp_Amsterdam_random10_NC = np.add(np.add(fdp_KPN_Amsterdam_random10_NC, fdp_T_Mobile_Amsterdam_random10_NC), fdp_Vodafone_Amsterdam_random10_NC)/3 # only possible because all the scenarios uses the same number of users.
ncplot = ax.boxplot([fdp_KPN_Amsterdam_random10_NC, fdp_T_Mobile_Amsterdam_random10_NC, fdp_Vodafone_Amsterdam_random10_NC, total_fdp_Amsterdam_random10_NC], positions=x + 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)

ax.axvspan((x[0]+x[1])/2, (x[1]+x[2])/2, color='#CCC', alpha=0.2, lw=0)
ax.axvspan((x[2]+x[3])/2, (x[3]+x[3]+2)/2, color='#CCC', alpha=0.2, lw=0)

for patch in fbplot['boxes']:
    patch.set_facecolor(util.get_boxplot_color(0))
for patch in nrplot['boxes']:
    patch.set_facecolor(util.get_boxplot_color(1))
for patch in ncplot['boxes']:
    patch.set_facecolor(util.get_boxplot_color(2))

ax.legend([fbplot["boxes"][0], nrplot["boxes"][0], ncplot["boxes"][0]], ['NR-fallback', 'NR-full', 'no cooperation'])
plt.xticks(x, name_MNO)
plt.ylabel('FDP')
plt.savefig('Figures/FDPperMNO_amsterdam_10percent_failure.pdf', dpi=1000)
#plt.show()




# ============ Plot diff after failure ===================

params = {'legend.fontsize': 'x-large',
          'axes.labelsize': 'x-large',
          'axes.titlesize': 'x-large',
          'xtick.labelsize': 'x-large',
          'ytick.labelsize': 'x-large',
          'lines.markersize': 8,
          'figure.autolayout': True}
pylab.rcParams.update(params)

markers = ['o', 'X', 'v', 's', '*', 'P', '1', '+']



total_fdp_Amsterdam_random10_NC = np.add(np.add(fdp_KPN_Amsterdam_random10_NC, fdp_T_Mobile_Amsterdam_random10_NC), fdp_Vodafone_Amsterdam_random10_NC)/3 # only possible because all the scenarios uses the same number of users.
total_fdp_Enschede_random10_NC = np.add(np.add(fdp_KPN_Enschede_random10_NC, fdp_T_Mobile_Enschede_random10_NC), fdp_Vodafone_Enschede_random10_NC)/3 # only possible because all the scenarios uses the same number of users.
total_fdp_Middelburg_random10_NC = np.add(np.add(fdp_KPN_Middelburg_random10_NC, fdp_T_Mobile_Middelburg_random10_NC), fdp_Vodafone_Middelburg_random10_NC)/3 # only possible because all the scenarios uses the same number of users.

total_fsp_Amsterdam_random10_NC = np.add(np.add(fsp_KPN_Amsterdam_random10_NC, fsp_T_Mobile_Amsterdam_random10_NC), fsp_Vodafone_Amsterdam_random10_NC)/3 # only possible because all the scenarios uses the same number of users.
total_fsp_Enschede_random10_NC = np.add(np.add(fsp_KPN_Enschede_random10_NC, fsp_T_Mobile_Enschede_random10_NC), fsp_Vodafone_Enschede_random10_NC)/3 # only possible because all the scenarios uses the same number of users.
total_fsp_Middelburg_random10_NC = np.add(np.add(fsp_KPN_Middelburg_random10_NC, fsp_T_Mobile_Middelburg_random10_NC), fsp_Vodafone_Middelburg_random10_NC)/3 # only possible because all the scenarios uses the same number of users.

# ['KPN', 'T-Mobile', 'Vodafone'] 
testeee = np.mean(p_KPN_Amsterdam_random10) - np.mean(p_KPN_Amsterdam)
NR_fallback_failure_fdp = {'Middelburg': [np.mean(fdp_KPN_Middelburg_random10) - np.mean(fdp_KPN_Middelburg), np.mean(fdp_T_Mobile_Middelburg_random10) - np.mean(fdp_T_Mobile_Middelburg), np.mean(fdp_Vodafone_Middelburg_random10) - np.mean(fdp_Vodafone_Middelburg), np.mean(total_fdp_Middelburg_random10) - np.mean(total_fdp_Middelburg)],
                           'Enschede': [np.mean(fdp_KPN_Enschede_random10) - np.mean(fdp_KPN_Enschede), np.mean(fdp_T_Mobile_Enschede_random10) - np.mean(fdp_T_Mobile_Enschede), np.mean(fdp_Vodafone_Enschede_random10) - np.mean(fdp_Vodafone_Enschede), np.mean(total_fdp_Enschede_random10) - np.mean(total_fdp_Enschede)],
                           'Amsterdam': [np.mean(fdp_KPN_Amsterdam_random10) - np.mean(fdp_KPN_Amsterdam), np.mean(fdp_T_Mobile_Amsterdam_random10) - np.mean(fdp_T_Mobile_Amsterdam), np.mean(fdp_Vodafone_Amsterdam_random10) - np.mean(fdp_Vodafone_Amsterdam), np.mean(total_fdp_Amsterdam_random10) - np.mean(total_fdp_Amsterdam)]}

NR_fallback_failure_fsp = {'Middelburg': [np.mean(fsp_KPN_Middelburg_random10) - np.mean(fsp_KPN_Middelburg), np.mean(fsp_T_Mobile_Middelburg_random10) - np.mean(fsp_T_Mobile_Middelburg), np.mean(fsp_Vodafone_Middelburg_random10) - np.mean(fsp_Vodafone_Middelburg), np.mean(total_fsp_Middelburg_random10) - np.mean(total_fsp_Middelburg)],
                           'Enschede': [np.mean(fsp_KPN_Enschede_random10) - np.mean(fsp_KPN_Enschede), np.mean(fsp_T_Mobile_Enschede_random10) - np.mean(fsp_T_Mobile_Enschede), np.mean(fsp_Vodafone_Enschede_random10) - np.mean(fsp_Vodafone_Enschede), np.mean(total_fsp_Enschede_random10) - np.mean(total_fsp_Enschede)],
                           'Amsterdam': [np.mean(fsp_KPN_Amsterdam_random10) - np.mean(fsp_KPN_Amsterdam), np.mean(fsp_T_Mobile_Amsterdam_random10) - np.mean(fsp_T_Mobile_Amsterdam), np.mean(fsp_Vodafone_Amsterdam_random10) - np.mean(fsp_Vodafone_Amsterdam), np.mean(total_fsp_Amsterdam_random10) - np.mean(total_fsp_Amsterdam)]}

NR_fallback_failure_p = {'Middelburg': [np.mean(p_KPN_Middelburg_random10) - np.mean(p_KPN_Middelburg), np.mean(p_T_Mobile_Middelburg_random10) - np.mean(p_T_Mobile_Middelburg), np.mean(p_Vodafone_Middelburg_random10) - np.mean(p_Vodafone_Middelburg), np.mean(total_p_Middelburg_random10) - np.mean(total_p_Middelburg)],
                           'Enschede': [np.mean(p_KPN_Enschede_random10) - np.mean(p_KPN_Enschede), np.mean(p_T_Mobile_Enschede_random10) - np.mean(p_T_Mobile_Enschede), np.mean(p_Vodafone_Enschede_random10) - np.mean(p_Vodafone_Enschede), np.mean(total_p_Enschede_random10) - np.mean(total_p_Enschede)],
                           'Amsterdam': [np.mean(p_KPN_Amsterdam_random10) - np.mean(p_KPN_Amsterdam), np.mean(p_T_Mobile_Amsterdam_random10) - np.mean(p_T_Mobile_Amsterdam), np.mean(p_Vodafone_Amsterdam_random10) - np.mean(p_Vodafone_Amsterdam), np.mean(total_p_Amsterdam_random10) - np.mean(total_p_Amsterdam)]}

#NR_fallback_failure_p_nor = {'Middelburg': [(np.mean(p_KPN_Middelburg_random10) - np.mean(p_KPN_Middelburg))/np.mean(p_KPN_Middelburg), (np.mean(p_T_Mobile_Middelburg_random10) - np.mean(p_T_Mobile_Middelburg))/np.mean(p_T_Mobile_Middelburg), (np.mean(p_Vodafone_Middelburg_random10) - np.mean(p_Vodafone_Middelburg))/np.mean(p_Vodafone_Middelburg), (np.mean(total_p_Middelburg_random10) - np.mean(total_p_Middelburg))/np.mean(total_p_Middelburg)],
#                           'Enschede': [(np.mean(p_KPN_Enschede_random10) - np.mean(p_KPN_Enschede))/np.mean(p_KPN_Enschede), (np.mean(p_T_Mobile_Enschede_random10) - np.mean(p_T_Mobile_Enschede))/np.mean(p_T_Mobile_Enschede), (np.mean(p_Vodafone_Enschede_random10) - np.mean(p_Vodafone_Enschede))/np.mean(p_Vodafone_Enschede), (np.mean(total_p_Enschede_random10) - np.mean(total_p_Enschede))/np.mean(total_p_Enschede)],
#                           'Amsterdam': [(np.mean(p_KPN_Amsterdam_random10) - np.mean(p_KPN_Amsterdam))/np.mean(p_KPN_Amsterdam), (np.mean(p_T_Mobile_Amsterdam_random10) - np.mean(p_T_Mobile_Amsterdam))/np.mean(p_T_Mobile_Amsterdam), (np.mean(p_Vodafone_Amsterdam_random10) - np.mean(p_Vodafone_Amsterdam))/np.mean(p_Vodafone_Amsterdam), (np.mean(total_p_Amsterdam_random10) - np.mean(total_p_Amsterdam))/np.mean(total_p_Amsterdam)]}

NR_fallback_failure_p_nor = {'Middelburg': [(np.mean(p_KPN_Middelburg_random10) - np.mean(p_KPN_Middelburg))/np.mean(p_KPN_Middelburg_NC), (np.mean(p_T_Mobile_Middelburg_random10) - np.mean(p_T_Mobile_Middelburg))/np.mean(p_T_Mobile_Middelburg_NC), (np.mean(p_Vodafone_Middelburg_random10) - np.mean(p_Vodafone_Middelburg))/np.mean(p_Vodafone_Middelburg_NC), (np.mean(total_p_Middelburg_random10) - np.mean(total_p_Middelburg))/np.mean(total_p_Middelburg_NC)],
                           'Enschede': [(np.mean(p_KPN_Enschede_random10) - np.mean(p_KPN_Enschede))/np.mean(p_KPN_Enschede_NC), (np.mean(p_T_Mobile_Enschede_random10) - np.mean(p_T_Mobile_Enschede))/np.mean(p_T_Mobile_Enschede_NC), (np.mean(p_Vodafone_Enschede_random10) - np.mean(p_Vodafone_Enschede))/np.mean(p_Vodafone_Enschede_NC), (np.mean(total_p_Enschede_random10) - np.mean(total_p_Enschede))/np.mean(total_p_Enschede_NC)],
                           'Amsterdam': [(np.mean(p_KPN_Amsterdam_random10) - np.mean(p_KPN_Amsterdam))/np.mean(p_KPN_Amsterdam_NC), (np.mean(p_T_Mobile_Amsterdam_random10) - np.mean(p_T_Mobile_Amsterdam))/np.mean(p_T_Mobile_Amsterdam_NC), (np.mean(p_Vodafone_Amsterdam_random10) - np.mean(p_Vodafone_Amsterdam))/np.mean(p_Vodafone_Amsterdam_NC), (np.mean(total_p_Amsterdam_random10) - np.mean(total_p_Amsterdam))/np.mean(total_p_Amsterdam_NC)]}

NR_full_failure_fdp = { 'Middelburg': [np.mean(fdp_KPN_Middelburg_random10_NR) - np.mean(fdp_KPN_Middelburg_NR), np.mean(fdp_T_Mobile_Middelburg_random10_NR) - np.mean(fdp_T_Mobile_Middelburg_NR), np.mean(fdp_Vodafone_Middelburg_random10_NR) - np.mean(fdp_Vodafone_Middelburg_NR), np.mean(total_fdp_Middelburg_random10_NR) - np.mean(total_fdp_Middelburg_NR)],
                        'Enschede': [np.mean(fdp_KPN_Enschede_random10_NR) - np.mean(fdp_KPN_Enschede_NR), np.mean(fdp_T_Mobile_Enschede_random10_NR) - np.mean(fdp_T_Mobile_Enschede_NR), np.mean(fdp_Vodafone_Enschede_random10_NR) - np.mean(fdp_Vodafone_Enschede_NR), np.mean(total_fdp_Enschede_random10_NR) - np.mean(total_fdp_Enschede_NR)],
                        'Amsterdam': [np.mean(fdp_KPN_Amsterdam_random10_NR) - np.mean(fdp_KPN_Amsterdam_NR), np.mean(fdp_T_Mobile_Amsterdam_random10_NR) - np.mean(fdp_T_Mobile_Amsterdam_NR), np.mean(fdp_Vodafone_Amsterdam_random10_NR) - np.mean(fdp_Vodafone_Amsterdam_NR), np.mean(total_fdp_Amsterdam_random10_NR) - np.mean(total_fdp_Amsterdam_NR)]}

NR_full_failure_fsp = { 'Middelburg': [np.mean(fsp_KPN_Middelburg_random10_NR) - np.mean(fsp_KPN_Middelburg_NR), np.mean(fsp_T_Mobile_Middelburg_random10_NR) - np.mean(fsp_T_Mobile_Middelburg_NR), np.mean(fsp_Vodafone_Middelburg_random10_NR) - np.mean(fsp_Vodafone_Middelburg_NR), np.mean(total_fsp_Middelburg_random10_NR) - np.mean(total_fsp_Middelburg_NR)],
                        'Enschede': [np.mean(fsp_KPN_Enschede_random10_NR) - np.mean(fsp_KPN_Enschede_NR), np.mean(fsp_T_Mobile_Enschede_random10_NR) - np.mean(fsp_T_Mobile_Enschede_NR), np.mean(fsp_Vodafone_Enschede_random10_NR) - np.mean(fsp_Vodafone_Enschede_NR), np.mean(total_fsp_Enschede_random10_NR) - np.mean(total_fsp_Enschede_NR)],
                        'Amsterdam': [np.mean(fsp_KPN_Amsterdam_random10_NR) - np.mean(fsp_KPN_Amsterdam_NR), np.mean(fsp_T_Mobile_Amsterdam_random10_NR) - np.mean(fsp_T_Mobile_Amsterdam_NR), np.mean(fsp_Vodafone_Amsterdam_random10_NR) - np.mean(fsp_Vodafone_Amsterdam_NR), np.mean(total_fsp_Amsterdam_random10_NR) - np.mean(total_fsp_Amsterdam_NR)]}

NR_full_failure_p = { 'Middelburg': [np.mean(p_KPN_Middelburg_random10_NR) - np.mean(p_KPN_Middelburg_NR), np.mean(p_T_Mobile_Middelburg_random10_NR) - np.mean(p_T_Mobile_Middelburg_NR), np.mean(p_Vodafone_Middelburg_random10_NR) - np.mean(p_Vodafone_Middelburg_NR), np.mean(total_p_Middelburg_random10_NR) - np.mean(total_p_Middelburg_NR)],
                        'Enschede': [np.mean(p_KPN_Enschede_random10_NR) - np.mean(p_KPN_Enschede_NR), np.mean(p_T_Mobile_Enschede_random10_NR) - np.mean(p_T_Mobile_Enschede_NR), np.mean(p_Vodafone_Enschede_random10_NR) - np.mean(p_Vodafone_Enschede_NR), np.mean(total_p_Enschede_random10_NR) - np.mean(total_p_Enschede_NR)],
                        'Amsterdam': [np.mean(p_KPN_Amsterdam_random10_NR) - np.mean(p_KPN_Amsterdam_NR), np.mean(p_T_Mobile_Amsterdam_random10_NR) - np.mean(p_T_Mobile_Amsterdam_NR), np.mean(p_Vodafone_Amsterdam_random10_NR) - np.mean(p_Vodafone_Amsterdam_NR), np.mean(total_p_Amsterdam_random10_NR) - np.mean(total_p_Amsterdam_NR)]}

#NR_full_failure_p_nor = { 'Middelburg': [(np.mean(p_KPN_Middelburg_random10_NR) - np.mean(p_KPN_Middelburg_NR))/np.mean(p_KPN_Middelburg_NR), (np.mean(p_T_Mobile_Middelburg_random10_NR) - np.mean(p_T_Mobile_Middelburg_NR))/np.mean(p_T_Mobile_Middelburg_NR), (np.mean(p_Vodafone_Middelburg_random10_NR) - np.mean(p_Vodafone_Middelburg_NR))/np.mean(p_Vodafone_Middelburg_NR), (np.mean(total_p_Middelburg_random10_NR) - np.mean(total_p_Middelburg_NR))/np.mean(total_p_Middelburg_NR)],
#                        'Enschede': [(np.mean(p_KPN_Enschede_random10_NR) - np.mean(p_KPN_Enschede_NR))/np.mean(p_KPN_Enschede_NR), (np.mean(p_T_Mobile_Enschede_random10_NR) - np.mean(p_T_Mobile_Enschede_NR))/np.mean(p_T_Mobile_Enschede_NR), (np.mean(p_Vodafone_Enschede_random10_NR) - np.mean(p_Vodafone_Enschede_NR))/np.mean(p_Vodafone_Enschede_NR), (np.mean(total_p_Enschede_random10_NR) - np.mean(total_p_Enschede_NR))/np.mean(total_p_Enschede_NR)],
#                        'Amsterdam': [(np.mean(p_KPN_Amsterdam_random10_NR) - np.mean(p_KPN_Amsterdam_NR))/np.mean(p_KPN_Amsterdam_NR), (np.mean(p_T_Mobile_Amsterdam_random10_NR) - np.mean(p_T_Mobile_Amsterdam_NR))/np.mean(p_T_Mobile_Amsterdam_NR), (np.mean(p_Vodafone_Amsterdam_random10_NR) - np.mean(p_Vodafone_Amsterdam_NR))/np.mean(p_Vodafone_Amsterdam_NR), (np.mean(total_p_Amsterdam_random10_NR) - np.mean(total_p_Amsterdam_NR))/np.mean(total_p_Amsterdam_NR)]}

NR_full_failure_p_nor = { 'Middelburg': [(np.mean(p_KPN_Middelburg_random10_NR) - np.mean(p_KPN_Middelburg_NR))/np.mean(p_KPN_Middelburg_NC), (np.mean(p_T_Mobile_Middelburg_random10_NR) - np.mean(p_T_Mobile_Middelburg_NR))/np.mean(p_T_Mobile_Middelburg_NC), (np.mean(p_Vodafone_Middelburg_random10_NR) - np.mean(p_Vodafone_Middelburg_NR))/np.mean(p_Vodafone_Middelburg_NC), (np.mean(total_p_Middelburg_random10_NR) - np.mean(total_p_Middelburg_NR))/np.mean(total_p_Middelburg_NC)],
                        'Enschede': [(np.mean(p_KPN_Enschede_random10_NR) - np.mean(p_KPN_Enschede_NR))/np.mean(p_KPN_Enschede_NC), (np.mean(p_T_Mobile_Enschede_random10_NR) - np.mean(p_T_Mobile_Enschede_NR))/np.mean(p_T_Mobile_Enschede_NC), (np.mean(p_Vodafone_Enschede_random10_NR) - np.mean(p_Vodafone_Enschede_NR))/np.mean(p_Vodafone_Enschede_NC), (np.mean(total_p_Enschede_random10_NR) - np.mean(total_p_Enschede_NR))/np.mean(total_p_Enschede_NC)],
                        'Amsterdam': [(np.mean(p_KPN_Amsterdam_random10_NR) - np.mean(p_KPN_Amsterdam_NR))/np.mean(p_KPN_Amsterdam_NC), (np.mean(p_T_Mobile_Amsterdam_random10_NR) - np.mean(p_T_Mobile_Amsterdam_NR))/np.mean(p_T_Mobile_Amsterdam_NC), (np.mean(p_Vodafone_Amsterdam_random10_NR) - np.mean(p_Vodafone_Amsterdam_NR))/np.mean(p_Vodafone_Amsterdam_NC), (np.mean(total_p_Amsterdam_random10_NR) - np.mean(total_p_Amsterdam_NR))/np.mean(total_p_Amsterdam_NC)]}

no_cooperation_failure_fdp = { 'Middelburg': [np.mean(fdp_KPN_Middelburg_random10_NC) - np.mean(fdp_KPN_Middelburg_NC), np.mean(fdp_T_Mobile_Middelburg_random10_NC) - np.mean(fdp_T_Mobile_Middelburg_NC), np.mean(fdp_Vodafone_Middelburg_random10_NC) - np.mean(fdp_Vodafone_Middelburg_NC), np.mean(total_fdp_Middelburg_random10_NC) - np.mean(total_fdp_Middelburg_NC)],
                        'Enschede': [np.mean(fdp_KPN_Enschede_random10_NC) - np.mean(fdp_KPN_Enschede_NC), np.mean(fdp_T_Mobile_Enschede_random10_NC) - np.mean(fdp_T_Mobile_Enschede_NC), np.mean(fdp_Vodafone_Enschede_random10_NC) - np.mean(fdp_Vodafone_Enschede_NC), np.mean(total_fdp_Enschede_random10_NC) - np.mean(total_fdp_Enschede_NC)],
                        'Amsterdam': [np.mean(fdp_KPN_Amsterdam_random10_NC) - np.mean(fdp_KPN_Amsterdam_NC), np.mean(fdp_T_Mobile_Amsterdam_random10_NC) - np.mean(fdp_T_Mobile_Amsterdam_NC), np.mean(fdp_Vodafone_Amsterdam_random10_NC) - np.mean(fdp_Vodafone_Amsterdam_NC), np.mean(total_fdp_Amsterdam_random10_NC) - np.mean(total_fdp_Amsterdam_NC)]}

no_cooperation_failure_fsp = { 'Middelburg': [np.mean(fsp_KPN_Middelburg_random10_NC) - np.mean(fsp_KPN_Middelburg_NC), np.mean(fsp_T_Mobile_Middelburg_random10_NC) - np.mean(fsp_T_Mobile_Middelburg_NC), np.mean(fsp_Vodafone_Middelburg_random10_NC) - np.mean(fsp_Vodafone_Middelburg_NC), np.mean(total_fsp_Middelburg_random10_NC) - np.mean(total_fsp_Middelburg_NC)],
                        'Enschede': [np.mean(fsp_KPN_Enschede_random10_NC) - np.mean(fsp_KPN_Enschede_NC), np.mean(fsp_T_Mobile_Enschede_random10_NC) - np.mean(fsp_T_Mobile_Enschede_NC), np.mean(fsp_Vodafone_Enschede_random10_NC) - np.mean(fsp_Vodafone_Enschede_NC), np.mean(total_fsp_Enschede_random10_NC) - np.mean(total_fsp_Enschede_NC)],
                        'Amsterdam': [np.mean(fsp_KPN_Amsterdam_random10_NC) - np.mean(fsp_KPN_Amsterdam_NC), np.mean(fsp_T_Mobile_Amsterdam_random10_NC) - np.mean(fsp_T_Mobile_Amsterdam_NC), np.mean(fsp_Vodafone_Amsterdam_random10_NC) - np.mean(fsp_Vodafone_Amsterdam_NC), np.mean(total_fsp_Amsterdam_random10_NC) - np.mean(total_fsp_Amsterdam_NC)]}

#no_cooperation_failure_p = { 'Middelburg': [np.mean(p_KPN_Middelburg_random10_NC) - np.mean(p_KPN_Middelburg_NC), np.mean(p_T_Mobile_Middelburg_random10_NC) - np.mean(p_T_Mobile_Middelburg_NC), np.mean(p_Vodafone_Middelburg_random10_NC) - np.mean(p_Vodafone_Middelburg_NC), np.mean(total_p_Middelburg_random10_NC) - np.mean(total_p_Middelburg_NC)],
#                        'Enschede': [np.mean(p_KPN_Enschede_random10_NC) - np.mean(p_KPN_Enschede_NC), np.mean(p_T_Mobile_Enschede_random10_NC) - np.mean(p_T_Mobile_Enschede_NC), np.mean(p_Vodafone_Enschede_random10_NC) - np.mean(p_Vodafone_Enschede_NC), np.mean(total_p_Enschede_random10_NC) - np.mean(total_p_Enschede_NC)],
#                        'Amsterdam': [np.mean(p_KPN_Amsterdam_random10_NC) - np.mean(p_KPN_Amsterdam_NC), np.mean(p_T_Mobile_Amsterdam_random10_NC) - np.mean(p_T_Mobile_Amsterdam_NC), np.mean(p_Vodafone_Amsterdam_random10_NC) - np.mean(p_Vodafone_Amsterdam_NC), np.mean(total_p_Amsterdam_random10_NC) - np.mean(total_p_Amsterdam_NC)]}

no_cooperation_failure_p_nor = { 'Middelburg': [(np.mean(p_KPN_Middelburg_random10_NC) - np.mean(p_KPN_Middelburg_NC))/np.mean(p_KPN_Middelburg_NC), (np.mean(p_T_Mobile_Middelburg_random10_NC) - np.mean(p_T_Mobile_Middelburg_NC))/np.mean(p_T_Mobile_Middelburg_NC), (np.mean(p_Vodafone_Middelburg_random10_NC) - np.mean(p_Vodafone_Middelburg_NC))/np.mean(p_Vodafone_Middelburg_NC), (np.mean(total_p_Middelburg_random10_NC) - np.mean(total_p_Middelburg_NC))/np.mean(total_p_Middelburg_NC)],
                        'Enschede': [(np.mean(p_KPN_Enschede_random10_NC) - np.mean(p_KPN_Enschede_NC))/np.mean(p_KPN_Enschede_NC), (np.mean(p_T_Mobile_Enschede_random10_NC) - np.mean(p_T_Mobile_Enschede_NC))/np.mean(p_T_Mobile_Enschede_NC), (np.mean(p_Vodafone_Enschede_random10_NC) - np.mean(p_Vodafone_Enschede_NC))/np.mean(p_Vodafone_Enschede_NC), (np.mean(total_p_Enschede_random10_NC) - np.mean(total_p_Enschede_NC))/np.mean(total_p_Enschede_NC)],
                        'Amsterdam': [(np.mean(p_KPN_Amsterdam_random10_NC) - np.mean(p_KPN_Amsterdam_NC))/np.mean(p_KPN_Amsterdam_NC), (np.mean(p_T_Mobile_Amsterdam_random10_NC) - np.mean(p_T_Mobile_Amsterdam_NC))/np.mean(p_T_Mobile_Amsterdam_NC), (np.mean(p_Vodafone_Amsterdam_random10_NC) - np.mean(p_Vodafone_Amsterdam_NC))/np.mean(p_Vodafone_Amsterdam_NC), (np.mean(total_p_Amsterdam_random10_NC) - np.mean(total_p_Amsterdam_NC))/np.mean(total_p_Amsterdam_NC)]}




# cities = ['Overijssel', 'Friesland', 'Utrecht']
cities = ['Middelburg', 'Enschede', 'Amsterdam']
MNOs = ['KPN', 'T-Mobile', 'Vodafone', 'Total']

#positions = [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20]

#delta = 0.1

#pos = {'KPN': [1, 8, 15], 'T-Mobile': [3, 10, 17], 'Vodafone': [5, 12, 19]}
#pos_NR = {'KPN': [2 - delta, 9 - delta, 16 - delta], 'T-Mobile': [4 - delta, 11 - delta, 18 - delta],
#          'Vodafone': [6 - delta, 13 - delta, 20 - delta]}

xticks = [3.5, 10.5, 17.5]

patterns = ["///", "O", "|", "-", "+", "x", "o", "O", ".", "*"]

FDPFSP = 'power' #''FSP' or 'FDP' or 'power'
#labels = ['no cooperation', 'NR-full', 'NR-fallback', 'NR-fallback-QOS']
labels = [ 'NR-fallback', 'NR-full', 'no cooperation']#, 'NR-fallback-QOS']

fig, ax = plt.subplots()
if FDPFSP == 'FDP': 
    data_list = [NR_fallback_failure_fdp, NR_full_failure_fdp, no_cooperation_failure_fdp]
    min_x = -0.01
    max_x = 0.01
    ax.axvspan(0,max_x, color='red', alpha=0.1, lw=0)
elif FDPFSP == 'FSP':
    data_list = [NR_fallback_failure_fsp, NR_full_failure_fsp, no_cooperation_failure_fsp]
    min_x = -0.1
    max_x = 0.1
    ax.axvspan(min_x, 0, color='red', alpha=0.1, lw=0)
elif FDPFSP == 'power':
    #data_list = [NR_fallback_failure_p, NR_full_failure_p, no_cooperation_failure_p]
    data_list = [NR_fallback_failure_p_nor, NR_full_failure_p_nor, no_cooperation_failure_p_nor]

    """ min_x = float('inf')
    max_x = -float('inf')
    for aux in data_list:
        for data in aux.values():
            min_x_aux = np.min(data)
            if min_x_aux < min_x:
                min_x = min_x_aux
            max_x_aux = np.max(data)
            if max_x_aux > max_x:
                max_x = max_x_aux
    diff = max_x - min_x
    min_x = min_x - 0.1*diff
    max_x = max_x + 0.1*diff """
    min_x = -0.35
    max_x = 0.35
    ax.axvspan(0,max_x, color='red', alpha=0.1, lw=0)


for x in range(len(cities)):
    plt.plot([min_x, max_x], [x - 0.2, x - 0.2], ':', color='gray', alpha=0.5, zorder=1)
    plt.plot([min_x, max_x], [x, x], ':', color='gray', alpha=0.5, zorder=1)
    plt.plot([min_x, max_x], [x + 0.2, x + 0.2], ':', color='gray', alpha=0.5, zorder=1)
    plt.plot([min_x, max_x], [x - 0.4, x - 0.4], ':', color='gray', alpha=0.5, zorder=1)

#if min_x <0:
#    ax.axvspan(min_x, 0, color='red', alpha=0.1, lw=0)

y_axes = {'KPN': [i + 0.2 for i in range(len(cities))], 'T-Mobile': [i for i in range(len(cities))],
          'Vodafone': [i - 0.2 for i in range(len(cities))], 'Total':[i - 0.4 for i in range(len(cities))]}


for i, data in zip(range(len(data_list)), data_list):
    for j in range(len(MNOs)):
        vals = [v[j] for k, v in data.items() if k in cities]
        if j == 0:
            plt.scatter(vals, y_axes[MNOs[j]], color=util.get_color(i), alpha=0.5, marker=markers[i], label=labels[i])
        else:
            plt.scatter(vals, y_axes[MNOs[j]], color=util.get_color(i), alpha=0.5, marker=markers[i])

if (FDPFSP=="power"):
    plt.xlabel("Power difference (W)")
else:
    plt.xlabel(FDPFSP)
plt.yticks(np.subtract(range(len(cities)),0.1), cities)

ax2 = ax.twinx()
ax2.set_yticks(sorted(y_axes['KPN'] + y_axes['T-Mobile'] + y_axes['Vodafone'] + y_axes['Total']), ['Total', 'MNO$_3$', 'MNO$_2$', 'MNO$_1$'] * len(cities))


ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=len(labels), fancybox=True)

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



#ax.set_ylim([0 - 0.3, 2 + 0.3])
#ax2.set_ylim([0 - 0.3, 2 + 0.3])
ax.set_ylim([0 - 0.6, 2 + 0.6])
ax2.set_ylim([0 - 0.6, 2 + 0.6])


plt.savefig(f'Figures/{FDPFSP}diff_with_fallback_failure_cities.pdf', dpi=1000, transparent=True)

plt.show()




""" # Amsterdam with 10% random failure
p_KPN_Amsterdam_random10, p_T_Mobile_Amsterdam_random10, p_Vodafone_Amsterdam_random10  = [], [], []
for samp in p_per_mno_Amsterdam_random10:
    p_KPN_Amsterdam_random10.append(samp["KPN"])
    p_T_Mobile_Amsterdam_random10.append(samp["T-Mobile"])
    p_Vodafone_Amsterdam_random10.append(samp["Vodafone"])


p_KPN_Amsterdam_random10_NR, p_T_Mobile_Amsterdam_random10_NR, p_Vodafone_Amsterdam_random10_NR  = [], [], []
for samp in p_per_mno_Amsterdam_random10_NR:
    p_KPN_Amsterdam_random10_NR.append(samp["KPN"])
    p_T_Mobile_Amsterdam_random10_NR.append(samp["T-Mobile"])
    p_Vodafone_Amsterdam_random10_NR.append(samp["Vodafone"])

p_KPN_Amsterdam_random10_NC, p_T_Mobile_Amsterdam_random10_NC, p_Vodafone_Amsterdam_random10_NC  = [], [], []
for samp in p_KPN_Amsterdam_random10_nc:
    p_KPN_Amsterdam_random10_NC.append(samp["KPN"])
for samp in p_T_Mobile_Amsterdam_random10_nc:
    p_T_Mobile_Amsterdam_random10_NC.append(samp["T-Mobile"])
for samp in p_Vodafone_Amsterdam_random10_nc:
    p_Vodafone_Amsterdam_random10_NC.append(samp["Vodafone"])

MNOs = ['KPN', 'T-Mobile', 'Vodafone']
name_MNO = ['MNO-1', 'MNO-2', 'MNO-3', 'Total']

#x = np.array([1, 2, 3])
fig, ax = plt.subplots()
total_p_Amsterdam_random10 = np.add(np.add(p_KPN_Amsterdam_random10, p_T_Mobile_Amsterdam_random10), p_Vodafone_Amsterdam_random10)
fbplot = ax.boxplot([p_KPN_Amsterdam_random10, p_T_Mobile_Amsterdam_random10, p_Vodafone_Amsterdam_random10, total_p_Amsterdam_random10], positions=x - 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)
total_p_Amsterdam_random10_NR = np.add(np.add(p_KPN_Amsterdam_random10_NR, p_T_Mobile_Amsterdam_random10_NR), p_Vodafone_Amsterdam_random10_NR)
nrplot = ax.boxplot([p_KPN_Amsterdam_random10_NR, p_T_Mobile_Amsterdam_random10_NR, p_Vodafone_Amsterdam_random10_NR, total_p_Amsterdam_random10_NR], positions=x, widths=box_width, patch_artist=True, showfliers=False)
total_p_Amsterdam_random10_NC = np.add(np.add(p_KPN_Amsterdam_random10_NC, p_T_Mobile_Amsterdam_random10_NC), p_Vodafone_Amsterdam_random10_NC)
ncplot = ax.boxplot([p_KPN_Amsterdam_random10_NC, p_T_Mobile_Amsterdam_random10_NC, p_Vodafone_Amsterdam_random10_NC, total_p_Amsterdam_random10_NC], positions=x + 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)

ax.axvspan((x[0]+x[1])/2, (x[1]+x[2])/2, color='#CCC', alpha=0.2, lw=0)
ax.axvspan((x[2]+x[3])/2, (x[3]+x[3]+2)/2, color='#CCC', alpha=0.2, lw=0)

for patch in fbplot['boxes']:
    patch.set_facecolor(util.get_boxplot_color(0))
for patch in nrplot['boxes']:
    patch.set_facecolor(util.get_boxplot_color(1))
for patch in ncplot['boxes']:
    patch.set_facecolor(util.get_boxplot_color(2))

ax.legend([fbplot["boxes"][0], nrplot["boxes"][0], ncplot["boxes"][0]], ['NR-fallback', 'NR-full', 'no cooperation'])
plt.xticks(x, name_MNO)
plt.ylabel('Total power consumption (W)')
plt.savefig('Figures/powerperMNO_amsterdam_10percent_failure.pdf', dpi=1000)
#plt.show()



# fsp Amsterdam
fsp_KPN_Amsterdam_random10, fsp_T_Mobile_Amsterdam_random10, fsp_Vodafone_Amsterdam_random10  = [], [], []
for samp in fsp_per_mno_Amsterdam_random10:
    fsp_KPN_Amsterdam_random10.append(samp["KPN"])
    fsp_T_Mobile_Amsterdam_random10.append(samp["T-Mobile"])
    fsp_Vodafone_Amsterdam_random10.append(samp["Vodafone"])

fsp_KPN_Amsterdam_random10_NR, fsp_T_Mobile_Amsterdam_random10_NR, fsp_Vodafone_Amsterdam_random10_NR  = [], [], []
for samp in fsp_per_mno_Amsterdam_random10_NR:
    fsp_KPN_Amsterdam_random10_NR.append(samp["KPN"])
    fsp_T_Mobile_Amsterdam_random10_NR.append(samp["T-Mobile"])
    fsp_Vodafone_Amsterdam_random10_NR.append(samp["Vodafone"])

fsp_KPN_Amsterdam_random10_NC, fsp_T_Mobile_Amsterdam_random10_NC, fsp_Vodafone_Amsterdam_random10_NC  = [], [], []
for samp in fsp_KPN_Amsterdam_random10_nc:
    fsp_KPN_Amsterdam_random10_NC.append(samp["KPN"])
for samp in fsp_T_Mobile_Amsterdam_random10_nc:
    fsp_T_Mobile_Amsterdam_random10_NC.append(samp["T-Mobile"])
for samp in fsp_Vodafone_Amsterdam_random10_nc:
    fsp_Vodafone_Amsterdam_random10_NC.append(samp["Vodafone"])


fig, ax = plt.subplots()
fbplot = ax.boxplot([fsp_KPN_Amsterdam_random10, fsp_T_Mobile_Amsterdam_random10, fsp_Vodafone_Amsterdam_random10, total_fsp_Amsterdam_random10], positions=x - 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)
nrplot = ax.boxplot([fsp_KPN_Amsterdam_random10_NR, fsp_T_Mobile_Amsterdam_random10_NR, fsp_Vodafone_Amsterdam_random10_NR, total_fsp_Amsterdam_random10_NR], positions=x, widths=box_width, patch_artist=True, showfliers=False)
total_fsp_Amsterdam_random10_NC = np.add(np.add(fsp_KPN_Amsterdam_random10_NC, fsp_T_Mobile_Amsterdam_random10_NC), fsp_Vodafone_Amsterdam_random10_NC)/3 # only possible because all the scenarios uses the same number of users.
ncplot = ax.boxplot([fsp_KPN_Amsterdam_random10_NC, fsp_T_Mobile_Amsterdam_random10_NC, fsp_Vodafone_Amsterdam_random10_NC, total_fsp_Amsterdam_random10_NC], positions=x + 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)

ax.axvspan((x[0]+x[1])/2, (x[1]+x[2])/2, color='#CCC', alpha=0.2, lw=0)
ax.axvspan((x[2]+x[3])/2, (x[3]+x[3]+2)/2, color='#CCC', alpha=0.2, lw=0)

for patch in fbplot['boxes']:
    patch.set_facecolor(util.get_boxplot_color(0))
for patch in nrplot['boxes']:
    patch.set_facecolor(util.get_boxplot_color(1))
for patch in ncplot['boxes']:
    patch.set_facecolor(util.get_boxplot_color(2))

ax.legend([fbplot["boxes"][0], nrplot["boxes"][0], ncplot["boxes"][0]], ['NR-fallback', 'NR-full', 'no cooperation'])
plt.xticks(x, name_MNO)
plt.ylabel('FSP')
plt.savefig('Figures/FSPperMNO_amsterdam_10percent_failure.pdf', dpi=1000)
#plt.show()


# fdp Amsterdam
fdp_KPN_Amsterdam_random10, fdp_T_Mobile_Amsterdam_random10, fdp_Vodafone_Amsterdam_random10  = [], [], []
for samp in fdp_per_mno_Amsterdam_random10:
    fdp_KPN_Amsterdam_random10.append(samp["KPN"])
    fdp_T_Mobile_Amsterdam_random10.append(samp["T-Mobile"])
    fdp_Vodafone_Amsterdam_random10.append(samp["Vodafone"])

fdp_KPN_Amsterdam_random10_NR, fdp_T_Mobile_Amsterdam_random10_NR, fdp_Vodafone_Amsterdam_random10_NR  = [], [], []
for samp in fdp_per_mno_Amsterdam_random10_NR:
    fdp_KPN_Amsterdam_random10_NR.append(samp["KPN"])
    fdp_T_Mobile_Amsterdam_random10_NR.append(samp["T-Mobile"])
    fdp_Vodafone_Amsterdam_random10_NR.append(samp["Vodafone"])

fdp_KPN_Amsterdam_random10_NC, fdp_T_Mobile_Amsterdam_random10_NC, fdp_Vodafone_Amsterdam_random10_NC  = [], [], []
for samp in fdp_KPN_Amsterdam_random10_nc:
    fdp_KPN_Amsterdam_random10_NC.append(samp["KPN"])
for samp in fdp_T_Mobile_Amsterdam_random10_nc:
    fdp_T_Mobile_Amsterdam_random10_NC.append(samp["T-Mobile"])
for samp in fdp_Vodafone_Amsterdam_random10_nc:
    fdp_Vodafone_Amsterdam_random10_NC.append(samp["Vodafone"])


fig, ax = plt.subplots()
fbplot = ax.boxplot([fdp_KPN_Amsterdam_random10, fdp_T_Mobile_Amsterdam_random10, fdp_Vodafone_Amsterdam_random10, total_fdp_Amsterdam_random10], positions=x - 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)
nrplot = ax.boxplot([fdp_KPN_Amsterdam_random10_NR, fdp_T_Mobile_Amsterdam_random10_NR, fdp_Vodafone_Amsterdam_random10_NR, total_fdp_Amsterdam_random10_NR], positions=x, widths=box_width, patch_artist=True, showfliers=False)
total_fdp_Amsterdam_random10_NC = np.add(np.add(fdp_KPN_Amsterdam_random10_NC, fdp_T_Mobile_Amsterdam_random10_NC), fdp_Vodafone_Amsterdam_random10_NC)/3 # only possible because all the scenarios uses the same number of users.
ncplot = ax.boxplot([fdp_KPN_Amsterdam_random10_NC, fdp_T_Mobile_Amsterdam_random10_NC, fdp_Vodafone_Amsterdam_random10_NC, total_fdp_Amsterdam_random10_NC], positions=x + 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)

ax.axvspan((x[0]+x[1])/2, (x[1]+x[2])/2, color='#CCC', alpha=0.2, lw=0)
ax.axvspan((x[2]+x[3])/2, (x[3]+x[3]+2)/2, color='#CCC', alpha=0.2, lw=0)

for patch in fbplot['boxes']:
    patch.set_facecolor(util.get_boxplot_color(0))
for patch in nrplot['boxes']:
    patch.set_facecolor(util.get_boxplot_color(1))
for patch in ncplot['boxes']:
    patch.set_facecolor(util.get_boxplot_color(2))

ax.legend([fbplot["boxes"][0], nrplot["boxes"][0], ncplot["boxes"][0]], ['NR-fallback', 'NR-full', 'no cooperation'])
plt.xticks(x, name_MNO)
plt.ylabel('FDP')
plt.savefig('Figures/FDPperMNO_amsterdam_10percent_failure.pdf', dpi=1000)
plt.show()
 """