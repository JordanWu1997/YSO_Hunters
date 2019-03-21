#!/usr/bin/ipython
'''------------------------------------------------------------------------------------
This program is to transform 2MASS J,H,K bands to UKIDSS Jw, Hw, Kw bands

Input : catalog with J, H, K band flux value, flux quality from 2MASS
Output: catalog with J, H, K band magnitude value in UKIDSS format

*NOTE: 
    1. empty column on SWIRE format catalog for storing magnitude
       (1) magnitude: J[35] H[56] K[77]
---------------------------------------------------------------------------------------
latest update : 2019/03/14 Jordan Wu'''

from sys import argv, exit
from os import system
import numpy as np

if len(argv) != 3:
    exit('Wrong Input Argument!\
        \nExample: python [program] [input table] [output file name]')
else:
    print('Start ...')

data = open(str(argv[1]), 'r')
system('wc ' + str(argv[1]))
two_mass_cat = data.readlines()
data.close()

if str(argv[2]) == '':
    output_name = 'output.tbl'
else:
    output_name = str(argv[2])

# Functions
#---------------------------------------------------------------------------------------

def JHK_flux_to_mag(J_flux, H_flux, K_flux):
    ''' 
    This function is to (1)change fluxes on the catalog to magnitudes
                        (2)transform magnitudes from 2MASS to UKIDSS
    '''
    if float(J_flux) > 0 and float(H_flux) > 0 and float(K_flux) > 0:
        F0_list = [1594000, 1024000, 666700]
        mag_J = -2.5 * np.log10(float(J_flux)/F0_list[0])
        mag_H = -2.5 * np.log10(float(H_flux)/F0_list[1])
        mag_K = -2.5 * np.log10(float(K_flux)/F0_list[2])
    else:
        mag_J, mag_H, mag_K = 0.0, 0.0, 0.0

    mag_Jw, mag_Hw, mag_Kw = 0.0, 0.0, 0.0
    if mag_J > 0.0 and mag_H > 0.0:
        mag_Jw = mag_J - 0.065 * (mag_J - mag_H)
        mag_Hw = mag_H + 0.07  * (mag_J - mag_H)
    elif mag_J > 0.0 and mag_K > 0.0:
        mag_Kw = mag_K + 0.01  * (mag_J - mag_K)
    return mag_Jw, mag_Hw, mag_Kw

def IRAC_MP1_errorlist(x):
    F0_list = [280900, 179700, 115000, 64130, 7140]
    df_list = [x[97], x[118], x[139], x[160], x[181]]

    dm_list = []
    for i in range(len(F0_list)):
        if df_list[i] != 0.0:
            dm = float(df_list[i])/F0_list[i] * 2.5*np.log10(np.e)
        else :
            dm = 0.0
        dm_list.append(dm)
    return dm_list

def IRAC_MP1_magnitudelist(x):
    '''
    This function is to change fluxes on the catalog to magnitudes
    '''
    flux_list = [float(x[96]), float(x[117]), float(x[138]), float(x[159]), float(x[180])]
    F0_list = [280900, 179700, 115000, 64130, 7140]
    flux_Qua = [x[100], x[121], x[142], x[163], x[184]]

    mag_list = []
    for i in range(len(F0_list)):
        if float(flux_list[i]) != 0.0:
            mag_list.append(-2.5*np.log10(float(flux_list[i])/F0_list[i]))
        else:
            mag_list.append(0.0)
    return mag_list

#---------------------------------------------------------------------------------------

Ukidss = []; i=0
for row in two_mass_cat:
    cols = row.split()

    # Transform 2MASS detection to UKIDSS
    mag_J, mag_K, mag_H = JHK_flux_to_mag(float(cols[33]), float(cols[54]), float(cols[75]))
    cols[35], cols[56], cols[77] = str(mag_J), str(mag_H), str(mag_K)
    
    # Calculate magnitude from old c2d catalog
    mag_list = IRAC_MP1_magnitudelist(cols)
    err_list = IRAC_MP1_errorlist(cols)
    cols[98] = str(mag_list[0])
    cols[119] = str(mag_list[1])
    cols[140] = str(mag_list[2])
    cols[161] = str(mag_list[3])
    cols[182] = str(mag_list[4])
    cols[99] = str(err_list[0])
    cols[120] = str(err_list[1])
    cols[141] = str(err_list[2])
    cols[162] = str(err_list[3])
    cols[183] = str(err_list[4])
    
    # Glue all cols in a long line
    new_row = '\t'.join(cols) + '\n'
    Ukidss.append(str(new_row))
    
    # Percentage Indicator
    if i>100 and i%100==0:
        print('%.6f' % (100*float(i)/float(len(two_mass_cat))) + '%')
    i+=1

out_file = open(output_name, 'w')
for row in Ukidss:
    out_file.write(row)
out_file.close()
system('wc ' + output_name)
