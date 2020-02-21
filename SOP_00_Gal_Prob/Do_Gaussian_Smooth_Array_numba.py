#!/usr/bin/python
from __future__ import print_function
import sys
import time
import numpy as np
from sys import argv, exit
from os import chdir, path, system
from numba import jit

#=========================================================================================
# Input variables
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

if path.isdir(out_dir):
    system('rm -r {}'.format(out_dir))
    system('mkdir {}'.format(out_dir))
else:
    system('mkdir {}'.format(out_dir))

#=========================================================================================
# Main Functions
def drawProgressBar(percent, barLen = 50):
    # percent float from 0 to 1.
    sys.stdout.write("\r")
    sys.stdout.write("[{:<{}}] {:.3f}%".format("=" * int(barLen * percent), barLen, (percent * 100)))
    sys.stdout.flush()

@jit(nopython=True)
def cal_smooth_beam(pos_array, num_array, no_lack_ind, beam):
    '''
    Calculate and smooth every point within a gaussian beam
    '''
    after_beam_smooth_pos = []
    after_beam_smooth_num = []
    for i in range(len(beam)):
        #=========================================================
        # Indicator
        #if i % 10000 == 0 and i>9999:
        #    print(i/len(beam))
        #=========================================================
        # Make New Key from Relative Position
        pos = beam[i]
        rel_pos = pos[:-1]
        new_pos = -999 * np.ones(dim)
        for j in range(len(no_lack_ind)):
            new_pos[no_lack_ind[j]] = int(pos_array[no_lack_ind[j]]) + int(rel_pos[j])
        #=========================================================
        # Check if New Position Vector within multi-D space
        # Note: upper is from shape which is total num of cube in each dim (index+1)

        pos_check = np.zeros(dim)
        for k in range(len(new_pos)):
            if new_pos[k] != -999:
                pos_check[k] = new_pos[k]

        if np.all(np.less(pos_check, upper)) and np.all(np.greater_equal(pos_check, lower)):
            weight = float(pos[-1])
            after_beam_smooth_pos.append(new_pos)
            after_beam_smooth_num.append(float(num_array[0]) * weight)
    return after_beam_smooth_pos, after_beam_smooth_num

def run_smooth(input_pos, input_num, beam):
    after_smooth_pos = []
    after_smooth_num = []
    for i in range(len(input_pos)):
        #=========================================================
        # Percentage Indicator
        drawProgressBar(float(i+1)/len(input_pos))
        #=========================================================
        # Do Gaussian Smooth
        no_lack_ind = np.where(input_pos != -999)[0]
        smooth_pos, smooth_num = cal_smooth_beam(input_pos, input_num, no_lack_ind, beam)
        after_smooth_pos.extend(smooth_pos)
        after_smooth_num.extend(smooth_num)
    return after_smooth_pos, after_smooth_num

#=========================================================================================
# Main Program
print('\nStart Calculating ...\n')
for lack in lack_list:
    #=========================================================================================
    # Initialization
    lower        = np.zeros(len(shape), dtype=int)
    upper        = np.array(shape, dtype=int)
    input_pos    = np.load(posv_dir + "Lack_{:d}{:d}{:d}_pos.npy".format(lack, lack, lack))
    input_num    = np.load(posv_dir + "Lack_{:d}{:d}{:d}_pos.npy".format(lack, lack, lack))
    beam         = np.load(beam_dir + "{:d}d_beam_sigma{:d}.npy".format(int(dim-lack), sigma))
    print(lack, lack_list, len(input_pos))
    #=========================================================================================
    # Start Calculation
    start = time.time()
    all_after_smooth_pos, all_after_smooth_num = run_smooth(input_pos, input_num, beam)
    end   = time.time()
    print("\nCalculate Lack {:d} Gaussian Smooth took {:.3f} secs".format(lack, end-start))
    #=========================================================================================
    # Save Results
    chdir(out_dir)
    start = time.time()
    np.save("{:d}d_after_smooth_pos_array".format(int(dim-lack)), np.array(all_after_smooth_pos))
    np.save("{:d}d_after_smooth_num_array".format(int(dim-lack)), np.array(all_after_smooth_num))
    end   = time.time()
    print("Save Lack {:d} Gaussian Smooth took {:.3f} secs\n".format(lack, end-start))
    chdir('../')
