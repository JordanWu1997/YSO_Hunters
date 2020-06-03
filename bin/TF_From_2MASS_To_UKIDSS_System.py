#!/usr/bin/python
'''------------------------------------------------------------------------------------
This program is to transform 2MASS J,H,K bands to UKIDSS Jw, Hw, Kw bands

Input : catalog with J, H, K band flux value, flux quality from 2MASS
Output: catalog with J, H, K band magnitude value in UKIDSS format

*NOTE:
    1. empty column on SWIRE format catalog for storing magnitude
       (1) magnitude: J[35] H[56] K[77]
---------------------------------------------------------------------------------------
latest update : 20200311 Jordan Wu'''

# Load Modules
#======================================================
from __future__ import print_function
from sys import argv, exit
from os import system
import numpy as np
from All_Variables import *
from Hsieh_Functions import *
from Useful_Functions import *

# Global Variables
#======================================================
flux_ID_2Mass = flux_ID_2Mass
mag_ID_2Mass  = mag_ID_2Mass

# Main Programs
#======================================================
if __name__ == '__main__':

    # Check inputs
    if len(argv) != 3:
        exit('\n\tWrong Input Argument!\
              \n\tExample: [program] [input table] [output file name]\
              \n\t[output file name]: filename or "default"\n')
    else:
        print('\nStart Transform from 2MASS to UKIDSS ...')

    two_mass_cat_name = str(argv[1])
    output_cat_name   = str(argv[2])
    if output_cat_name == 'default':
        output_name = 'output.tbl'

    print('\nInput: ')
    with open(two_mass_cat_name, 'r') as cat:
        system('wc -l {}'.format(two_mass_cat_name))
        two_mass_cat = cat.readlines()

    ukidss_cat = []
    for i, line in enumerate(two_mass_cat):
        # Transform 2MASS detection to UKIDSS
        cols = line.split()
        mag_J, mag_K, mag_H = JHK_flux_to_mag(float(cols[flux_ID_2Mass[0]]), float(cols[flux_ID_2Mass[1]]), float(cols[flux_ID_2Mass[2]]))
        cols[mag_ID_2Mass[0]], cols[mag_ID_2Mass[1]], cols[mag_ID_2Mass[2]] = str(mag_J), str(mag_H), str(mag_K)
        ukidss_cat.append(format('\t'.join(cols)))
        # Percentage Indicator
        drawProgressBar(float(i+1)/len(two_mass_cat))

    print('\nOutput: ')
    with open(output_cat_name, 'w') as output:
        for line in ukidss_cat:
            output.write('{}\n'.format(line))
        system('wc -l {}'.format(output_cat_name))
    print()
