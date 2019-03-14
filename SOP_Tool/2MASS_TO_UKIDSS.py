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
import numpy as np

if len(argv) != 3:
    exit('Wrong Input Argument!\
        \nExample: python [program] [input table] [output file name]')

data = open(str(argv[1]), 'r')
2mass_cat = data.readlines()
data.close()

if str(argv[2]) == '':
    output_name = 'output.tbl'
else:
    output_name = str(argv[2])

def JHK_flux_to_mag(J_flux, H_flux, K_flux):
    ''' 
    This function is to change fluxes on the catalog to magnitudes
    '''
    F0_list = [1594000, 1024000, 666700 ]
    mag_J = -2.5 * np.log10(float(J_flux)/F0_list[0])
    mag_H = -2.5 * np.log10(float(H_flux)/F0_list[1])
    mag_K = -2.5 * np.log10(float(K_flux)/F0_list[2])
    return mag_J, mag_H, mag_K

def from_2mass_to_ukidss(mag_J, mag_H, mag_K):
    mag_Jw, mag_Hw, mag_Kw = 0.0, 0.0, 0.0
    if mag_J > 0.0 and mag_H > 0.0 and mag_K > 0.0:
        mag_Jw = mag_J - 0.065 * (mag_J - mag_H)
        mag_Hw = mag_H + 0.07  * (mag_J - mag_H)
        mag_Kw = mag_K + 0.01  * (mag_J - mag_K)
    return mag_Jw, mag_Hw, mag_Kw

Ukidss = []
for row in 2mass_cat:
    cols = row.split()
    flux_J, flux__H, flux_K = float(cols[33]), float(cols[54]), float(cols[75])
    mag_J, mag_H, mag_K = from_2mass_to_ukidss(flux_J, flux_H, flux_K)
    col[35], cols[56], cols[77] = from_2mass_to_ukidss(mag_J, mag_H, mag_K)
    new_row = '\t'.join(cols)
    Ukiss.append(str(new_row))

out_file = open(output_name, 'w')
for row in Ukidss:
    out_file.write(row + '\n')
out_file.close()
