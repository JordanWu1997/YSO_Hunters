#!/usr/bin/ipython
'''------------------------------------------------------------------------------------
This program is to replace new 2MASS J,H,K mag with UKIDSS Jw, Hw, Kw mag

Input : (1)SWIRE catalog to be replaced
        (2)UKIDSS catalog to replace
        (3)Output catalog filename

Output: (1)New catalog with UKIDSS J, H, K band magnitude and error

*NOTE: 
    1. empty column on SWIRE format catalog for storing magnitude
       (1) magnitude: J[35] H[56] K[77]
       (2) mag_err: J[36], H[57], K[78]
---------------------------------------------------------------------------------------
latest update : 2019/03/14 Jordan Wu'''

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
two_mass_cat = data1.readlines()[14:]
data1.close()

data2 = open(str(argv[2]), 'r')
UK_cat = data2.readlines()[14:]
data2.close()

t_start = time.time()
Out_catalog = []
for i in len(two_mass_cat):
    col1 = two_mass_cat[i].split()
    col2 = UK_cat[i].split()    
    # Magnitude
    col1[35], col1[56], col1[77] = col2[10].strip(','), col2[12].strip(','), col2[14].strip(',')
    # Mag Error
    col1[36], col1[57], col1[78] = col2[11].strip(','), col2[13].strip(','), col2[15].strip(',')

    new_row = '\t'.join(col1)
    Out_catalog.append(str(new_row))
    print(('%f.6' % (i/len(two_mass_cat)*100)) + '%')

t_end = time.time()
print('Replace procedure took %.6f ...' % (t_start - t_end))
print('Source position are not reliable %i' % NUM)

Output = open(str(argv[3]), 'w')
for row in Out_catalog:
    Output.write(row + '\n')
Output.close()
