#!/usr/bin/ipython

import os
import numpy as np
from sys import exit
import matplotlib.pyplot as plt

cut_data = str(raw_input('Start Cutting Data ? (Yes or No) If data already exists, No PLEASE ') or 'Yes')
lower_bound = int(raw_input('Lower bound magnitude = ? (Bright End) ' or 7))
upper_bound = int(raw_input('Upper bound magniture = ? (Faint  End) ' or 12))
interval = float(raw_input('interval = ? (unit: mag) ') or 0.1)

#==============================================================================================
# Part 1 : Get Data
#==============================================================================================
gal_cat = '/home/ken/C2D-SWIRE_20180710/Converted_catalog/catalog-SWIRE_UKIDSS_ELAIS_N1_WI_CONDITION.tbl'
path = '/home/ken/C2D-SWIRE_20180710/Galaxy_Prob_WI_Diff_Binsize/Construct_Tomography/'
CHA_II_cat = path + 'CHA_II_NEW_ALGO.tbl'
LUP_I_cat = path + 'LUP_I_NEW_ALGO.tbl'
LUP_III_cat = path + 'LUP_III_NEW_ALGO.tbl'
LUP_IV_cat = path + 'LUP_IV_NEW_ALGO.tbl'

if cut_data == 'Yes':

    # Construct Storage Dir
    if os.path.isdir('Cut_Data'):
        os.system('rm -fr Cut_Data')
    os.system('mkdir Cut_Data')
    
    # Start cutting Data
    os.chdir('Cut_Data')
    gal_cat = '/home/ken/C2D-SWIRE_20180710/Converted_catalog/catalog-SWIRE_UKIDSS_ELAIS_N1_WI_CONDITION.tbl'
    os.system('awk \'$99>=15.0&&$99<18.0&&$120>=15.0&&$120<18.0&&$183>=7.0&&$183<12.0\
                &&$101!=\"E\"&&$101!=\"U\"&&$122!=\"E\"&&$122!=\"U\"&&$185!=\"E\"&&$185!=\"U\"\
                {print $99,$120,$183}\' ' + gal_cat + ' > UKIDSS_SWIRE_WI_CONDITION_IR1IR2MP1.tbl')
    os.system('awk \'$99>=15.0&&$99<18.0&&$120>=15.0&&$120<18.0&&$183>=7.0&&$183<12.0\
                &&$101!=\"E\"&&$101!=\"U\"&&$122!=\"E\"&&$122!=\"U\"&&$185!=\"E\"&&$185!=\"U\"\
                {print $99,$120,$183}\' ' + CHA_II_cat + ' > CHA_II_NEW_ALGO_WI_CONDITION_IR1IR2MP1.tbl')
    os.system('awk \'$99>=15.0&&$99<18.0&&$120>=15.0&&$120<18.0&&$183>=7.0&&$183<12.0\
                &&$101!=\"E\"&&$101!=\"U\"&&$122!=\"E\"&&$122!=\"U\"&&$185!=\"E\"&&$185!=\"U\"\
                {print $99,$120,$183}\' ' + LUP_I_cat + ' > LUP_I_NEW_ALGO_WI_CONDITION_IR1IR2MP1.tbl')
    os.system('awk \'$99>=15.0&&$99<18.0&&$120>=15.0&&$120<18.0&&$183>=7.0&&$183<12.0\
               &&$101!=\"E\"&&$101!=\"U\"&&$122!=\"E\"&&$122!=\"U\"&&$185!=\"E\"&&$185!=\"U\"\
                {print $99,$120,$183}\' ' + LUP_III_cat + ' > LUP_III_NEW_ALGO_WI_CONDITION_IR1IR2MP1.tbl')
    os.system('awk \'$99>=15.0&&$99<18.0&&$120>=15.0&&$120<18.0&&$183>=7.0&&$183<12.0\
               &&$101!=\"E\"&&$101!=\"U\"&&$122!=\"E\"&&$122!=\"U\"&&$185!=\"E\"&&$185!=\"U\"\
               {print $99,$120,$183}\' ' + LUP_IV_cat + ' > LUP_IV_NEW_ALGO_WI_CONDITION_IR1IR2MP1.tbl')
    os.chdir('../')

#==============================================================================================
# Part 2 : Load Cut Data
#==============================================================================================
os.chdir('Cut_Data')
gal_data = np.loadtxt('UKIDSS_SWIRE_WI_CONDITION_IR1IR2MP1.tbl')
CHA_II_data = np.loadtxt('CHA_II_NEW_ALGO_WI_CONDITION_IR1IR2MP1.tbl')
LUP_I_data = np.loadtxt('LUP_I_NEW_ALGO_WI_CONDITION_IR1IR2MP1.tbl')
LUP_III_data = np.loadtxt('LUP_III_NEW_ALGO_WI_CONDITION_IR1IR2MP1.tbl')
LUP_IV_data = np.loadtxt('LUP_IV_NEW_ALGO_WI_CONDITION_IR1IR2MP1.tbl')
os.chdir('../')

#==============================================================================================
# Part 3 : Plot Data Tomography
#==============================================================================================
if os.path.isdir('Gallery'):
    os.system('rm -fr Gallery')
    os.system('mkdir Gallery')
else:
    os.system('mkdir Gallery')

os.chdir('Gallery')
bounds = np.arange(lower_bound, upper_bound+interval, interval)
for i in range(len(bounds)-1):
    fig, axe = plt.subplots(1,1)
    axe.set_aspect('equal')
    for j in range(len(gal_data)):
        MP1 = gal_data[j][2]
        if MP1 >= bounds[i] and MP1 < bounds[i+1]:
            axe.plot(gal_data[j][0], gal_data[j][1], 'go')
    for k in range(len(CHA_II_data)):
        MP1 = CHA_II_data[k][2]
        if MP1 >= bounds[i] and MP1 < bounds[i+1]:
            axe.plot(CHA_II_data[k][0], CHA_II_data[k][1], 'ro')
    for l in range(len(LUP_I_data)):
        MP1 = LUP_I_data[l][2]
        if MP1 >= bounds[i] and MP1 < bounds[i+1]:
            axe.plot(LUP_I_data[l][0], LUP_I_data[l][1], 'bo')
    for m in range(len(LUP_III_data)):
        MP1 = LUP_III_data[m][2]
        if MP1 >= bounds[i] and MP1 < bounds[i+1]:
            axe.plot(LUP_III_data[m][0], LUP_III_data[m][1], 'yo')
    for n in range(len(LUP_IV_data)):
        MP1 = LUP_IV_data[n][2]
        if MP1 >= bounds[i] and MP1 < bounds[i+1]:
            axe.plot(LUP_IV_data[n][0], LUP_IV_data[n][1], 'co')
    
    axe.plot([], [], 'go', label='Galaxy')
    axe.plot([], [], 'ro', label='CHA_II_NEW_ALGO')
    axe.plot([], [], 'bo', label='LUP_I_NEW_ALGO')
    axe.plot([], [], 'yo', label='LUP_III_NEW_ALGO')
    axe.plot([], [], 'co', label='LUP_IV_NEW_ALGO')

    axe.legend(loc=2)
    axe.set_xlabel('IR1', fontsize=14)
    axe.set_ylabel('IR2', fontsize=14)
    axe.set_xlim(15, 18)
    axe.set_ylim(15, 18)
    axe.set_xticks(np.arange(15, 18+0.5, 0.5))
    axe.set_yticks(np.arange(15, 18+0.5, 0.5))
    axe.set_xticklabels(np.arange(15, 18+0.5, 0.5))
    axe.set_yticklabels(np.arange(15, 18+0.5, 0.5))
    axe.set_title(('%.1f > MP1 >= %.1f' % (bounds[i+1], bounds[i])), fontsize=14)
    axe.grid()

    index = ''
    if i < 10:
        index = '00' + str(i)
    elif i < 100:
        index = '0' + str(i)
    elif i < 1000:
        index = str(i)
    elif i >= 1000:
        print('Too Many Images ...')
        index = str(i)
    plt.savefig('%s-IR1IR2_ON_MP1_AXIS.png' % index)

os.system('convert -delay 20 -loop 0 *.png Tomography.gif')
