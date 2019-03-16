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
latest update : 2019/03/16 Jordan Wu'''

from sys import argv, exit
import numpy as np
import time

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

data1 = open(str(argv[1]), 'r')
two_mass_cat = data1.readlines()
data1.close()

data2 = open(str(argv[2]), 'r')
UK_cat_origin = data2.readlines()[14:]
data2.close()

# Input file check for repeating sources
#==================================================
if len(two_mass_cat) < len(UK_cat_origin):
    t_start = time.time()
    UK_cat = [UK_cat_origin[0]]
    for i in range(len(UK_cat_origin)-1):
        col_1 = UK_cat_origin[i].split()
        col_2 = UK_cat_origin[i+1].split()
        UK_cat.append(UK_cat_origin[i+1])
        if col_1[1] == col_2[1]:
            UK_cat.remove(UK_cat_origin[i])
    t_end = time.time()
    print('\nDealing with repeated sources in catalog took %.6f secs ...' % (t_end - t_start))
    print('\nNR in new UKIDSS ELAIS N1 catalog: %i' % len(UK_cat))

    Output = open(str(argv[2])+'_reduction', 'w')
    for row in UK_cat:
        Output.write(str(row))
    Output.close()
    
    # Save and Reload catalog corrected
    data1 = open(str(argv[1]), 'r')
    data2 = open(str(argv[2])+'_reduction', 'r')
    swire = np.array(data1.readlines())
    ukidss = np.array(data2.readlines())
    data1.close(); data2.close();

else:
    swire = np.array(two_mass_cat)
    ukidss = np.array(UK_cat_origin)
#==================================================

print('\nStart writing ...\n')
t_start = time.time()
swire_ra = []
for row in swire:
    swire_ra.append(row.split()[0])
swire_ra = np.array(swire_ra)

for i in range(len(ukidss)):
    row_u = ukidss[i]
    ra = row_u.split()[1]
    ra = ra.strip(',')
    ra = ra.strip('+')
    
    mag_J = row_u.split()[10].strip(',')
    mag_H = row_u.split()[12].strip(',')
    mag_K = row_u.split()[14].strip(',')
    err_J = row_u.split()[11].strip(',')
    err_H = row_u.split()[13].strip(',')
    err_K = row_u.split()[15].strip(',')
    
    # Write UKIDSS J,H,K magnitude and error
    index = int(np.where(swire_ra == ra)[0][0])
    row = swire[index]
    row_s = row.split()
    row_s[35] = mag_J
    row_s[56] = mag_H
    row_s[77] = mag_K
    row_s[36] = err_J 
    row_s[57] = err_H
    row_s[78] = err_K
    swire[index] = '\t'.join(row_s)
    
    # Write SWIRE IR1~MP1 magnitude and error
    mag_list = IRAC_MP1_magnitudelist(row_s)
    err_list = IRAC_MP1_errorlist(row_s)
   
    #df_list = [x[97], x[118], x[139], x[160], x[181]]
    row_s[98] = str(mag_list[0])
    row_s[119] = str(mag_list[1])
    row_s[140] = str(mag_list[2])
    row_s[161] = str(mag_list[3])
    row_s[182] = str(mag_list[4])

    row_s[99] = str(err_list[0])
    row_s[120] = str(err_list[1])
    row_s[141] = str(err_list[2])
    row_s[162] = str(err_list[3])
    row_s[183] = str(err_list[4])
    
    swire[index] = '\t'.join(row_s)
    # Percentage Indicator
    if i>100 and i%100==0: 
        print('%.6f' % (100*float(i)/float(len(ukidss))) + '%') 

t_end = time.time()
print('\nThis procedure took %.6f secs ...' % (t_end - t_start))

Output = open(str(argv[3]), 'w')
for row in swire:
    Output.write(row + '\n')
Output.close()
