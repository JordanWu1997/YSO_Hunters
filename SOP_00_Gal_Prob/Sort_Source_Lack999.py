#!/usr/bin/python
from __future__ import print_function
import time
import sys
import numpy as np
from numba import jit
from os import system, chdir
from sys import argv, exit

if len(argv) != 3:
    exit('\n\tError: Wrong Arguments\
    \n\tExample: [program] [dim] [cube size]\
    \n\t[dim]: dim of magnitude space (for now only "6")\
    \n\t[cube size]: length of multi-d cube in magnitude unit\n')

print("\nLoading ...\n")
dim      = int(argv[1])       # Dimension of multi-D method
lack_lim = dim - 3 + 1        # Note: start from 0
cube     = float(argv[2])     # Beamsize for each cube
posv_dir = 'GPV_' + str(dim) + 'Dposvec_bin' + str(cube) + '/'
shape    = list(np.load(posv_dir + "Shape.npy"))
gal_pos  = np.load(posv_dir + "Gal_Position_vectors.npy")
gal_num  = np.load(posv_dir + "Gal_Position_numbers.npy")

#=======================================================
# Functions
def drawProgressBar(percent, barLen = 50):
    # percent float from 0 to 1.
    sys.stdout.write("\r")
    sys.stdout.write("[{:<{}}] {:.3f}%".format("=" * int(barLen * percent), barLen, (percent * 100)))
    sys.stdout.flush()

#=======================================================
# Sort
w_start = time.time()
for i in range(lack_lim):
    lack_pos = []
    lack_num = []
    total_pos = len(gal_pos)
    s_start = time.time()
    for j in range(total_pos):
        drawProgressBar(float(j+1) / total_pos)
        if len(np.where(gal_pos[j] == -999)[0]) == i:
            lack_pos.append(gal_pos[j])
            lack_num.append(gal_num[j])
    lack_pos_array = np.array(lack_pos)
    lack_num_array = np.array(lack_num)
    chdir(posv_dir)
    np.save('Lack_{:d}{:d}_pos'.format(i, i), lack_pos_array)
    np.save('Lack_{:d}{:d}_num'.format(i, i), lack_num_array)
    chdir('../')
    s_end     = time.time()
    print('\nFilter out lack {:d} band took {:.3f} sec\n'.format(i, s_end-s_start))
w_end   = time.time()
print('\nWhole sorting process took {:.3f} sec\n'.format(w_end-w_start))
