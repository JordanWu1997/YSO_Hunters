#!/usr/bin/python
'''
------------------------------------------------------------------------------------------------------------
Example: [program] [dim] [cube size] [sigma] [bond] [ref-D]
    Input Variables:
    [dim]:       dimension for smooth (for now only "6")\
    [cube size]: length of multi-d cube in magnitude unit\
    [sigma]:     standard deviation for gaussian dist. in magnitude\
    [bond]:      boundary radius of gaussian beam unit in cell\
    [ref-D]:     reference dimension which to modulus other dimension to\n')

Caution: This program must be run under PYTHON 2
         Otherwise, numpy dictionary array loading will go wrong ...
------------------------------------------------------------------------------------------------------------
Latest Updated: 2020.07.14 Jordan Wu'''

# Import Modules
#==========================================================
from __future__ import print_function
from sys import argv, exit
from All_Variables import *
from Useful_Functions import *
from Hsieh_Functions import *
import numpy as np
import time
import glob

# Functions
#==========================================================

# Main Program
#==========================================================
if __name__ == '__main__':
    s_start = time.time()

    # Check inputs
    if len(argv) != 6:
        exit('\n\tError: Wrong Arguments\
        \n\tExample: [program] [dim] [cube size] [sigma] [bond] [ref-D]\
        \n\t[dim]: dimension for smooth (for now only "6")\
        \n\t[cube size]: length of multi-d cube in magnitude unit\
        \n\t[sigma]: standard deviation for gaussian dist. in magnitude\
        \n\t[bond]: boundary radius of gaussian beam unit in cell\
        \n\t[ref-D]: reference dimension which to modulus other dimension to\n')

    # Input variables
    dim         = int(argv[1])       # Dimension of position vector
    cube        = float(argv[2])     # Beamsize for each cube
    sigma       = int(argv[3])       # STD for Gaussian Smooth
    bond        = int(argv[4])       # Bond for Gaussian Smooth
    refD        = int(argv[5])       # Reference Beam Dimension
    out_prefix  = 'GPV_after_smooth_{:d}D_bin{:.1f}_sigma{:d}_bond{:d}_refD{:d}'.format(dim, cube, sigma, bond, refD)
    out_dir     = '{}/'.format(out_prefix)

    # Update dictionary for different lack band number
    for lack in range(dim-3+1):
        print('\nCombining Lack {:d} sources pos/num...'.format(lack))

        # Generate different lack list
        lack_pos_ls = sorted(glob.glob('{}/after_smooth_lack_{:d}_*_all_cas_pos.npy'.format(out_prefix, lack)))
        lack_num_ls = sorted(glob.glob('{}/after_smooth_lack_{:d}_*_all_cas_num.npy'.format(out_prefix, lack)))
        lack_pos_arr_ls = [np.load(lack_pos) for lack_pos in lack_pos_ls]
        lack_num_arr_ls = [np.load(lack_num) for lack_num in lack_num_ls]
        print('\n'.join(lack_pos_ls))
        print('\n'.join(lack_num_ls))

        # Combined different lack list into one
        comb_num, tot_num = 0, sum([len(lack_num_arr) for lack_num_arr in lack_num_arr_ls])
        lack_pos_list, lack_num_list = [], []
        for i in range(len(lack_num_arr_ls)):
            lack_pos_arr = lack_pos_arr_ls[i]
            lack_num_arr = lack_num_arr_ls[i]
            for j in range(len(lack_num_arr)):
                lack_pos = lack_pos_arr[j]
                lack_num = lack_num_arr[j]
                lack_pos_list.append(lack_pos)
                lack_num_list.append(lack_num)
                comb_num += 1
                drawProgressBar(float(comb_num) / tot_num)

        # Save output dictionary (key in tuple)
        print('\n\nSaving Lack {:d} sources dictionary'.format(lack))
        out_dict = dict()
        for i in range(len(lack_num_list)):
            out = {tuple(lack_pos_list[i]): float(lack_num_list[i])}
            out_dict.update(out)
        np.save('{}all_detect_grid_Full_{:d}d.npy'.format(out_dir, dim-lack), out_dict)
        print('{}all_detect_grid_Full_{:d}d.npy'.format(out_dir, dim-lack))

    # Print out result ...
    s_end   = time.time()
    print('\nUpdate Galaxy Probability Dictionary For all Lack Bands took {:.3f} secs\n'.format(s_end-s_start))
