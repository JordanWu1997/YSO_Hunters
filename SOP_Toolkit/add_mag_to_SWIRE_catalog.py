#!/usr/bin/ipython
from sys import argv
import numpy as np
import math as mh
import os

# J,H,K,IR1,IR2.IR3,IR4.MP1 on c2d catalog
def c2d_errorlist(x):
    F0_list = [1594000.0, 1024000.0, 666700.0, 280900.0, 179700.0, 115000.0, 64130.0, 7140.0]
    df_list = [x[34], x[55], x[76], x[97], x[118], x[139], x[160], x[181]]
    dm_list = []
    for i in range(len(F0_list)):
        if df_list[i] > 0.0:
            dm = (float(df_list[i])/F0_list[i]) * 2.5 * mh.log10(mh.e)
        else:
            dm = 0.0
        dm_list.append(str(dm))
    return dm_list

def c2d_magnitudelist(x):
    '''
    This function is to change fluxes on the catalog to magnitudes
    '''
    F0_list = [1594000.0, 1024000.0, 666700.0, 280900.0, 179700.0, 115000.0, 64130.0, 7140.0]
    flux_list = [x[33], x[54], x[75], x[96], x[117], x[138], x[159], x[180]]
    mag_list = []
    for i in range(len(F0_list)):
        if float(flux_list[i]) > 0.0:
            mag = -2.5 * mh.log10(float(flux_list[i])/F0_list[i])
        else:
            mag = 0.0
        mag_list.append(str(mag))
    return mag_list

in_cat = open(str(argv[1]), 'r')
ou_cat = open(str(argv[2]), 'w')
cat = in_cat.readlines()
in_cat.close()

out = []
for i in range(len(cat)):
    # Percentage Indicator
    if i>1000 and i%1000==0:
        print('%.6f' % (100*float(i)/float(len(cat))) + '%')    
    row = cat[i].split()
    mag_list = c2d_magnitudelist(row)
    err_list = c2d_errorlist(row)
    row[35], row[56], row[77], row[98], row[119], row[140], row[161], row[182] = mag_list[0], mag_list[1], mag_list[2], mag_list[3], mag_list[4], mag_list[5], mag_list[6], mag_list[7]
    row[36], row[57], row[78], row[99], row[120], row[141], row[162], row[183] = err_list[0], err_list[1], err_list[2], err_list[3], err_list[4], err_list[5], err_list[6], err_list[7]
    out.append('\t'.join(row)+'\n')
    
for row in out:
    ou_cat.write(row)
ou_cat.close()
os.system('wc ' + str(argv[2]))
