#!/usr/bin/python
import numpy as np
from glob import glob
from time import time
from sys import argv
from os import system, chdir, path

# Check Input Arguments
if len(argv) != 6:
    exit('\n\tError: Wrong Arguments\
    \n\tExample: [program] [dim] [cube size] [sigma] [bond] [ref-D]\
    \n\t[dim]: dimension of galaxy position vector\
    \n\t[cube size]: length of multi-d cube in magnitude unit\
    \n\t[sigma]: standard deviation for gaussian dist. in magnitude\
    \n\t[bond]: boundary radius of gaussian beam unit in cell\
    \n\t[ref-D]: reference dimension which to modulus other dimension to\n')

# Parameters
dim     = int(argv[1])
cube    = float(argv[2])
sigma   = int(argv[3])
bond    = int(argv[4])
refD    = int(argv[5])
program = 'Make_3D_Gal_Prob_Tomography.py'
storage = 'Tomography_{:d}D_bin{:.1f}_sigma{:d}_bond{:d}_refD{:d}'.format(dim, cube, sigma, bond, refD)

# Initialize Storage Directory
chdir(storage)
if path.isdir('All_band'):
    system('rm -fr All_band')
system('mkdir All_band')

# Main Program
if __name__ == '__main__':
    t_start = time()
    for k in range(dim):
        for j in range(k):
            for i in range(j):
                print(i, j, k)
                system('{} {:d} {:d} {:d} {:.1f}\
                        ../GPV_after_smooth_{:d}D_bin{:.1f}_sigma{:d}_bond{:d}_refD{:d}/3d_after_smooth.npy \
                        ../GPV_{:d}Dposvec_bin{:.1f}/Shape.npy y'.format(program, i, j, k, cube, dim, cube, sigma, bond, refD, dim, cube))
                chdir(glob('{:d}{:d}{:d}*'.format(i, j, k))[0])
                system('convert -delay 20 -loop 0 *.png {:d}{:d}{:d}.gif'.format(i, j, k))
                system('cp {:d}{:d}{:d}.gif ../All_band'.format(i, j, k))
                chdir('../')
    t_end   = time()
    print('Main Program took {:.3f} secs'.format(t_end - t_start))
