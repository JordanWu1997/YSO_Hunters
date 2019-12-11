#!/usr/bin/python
import numpy as np
from sys import argv, exit
from os import chdir, path, system
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
sub_dir  = 'tmp_L{:d}/'.format(lack)
beam_dir = 'GPV_smooth_sigma{:d}_bond{:d}_refD{:d}/'.format(sigma, bond, refD)
shape    = list(np.load(posv_dir + "Shape.npy"))

lack_list = [lack]
for lack in lack_list:
    source = np.load(out_dir + sub_dir + "{:0>3d}_tmp_cat.npy".format(index)).item()
    beam   = np.load(beam_dir + "{:d}d_beam_sigma{:d}.npy".format(int(dim-lack), sigma))
    #=========================================================================================
    start  = time.time()
    after_smooth = dict()
    for i, key in enumerate(source.keys()):
        # Percentage Indicator
        if i % 100 == 0:
            print('Now: ' + str(float(i)/len(source) * 100) + '%')
        # Do Gaussian Smooth
        gal = list(key)
        if gal.count("Lack") <= (len(shape)-3):
            pos_array = np.array(gal, dtype=object)
            pos_array[pos_array == "Lack"] = 0
            for pos in beam:
                lower = np.array([0] * (len(shape)))
                upper = np.array(shape)
                # Note: upper is from shape which is total num of cube in each dim (index+1)
                if all(pos_array < upper) and all(pos_array >= lower):
                    value  = float(source[key])
                    weight = float(pos[-1])
                    if key not in after_smooth.keys():
                        after_smooth.update({key: value * weight})
                    else:
                        after_smooth[key] += value * weight
    end   = time.time()
    print("Saving result ...\n")
    chdir(out_dir + sub_dir)
    np.save("{:0>3d}_{:d}d_after_smooth".format(int(index), int(dim-lack)), np.array(after_smooth))
    print("Gaussian Smooth took {:.3f} secs\n".format(end-start))
