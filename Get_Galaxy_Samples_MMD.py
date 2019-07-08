#!/usr/bin/ipython
'''-------------------------------------------------------------------------------------
This program is to plot MMD (Magnitude-Magnitude Diagrams): 

Input :
        (1)Catalog in SWIRE format to plot MMD
        (2)If catalogs are more than one, just enter them sequentially
        (3)If no input catalogs are entered, it will ONLY return reference MMD
Output: 
        (1)CCD in J,IR1,IR2,IR3,IR4,MP1 6 bands' combinations. (total 15)
        (2)15 MMD will be stored in 5 different images (3 MMD for each)

**NOTE: The sequence of INPUT CATALOG will affect the layer of display diagrams (Bottom->Top)
        Recommendation: Put those catalogs covering more objects in the front of input line
---------------------------------------------------------------------------------------
latest update : 2019/05/05 Jordan Wu'''

import os
import numpy as np
from sys import argv, exit
import matplotlib.pyplot as plt

model = str(argv[-1])
BG = str(argv[-2])
if BG == 'True':
    color = [' **blank** ', 'ro', 'bo', 'co', 'mo', 'yo']
    markersize = [' **blank** ', 7.0, 6.0, 5.0, 4.0, 3.0]
else:
    color = [' **blank** ', 'go', 'ro', 'bo', 'co', 'mo', 'yo']
    markersize = [' **blank** ', '8.0', 7.0, 6.0, 5.0, 4.0, 3.0]

#if len(argv) > len(color):
#    exit('Too many input catalogs ... (Max: 5)')
#else:
#    print('Input check pass ...')

cat_list, col_list, mark_list = [], [], []
for i in range(len(argv)-2):
    if i != 0:
        cat_list.append(str(argv[i]))
        col_list.append(color[i])
        mark_list.append(markersize[i])
print('Input :', cat_list)

band = ['J', 'IR1', 'IR2', 'IR3', 'IR4', 'MP1']
awk_id = [36, 99, 120, 141, 162, 183]
qua_id = [38, 101, 122, 143, 164, 185]
limit = [[4.0,18.0], [8.0,18.0], [7.0,18.0], [5.0,18.0], [5.0,18.0], [3.5,11.0]]

if model == 'old':
    gal_cat = '/home/ken/C2D-SWIRE_20180710/Converted_catalog/catalog-SWIRE_UKIDSS_ELAIS_N1.tbl'
elif model =='new':
    gal_cat = '/home/ken/C2D-SWIRE_20180710/Converted_catalog/catalog-SWIRE_UKIDSS_ELAIS_N1_WI_CONDITION.tbl'

#==================================================================================================================================
if BG == 'True':
    print('\nGet background galaxy magnitude data for different bands ...')
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
                if i == 0: # FLUX QUALITY OF J BAND IS FROM 2MASS, NOT FROM UKIDSS -> SKIP
                    os.system('awk \'$' + str(awk_id[i]) + '>0.0 && $' + str(awk_id[j]) + '>0.0 && $' + str(qua_id[j]) +'!=\"E\" && $'\
                    + str(qua_id[j]) + '!=\"U\" {print $' + str(awk_id[i]) + ', $' + str(awk_id[j]) + '}\' ' + gal_cat + ' > '\
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
