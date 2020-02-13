#!/usr/bin/python
import time
import numpy as np
from sys import argv, exit
from os import chdir, path, system
from numba import jit
from __future__ import print_function

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
    \n\t[lack]: number of lack band of input sources\n')

dim       = int(argv[1])       # Dimension of position vector
cube      = float(argv[2])     # Beamsize for each cube
sigma     = int(argv[3])       # STD for Gaussian Smooth
bond      = int(argv[4])
refD      = int(argv[5])       # Reference Beam Dimension
lack_list = [int(arg) for arg in argv[6:]]

posv_dir = 'GPV_{:d}Dposvec_bin{:.1f}/'.format(dim, cube)
out_dir  = 'GPV_after_smooth_{:d}D_bin{:.1f}_sigma{:d}_bond{:d}_refD{:d}/'.format(dim, cube, sigma, bond, refD)
beam_dir = 'GPV_smooth_sigma{:d}_bond{:d}_refD{:d}/'.format(sigma, bond, refD)
shape    = list(np.load(posv_dir + "Shape.npy"))

if not path.isdir(out_dir):
    system('mkdir {}'.format(out_dir))

#=========================================================================================
# Main Functions
@jit(nopython=True)
def cal_smooth_beam(beam, no_lack_ind, galaxy_num):
    '''
    Calculate and smooth every point within a gaussian beam
    '''
    after_beam_smooth = []
    for i in range(len(beam)):
        pos = beam[i]
        #=========================================================
        # Make New Key from Relative Position
        rel_pos = pos[:-1]
        new_key = -999 * np.ones(dim)
        for ind in no_lack_ind:
            new_key[ind] = int(gal_pos_array[ind])
        for j in range(len(rel_pos)):
            new_key[j] += int(rel_pos[j])
        #=========================================================
        # Check if New Position Vector within multi-D space
        # Note: upper is from shape which is total num of cube in each dim (index+1)
        pos_check = new_key[:]
        pos_check[pos_check == -999] = 0
        if np.all(np.less(pos_check, upper)) and np.all(np.greater_equal(pos_check, lower)):
            weight = float(pos[-1])
            storage = list(new_key) + [galaxy_num * weight]
            after_beam_smooth.append(list(new_key) + [galaxy_num * weight])
    return after_beam_smooth

#=========================================================================================
# Main Program
for lack in lack_list:
    #=========================================================================================
    # Initialization
    print(lack, lack_list)
    lower        = np.zeros(len(shape))
    upper        = np.array(shape)
    source       = np.load(posv_dir + "Lack_{:d}band_sources.npy".format(lack)).item()
    beam         = np.load(beam_dir + "{:d}d_beam_sigma{:d}.npy".format(int(dim-lack), sigma))
    after_smooth = []
    #=========================================================================================
    # Start Calculation
    start = time.time()
    for i, key in enumerate(source.keys()):
        #=========================================================
        # Percentage Indicator
        if i % 100 == 0:
            print('Now: ' + str(float(i)/len(source) * 100) + '%')
        #=========================================================
        # Do Gaussian Smooth
        gal_pos = list(key)
        if gal_pos.count("Lack") <= (len(shape)-3):
            gal_pos_array = np.array(gal_pos, dtype=int)
            gal_pos_array_str = np.array(gal_pos_array, dtype=str)
            no_lack_ind = np.where(gal_pos_array_str != "Lack")[0]
            source_galaxy_num = source[key]
            beam_smooth_result = cal_smooth_beam(beam, no_lack_ind, source_galaxy_num)
            after_smooth.append(beam_smooth_result)
    end   = time.time()
    print("Lack {:d} Gaussian Smooth took {:.3f} secs\n".format(lack, end-start))
    #=========================================================================================
    # Save results
    print("Saving result ...\n")
    chdir(out_dir)
    start = time.time()
    np.save("{:d}d_after_smooth_array".format(int(dim-lack)), np.array(after_smooth, dtype=object))
    end   = time.time()
    print("Save Lack {:d} Gaussian Smooth took {:.3f} secs\n".format(lack, end-start))
    chdir('../')