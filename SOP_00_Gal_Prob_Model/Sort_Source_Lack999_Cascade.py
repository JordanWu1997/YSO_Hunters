#!/usr/bin/env python
from __future__ import print_function
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

#=======================================================
# Main Function
@jit(nopython=True)
def cascade_array(sort_position, sort_value):
    '''
    Use this to find out sources locate in same position and cascade them
    Note: No tuple() support in numba, No format() support in numba
    '''
    #================================================
    # Input
    after_cascade_pos = []
    after_cascade_value = []
    start = 0
    end   = 0
    for i in range(len(sort_value)-1):
        #================================================
        # Indicator
        #if i % 1000 == 0 and i>999:
        #    print(float(i+1)/len(sort_value))
        #================================================
        # Get reference and target
        tar, ref = sort_position[i], sort_position[i+1]
        end += 1
        #================================================
        # Determine repeated or not
        if not np.all(np.equal(tar, ref)):
            after_cascade_pos.append(sort_position[start])
            after_cascade_value.append(np.sum(sort_value[start:end]))
            start = end
    #================================================
    # Include the last term
    after_cascade_pos.append(sort_position[start])
    after_cascade_value.append(np.sum(sort_value[start:]))
    return after_cascade_pos, after_cascade_value

#=======================================================
# Main Program
p_start = time.time()
print("\nStart Cascading ...\n")
#================================================
# Lack n case
for i in range(lack_lim):
    s_start = time.time()
    all_lack_pos, all_lack_num = [], []
    #================================================
    # Load projected pos & num
    for j in range(i):
        project_pos = np.load(lack_dir + 'Lack_{:d}{:d}_pos.npy'.format(j, i))
        project_num = np.load(lack_dir + 'Lack_{:d}{:d}_num.npy'.format(j, i))
        print('# of pos in Lack_{:d}{:d}_pos.npy: {:d}'.format(j, i, len(project_pos)))
        for k in range(len(project_pos)):
            all_lack_pos.append(project_pos[k])
            all_lack_num.append(project_num[k])
    #================================================
    # Non-projected pos & num
    lack_pos = np.load(lack_dir + 'Lack_{:d}{:d}_pos.npy'.format(i, i))
    lack_num = np.load(lack_dir + 'Lack_{:d}{:d}_num.npy'.format(i, i))
    print('# of pos in Lack_{:d}{:d}_pos.npy: {:d}'.format(i, i, len(lack_pos)))
    for l in range(len(lack_pos)):
        all_lack_pos.append(lack_pos[l])
        all_lack_num.append(lack_num[l])
    #================================================
    # Sort explictly
    all_lack_pos_array = np.array(all_lack_pos)
    all_lack_pos_array_t = np.transpose(all_lack_pos_array)
    all_lack_num_array = np.array(all_lack_num)
    sort_ind = np.lexsort(tuple(all_lack_pos_array_t))
    sort_pos = np.array(all_lack_pos_array[sort_ind], dtype=int)
    sort_num = np.array(all_lack_num_array[sort_ind], dtype=int)
    #================================================
    # Cascade pos & num
    print('\nbefore cascade: {:d}'.format(len(sort_pos)))
    after_cascade_pos, after_cascade_num = cascade_array(sort_pos, sort_num)
    print('after  cascade: {:d}'.format(len(after_cascade_pos)))
    #================================================
    # Save results
    chdir(lack_dir)
    np.save('Lack_{:d}{:d}{:d}_pos'.format(i, i, i), np.array(after_cascade_pos))
    np.save('Lack_{:d}{:d}{:d}_num'.format(i, i, i), np.array(after_cascade_num))
    chdir('../../')
    s_end   = time.time()
    print('Cascade lack {:d} took {:.3f} sec\n'.format(i, s_end-s_start))
p_end   = time.time()
print('Whole cascade process took {:.3f} sec\n'.format(p_end-p_start))
