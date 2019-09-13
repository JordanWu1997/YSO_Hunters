#!/usr/bin/ipython
'''-------------------------------------------------------------------------------------
This program is to write :
    (1) new UKIDSS J,H,K mag and error
    (2) old SWIRE IR1,IR2,IR3,IR4,MP1 mag and error to an old SWIRE catalog (for ELAIS N1)

**NOTE**
    Since UKIDSS catalog has a saturate issue, we use new UKIDSS data with condition:
       (1) Replace UKIDSS data ONLY with J band magnitude larger than 11.5 mag
       (2) For UKIDSS data with J band magnitude smaller than 11.5 mag, reject to replace
           with UKIDSS data. However, 2MASS data still have to do calibration to UKIDSS format

    1. Empty columns on SWIRE format catalog for storing UKIDSS magnitude and error
       (1) magnitude: J[35], H[56], K[77]
       (2) mag_err: J[36], H[57], K[78]

    2. Empty columns on SWIRE format catalog for storing SWIRE mag and error
       (1) magnitude: IR1[102], IR2[123], IR3[144], IR4[165], MP1[186]
       (2) mag_err: IR1[103], IR2[124], IR3[145], IR4[166], MP1[187]

    3. If a band is undetected, the magnitude and error will be assigned as '0.0'

---------------------------------------------------------------------------------------
latest update : 2019/09/13 Jordan Wu'''

from sys import argv, exit
from astropy.coordinates import SkyCoord
import numpy as np
import math as mh
import time
import os

if len(argv) != 6:
    exit('\n\tWrong Input Argument!\
        \n\tExample: python [program] [SWIRE] [UKIDSS] [Header length] [Output filename] [Option]\
        \n\t[Option]: 2MASSBR <= keep 2MASS Bright Sources (Jmag>11.5)\
        \n\t**Note**: This Program Replace [SWIRE] J,H,K with [UKIDSS]\n')

# For transformation of old 2MASS data to new UKIDSS format
#=====================================================================
def JHK_flux_to_mag(J_flux, H_flux, K_flux, to_UKIDSS=True):
    '''
    This function is to (1)change fluxes on the catalog to magnitudes
                        (2)transform magnitudes from 2MASS to UKIDSS
    **Note** F0 unit: mJy
    '''
    F0_list = [1594000, 1024000, 666700]
    if float(J_flux) > 0.0:
        mag_J = -2.5 * np.log10(float(J_flux)/F0_list[0])
    if float(H_flux) > 0.0:
        mag_H = -2.5 * np.log10(float(H_flux)/F0_list[1])
    if float(K_flux) > 0.0:
        mag_K = -2.5 * np.log10(float(K_flux)/F0_list[2])

    if to_UKIDSS == True:
        if mag_J > 0.0 and mag_H > 0.0:
            mag_J = mag_J - 0.065 * (mag_J - mag_H)
            mag_H = mag_H + 0.07  * (mag_J - mag_H)
        if mag_J > 0.0 and mag_K > 0.0:
            mag_K = mag_K + 0.01  * (mag_J - mag_K)
    else:
        pass

    return str(mag_Jw), str(mag_Hw), str(mag_Kw)

def IRAC_MP1_errorlist(x):
    F0_list = [280900, 179700, 115000, 64130, 7140]
    df_list = [x[97], x[118], x[139], x[160], x[181]]
    dm_list = []
    for i in range(len(F0_list)):
        if df_list[i] > 0.0:
            dm = (float(df_list[i])/F0_list[i]) * 2.5 * mh.log10(mh.e)
        else :
            dm = 0.0
        dm_list.append(str(dm))
    return dm_list

def IRAC_MP1_magnitudelist(x):
    flux_list = [x[96], x[117], x[138], x[159], x[180]]
    F0_list = [280900.0, 179700.0, 115000.0, 64130.0, 7140.0]
    mag_list = []
    for i in range(len(F0_list)):
        if float(flux_list[i]) > 0.0:
            mag = -2.5 * mh.log10(float(flux_list[i])/F0_list[i])
        else:
            mag = 0.0
        mag_list.append(str(mag))
    return mag_list
#=====================================================================

with open(str(argv[1]), 'r') as data:
    two_mass_cat = data.readlines()
with open(str(argv[2]), 'r') as data:
    head = int(argv[3])
    ukidss_cat = data.readlines()[head:]

t_start = time.time()
out_catalog = []
for i in range(len(ukidss_cat)):

    index = int(ukidss_cat[i].split()[0].strip(',')) - 1
    row_s = two_mass_cat[index].split()
    row_u = ukidss_cat[i].split()

    # Percentage Indicator
    if i>1000 and i%1000==0:
        print('%.6f' % (100*float(i)/float(len(ukidss_cat))) + '%')

    # Write SWIRE IR1~MP1 magnitude and error
    mag_list = IRAC_MP1_magnitudelist(row_s)
    err_list = IRAC_MP1_errorlist(row_s)
    row_s[98], row_s[119], row_s[140], row_s[161], row_s[182] = mag_list[0], mag_list[1], mag_list[2], mag_list[3], mag_list[4]
    row_s[99], row_s[120], row_s[141], row_s[162], row_s[183] = err_list[0], err_list[1], err_list[2], err_list[3], err_list[4]

    # Write UKIDSS JHK magnitude and error
    mag_J, mag_H, mag_K = row_u.split(',')[10], row_u.split(',')[12], row_u.split(',')[14]
    err_J, err_H, err_K = row_u.split(',')[11], row_u.split(',')[13], (row_u.split(',')[15]).strip('\n')

    # If No Detection => Transform from 2MASS to UKIDSS
    if float((row_u[i].split(','))[6]) == 0.0 or float((row_u[i].split(','))[7]) == 0.0:
        row_s[35], row_s[56], row_s[77] = JHK_flux_to_mag(row_s[33], row_s[54], row_s[75])
        row_s[36], row_s[57], row_s[78] = 0.0, 0.0, 0.0
    else:
        row_s[35], row_s[56], row_s[77] = mag_J, mag_H, mag_K
        row_s[36], row_s[57], row_s[78] = err_J, err_H, err_K

    # Pick Up Bright Sources In 2MASS Observation
    if str(argv[5]) == '2MASSBR':
        if float(mag_J) < 11.5:
            row_s[35], row_s[56], row_s[77] = JHK_flux_to_mag(row_s[33], row_s[54], row_s[75])
            row_s[36], row_s[57], row_s[78] = 0.0, 0.0, 0.0

    # Write New Output Catalog
    out_catalog.append(row_s)

# Write Output
with open(str(argv[4]), 'w') as out:
    for row in out_catalog:
        out.write(row)

t_end = time.time()
print('\nThis procedure took %.6f secs ...' % (t_end - t_start))
