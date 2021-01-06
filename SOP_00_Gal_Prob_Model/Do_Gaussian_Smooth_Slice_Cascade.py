#!/usr/bin/env python
from __future__ import print_function
import sys
import time
import numpy as np
from sys import argv, exit
from os import chdir, path, system
from numba import jit

#=========================================================================================
# Input variables
if len(argv) < 10:
    exit('\n\tError: Wrong Arguments\
    \n\tExample: [program] [dim] [cube size] [sigma] [bond] [ref-D] [lack] [band_inp] [band_ind_1] [band_ind_2] [...]\
    \n\t[dim]: dimension for smooth (for now only "6")\
    \n\t[cube size]: length of multi-d cube in magnitude unit\
    \n\t[sigma]: standard deviation for gaussian dist. in magnitude\
    \n\t[bond]: boundary radius of gaussian beam unit in cell\
    \n\t[ref-D]: reference dimension which to modulus other dimension to\
    \n\t[lack]: number of lack bands\
    \n\t[band_inp]: band used to do smooth in string e.g. 012345\
    \n\t[slice_num]: number of slices of the input catalog\
    \n\t[slice_ind(s)]: indice of slices after smooth to cascade (or "all") \n')

dim         = int(argv[1])       # Dimension of position vector
cube        = float(argv[2])     # Beamsize for each cube
sigma       = int(argv[3])       # STD for Gaussian Smooth
bond        = int(argv[4])
refD        = int(argv[5])       # Reference Beam Dimension
lack        = int(argv[6])
band_inp    = str(argv[7])
slice_num   = int(argv[8])

# Generate slice index list
slice_ind_list  = []
if str(argv[9]) != 'all':
    slice_ind_list = [int(i) for i in argv[9:]]
else:
    slice_ind_list = [i for i in range(slice_num)]

# Directory
posv_dir = 'GPV_{:d}Dposvec_bin{:.1f}/'.format(dim, cube)
band_dir = posv_dir + 'Band_pos_num/'
slic_dir = band_dir + 'Slice_{}_{:0>3d}/'.format(band_inp, slice_num)
out_dir  = 'GPV_after_smooth_{:d}D_bin{:.1f}_sigma{:d}_bond{:d}_refD{:d}/'.format(dim, cube, sigma, bond, refD)
temp_dir = out_dir  + 'After_Smooth_{}/'.format(band_inp)

#================================================
# Main Functions
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

#=========================================================================================
# Load Position/Probability array
l_start = time.time()
pos_list, num_list = [], []
for i in range(len(slice_ind_list)):
    pos = np.load(temp_dir + "after_smooth_{}_{:0>3d}_pos.npy".format(band_inp, slice_ind_list[i]))
    num = np.load(temp_dir + "after_smooth_{}_{:0>3d}_num.npy".format(band_inp, slice_ind_list[i]))
    pos_list.extend(pos)
    num_list.extend(num)

pos_array = np.array(pos_list)
num_array = np.array(num_list)
position_t = np.transpose(pos_array)
#================================================
# Sort Input Galaxy Position/Probability array
sort_ind = np.lexsort(tuple(position_t))
sort_pos = np.array(pos_array[sort_ind], dtype=int)
sort_num = np.array(num_array[sort_ind], dtype=float)
#================================================
# Cascade Repeated Position
after_cascade_pos, after_cascade_num = cascade_array(sort_pos, sort_num)
after_cascade_pos_array = np.array(after_cascade_pos)
after_cascade_num_array = np.array(after_cascade_num)
#================================================
# Save result
chdir(temp_dir)
np.save("after_smooth_cas_{}_{:0>3d}_{:0>3d}_pos".format(\
        band_inp, slice_ind_list[0], slice_ind_list[-1]), after_cascade_pos_array)
np.save("after_smooth_cas_{}_{:0>3d}_{:0>3d}_num".format(\
        band_inp, slice_ind_list[0], slice_ind_list[-1]), after_cascade_num_array)
chdir('../../')
