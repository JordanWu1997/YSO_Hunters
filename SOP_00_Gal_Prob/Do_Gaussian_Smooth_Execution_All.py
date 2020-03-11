#!/usr/bin/python
from __future__ import print_function
import time
import numpy as np
from sys import argv, exit
from os import system, path, chdir
from numba import jit
from itertools import combinations
from Useful_Functions import *

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
if len(argv) != 8:
    exit('\n\tError: Wrong Arguments\
    \n\tExample: [program] [dim] [cube size] [sigma] [bond] [ref-D] [slice_num] [one_by_one]\
    \n\t[dim]: dimension for smooth (for now only "6")\
    \n\t[cube size]: length of multi-d cube in magnitude unit\
    \n\t[sigma]: standard deviation for gaussian dist. in magnitude\
    \n\t[bond]: boundary radius of gaussian beam unit in cell\
    \n\t[ref-D]: reference dimension which to modulus other dimension to\
    \n\t[slice_num]: number of slices of the input catalog\
    \n\t[one_by_one]: smooth then cascade one by one or not ("yes"/"no") \n')

#================================================
# Inputs
dim         = int(argv[1])       # Dimension of position vector
cube        = float(argv[2])     # Beamsize for each cube
sigma       = int(argv[3])       # STD for Gaussian Smooth
bond        = int(argv[4])
refD        = int(argv[5])       # Reference Beam Dimension
slice_num   = int(argv[6])
one_by_one  = str(argv[7])       # Smooth then cascade one by one or not

slice_ind_list = [i for i in range(slice_num)]
lack_lim    = dim - 3 + 1

# Directory
posv_dir = 'GPV_{:d}Dposvec_bin{:.1f}/'.format(dim, cube)
band_dir = posv_dir + 'Band_pos_num/'
out_dir  = 'GPV_after_smooth_{:d}D_bin{:.1f}_sigma{:d}_bond{:d}_refD{:d}/'.format(dim, cube, sigma, bond, refD)

# Band directory list
lack_inp_list = []
band_inp_list = []
temp_dir_list = []
slic_dir_list = []
for i in range(lack_lim):
    for comb in combinations(np.arange(dim), dim-i):
        band_list = list(comb)
        band_index = ''
        for band in band_list:
            band_index += str(int(band))
        temp_dir = out_dir  + 'After_Smooth_{}/'.format(band_index)
        slic_dir = band_dir + 'Slice_{}_{:0>3d}/'.format(band_index, slice_num)
        lack_inp_list.append(i)
        band_inp_list.append(band_index)
        temp_dir_list.append(temp_dir)
        slic_dir_list.append(slic_dir)

# Check storage directory
if not path.isdir(out_dir):
    system('mkdir ' + out_dir)
for i in range(len(temp_dir)):
    if not path.isdir(temp_dir):
        system('mkdir ' + temp_dir)

#================================================
# Main Programs
m_start = time.time()
for i in range(len(band_inp_list)):

    #================================================
    # Slice input galaxy pos/num array
    if not path.isdir(slic_dir_list[i]):
        s_start = time.time()
        system('\nDo_Gaussian_Smooth_Slice.py {:d} {:.1f} {:d}'.format(dim, cube, slice_num))
        s_end   = time.time()
        print('\nSlice {} took {:.3f} sec'.format(band_inp_list[i], s_end-s_start))
    else:
        print('\n{} already been sliced, use existed one'.format(band_inp_list[i]))

    #================================================
    # One by one smooth then cascade
    b_start = time.time()
    if one_by_one == 'yes': # smooth -> cascade -> smooth -> cascade ...
        system('Do_Gaussian_Smooth_Slice_Index.py {:d} {:.1f} {:d} {:d} {:d} {:d} {} {:d} {:d}'.format(\
                dim, cube, sigma, bond, refD, lack_inp_list[i], band_inp_list[i], slice_num, 0))
        pos = np.load(temp_dir_list[i] + "after_smooth_{}_{:0>3d}_pos.npy".format(band_inp_list[i], slice_ind_list[0]))
        num = np.load(temp_dir_list[i] + "after_smooth_{}_{:0>3d}_num.npy".format(band_inp_list[i], slice_ind_list[0]))
        for j in range(1, slice_num):
            system('Do_Gaussian_Smooth_Slice_Index.py {:d} {:.1f} {:d} {:d} {:d} {:d} {} {:d} {:d}'.format(\
                dim, cube, sigma, bond, refD, lack_inp_list[i], band_inp_list[i], slice_num, j))
            new_pos  = np.load(temp_dir_list[i] + "after_smooth_{}_{:0>3d}_pos.npy".format(band_inp_list[i], slice_ind_list[j]))
            new_num  = np.load(temp_dir_list[i] + "after_smooth_{}_{:0>3d}_num.npy".format(band_inp_list[i], slice_ind_list[j]))
            join_pos = np.concatenate((pos, new_pos), axis=0)
            join_num = np.concatenate((num, new_num), axis=0)
            cas_pos, cas_num = cascade_array(join_pos, join_num)
            pos, num = np.array(cas_pos), np.array(cas_num)
            drawProgressBar(float(j+1)/slice_num)
    # Cascade all in one time
    elif one_by_one == 'no':
        for j in range(slice_num):
            system('Do_Gaussian_Smooth_Slice_Index.py {:d} {:.1f} {:d} {:d} {:d} {:d} {} {:d} {:d}'.format(\
                dim, cube, sigma, bond, refD, lack_inp_list[i], band_inp_list[i], slice_num, j))
        for j in range(slice_num):
            new_pos  = np.load(temp_dir_list[i] + "after_smooth_{}_{:0>3d}_pos.npy".format(band_inp_list[i], slice_ind_list[j]))
            new_num  = np.load(temp_dir_list[i] + "after_smooth_{}_{:0>3d}_num.npy".format(band_inp_list[i], slice_ind_list[j]))
            join_pos = np.concatenate((pos, new_pos), axis=0)
            join_num = np.concatenate((num, new_num), axis=0)
        cas_pos, cas_num = cascade_array(join_pos, join_num)
        pos, num = np.array(cas_pos), np.array(cas_num)

    #================================================
    # Save all band result
    chdir(out_dir)
    np.save("after_smooth_lack_{:d}_{}_all_cas_pos".format(lack_inp_list[i], band_inp_list[i]), pos)
    np.save("after_smooth_lack_{:d}_{}_all_cas_num".format(lack_inp_list[i], band_inp_list[i]), num)
    chdir('../')
    b_end   = time.time()
    print('\n{} took {:.3f} sec'.format(band_inp_list[i], b_end-b_start))
m_end   = time.time()
print('\nAll band gaussian smooth took {:.3f} sec'.format(m_end-m_start))
