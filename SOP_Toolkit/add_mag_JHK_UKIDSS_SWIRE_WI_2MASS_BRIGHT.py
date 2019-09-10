#!/usr/bin/ipython
'''-------------------------------------------------------------------------------------
This program is to write : 
    (1) new UKIDSS J,H,K mag and error
    (2) old SWIRE IR1,IR2,IR3,IR4,MP1 mag and error                        
    to an old SWIRE catalog (for ELAIS N1)

Input :
    (1)SWIRE catalog to be replaced
    (2)UKIDSS catalog to replace (WITHOUT HEADERS !!)
    (3)Output catalog filename

Output: 
    New catalog with 
        (1)UKIDSS J, H, K band magnitude and error
        (2)SWIRE IR1,IR2,IR3,IR4,MP1 band magnitude and error

*NOTE: 
    ***
    Since UKIDSS catalog has a saturate issue, we use new UKIDSS data with condition:
       (1) Replace UKIDSS data ONLY with J band magnitude larger than 11.5 mag
       (2) For UKIDSS data with J band magnitude smaller than 11.5 mag, reject to replace
           with UKIDSS data. However, 2MASS data still have to do calibration to UKIDSS format
    ***
    
    1. Empty columns on SWIRE format catalog for storing UKIDSS magnitude and error
       (1) magnitude: J[35], H[56], K[77]
       (2) mag_err: J[36], H[57], K[78]
    
    2. Empty columns on SWIRE format catalog for storing SWIRE mag and error
       (1) magnitude: IR1[102], IR2[123], IR3[144], IR4[165], MP1[186]
       (2) mag_err: IR1[103], IR2[124], IR3[145], IR4[166], MP1[187]
    
    3. If a band is undetected, the magnitude and error will be assigned as '0.0'

    4. If a 2MASS object is found more than one source in UKIDSS catalog,
       distance to the original RADEC on SWIRE catalog will be calculated, 
       and the nearest one will be selected.
---------------------------------------------------------------------------------------
latest update : 2019/03/30 Jordan Wu'''

from sys import argv, exit
from astropy.coordinates import SkyCoord
import numpy as np
import math as mh
import time
import os

if len(argv) != 5:
    exit('\n\tWrong Input Argument!\
        \n\tExample: python [program] [Swire] [UKIDSS] [HEADER_LENGTH] [output file name]\
        \n\tNote: Replace [Swire] J,H,K with [UKIDSS]\n')
else:
    print('\nStart input check ...')

# For transformation of old 2MASS data to new UKIDSS format
#=====================================================================
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
    return str(mag_Jw), str(mag_Hw), str(mag_Kw)
#=====================================================================

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
    '''
    This function is to change fluxes on the catalog to magnitudes
    '''
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

data1 = open(str(argv[1]), 'r')
two_mass_cat = data1.readlines()
data1.close()

HEADER_LEN = int(argv[3])
data2 = open(str(argv[2]), 'r')
UK_cat_origin = data2.readlines()[HEADER_LEN:]
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
    print('End of finding repeated sources ...\n')
    
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
        row_s[98], row_s[119], row_s[140], row_s[161], row_s[182] = mag_list[0], mag_list[1], mag_list[2], mag_list[3], mag_list[4]
        row_s[99], row_s[120], row_s[141], row_s[162], row_s[183] = err_list[0], err_list[1], err_list[2], err_list[3], err_list[4]
        
        # Write UKIDSS J,H,K magnitude and error 
        UKIDSS_mag = row_u.split(',')[10], row_u.split(',')[12], row_u.split(',')[14]
        UKIDSS_err = row_u.split(',')[11], row_u.split(',')[13], (row_u.split(',')[15]).strip('\n')
        mag_J, mag_H, mag_K = UKIDSS_mag[0], UKIDSS_mag[1], UKIDSS_mag[2]
        err_J, err_H, err_K = UKIDSS_err[0], UKIDSS_err[1], UKIDSS_err[2]
        
        #=================================================
        # Only Pick Up Faint Sources In UKIDSS Observation
        # Mag of Non-detected Band will be assigned as 0.0
        #=================================================
        if float(mag_J) >= 11.5:
            row_s[35], row_s[56], row_s[77] = mag_J, mag_H, mag_K
            row_s[36], row_s[57], row_s[78] = err_J, err_H, err_K
        else:
            row_s[35], row_s[56], row_s[77] = JHK_flux_to_mag(row_s[33], row_s[54], row_s[75])
        
        out.append('\t'.join(row_s)+'\n')
        if i>1000 and i%1000==0: 
            print('%.6f' % (100*float(i)/float(len(ukidss))) + '%') 
else:
    print('wrong catalog line number')
    print('SWIRE NR: %i' % len(swire)) 
    print('UKIDSS NR: %i' % len(ukidss))

t_end = time.time()
print('\nThis procedure took %.6f secs ...' % (t_end - t_start))

Output = open(str(argv[4]), 'w')
for row in out:
    Output.write(row)
Output.close()
os.system('wc ' + str(argv[4]))
