#!/usr/bin/python
# Slice
# \n\tExample: [program] [dim] [cube size] [sigma] [bond] [ref-D] [num_TH] [lack_inp]\
# Gaussian Smooth
# \n\tExample: [program] [dim] [cube size] [sigma] [bond] [ref-D] [lack] [index]\

import numpy as np
from sys import argv, exit
from os import system, chdir
from glob import glob
from time import time

if len(argv) < 7:
    exit('\n\tError: Wrong Arguments\
    \n\tExample: [program] [dim] [cube size] [sigma] [bond] [ref-D] [lack_inp]\
    \n\t[dim]: dimension for smooth (for now only "6")\
    \n\t[cube size]: length of multi-d cube in magnitude unit\
    \n\t[sigma]: standard deviation for gaussian dist. in magnitude\
    \n\t[bond]: boundary radius of gaussian beam unit in cell\
    \n\t[ref-D]: reference dimension which to modulus other dimension to\
    \n\t[lack_inp]: number of lack band of input source dictionary (0 1 2 3)\n')

dim      = int(argv[1])
cube     = float(argv[2])
sigma    = int(argv[3])
bond     = int(argv[4])
refD     = int(argv[5])
lack_inp = [int(inp) for inp in (argv[6:])]    # List of number of lack band of input sources
out_dir  = 'GPV_after_smooth_{:d}D_bin{:.1f}_sigma{:d}_bond{:d}_refD{:d}/'.format(dim, cube, sigma, bond, refD)
sub_dir  = ['tmp_L{:d}/'.format(lack) for lack in lack_inp]


for i, sub in enumerate(sub_dir):
    print('\n' + sub)
    chdir(out_dir + sub)
    pieces = sorted(glob('*_{:d}d_after_smooth.npy'.format(dim-lack_inp[i])))
    out_dict = dict()
    for j, piece in enumerate(pieces):
        print('Now {:d}_dir, {:d}/{:d}'.format(i, j, len(pieces)))
        ld_dict = np.load(piece).item()
        for key in ld_dict.keys():
            if key not in out_dict.keys():
                out_dict.update({key: ld_dict[key]})
            else:
                out_dict[key] += ld_dict[key]
    chdir('../')
    np.save('{:d}d_after_smooth'.format(dim-lack_inp[i]), out_dict)
    chdir('../')
