#!/usr/bin/env python
from __future__ import print_function
import sys
import time
import numpy as np
from numba import jit
from os import system, chdir, path
from sys import argv, exit
from itertools import combinations

if len(argv) != 3:
    exit('\n\tError: Wrong Arguments\
    \n\tExample: [program] [dim] [cube size]\
    \n\t[dim]: dim of magnitude space (for now only "6")\
    \n\t[cube size]: length of multi-d cube in magnitude unit\n')

#=======================================================
# Input
dim      = int(argv[1])       # Dimension of multi-D method
lack_lim = dim - 3 + 1        # Note: start from 0
cube     = float(argv[2])     # Beamsize for each cube
posv_dir = 'GPV_' + str(dim) + 'Dposvec_bin' + str(cube) + '/'
lack_dir = posv_dir + 'Lack_pos_num/'
band_dir = posv_dir + 'Band_pos_num/'

# Check storage directory
if path.isdir(band_dir):
    system('rm -rf ' + band_dir)
    system('mkdir ' + band_dir)
else:
    system('mkdir ' + band_dir)

#=======================================================
# Main Function
def drawProgressBar(percent, barLen = 50):
    '''
    draw progress bar
    '''
    # percent float from 0 to 1.
    sys.stdout.write("\r")
    sys.stdout.write("[{:<{}}] {:.3f}%".format("=" * int(barLen * percent), barLen, (percent * 100)))
    sys.stdout.flush()

@jit(nopython=True)
def sort_band_wo_lack(sort_pos, sort_num):
    comb_pos = []
    comb_num = []
    for j in range(len(sort_pos)):
        sort_pos_j = sort_pos[j]
        comb_pos.append(sort_pos[j])
        comb_num.append(sort_num[j])
    return comb_pos, comb_num

@jit(nopython=True)
def sort_band_wi_lack(sort_pos, sort_num, band_ind):
    '''
    Note: numba not support dtype=int, all is default float
    '''
    # Create no band index list
    no_band_ind = []
    for l in range(dim):
        inlist = 0
        for m in range(len(band_ind)):
            if band_ind[m] == l:
                inlist += 1
        if inlist == 0:
            no_band_ind.append(l)
    # Create reference array (lack is -999.)
    ref = -999 * np.ones(dim)
    for ind in band_ind:
        ref[band_ind] = 0.
    # Start sort by band
    comb_pos = []
    comb_num = []
    for j in range(len(sort_pos)):
        sort_pos_j = sort_pos[j]
        tar = -999 * np.ones(dim)
        for k, bd in enumerate(sort_pos_j):
            if bd != -999:
                tar[k] = 0.
        if np.array_equal(tar, ref):
            comb_pos.append(sort_pos[j])
            comb_num.append(sort_num[j])
    return comb_pos, comb_num

#=======================================================
# Main Program
p_start = time.time()
print("\nStart sorting by band ...")
for i in range(lack_lim):

    # Sort input lack galaxy pos array
    l_start  = time.time()
    lack_pos = np.load(lack_dir + 'Lack_{:d}{:d}{:d}_pos.npy'.format(i, i, i))
    lack_num = np.load(lack_dir + 'Lack_{:d}{:d}{:d}_num.npy'.format(i, i, i))
    lack_pos_t = np.transpose(lack_pos)
    sort_ind = np.lexsort(tuple(lack_pos_t))
    sort_pos = np.array(lack_pos[sort_ind])
    sort_num = np.array(lack_num[sort_ind])
    l_end    = time.time()
    print('\nLoading and sorting LACK{:d} took {:.3f} sec'.format(i, l_end-l_start))

    # Sorting with different combination of lack bands
    for comb in combinations(np.arange(dim), dim-i):
        band_ind = np.array(comb)
        c_start  = time.time()
        # No Lack case
        if i == 0:
            comb_pos, comb_num = sort_band_wo_lack(sort_pos, sort_num)
        # Lack N case
        else:
            comb_pos, comb_num = sort_band_wi_lack(sort_pos, sort_num, band_ind)
        comb_pos_array = np.array(comb_pos)
        comb_num_array = np.array(comb_num)

        # Saving with band indice
        band_out = ''
        for band in band_ind:
            band_out += str(int(band))
        chdir(band_dir)
        np.save('Lack_{:d}_{}_pos'.format(i, band_out), np.array(comb_pos_array))
        np.save('Lack_{:d}_{}_num'.format(i, band_out), np.array(comb_num_array))
        chdir('../../')
        c_end    = time.time()
        print(band_ind, 'took {:.3f} sec'.format(c_end-c_start))

p_end   = time.time()
print('\nWhole sort by band process took {:.3f} sec\n'.format(p_end-p_start))
