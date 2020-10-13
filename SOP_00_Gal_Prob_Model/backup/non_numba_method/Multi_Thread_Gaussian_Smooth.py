#!/usr/bin/python

# Slice
# \n\tExample: [program] [dim] [cube size] [sigma] [bond] [ref-D] [num_TH] [lack_inp]\
# Gaussian Smooth
# \n\tExample: [program] [dim] [cube size] [sigma] [bond] [ref-D] [lack] [index]\

from sys import argv, exit
from os import system
from time import time

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

#======================================
# Input Variables
dim      = int(argv[1])
cube     = float(argv[2])
sigma    = int(argv[3])
bond     = int(argv[4])
refD     = int(argv[5])
num_th   = int(argv[6])
lack_inp = [int(inp) for inp in (argv[7:])]    # List of number of lack band of input sources

#======================================
# Slice input galaxy position dictionary
print('Start Slicing Into Pieces ...')
system('{} {:d} {:.1f} {:d} {:d} {:d} {:d} {}'.format(\
        'Slice_Sort_Lack_Source.py', dim, cube, sigma, bond, refD, num_th, ' '.join([str(inp) for inp in lack_inp])))

#======================================
# Mannual multi-thread process
print('Start Multi-Thread Calculation ...')
for lack in lack_inp:
    for i in range(num_th):
        print('lack_{:d}band_index{:0>3d}'.format(lack, i))
        system('{} {:d} {:.1f} {:d} {:d} {:d} {:d} {:d} &'.format(\
            'Do_Gaussian_Smooth_Index.py', dim, cube, sigma, bond, refD, lack, i))
