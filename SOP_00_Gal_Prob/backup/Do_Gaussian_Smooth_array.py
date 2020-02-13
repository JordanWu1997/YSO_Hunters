#!/usr/bin/python
import numpy as np
from sys import argv, exit
from os import chdir, path, system
import time
import copy

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
            gal_pos_array = np.array(gal_pos, dtype=object)
            gal_pos_array_str = np.array(gal_pos_array, dtype=str)
            for pos in beam:

                #=========================================================
                # Make New Key from Relative Position
                rel_pos = pos[:-1]
                no_lack_ind = np.where(gal_pos_array_str != "Lack")[0]
                new_key = np.zeros(dim)
                new_key[:] = -999
                new_key[no_lack_ind] = gal_pos_array[no_lack_ind] + rel_pos

                #=========================================================
                # Check if New Position Vector within multi-D space
                # Note: upper is from shape which is total num of cube in each dim (index+1)
                pos_check = copy.deepcopy(new_key)
                pos_check[pos_check == -999] = 0
                pos_check = np.array(pos_check, dtype=int)
                if all(np.less(pos_check, upper)) and all(np.greater_equal(pos_check, lower)):
                    value  = float(source[key])
                    weight = float(pos[-1])
                    new_key_int = np.array(new_key, dtype=int)
                    after_smooth.append(list(new_key_int) + [value*weight])
            break
 #=========================================================================================
    # Save results
    end   = time.time()
    print("Lack {:d} Gaussian Smooth took {:.3f} secs\n".format(lack, end-start))
    print("Saving result ...\n")
    chdir(out_dir)
    start = time.time()
    np.save("{:d}d_after_smooth_array".format(int(dim-lack)), np.array(after_smooth, dtype=object))
    end   = time.time()
    print("Save Lack {:d} Gaussian Smooth took {:.3f} secs\n".format(lack, end-start))
    chdir('../')
