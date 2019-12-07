#!/usr/bin/python
import numpy as np
from sys import argv, exit
from os import chdir, path, system
import time

if len(argv) != 7:
    exit('\n\tError: Wrong Arguments\
    \n\tExample: [program] [dim] [cube size] [sigma] [bond] [ref-D] [suffix]\
    \n\t[dim]: dimension for smooth (for now only "6")\
    \n\t[cube size]: length of multi-d cube in magnitude unit\
    \n\t[sigma]: standard deviation for gaussian dist. in magnitude\
    \n\t[bond]: boundary radius of gaussian beam unit in cell\
    \n\t[ref-D]: reference dimension which to modulus other dimension to\
    \n\t[suffix]: suffix to indicate which part of catalog when multi-processing (or "none")\n')

dim    = int(argv[1])       # Dimension of position vector
cube   = float(argv[2])     # Beamsize for each cube
sigma  = int(argv[3])       # STD for Gaussian Smooth
bond   = int(argv[4])
ref    = int(argv[5])       # Reference Beam Dimension
suffix = str(argv[6])

posv_dir = 'GPV_{:d}Dposvec_bin{:.1f}/'.format(dim, cube)
beam_dir = 'GPV_smooth_sigma{:d}_bond{:d}_refD{:d}/'.format(sigma, bond, ref)
out_dir  = 'GPV_after_smooth_{:d}D_bin{:.1f}_sigma{:d}_bond{:d}_refD{:d}/'.format(dim, cube, sigma, bond, ref)
shape  = list(np.load(posv_dir + "Shape.npy"))

lack_list = [0, 1, 2, 3]
for lack in lack_list:
    source = np.load(posv_dir + "Lack_{:d}band_sources.npy".format(lack)).item()
    beam   = np.load(beam_dir + "{:d}d_beam_sigma{:d}.npy".format(int(dim-lack), sigma))
    #=========================================================================================
    start = time.time()
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
    print("Gaussian Smooth took {:.3f} secs\n".format(end-start))
    #========================================================================================
    if not path.isdir(out_dir):
        print("Directory doesn't exist ...")
        print("Create new one ...\n")
        system('mkdir ' + out_dir)
    else:
        print("Directory exists ...")
        print("Use exist one ...\n")
    #========================================================================================
    print("Saving result ...\n")
    chdir(out_dir)
    if suffix != 'none':
        np.save("{:0>3d}_{:d}d_after_smooth".format(int(suffix), int(dim-lack)), np.array(after_smooth))
    else:
        np.save("{:d}d_after_smooth".format(int(dim-lack)), np.array(after_smooth))
    chdir('../')
    #=======================================================================================
