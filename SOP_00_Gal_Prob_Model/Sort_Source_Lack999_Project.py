#!/usr/bin/python
from __future__ import print_function
import sys
import time
import numpy as np
from os import system, chdir
from sys import argv, exit
from itertools import combinations

if len(argv) != 3:
    exit('\n\tError: Wrong Arguments\
    \n\tExample: [program] [dim] [cube size]\
    \n\t[dim]: dim of magnitude space (for now only "6")\
    \n\t[cube size]: length of multi-d cube in magnitude unit\n')

#=======================================================
# Input
dim      = int(argv[1])       # Dimension of multi-D method
lack_lim = dim - 3 + 1        # Note: start from 0
cube     = float(argv[2])     # Beamsize for each cube
posv_dir = 'GPV_' + str(dim) + 'Dposvec_bin' + str(cube) + '/'
lack_dir = posv_dir + 'Lack_pos_num/'

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

def find_no_lack(lst):
    '''
    find no lack index
    '''
    index_list = [i for i, x in enumerate(lst) if x != -999]
    return index_list

#=======================================================
# Main Program
p_start = time.time()
print("\nStart projecting ...\n")
for i in range(lack_lim):
    for j in range(i):
        print('L{:d} -> L{:d}'.format(j, i))
        s_start = time.time()
        project_pos, project_num = [], []
        lack_pos = np.load(lack_dir + 'Lack_{:d}{:d}_pos.npy'.format(j, j))
        lack_num = np.load(lack_dir + 'Lack_{:d}{:d}_num.npy'.format(j, j))
        for k in range(len(lack_pos)):
            drawProgressBar(float(k+1)/len(lack_pos))
            pos = lack_pos[k]
            num = lack_num[k]
            no_lack_ind = find_no_lack(pos)
            for comb in combinations(no_lack_ind, i-j):
                new_pos = list(pos)
                for ind in comb:
                    new_pos[ind] = -999
                project_pos.append(new_pos)
                project_num.append(num)
        chdir(lack_dir)
        np.save('Lack_{:d}{:d}_pos'.format(j, i), np.array(project_pos))
        np.save('Lack_{:d}{:d}_num'.format(j, i), np.array(project_num))
        chdir('../../')
        s_end   = time.time()
        print('\nFrom lack {:d} to lack {:d} band took {:.3f} sec\n'.format(j, i, s_end-s_start))
p_end   = time.time()
print('Whole projection took {:.3f} sec\n'.format(p_end-p_start))
