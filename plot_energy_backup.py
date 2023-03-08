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

# fsp_Middelburg = util.from_data(f'data/Realisations/Middelburgall_MNOs0.021backup{max_iterations}_totalfsp.p')
# fdp_Middelburg = util.from_data(f'data/Realisations/Middelburgall_MNOs0.021backup{max_iterations}_totalfdp.p')

# National Roaming
p_per_mno_fp_Middelburg_NR = util.from_data(f'data/Realisations/Middelburgall_MNOs0.021{max_iterations}_totalpower_per_mno_fp.p')
p_per_mno_Middelburg_NR = util.from_data(f'data/Realisations/Middelburgall_MNOs0.021{max_iterations}_totalpower_per_mno.p')
p_per_mno_fp_Enschede_NR = util.from_data(f'data/Realisations/Enschedeall_MNOs0.021{max_iterations}_totalpower_per_mno_fp.p')
p_per_mno_Enschede_NR = util.from_data(f'data/Realisations/Enschedeall_MNOs0.021{max_iterations}_totalpower_per_mno.p')

fdp_per_mno_Middelburg_NR = util.from_data(f'data/Realisations/Middelburgall_MNOs0.021{max_iterations}_fdp_per_MNO.p')
fdp_per_mno_Enschede_NR = util.from_data(f'data/Realisations/Enschedeall_MNOs0.021{max_iterations}_fdp_per_MNO.p')
fsp_per_mno_Middelburg_NR = util.from_data(f'data/Realisations/Middelburgall_MNOs0.021{max_iterations}_fsp_per_MNO.p')
fsp_per_mno_Enschede_NR = util.from_data(f'data/Realisations/Enschedeall_MNOs0.021{max_iterations}_fsp_per_MNO.p')

# fsp_Enschede_NR = util.from_data(f'data/Realisations/Enschedeall_MNOs0.021{max_iterations}_totalfsp.p')
# fdp_Enschede_NR = util.from_data(f'data/Realisations/Enschedeall_MNOs0.021{max_iterations}_totalfdp.p')

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
name_MNO = ['MNO-1', 'MNO-2', 'MNO-3']#, 'Total']

#x = np.array([1, 2, 3])
x = np.array([2, 4, 6])
fig, ax = plt.subplots()
#fbplot = ax.boxplot(dataFDP, positions=x - 0.17, widths=0.3, patch_artist=True, showfliers=False)
#nrplot = ax.boxplot(dataFSP, positions=x + 0.17, widths=0.3, patch_artist=True, showfliers=False)
box_width = 0.25
fbplot = ax.boxplot([p_KPN_Middelburg, p_T_Mobile_Middelburg, p_Vodafone_Middelburg], positions=x - 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)
nrplot = ax.boxplot([p_KPN_Middelburg_NR, p_T_Mobile_Middelburg_NR, p_Vodafone_Middelburg_NR], positions=x, widths=box_width, patch_artist=True, showfliers=False)
ncplot = ax.boxplot([p_KPN_Middelburg_NC, p_T_Mobile_Middelburg_NC, p_Vodafone_Middelburg_NC], positions=x + 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)

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


# fdp and fsp Middelburg
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
fbplot = ax.boxplot([fsp_KPN_Middelburg, fsp_T_Mobile_Middelburg, fsp_Vodafone_Middelburg], positions=x - 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)
nrplot = ax.boxplot([fsp_KPN_Middelburg_NR, fsp_T_Mobile_Middelburg_NR, fsp_Vodafone_Middelburg_NR], positions=x, widths=box_width, patch_artist=True, showfliers=False)
ncplot = ax.boxplot([fsp_KPN_Middelburg_NC, fsp_T_Mobile_Middelburg_NC, fsp_Vodafone_Middelburg_NC], positions=x + 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)

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
name_MNO = ['MNO-1', 'MNO-2', 'MNO-3']#, 'Total']

#x = np.array([1, 2, 3])
fig, ax = plt.subplots()
#fbplot = ax.boxplot(dataFDP, positions=x - 0.17, widths=0.3, patch_artist=True, showfliers=False)
#nrplot = ax.boxplot(dataFSP, positions=x + 0.17, widths=0.3, patch_artist=True, showfliers=False)
fbplot = ax.boxplot([p_KPN_Enschede, p_T_Mobile_Enschede, p_Vodafone_Enschede], positions=x - 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)
nrplot = ax.boxplot([p_KPN_Enschede_NR, p_T_Mobile_Enschede_NR, p_Vodafone_Enschede_NR], positions=x, widths=box_width, patch_artist=True, showfliers=False)
ncplot = ax.boxplot([p_KPN_Enschede_NC, p_T_Mobile_Enschede_NC, p_Vodafone_Enschede_NC], positions=x + 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)

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
plt.savefig('Figures/powerperMNO_enschede.pdf', dpi=1000)
#plt.show()


# fsp and fdp Enschede
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

MNOs = ['KPN', 'T-Mobile', 'Vodafone']
name_MNO = ['MNO-1', 'MNO-2', 'MNO-3']#, 'Total']

#x = np.array([1, 2, 3])
fig, ax = plt.subplots()
#fbplot = ax.boxplot(dataFDP, positions=x - 0.17, widths=0.3, patch_artist=True, showfliers=False)
#nrplot = ax.boxplot(dataFSP, positions=x + 0.17, widths=0.3, patch_artist=True, showfliers=False)
fbplot = ax.boxplot([fsp_KPN_Enschede, fsp_T_Mobile_Enschede, fsp_Vodafone_Enschede], positions=x - 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)
nrplot = ax.boxplot([fsp_KPN_Enschede_NR, fsp_T_Mobile_Enschede_NR, fsp_Vodafone_Enschede_NR], positions=x, widths=box_width, patch_artist=True, showfliers=False)
ncplot = ax.boxplot([fsp_KPN_Enschede_NC, fsp_T_Mobile_Enschede_NC, fsp_Vodafone_Enschede_NC], positions=x + 1.5*box_width, widths=box_width, patch_artist=True, showfliers=False)

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
plt.savefig('Figures/FSPperMNO_enschede.pdf', dpi=1000)
#plt.show()





""" NR_full_fdp = {'Overijssel': [0.0013884019353481523, 0.00128321997054905, 0.0012481593156160157],
               'Friesland': [0.002189255365115944, 0.0019348024389072927, 0.002083633395746315],
               'Utrecht': [0.0017897367852624433, 0.0015613910574875799, 0.0017002499459993212],

               'Middelburg': [7.874015748031496e-05, 2.6246719160104988e-05, 5.2493438320209976e-05],
               'Enschede': [0.004504132231404959, 0.00449232585596222, 0.004462809917355372],
               'Amsterdam': [0.0053018617021276596, 0.005128989361702128, 0.005414893617021277]
               }

NR_full_fsp = {'Overijssel': [0.7728181754435173, 0.8352675127971391, 0.8211843489236379],
               'Friesland': [0.762916606654184, 0.828945220605886, 0.8142700081616976],
               'Utrecht': [0.799202332829327, 0.8570836547659456, 0.8458829882432808],

               'Middelburg': [0.9310236220472441, 0.9546719160104987, 0.9492913385826771],
               'Enschede': [0.8615997638724912, 0.8985773317591499, 0.8920188902007083],
               'Amsterdam': [0.8428470744680852, 0.8908470744680851, 0.8869507978723404]
               }

NR_fallback_fdp = {'Middelburg': [7.874015748031496e-05, 2.6246719160104988e-05, 5.2493438320209976e-05],
                   'Enschede': [0.004504132231404959, 0.00449232585596222, 0.004462809917355372],
                   'Amsterdam': [0.0053018617021276596, 0.005128989361702128, 0.005414893617021277],

                   'Overijssel': [0.0013884019353481523, 0.00128321997054905, 0.0012481593156160157],
                   'Friesland': [0.002189255365115944, 0.0019348024389072927, 0.002083633395746315],
                   'Utrecht': [0.0017897367852624433, 0.0015613910574875799, 0.0017002499459993212]}

NR_fallback_fsp = {'Middelburg': [0.7809711286089239, 0.8258005249343832, 0.9010498687664042],
                   'Enschede': [0.7187898465171192, 0.6746930342384888, 0.8213695395513577],
                   'Amsterdam': [0.6995066489361702, 0.7091303191489362, 0.7797220744680851],

                   'Overijssel': [0.6333426828413155, 0.5580183717831849, 0.7010237711240446],
                   'Friesland': [0.5933794229199674, 0.5726775169235201, 0.6938259157904845],
                   'Utrecht': [0.6617366618323202, 0.6232634924553337, 0.737396241552751]}

no_cooperation_fdp = {'Middelburg': [0.0013123359580052493, 0.0, 0.012860892388451443],
                      'Enschede': [0.006493506493506494, 0.003128689492325856, 0.020070838252656435],
                      'Amsterdam': [0.04313829787234043, 0.01452127659574468, 0.06809840425531914],

                      'Overijssel': [0.016268143888927847, 0.013252927564686908, 0.05301171025874763],
                      'Friesland': [0.022324643525853376, 0.017379614959911662, 0.06947044985356954],
                      'Utrecht': [0.028080353010152128, 0.01468818465146419, 0.06159163143765236]}

no_cooperation_fsp = {'Middelburg': [0.8813648293963254, 0.9519685039370078, 0.8535433070866142],
                      'Enschede': [0.7723730814639905, 0.8739669421487604, 0.6452774498229044],
                      'Amsterdam': [0.6964627659574468, 0.8274468085106383, 0.640811170212766],

                      'Overijssel': [0.6413996213449267, 0.7210574293527803, 0.5291354042493513],
                      'Friesland': [0.5966200969801718, 0.7172211820058573, 0.5358394546065581],
                      'Utrecht': [0.6596722930231123, 0.7592804023822014, 0.5866942327274971]}

two_NR_fallback_fdp = {'Middelburg': [0.0003937007874015748, 0.0005249343832020997],
                       'Enschede': [0.003677685950413223, 0.003654073199527745],
                       'Amsterdam': [0.005803191489361702, 0.005630319148936171],

                       'Overijssel': [0.0042360283290091855, 0.0042963326554940045],
                       'Friesland': [0.006694512458591387, 0.006743482644390033],
                       'Utrecht': [0.00531582682753726, 0.005351930138550313]}

two_NR_fallback_fsp = {'Middelburg': [0.8443569553805774, 0.9201837270341208],
                       'Enschede': [0.6560212514757969, 0.8430342384887839],
                       'Amsterdam': [0.6882726063829787, 0.7928284574468085],

                       'Overijssel': [0.546650305027698, 0.6997440572189888],
                       'Friesland': [0.5608814633443756, 0.6915876902395698],
                       'Utrecht': [0.6139346437498071, 0.7379507513808745]
                       }

NR_fallback_QOS_fdp = {'Middelburg': [0.0001837270341207349, 0.0003937007874015748, 0.0001837270341207349],
                       'Enschede': [0.002668240850059032, 0.00551357733175915, 0.004386068476977568],
                       'Amsterdam': [0.006416223404255319, 0.009990691489361702, 0.0062393617021276595],

                       'Overijssel': [0.004381179440431948, 0.011237641119136105, 0.005974335600589019],
                       'Friesland': [0.006838062316961928, 0.017717605261894476, 0.009837726247059388],
                       'Utrecht': [0.005811398771870275, 0.0137559786465887, 0.007262937019779678]
                       }

NR_fallback_QOS_fsp = {'Middelburg': [0.8322309711286089, 0.8498687664041995, 0.921994750656168],
                       'Enschede': [0.745974025974026, 0.6725619834710744, 0.8556316410861865],
                       'Amsterdam': [0.7223031914893617, 0.7102353723404256, 0.8197965425531915],

                       'Overijssel': [0.6461804922515952, 0.5680359021106515, 0.7212187083654723],
                       'Friesland': [0.6074549906380527, 0.5830515147150608, 0.7173728935618608],
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
labels = ['no cooperation', 'NR-full', 'NR-fallback', 'NR-fallback-QOS', 'NR-fallback 1&3']

max_x = 0.2

fig, ax = plt.subplots()
for x in range(len(cities)):
    plt.plot([-0.001, max_x], [x - 0.2, x - 0.2], ':', color='gray', alpha=0.5, zorder=1)
    plt.plot([-0.001, max_x], [x, x], ':', color='gray', alpha=0.5, zorder=1)
    plt.plot([-0.001, max_x], [x + 0.2, x + 0.2], ':', color='gray', alpha=0.5, zorder=1)

y_axes = {'KPN': [i + 0.2 for i in range(len(cities))], 'T-Mobile': [i for i in range(len(cities))],
          'Vodafone': [i - 0.2 for i in range(len(cities))]}

for i, data in zip(range(4), [no_cooperation_fdp, NR_full_fdp, NR_fallback_fdp, NR_fallback_QOS_fdp]):
    for j in range(len(MNOs)):
        vals = [v[j] for k, v in data.items() if k in cities]
        if j == 0:
            plt.scatter(vals, y_axes[MNOs[j]], color=util.get_color(i), alpha=0.5, marker=markers[i], label=labels[i])
        else:
            plt.scatter(vals, y_axes[MNOs[j]], color=util.get_color(i), alpha=0.5, marker=markers[i])
i = 4
for j, index in zip([0, 1], [1, 2]):
    vals = [v[j] for k, v in two_NR_fallback_fdp.items() if k in cities]
    if j == 0:
        plt.scatter(vals, y_axes[MNOs[index]], color=util.get_color(i), alpha=0.5, marker=markers[i], label=labels[i])
    else:
        plt.scatter(vals, y_axes[MNOs[index]], color=util.get_color(i), alpha=0.5, marker=markers[i])

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
min_x = 0.

for x in range(len(cities)):
    plt.plot([min_x, 1.0], [x - 0.2, x - 0.2], ':', color='gray', alpha=0.5, zorder=1)
    plt.plot([min_x, 1.0], [x, x], ':', color='gray', alpha=0.5, zorder=1)
    plt.plot([min_x, 1.0], [x + 0.2, x + 0.2], ':', color='gray', alpha=0.5, zorder=1)

y_axes = {'KPN': [i + 0.2 for i in range(len(cities))], 'T-Mobile': [i for i in range(len(cities))],
          'Vodafone': [i - 0.2 for i in range(len(cities))]}

for i, data in zip(range(4), [no_cooperation_fsp, NR_full_fsp, NR_fallback_fsp, NR_fallback_QOS_fsp]):
    for j in range(len(MNOs)):
        vals = [v[j] for k, v in data.items() if k in cities]
        if j == 0:
            plt.scatter(vals, y_axes[MNOs[j]], color=util.get_color(i), alpha=0.5, marker=markers[i], label=labels[i])
        else:
            plt.scatter(vals, y_axes[MNOs[j]], color=util.get_color(i), alpha=0.5, marker=markers[i])
i = 4
for j, index in zip([0, 1], [1, 2]):
    vals = [v[j] for k, v in two_NR_fallback_fsp.items() if k in cities]
    if j == 0:
        plt.scatter(vals, y_axes[MNOs[index]], color=util.get_color(i), alpha=0.5, marker=markers[i], label=labels[i])
    else:
        plt.scatter(vals, y_axes[MNOs[index]], color=util.get_color(i), alpha=0.5, marker=markers[i])
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
    plt.savefig(f'Figures/{FDPFSP}with_fallback_cities.pdf', dpi=1000, transparent=True)
else:
    plt.savefig(f'Figures/{FDPFSP}with_fallback_provinces.pdf', dpi=1000, transparent=True)

plt.show()
 """