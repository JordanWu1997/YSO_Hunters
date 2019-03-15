#!/usr/bin/ipython
'''-------------------------------------------------------------------------------------
This program is to replace old 2MASS J,H,K mag with new UKIDSS Jw, Hw, Kw mag
Input : (1)SWIRE catalog to be replaced
        (2)UKIDSS catalog to replace
        (3)Output catalog filename

Output: (1)New catalog with UKIDSS J, H, K band magnitude and error

*NOTE: 
    1. empty column on SWIRE format catalog for storing magnitude
       (1) magnitude: J[35] H[56] K[77]
       (2) mag_err: J[36], H[57], K[78]
    2. if a 2MASS object is found more than one source in UKIDSS catalog,
       only the last source in catalog will take into consideration.
---------------------------------------------------------------------------------------
latest update : 2019/03/15 Jordan Wu'''

from sys import argv, exit
import numpy as np
import time

if len(argv) != 4:
    exit('Wrong Input Argument!\
        \nExample: python [program] [Swire] [UKIDSS] [output file name]\
        \nNote: Replace [Swire] J,H,K with [UKIDSS]')
else:
    print('Start ...')

data1 = open(str(argv[1]), 'r')
two_mass_cat = data1.readlines()
data1.close()

data2 = open(str(argv[2]), 'r')
UK_cat_origin = data2.readlines()[14:]
data2.close()

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
    print('Dealing with repeated sources in catalog took %.6f secs ...' % (t_end - t_start))
    print('NR in new UKIDSS ELAIS N1 catalog: %i' % len(UK_cat))
    
    Output = open(str(argv[2])+'reduction', 'w')
    for row in UK_cat:
        Output.write(str(row))
    Output.close()
else:
    UK_cat = UK_cat_origin

'''
t_start = time.time()
Out_catalog = []
for i in range(len(two_mass_cat)):
    col1 = two_mass_cat[i].split()
    for j in range(len(UK_cat)):
        col2 = UK_cat[j].split()     
        if round(float(col1[0]), 6) == round(float(col2[1].strip(',')), 6):
            # Magnitude: J, H, K 
            col1[35], col1[56], col1[77] = col2[10].strip(','), col2[12].strip(','), col2[14].strip(',')
            # Mag Error: J, H, K
            col1[36], col1[57], col1[78] = col2[11].strip(','), col2[13].strip(','), col2[15].strip(',')
            new_row = '\t'.join(col1)
            Out_catalog.append(str(new_row))
    if (i>=100) and (i%100 == 0):
        print('%.6f' % (float(i*100)/float(len(two_mass_cat))) + '%')
t_end = time.time()
print('Replace procedure took %.6f secs ...' % (t_end - t_start))

Output = open(str(argv[3]), 'w')
for row in Out_catalog:
    Output.write(row + '\n')
Output.close()
'''
