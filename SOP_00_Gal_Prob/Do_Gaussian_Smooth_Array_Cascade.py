#!/usr/bin/python
from __future__ import print_function
import sys
import time
import numpy as np
from sys import argv, exit
from os import chdir, path, system
from numba import jit

#=========================================================================================
#  Input variables
if len(argv) < 7:
    exit('\n\tError: Wrong Arguments\
    \n\tExample: [program] [dim] [cube size] [sigma] [bond] [ref-D] [lack]\
    \n\t[dim]: dimension for smooth (for now only "6")\
    \n\t[cube size]: length of multi-d cube in magnitude unit\
    \n\t[sigma]: standard deviation for gaussian dist. in magnitude\
    \n\t[bond]: boundary radius of gaussian beam unit in cell\
    \n\t[ref-D]: reference dimension which to modulus other dimension to\
    \n\t[lack]: number of lack band of input sources (or "all")\n')

dim       = int(argv[1])       # Dimension of position vector
cube      = float(argv[2])     # Beamsize for each cube
sigma     = int(argv[3])       # STD for Gaussian Smooth
bond      = int(argv[4])
refD      = int(argv[5])       # Reference Beam Dimension

if argv[6] != 'all':
    lack_list = [int(arg) for arg in argv[6:]]
else:
    lack_lim  = dim - 3 + 1
    lack_list = [i for i in range(lack_lim)]

posv_dir = 'GPV_{:d}Dposvec_bin{:.1f}/'.format(dim, cube)
out_dir  = 'GPV_after_smooth_{:d}D_bin{:.1f}_sigma{:d}_bond{:d}_refD{:d}/'.format(dim, cube, sigma, bond, refD)
beam_dir = 'GPV_smooth_sigma{:d}_bond{:d}_refD{:d}/'.format(sigma, bond, refD)
shape    = list(np.load(posv_dir + "Shape.npy"))

if not path.isdir(out_dir):
    system('mkdir {}'.format(out_dir))

#================================================
# Functions
def drawProgressBar(percent, barLen = 50):
    # percent float from 0 to 1.
    sys.stdout.write("\r")
    sys.stdout.write("[{:<{}}] {:.3f}%".format("=" * int(barLen * percent), barLen, (percent * 100)))
    sys.stdout.flush()

@jit(nopython=True)
def cascade_array(sort_position, sort_value):
    '''
    Use this to find out sources locate in same position and cascade them
    Note: No tuple() support in numba, No format() support in numba
    '''
    #================================================
    # Input
    after_cascade_pos = []
    after_cascade_value = []
    start = 0
    end   = 0
    for i in range(len(sort_value)-1):
        #================================================
        # Indicator
        #if i % 1000 == 0 and i>999:
        #    print(float(i+1)/len(sort_value))
        #================================================
        # Get reference and target
        tar, ref = sort_position[i], sort_position[i+1]
        end += 1
        #================================================
        # Determine repeated or not
        if not np.all(np.equal(tar, ref)):
            after_cascade_pos.append(sort_position[start])
            after_cascade_value.append(np.sum(sort_value[start:end]))
            start = end
    #================================================
    # Include the last term
    after_cascade_pos.append(sort_position[start])
    after_cascade_value.append(np.sum(sort_value[start:]))
    return after_cascade_pos, after_cascade_value

def update_dict(after_cascade_pos, after_cascade_value):
    '''
    This is to update dictionary with key [position] and its value
    '''
    #================================================
    # Input
    out_dict = dict()
    for i in range(len(after_cascade_value)):
        #================================================
        # Indicator
        drawProgressBar(float(i+1)/len(after_cascade_value))
        #================================================
        # Update dictionary
        key = tuple(after_cascade_pos[i])
        out_dict[key] = float(after_cascade_value[i])
    return out_dict

#=========================================================================================
# Main Program
for lack in lack_list:
    #================================================
    # Load Position/Probability array
    l_start = time.time()
    pos_array  = np.load(out_dir + "{:d}d_after_smooth_pos_array.npy".format(dim-lack))
    num_array  = np.load(out_dir + "{:d}d_after_smooth_num_array.npy".format(dim-lack))
    position_t = np.transpose(pos_array)
    l_end   = time.time()
    print('\n', lack, lack_list)
    print("Lack {:d} Load took {:.3f} secs".format(lack, l_end-l_start))
    #================================================
    # Sort Input Galaxy Position/Probability array
    s_start = time.time()
    sort_ind = np.lexsort(tuple(position_t))
    sort_pos = np.array(pos_array[sort_ind], dtype=int)
    sort_num = np.array(num_array[sort_ind], dtype=float)
    s_end   = time.time()
    print("Lack {:d} Sort took {:.3f} secs\n".format(lack, s_end-s_start))
    #================================================
    # Cascade Repeated Position
    c_start = time.time()
    after_cascade_pos, after_cascade_num = cascade_array(sort_pos, sort_num)
    print("# of point: {:d} (before cascade)".format(len(sort_num)))
    print("# of point: {:d} (after cascade)\n".format(len(after_cascade_num)))
    print('Update pos & num to dictionary ...')
    after_cascade_dict = update_dict(after_cascade_pos, after_cascade_num)
    c_end   = time.time()
    print("\nCascading Lack {:d} took {:.3f} secs\n".format(lack, c_end-c_start))
    #================================================
    # Save result
    print("Saving result ...")
    chdir(out_dir)
    s_start = time.time()
    np.save("{:d}d_after_smooth_casacade_dict".format(int(dim-lack)), np.array(after_cascade_dict))
    s_end   = time.time()
    print("Saving Lack {:d} took {:.3f} secs\n".format(lack, s_end-s_start))
    chdir('../')
