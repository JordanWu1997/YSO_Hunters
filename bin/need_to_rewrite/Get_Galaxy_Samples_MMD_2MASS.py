#!/usr/bin/ipython
'''-------------------------------------------------------------------------------------
This program is to plot MMD (Magnitude-Magnitude Diagrams): 

Input :
        (1)Catalog in SWIRE format to plot MMD
        (2)If catalogs are more than one, just enter them sequentially
        (3)If no input catalogs are entered, it will ONLY return reference MMD
Output: 
        (1)CCD in J,IR1,IR2,IR3,IR4,MP1 6 bands' combinations. (total 15)
        (2)15 MMD will be stored in 5 different imagess (3 MMD for each)
---------------------------------------------------------------------------------------
latest update : 2019/03/30 Jordan Wu'''

import os
import numpy as np
from sys import argv
import matplotlib.pyplot as plt

color = [' ', 'ro', 'bo', 'yo', 'ko']
cat_list, col_list = [], []
for i in range(len(argv)):
    if i != 0:
        cat_list.append(str(argv[i]))
        col_list.append(color[i])

print(cat_list)
band = ['J', 'IR1', 'IR2', 'IR3', 'IR4', 'MP1']
mag_id = [35, 98, 119, 140, 161, 182]
awk_id = [36, 99, 120, 141, 162, 183]
limit = [[4.0,18.0], [8.0,18.0], [7.0,18.0], [5.0,17.0], [5.0,18.0], [3.5,11.0]]
gal_cat = '/home/ken/C2D-SWIRE_20180710/Converted_catalog/catalog-SWIRE_ELAIS_N1_WI_mag.tbl'

#==================================================================================================================================
print('\nGet galaxy magnitude data for different bands ...')
if os.path.isdir('GALAXY_SAMPLE'):
    os.system('rm -fr GALAXY_SAMPLE')
    os.system('mkdir GALAXY_SAMPLE')
else:
    os.system('mkdir GALAXY_SAMPLE')
os.chdir('GALAXY_SAMPLE')
for i in range(len(band)):
    for j in range(len(band)):
        if j > i:
            print(band[i], band[j])
            os.system('awk \'$' + str(awk_id[i]) + '!=\"0.0\" && $' + str(awk_id[j]) + '!=\"0.0\" '+ '{print $' + str(awk_id[i])\
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
                if i == 0:
                    os.system('awk \'$' + str(awk_id[i]) + '!~/0.000000*/ && $' + str(awk_id[j]) + '!~/0.000000*/ && $' + str(awk_id[i])\
                    + '!~/-9.99*/ && $' + str(awk_id[j]) + '!~/-9.99*/{print $' + str(awk_id[i]) + ', $' + str(awk_id[j]) + '}\' '\
                    + cat_list[k] + ' > ' + 'MMD_DATA' + str(k+1) + '/' + band[i] + band[j] + '.txt')
                else:
                    os.system('awk \'$' + str(awk_id[i]) + '!=\"0.0\" && $' + str(awk_id[j]) + '!=\"0.0\" '+ '{print $' + str(awk_id[i])\
                    + ', $' + str(awk_id[j]) + '}\' ' + cat_list[k] + ' > ' + 'MMD_DATA' + str(k+1) + '/' + band[i] + band[j] + '.txt')
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
    fig, axes = plt.subplots(1, 3, figsize=(50, 30))
    for j in range(3):
        print(axes_list[i][j])
        GMMD = np.transpose(np.loadtxt('GALAXY_SAMPLE/' + plot_list[i][j]))
        axes[j].plot(GMMD[0], GMMD[1], 'go')
        for k in range(len(cat_list)):
            MMD = np.transpose(np.loadtxt('MMD_DATA' + str(k+1) + '/' + plot_list[i][j]))
            if len(MMD) != 0 :
                axes[j].plot(MMD[0], MMD[1], col_list[k], label=cat_list[k])
        axes[j].set_xlabel(axes_list[i][j][0])
        axes[j].set_ylabel(axes_list[i][j][1])
        axes[j].axvline(limit_list[i][j][0][0], color='blue', linestyle='--')
        axes[j].axvline(limit_list[i][j][0][1], color='blue', linestyle='--')
        axes[j].axhline(limit_list[i][j][1][0], color='blue', linestyle='--')
        axes[j].axhline(limit_list[i][j][1][1], color='blue', linestyle='--')
        axes[j].set_xticklabels(list(np.arange(limit_list[i][j][0][0], limit_list[i][j][0][1], 1)) + [limit_list[i][j][0][1]])
        axes[j].set_yticklabels(list(np.arange(limit_list[i][j][1][0], limit_list[i][j][1][1], 1)) + [limit_list[i][j][1][1]])
        axes[j].legend()
        axes[j].grid()
    plt.savefig('MMD' + str(i+1) + '.png')
plt.show()
