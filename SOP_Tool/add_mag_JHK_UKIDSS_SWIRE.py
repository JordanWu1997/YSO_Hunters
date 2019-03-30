#!/usr/bin/ipython
'''-------------------------------------------------------------------------------------
This program is to write : 
    (1) new UKIDSS J,H,K mag and error
    (2) old SWIRE IR1,IR2,IR3,IR4,MP1 mag and error                        
    to an old SWIRE catalog (for ELAIS N1)

Input :
    (1)SWIRE catalog to be replaced
    (2)UKIDSS catalog to replace
    (3)Output catalog filename

Output: 
    New catalog with 
        (1)UKIDSS J, H, K band magnitude and error
        (2)SWIRE IR1,IR2,IR3,IR4,MP1 band magnitude and error

*NOTE: 
    1. Empty columns on SWIRE format catalog for storing UKIDSS magnitude and error
       (1) magnitude: J[35], H[56], K[77]
       (2) mag_err: J[36], H[57], K[78]
    
    2. Empty columns on SWIRE format catalog for storing SWIRE mag and error
       (1) magnitude: IR1[102], IR2[123], IR3[144], IR4[165], MP1[186]
       (2) mag_err: IR1[103], IR2[124], IR3[145], IR4[166], MP1[187]
    
    3. If a band is undetected, the magnitude and error will be assigned as '0.0'

    4. If a 2MASS object is found more than one source in UKIDSS catalog,
       only the last source in catalog will take into consideration.

---------------------------------------------------------------------------------------
latest update : 2019/03/18 Jordan Wu'''

from sys import argv, exit
from astropy.coordinates import SkyCoord
import numpy as np
import math as mh
import time
import os

if len(argv) != 4:
    exit('Wrong Input Argument!\
        \nExample: python [program] [Swire] [UKIDSS] [output file name]\
        \nNote: Replace [Swire] J,H,K with [UKIDSS]')
else:
    print('\nStart input check ...')

def IRAC_MP1_errorlist(x):
    F0_list = [280900, 179700, 115000, 64130, 7140]
    df_list = [x[97], x[118], x[139], x[160], x[181]]
    
    dm_list = []
    for i in range(len(F0_list)):
        if df_list[i] != 0.0:
            dm = (float(df_list[i])/F0_list[i]) * 2.5 * mh.log10(mh.e)
        else :
            dm = 0.0
        dm_list.append(str(dm))
    return dm_list

def IRAC_MP1_magnitudelist(x):
    '''
    This function is to change fluxes on the catalog to magnitudes
    '''
    flux_list = [x[96], x[117], x[138], x[159], x[180]]
    F0_list = [280900.0, 179700.0, 115000.0, 64130.0, 7140.0]
    
    mag_list = []
    for i in range(len(F0_list)):    
        if float(flux_list[i]) != 0.0:    
            mag = -2.5 * mh.log10(float(flux_list[i])/F0_list[i])
        else:
            mag = 0.0
        mag_list.append(str(mag))
    return mag_list

data1 = open(str(argv[1]), 'r')
two_mass_cat = data1.readlines()
data1.close()

data2 = open(str(argv[2]), 'r')
UK_cat_origin = data2.readlines()
data2.close()

# Input file check for repeating sources
#==================================================

if len(two_mass_cat) < len(UK_cat_origin):
    t_start = time.time()
    
    Repeat_dict = {}
    for i in range(len(UK_cat_origin)):
        index = int(UK_cat_origin[i].split()[0].strip(',')) - 1
        Repeat_dict.update({index: ''})
        Repeat_dict[index] += UK_cat_origin[i] + ';'
        if i>1000 and i%1000==0:
            print('%.6f' % (100*float(i)/float(len(UK_cat_origin))) + '%')
    print('\nEnd of finding repeated sources ...')
    
    no_rpt_catalog = []
    for i in range(len(Repeat_dict)):
        if i>1000 and i%1000==0:
            print('%.6f' % (100*float(i)/float(len(Repeat_dict))) + '%')
    
        REPT = Repeat_dict[i].split(';')[:-1]
        SKYC = []
        for j in range(len(REPT)):
            ra0 = str(float((REPT[j].split(','))[1]))
            dec0 = str(float((REPT[j].split(','))[2]))
            SKYC0 = SkyCoord(ra0, dec0, unit="deg", frame='fk5')
            SKYC.append(SkyCoord(str(float((REPT[j].split(','))[6])), str(float((REPT[j].split(','))[7])), unit = 'deg', frame = 'fk5'))
        
        SEP = []
        for k in range(len(SKYC)):
            SEP.append(SKYC0.separation(SKYC[k]).value)
        ind = SEP.index(max(SEP))
        no_rpt_catalog.append(REPT[ind])
                
    t_end = time.time()
    print('\nEnd of comparing distances between repeated sources ...')
    print('\nDealing with repeated sources in catalog took %.6f secs ...' % (t_end - t_start))
    print('\nNR in new UKIDSS ELAIS N1 catalog: %i' % len(no_rpt_catalog))

    Output = open(str(argv[2])+'_reduction', 'w')
    for i, row in enumerate(no_rpt_catalog):
        if i>1000 and i%1000==0:
            print('%.6f' % (100*float(i)/float(len(no_rpt_catalog))) + '%')
        Output.write(str(row))
    Output.close()
    
    # Save and Reload catalog corrected
    data3 = open(str(argv[1]), 'r')
    data4 = open(str(argv[2])+'_reduction', 'r')
    swire = data3.readlines()
    ukidss = data4.readlines()
    data3.close()
    data4.close()

else:
    swire = two_mass_cat
    ukidss = UK_cat_origin

#==================================================

print('\nStart writing ...\n')
t_start = time.time()

out = []
if len(ukidss) == len(swire):
    
    for i in range(len(swire)):
        row_s = swire[i].split()
        row_u = ukidss[i]
        # Write SWIRE IR1~MP1 magnitude and error 
        mag_list = IRAC_MP1_magnitudelist(row_s)
        err_list = IRAC_MP1_errorlist(row_s)
        mag_list = IRAC_MP1_magnitudelist(row_s)
        err_list = IRAC_MP1_errorlist(row_s)
        row_s[98], row_s[119], row_s[140], row_s[161], row_s[182] = mag_list[0], mag_list[1], mag_list[2], mag_list[3], mag_list[4]
        row_s[99], row_s[120], row_s[141], row_s[162], row_s[183] = err_list[0], err_list[1], err_list[2], err_list[3], err_list[4]

        # Write UKIDSS J,H,K magnitude and error 
        mag_J, mag_H, mag_K = row_u.split(',')[10], row_u.split(',')[12], row_u.split(',')[14]
        err_J, err_H, err_K = row_u.split(',')[11], row_u.split(',')[13], (row_u.split(',')[15]).strip('\n')
        row_s[35], row_s[56], row_s[77] = mag_J, mag_H, mag_K
        row_s[36], row_s[57], row_s[78] = err_J, err_H, err_K
        
        out.append('\t'.join(row_s)+'\n')
        # Percentage Indicator
        if i>1000 and i%1000==0: 
            print('%.6f' % (100*float(i)/float(len(ukidss))) + '%') 

t_end = time.time()
print('\nThis procedure took %.6f secs ...' % (t_end - t_start))

Output = open(str(argv[3]), 'w')
for row in out:
    Output.write(row)
Output.close()

os.system('wc ' + str(argv[3]))
