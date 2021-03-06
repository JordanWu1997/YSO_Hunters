#!/usr/bin/python
import numpy as np
from sys import argv, exit
from os import chdir, path, system
from joblib import Parallel, delayed
import time

if len(argv) != 8:
    exit('\n\tError: Wrong Arguments\
    \n\tExample: [program] [dim] [cube size] [sigma] [bond] [ref-D] [lack] [index]\
    \n\t[dim]: dimension for smooth (for now only "6")\
    \n\t[cube size]: length of multi-d cube in magnitude unit\
    \n\t[sigma]: standard deviation for gaussian dist. in magnitude\
    \n\t[bond]: boundary radius of gaussian beam unit in cell\
    \n\t[ref-D]: reference dimension which to modulus other dimension to\
    \n\t[lack]: number of lack band of input sources\
    \n\t[index]: index to indicate which part of catalog when multi-processing (e.g 00X)\n')

dim    = int(argv[1])       # Dimension of position vector
cube   = float(argv[2])     # Beamsize for each cube
sigma  = int(argv[3])       # STD for Gaussian Smooth
bond   = int(argv[4])
refD   = int(argv[5])       # Reference Beam Dimension
lack   = int(argv[6])
index  = int(argv[7])

posv_dir = 'GPV_{:d}Dposvec_bin{:.1f}/'.format(dim, cube)
out_dir  = 'GPV_after_smooth_{:d}D_bin{:.1f}_sigma{:d}_bond{:d}_refD{:d}/'.format(dim, cube, sigma, bond, refD)
beam_dir = 'GPV_smooth_sigma{:d}_bond{:d}_refD{:d}/'.format(sigma, bond, refD)
shape    = list(np.load(posv_dir + "Shape.npy"))

#===================================================================================
def gaussian_smooth(pos, gal_pos_array, gal_pos_array_str, new_key, no_lack_ind):
    rel_pos = pos[:-1]
    new_key[:] = "Lack"

    pos_check = new_key[:]
    pos_check[pos_check == 'Lack'] = '0'
    pos_check = np.array(pos_check, dtype=float)
    pos_check = np.array(pos_check, dtype=int)

    if all(np.less(pos_check, upper)) and all(np.greater_equal(pos_check, lower)):
        value  = float(source[key])
        weight = float(pos[-1])
        new_key_flt = np.array(new_key, dtype=float)
        new_key_int = np.array(new_key_flt, dtype=int)
        new_key_tuple = tuple(new_key_int)
        #if new_key_tuple not in after_smooth.keys():
        #    after_smooth.update({new_key_tuple: value * weight})
        #else:
        #    after_smooth[new_key_tuple] += value * weight
    #print(new_key)
#===================================================================================

lack_list = [lack]
new_key = np.chararray(dim, itemsize=4)
lower = np.zeros(len(shape))
upper = np.array(shape)
for lack in lack_list:
    sub_dir = 'tmp_L{:d}/'.format(lack)
    source  = np.load(out_dir + sub_dir + "{:0>3d}_tmp_cat.npy".format(index)).item()
    beam    = np.load(beam_dir + "{:d}d_beam_sigma{:d}.npy".format(int(dim-lack), sigma))
    #=========================================================================================
    start   = time.time()
    #after_smooth = dict()
    for i, key in enumerate(source.keys()):
        #=========================================================
        # Percentage Indicator
        if i % 100 == 0:
            print('Now: ' + str(float(i)/len(source) * 100) + '%')
        #=========================================================
        # Do Gaussian Smooth
        gal_pos = list(key)
        if gal_pos.count("Lack") <= (len(shape)-3):
            gal_pos_array = np.asarray(gal_pos)
            gal_pos_array_str = np.array(gal_pos_array, dtype=str)
            no_lack_ind = np.where(gal_pos_array_str != "Lack")[0]
            Parallel(n_jobs=10)(delayed(gaussian_smooth)(pos, gal_pos_array, gal_pos_array_str, new_key, no_lack_ind) for pos in beam)
        break
    end   = time.time()
    print("Saving result ...\n")
    chdir(out_dir + sub_dir)
    #np.save("{:0>3d}_{:d}d_after_smooth".format(int(index), int(dim-lack)), np.array(after_smooth))
    print("Gaussian Smooth took {:.3f} secs\n".format(end-start))
