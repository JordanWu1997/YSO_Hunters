#!/usr/bin/python
from __future__ import print_function
import sys
import time
import numpy as np
from sys import argv, exit
from os import system, chdir, path
from itertools import combinations

if len(argv) != 4:
    exit('\n\tError: Wrong Arguments\
    \n\tExample: [program] [dim] [cube size] [sl_num]\
    \n\t[dim]: dimension for smooth (for now only "6")\
    \n\t[cube size]: length of multi-d cube in magnitude unit\
    \n\t[sl_num]: number to slice input into pieces\n')

#==============================================================================================================
# Input variables
dim       = int(argv[1])       # Dimension of position vector
cube      = float(argv[2])     # Beamsize for each cube
sl_num    = int(argv[3])       # Number of slices
lack_lim  = dim - 3 + 1
posv_dir  = 'GPV_' + str(dim) + 'Dposvec_bin' + str(cube) + '/'
band_dir  = posv_dir + 'Band_pos_num/'

#=======================================================
# Main Function
def drawProgressBar(percent, barLen = 50):
    '''
    draw progress bar
    '''
    # percent float from 0 to 1.
    sys.stdout.write("\r")
    sys.stdout.write("[{:<{}}] {:.3f}%".format("=" * int(barLen * percent), barLen, (percent * 100)))
    sys.stdout.flush()

#==============================================================================================================
# Main Program
t_start = time.time()
print('\nStart Slicing ...\n')
for i in range(lack_lim):
    for comb in combinations(np.arange(dim), dim-i):

        # Set band indice
        band_list = list(comb)
        band_index = ''
        for band in band_list:
            band_index += str(int(band))

        # Load pos/num
        l_start = time.time()
        input_pos = np.load(band_dir + 'Lack_{:d}_{}_pos.npy'.format(dim-len(band_list), band_index))
        input_num = np.load(band_dir + 'Lack_{:d}_{}_num.npy'.format(dim-len(band_list), band_index))
        l_end   = time.time()
        #print(band_list, 'loading took {:.3f} sec'.format(l_end-l_start))

        # Output directories
        out_dir   = band_dir + 'Slice_{}_{:0>3d}/'.format(band_index, sl_num)
        if path.isdir(out_dir):
            system('rm -fr ' + out_dir)
            system('mkdir ' + out_dir)
        else:
            system('mkdir ' + out_dir)

        # Start slicing
        s_start = time.time()
        end_cuts = [int(len(input_pos)*(float(k)/sl_num)) for k in range(sl_num+1)]
        end_cuts[-1] += 1
        chdir(out_dir)
        for j in range(sl_num):
            #drawProgressBar(float(j+1)/sl_num)
            output_pos = input_pos[end_cuts[j]:end_cuts[j+1]]
            output_num = input_num[end_cuts[j]:end_cuts[j+1]]
            np.save('{:0>3d}_pos'.format(j), output_pos)
            np.save('{:0>3d}_num'.format(j), output_num)
        chdir('../../../')
        s_end   = time.time()
        #print('\nSlicing took {:.3f} sec\n'.format(s_end-s_start))
t_end = time.time()
print('Whole slice process took {:.3f} sec\n'.format(t_end - t_start))
