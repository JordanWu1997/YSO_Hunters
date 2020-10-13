#!/usr/bin/python
from __future__ import print_function
import numpy as np
from sys import argv, exit
from os import chdir, path, system
from itertools import combinations

#=========================================================================================
# Input variables
if len(argv) != 6:
    exit('\n\tError: Wrong Arguments\
    \n\tExample: [program] [dim] [cube size] [sigma] [bond] [ref-D]\
    \n\t[dim]: dimension for smooth (for now only "6")\
    \n\t[cube size]: length of multi-d cube in magnitude unit\
    \n\t[sigma]: standard deviation for gaussian dist. in magnitude\
    \n\t[bond]: boundary radius of gaussian beam unit in cell\
    \n\t[ref-D]: reference dimension which to modulus other dimension to\n')

dim      = int(argv[1])       # Dimension of position vector
cube     = float(argv[2])     # Beamsize for each cube
sigma    = int(argv[3])       # STD for Gaussian Smooth
bond     = int(argv[4])
refD     = int(argv[5])       # Reference Beam Dimension
lack_lim = dim - 3 + 1

posv_dir = 'GPV_{:d}Dposvec_bin{:.1f}/'.format(dim, cube)
band_dir = posv_dir + 'Band_pos_num/'
beam_dir = 'GPV_smooth_sigma{:d}_bond{:d}_refD{:d}/'.format(sigma, bond, refD)
shape    = list(np.load(posv_dir + "Shape.npy"))

max_list = []
for i in range(lack_lim):
    max_lack = 0
    beam = np.load(beam_dir + '{:d}d_beam_sigma{:d}.npy'.format(dim-i, sigma))
    beam_loop = len(beam)
    print('\n# {:d}d_beam: {:d}'.format(dim-i, beam_loop))
    for comb in combinations(np.arange(dim), dim-i):
        band_list = list(comb)
        band_index = ''
        for band in band_list:
            band_index += str(int(band))
        posv_list = np.load(band_dir + 'Lack_{:d}_{}_pos.npy'.format(i, band_index))
        posv_loop = len(posv_list)
        print('# {}: {:d} | # {} * Beam = {:d}'.format(band_index, posv_loop, band_index, posv_loop*beam_loop))
        if posv_loop*beam_loop > max_lack:
            max_lack = posv_loop*beam_loop
    max_list.append(max_lack)

print('\n# Max Loop: ')
for i in range(len(max_list)):
    print('# Lack{:d} Max Loop = {:d}'.format(i, max_list[i]))

#TODO Add estimate storage size, and time that may need
