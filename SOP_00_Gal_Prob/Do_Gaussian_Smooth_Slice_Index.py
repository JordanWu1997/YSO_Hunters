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
if len(argv) != 10:
    exit('\n\tError: Wrong Arguments\
    \n\tExample: [program] [dim] [cube size] [sigma] [bond] [ref-D] [lack] [band_inp] [slice_num] [slice_ind]\
    \n\t[dim]: dimension for smooth (for now only "6")\
    \n\t[cube size]: length of multi-d cube in magnitude unit\
    \n\t[sigma]: standard deviation for gaussian dist. in magnitude\
    \n\t[bond]: boundary radius of gaussian beam unit in cell\
    \n\t[ref-D]: reference dimension which to modulus other dimension to\
    \n\t[lack]: number of lack bands\
    \n\t[band_inp]: band used to do smooth in string e.g. 012345\
    \n\t[slice_num]: number of slices of the input catalog\
    \n\t[slice_ind]: index of slices\n')

dim       = int(argv[1])       # Dimension of position vector
cube      = float(argv[2])     # Beamsize for each cube
sigma     = int(argv[3])       # STD for Gaussian Smooth
bond      = int(argv[4])
refD      = int(argv[5])       # Reference Beam Dimension
lack      = int(argv[6])
band_inp  = str(argv[7])
slice_num = int(argv[8])
slice_ind = int(argv[9])

band_list = []
for i in range(len(band_inp)):
    band_list.append(band_inp[i])

posv_dir = 'GPV_{:d}Dposvec_bin{:.1f}/'.format(dim, cube)
band_dir = posv_dir + 'Band_pos_num/'
slic_dir = band_dir + 'Slice_{}_{:0>3d}/'.format(band_inp, slice_num)
out_dir  = 'GPV_after_smooth_{:d}D_bin{:.1f}_sigma{:d}_bond{:d}_refD{:d}/'.format(dim, cube, sigma, bond, refD)
temp_dir = out_dir  + 'After_{}/'.format(band_inp)
beam_dir = 'GPV_smooth_sigma{:d}_bond{:d}_refD{:d}/'.format(sigma, bond, refD)
shape    = list(np.load(posv_dir + "Shape.npy"))

if not path.isdir(temp_dir):
    system('mkdir {}'.format(temp_dir))

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
        # Make New Key from Relative Position
        pos = beam[i]
        rel_pos = pos[:-1]
        new_pos = -999 * np.ones(dim)
        for j in range(len(no_lack_ind)):
            new_pos[no_lack_ind[j]] = pos_array[no_lack_ind[j]] + rel_pos[j]
        #=========================================================
        # Check if New Position Vector within multi-D space
        # Note: upper is from shape which is total num of cube in each dim (index+1)
        pos_check = np.zeros(dim)
        for k in range(len(new_pos)):
            if new_pos[k] != -999.:
                pos_check[k] = new_pos[k]
        if np.all(np.less(pos_check, upper)) and np.all(np.greater_equal(pos_check, lower)):
            weight = float(pos[-1])
            after_beam_smooth_pos.append(new_pos)
            after_beam_smooth_num.append(float(num_array) * weight)
    return after_beam_smooth_pos, after_beam_smooth_num

@jit()
def run_smooth(input_pos, input_num, beam):
    after_smooth_pos = []
    after_smooth_num = []
    for i in range(len(input_pos)):
        #drawProgressBar(float(i+1)/len(input_pos))
        #=========================================================
        # Do Gaussian Smooth
        no_lack_ind = np.where(input_pos[i] != -999)[0]
        smooth_pos, smooth_num = cal_smooth_beam(input_pos[i], input_num[i], no_lack_ind, beam)
        after_smooth_pos.extend(smooth_pos)
        after_smooth_num.extend(smooth_num)
    return after_smooth_pos, after_smooth_num

#=========================================================================================
# Main Program
#=========================================================================================
# Initialization
lower       = np.zeros(len(shape), dtype=int)
upper       = np.array(shape, dtype=int)
input_pos   = np.load(slic_dir + "{:0>3d}_pos.npy".format(slice_ind))
input_num   = np.load(slic_dir + "{:0>3d}_num.npy".format(slice_ind))
beam        = np.load(beam_dir + "{:d}d_beam_sigma{:d}.npy".format(int(dim-lack), sigma))
#=========================================================================================
# Start Calculation
all_after_smooth_pos, all_after_smooth_num = run_smooth(input_pos, input_num, beam)
all_after_smooth_pos_array = np.array(all_after_smooth_pos, int)
all_after_smooth_num_array = np.array(all_after_smooth_num, float)
#=========================================================================================
# Save Results
chdir(temp_dir)
np.save("after_{}_{:0>3d}_pos".format(band_inp, slice_ind), all_after_smooth_pos_array)
np.save("after_{}_{:0>3d}_num".format(band_inp, slice_ind), all_after_smooth_num_array)
chdir('../../')
