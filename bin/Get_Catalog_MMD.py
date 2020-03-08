#!/usr/bin/ipython
'''-------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------
'''

import os
import numpy as np
from sys import argv, exit
import matplotlib.pyplot as plt
from itertools import combinations

# Input J, IR1, IR2, IR3, IR4, MP1
# If the band is lack, magnitude is assigned to -999
# TODO Make SEIP catalog all band QUA is always "A"
# TODO Make TMUS catalog which J band QUA is always "A"

SEIP_mag_catalog = str(argv[1])
TMUS_mag_catalog = str(argv[2])

band_nam = ['J', 'IR1', 'IR2', 'IR3', 'IR4', 'MP1']
band_ind = [0, 1, 2, 3, 4, 5]
mag_id = [0, 1, 2, 3, 4, 5]
qua_id = [6, 7, 8, 9, 10, 11]
band_lim = [[4.0,18.0], [8.0,18.0], [7.0,18.0], [5.0,18.0], [5.0,18.0], [3.5,11.0]]

def get_2band(bd_ind, awk_id, qua_id):
    for
    os.system('awk \'$' + str(S_awk_id[i]) + '>0.0 && $' + str(awk_id[j]) + '>0.0 && $' + str(qua_id[j]) +'!=\"E\" && $'\
              + str(qua_id[j]) + '!=\"U\" {print $' + str(awk_id[i]) + ', $' + str(awk_id[j]) + '}\' ' + SEIP_mag_catalog + ' > '\
                    + band[i] + band[j] + '.txt')



# TODO Plot 3 kinds of MMD
# - New SEIP catalog galaxies
# - 2MASS + UKIDSS + SPIZER galaxies
# - 2MASS + UKIDSS + SPIZER galaxies only with QUA is not U
for comb in combinations(band_ind, 2):
    bands = list(comb)
    os.system('awk \'$' + str(S_awk_id[i]) + '>0.0 && $' + str(awk_id[j]) + '>0.0 && $' + str(qua_id[j]) +'!=\"E\" && $'\
              + str(qua_id[j]) + '!=\"U\" {print $' + str(awk_id[i]) + ', $' + str(awk_id[j]) + '}\' ' + SEIP_mag_catalog + ' > '\
                    + band[i] + band[j] + '.txt')
                else:
                    os.system('awk \'$' + str(awk_id[i]) + '>0.0 && $' + str(qua_id[i]) + '!=\"E\" && $'+ str(qua_id[i]) + '!=\"U\" && $'\
                    + str(awk_id[j]) + '>0.0 && $' + str(qua_id[j]) + '!=\"E\" && $' + str(qua_id[j]) + '!=\"U\" {print $' + str(awk_id[i])\
                    + ', $' + str(awk_id[j]) + '}\' ' + gal_cat + ' > ' + band[i] + band[j] + '.txt')
    os.chdir('../')
#==================================================================================================================================

for k in range(len(cat_list)):
    print('\nGet catalog %i magnitude data for different bands ...' % (k+1))
    if os.path.isdir('MMD_DATA' + str(k+1)):
        os.system('rm -fr MMD_DATA' + str(k+1))
        os.system('mkdir MMD_DATA' + str(k+1))
    else:
        os.system('mkdir MMD_DATA' + str(k+1))

    for i in range(len(band)):
        for j in range(len(band)):
            if j > i:
                print(band[i], band[j])
                if i == 0: # FLUX QUALITY OF J BAND IS FROM 2MASS, NOT FROM UKIDSS -> SKIP
                    os.system('awk \'$' + str(awk_id[i]) + '>0.0 && $' + str(awk_id[j]) + '>0.0 && $' + str(qua_id[j]) +'!=\"E\" && $'\
                    + str(qua_id[j]) + '!=\"U\" {print $' + str(awk_id[i]) + ', $' + str(awk_id[j]) + '}\' ' + cat_list[k]+ ' > '\
                    + 'MMD_DATA' + str(k+1) + '/'+ band[i] + band[j] + '.txt')
                else:
                    os.system('awk \'$' + str(awk_id[i]) + '>0.0 && $' + str(qua_id[i]) + '!=\"E\" && $'+ str(qua_id[i]) + '!=\"U\" && $'\
                    + str(awk_id[j]) + '>0.0 && $' + str(qua_id[j]) + '!=\"E\" && $' + str(qua_id[j]) + '!=\"U\" {print $' + str(awk_id[i])\
                    + ', $' + str(awk_id[j]) + '}\' '+ cat_list[k]+ ' > '  + 'MMD_DATA' + str(k+1) + '/' + band[i] + band[j] + '.txt')

#==================================================================================================================================

axes_list = []
plot_list = []
limit_list = []
for i in range(len(band)):
    for j in range(len(band)):
        if j > i:
            axes_list.append([band[i], band[j]])
            plot_list.append(band[i] + band[j] + '.txt')
            limit_list.append(limit[i] + limit[j])
print('\nStart ploting ...')
axes_list = np.reshape(axes_list, (5,3,2))
plot_list = np.reshape(plot_list, (5,3))
limit_list = np.reshape(limit_list, (5,3,2,2))
for i in range(5):
    #fig, axes = plt.subplots(1, 3, figsize=(50, 30))
    fig, axes = plt.subplots(1,3)
    for j in range(3):
        print(axes_list[i][j])
        axes[j].invert_xaxis()
        axes[j].invert_yaxis()
        if BG == 'True':
            GMMD = np.transpose(np.loadtxt('GALAXY_SAMPLE/' + plot_list[i][j]))
            axes[j].plot(GMMD[0], GMMD[1], 'go', label='UKIDSS_SWIRE_GALAXY')
        for k in range(len(cat_list)):
            MMD = np.transpose(np.loadtxt('MMD_DATA' + str(k+1) + '/' + plot_list[i][j]))
            if len(MMD) != 0 :
                axes[j].plot(MMD[0], MMD[1], col_list[k], ms=mark_list[k], label=cat_list[k])
        axes[j].set_xlabel(axes_list[i][j][0], fontsize=14)
        axes[j].set_ylabel(axes_list[i][j][1], fontsize=14)
        axes[j].axvline(limit_list[i][j][0][0], color='black', linestyle='--')
        axes[j].axvline(limit_list[i][j][0][1], color='black', linestyle='--')
        axes[j].axhline(limit_list[i][j][1][0], color='black', linestyle='--')
        axes[j].axhline(limit_list[i][j][1][1], color='black', linestyle='--')
        axes[j].xaxis.label.set_size(10)
        axes[j].yaxis.label.set_size(10)
        axes[j].legend()
        axes[j].grid()
    plt.savefig('MMD' + str(i+1) + '.png')
plt.show()
