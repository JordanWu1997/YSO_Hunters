#!/usr/bin/python

import numpy as np
from glob import glob
from time import time
from sys import argv, exit
from os import system, chdir, path

if len(argv) < 8:
    exit('\n\tError: Wrong Arguments\
    \n\tExample: [program] [dim] [cube size] [sigma] [bond] [ref-D] [num_TH] [lack_inp]\
    \n\t[dim]: dimension for smooth (for now only "6")\
    \n\t[cube size]: length of multi-d cube in magnitude unit\
    \n\t[sigma]: standard deviation for gaussian dist. in magnitude\
    \n\t[bond]: boundary radius of gaussian beam unit in cell\
    \n\t[ref-D]: reference dimension which to modulus other dimension to\
    \n\t[num_TH]: number to slice input galaxy position vector dictionary\
    \n\t[lack_inp]: number of lack band of input source dictionary (0 1 2 3)\n')


#==============================================================================================================
# Input variables
dim        = int(argv[1])       # Dimension of position vector
cube       = float(argv[2])     # Beamsize for each cube
sigma      = int(argv[3])       # STD for Gaussian Smooth
bond       = int(argv[4])       # Boundary for Gaussian Smooth
refD       = int(argv[5])       # Reference Beam Dimension
num_th     = int(argv[6])       # Number of threads to use
lack_inp   = [int(inp) for inp in (argv[7:])]    # List of number of lack band of input sources
posv_dir   = 'GPV_{:d}Dposvec_bin{:.1f}/'.format(dim, cube)
inp_dict   = [posv_dir + "Lack_{:d}band_sources.npy".format(lack) for lack in lack_inp]
out_dir    = 'GPV_after_smooth_{:d}D_bin{:.1f}_sigma{:d}_bond{:d}_refD{:d}/'.format(dim, cube, sigma, bond, refD)
sub_dir    = ['tmp_L{:d}/'.format(lack) for lack in lack_inp]

#==============================================================================================================
# Main Program
t_start = time()
for i in range(len(lack_inp)):

    #==============================================
    # Initialize output directory
    if (not path.isdir(out_dir)):
        print("Directory doesn't exist ...")
        print("Create new one ...\n")
        system('mkdir ' + out_dir)
    else:
        print("Directory exists ...")
        print("Use exist one ...\n")
    if (not path.isdir(out_dir + sub_dir[i])):
        print("Sub-Directory doesn't exist ...")
        print("Create new one ...\n")
        system('mkdir ' + out_dir + sub_dir[i])
    else:
        print("Sub-Directory exists ...")
        print("Use exist one ...\n")

    #==============================================
    # Load input dictionary
    ld_dict = np.load(inp_dict[i]).item()
    key_len = len(ld_dict.keys())

    #==============================================
    # Start slicing
    for j in range(num_th):
        chdir(out_dir + sub_dir[i])
        # Set cut ends
        end_cuts = []
        for k in range(num_th+1):
            end_cuts.append(int(key_len*(float(k)/num_th)))
        end_cuts[-1] += 1
        # Store dictionry
        sv_dict = dict()
        for l in range(key_len):
            if (l >= end_cuts[j]) and (l < end_cuts[j+1]):
                sv_dict[ld_dict.keys()[l]] = ld_dict[ld_dict.keys()[l]]
        np.save('{:0>3d}_tmp_cat'.format(j), sv_dict)
        chdir('../../')

#==============================================
# Report time
t_end = time()
print('Whole Process took {:.3f} secs'.format(t_end - t_start))
