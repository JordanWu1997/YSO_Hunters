#!/usr/bin/python
from __future__ import print_function
import numpy as np
from sys import argv, exit
from os import system, path, chdir
from numba import jit
import time

'''
# Sort_Source_Lack999_Slice.py (SLICE)
# [program] [dim] [cube size] [sl_num]

# Do_Gaussian_Smooth_Slice_Index.py (INDEX)
# [program] [dim] [cube size] [sigma] [bond] [ref-D] [lack] [band_inp] [slice_num] [slice_ind]

# Do_Gaussian_Smooth_Slice_Cascade.py (CASCADE)
# [program] [dim] [cube size] [sigma] [bond] [ref-D] [lack] [band_inp] [band_ind_1] [band_ind_2]
'''

#================================================
# Check Inputs
if len(argv) != 9 :
    exit('\n\tError: Wrong Arguments\
    \n\tExample: [program] [dim] [cube size] [sigma] [bond] [ref-D] [lack] [band_inp] [slice_num]\
    \n\t[dim]: dimension for smooth (for now only "6")\
    \n\t[cube size]: length of multi-d cube in magnitude unit\
    \n\t[sigma]: standard deviation for gaussian dist. in magnitude\
    \n\t[bond]: boundary radius of gaussian beam unit in cell\
    \n\t[ref-D]: reference dimension which to modulus other dimension to\
    \n\t[lack]: number of lack bands\
    \n\t[band_inp]: band used to do smooth in string e.g. 012345\
    \n\t[slice_num]: number of slices of the input catalog\n')

#================================================
# Inputs
dim         = int(argv[1])       # Dimension of position vector
cube        = float(argv[2])     # Beamsize for each cube
sigma       = int(argv[3])       # STD for Gaussian Smooth
bond        = int(argv[4])
refD        = int(argv[5])       # Reference Beam Dimension
lack        = int(argv[6])
band_inp    = str(argv[7])
slice_num   = int(argv[8])
slice_ind_list = [i for i in range(slice_num)]

# Directory
posv_dir = 'GPV_{:d}Dposvec_bin{:.1f}/'.format(dim, cube)
band_dir = posv_dir + 'Band_pos_num/'
slic_dir = band_dir + 'Slice_{}_{:0>3d}/'.format(band_inp, slice_num)
out_dir  = 'GPV_after_smooth_{:d}D_bin{:.1f}_sigma{:d}_bond{:d}_refD{:d}/'.format(dim, cube, sigma, bond, refD)
temp_dir = out_dir  + 'After_{}/'.format(band_inp)

# Check storage directory
if not path.isdir(out_dir):
    system('mkdir ' + out_dir)
if not path.isdir(temp_dir):
    system('mkdir ' + temp_dir)

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

#================================================
# Main Programs
s_start = time.time()
system('Sort_Source_Lack999_Slice.py {:d} {:.1f} {:d}'.format(dim, cube, slice_num))
system('Do_Gaussian_Smooth_Slice_Index.py {:d} {:.1f} {:d} {:d} {:d} {:d} {} {:d} {:d}'.format(dim, cube, sigma, bond, refD, lack, band_inp, slice_num, 0))

# smooth -> cascade -> smooth -> cascade ...
pos = np.load(temp_dir + "after_{}_{:0>3d}_pos.npy".format(band_inp, slice_ind_list[0]))
num = np.load(temp_dir + "after_{}_{:0>3d}_num.npy".format(band_inp, slice_ind_list[0]))

print(0)
for i in range(1, slice_num):
    print(i)
    system('Do_Gaussian_Smooth_Slice_Index.py {:d} {:.1f} {:d} {:d} {:d} {:d} {} {:d} {:d}'.format(dim, cube, sigma, bond, refD, lack, band_inp, slice_num, i))
    new_pos  = np.load(temp_dir + "after_{}_{:0>3d}_pos.npy".format(band_inp, slice_ind_list[i]))
    new_num  = np.load(temp_dir + "after_{}_{:0>3d}_num.npy".format(band_inp, slice_ind_list[i]))
    join_pos = np.concatenate((pos, new_pos), axis=0)
    join_num = np.concatenate((num, new_num), axis=0)
    cas_pos, cas_num = cascade_array(join_pos, join_num)
    pos, num = np.array(cas_pos), np.array(cas_num)

chdir(out_dir)
np.save("Lack_{:d}_{}_all_cas_pos".format(lack, band_inp), pos)
np.save("Lack_{:d}_{}_all_cas_num".format(lack, band_inp), num)
chdir('../')
s_end   = time.time()
print('\nWhole took {:.3f} sec'.format(s_end-s_start))
