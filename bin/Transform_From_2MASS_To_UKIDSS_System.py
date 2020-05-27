#!/usr/bin/ipython
'''------------------------------------------------------------------------------------
This program is to transform 2MASS J,H,K bands to UKIDSS Jw, Hw, Kw bands

Input : catalog with J, H, K band flux value, flux quality from 2MASS
Output: catalog with J, H, K band magnitude value in UKIDSS format

*NOTE:
    1. empty column on SWIRE format catalog for storing magnitude
       (1) magnitude: J[35] H[56] K[77]
---------------------------------------------------------------------------------------
latest update : 20200311 Jordan Wu'''

from sys import argv, exit
from os import system
import numpy as np
from Hsieh_Functions import *
from Useful_Functions import *

if len(argv) != 3:
    exit('Wrong Input Argument!\
        \nExample: python [program] [input table] [output file name]')
else:
    print('Start ...')

#=========================================================
data = open(str(argv[1]), 'r')
system('wc ' + str(argv[1]))
two_mass_cat = data.readlines()
data.close()

if str(argv[2]) == '':
    output_name = 'output.tbl'
else:
    output_name = str(argv[2])

#=========================================================
Ukidss = []
for i, row in enumerate(two_mass_cat):
    # Transform 2MASS detection to UKIDSS
    cols = row.split()
    mag_J, mag_K, mag_H = JHK_flux_to_mag(float(cols[33]), float(cols[54]), float(cols[75]))
    cols[35], cols[56], cols[77] = str(mag_J), str(mag_H), str(mag_K)
    # Calculate magnitude from old c2d catalog
    mag_list = mJy_to_mag_ONLY_Spitzer(cols)
    err_list = flux_error_to_mag_ONLY_Spitzer(cols)
    for i, ID in enumerate(mag_ID_Spitzer):
        cols[ID] = str(mag_list[i])
    for j, ID in enumerate(mag_err_ID_Spitzer):
        cols[ID] = str(err_list[j])
    # Glue all cols in a long line
    new_row = '\t'.join(cols) + '\n'
    Ukidss.append(str(new_row))
    # Percentage Indicator
    drawProgressBar(float(i+1)/len(two_mass_cat))

#=========================================================
out_file = open(output_name, 'w')
for row in Ukidss:
    out_file.write(row)
out_file.close()
system('wc ' + output_name)
