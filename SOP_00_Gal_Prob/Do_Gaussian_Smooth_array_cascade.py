#!/usr/bin/python
import numpy as np
from sys import argv, exit
from os import chdir, path, system
import time

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
    \n\t[lack]: number of lack band of input sources\n')

dim    = int(argv[1])       # Dimension of position vector
cube   = float(argv[2])     # Beamsize for each cube
sigma  = int(argv[3])       # STD for Gaussian Smooth
bond   = int(argv[4])
refD   = int(argv[5])       # Reference Beam Dimension
lack   = [int(arg) for arg in argv[6:]]

posv_dir = 'GPV_{:d}Dposvec_bin{:.1f}/'.format(dim, cube)
out_dir  = 'GPV_after_smooth_{:d}D_bin{:.1f}_sigma{:d}_bond{:d}_refD{:d}/'.format(dim, cube, sigma, bond, refD)
beam_dir = 'GPV_smooth_sigma{:d}_bond{:d}_refD{:d}/'.format(sigma, bond, refD)
shape    = list(np.load(posv_dir + "Shape.npy"))

if not path.isdir(out_dir):
    system('mkdir {}'.format(out_dir))

#=========================================================================================
# Main Program
lack_list = lack
for lack in lack_list:

    #================================================
    # Load Position/Probability array
    l_start = time.time()
    GPV_array  = np.load(out_dir + "{:d}d_after_smooth_array.npy".format(dim-lack))
    value      = GPV_array[:, -1]
    position   = [GPV_array[:, i] for i in range(dim)]
    sort_prior = [GPV_array[:, dim-i-1] for i in range(dim)]
    l_end   = time.time()
    print("Lack {:d} Load took {:.3f} secs\n".format(lack, l_end-l_start))

    #================================================
    # Sort Input Galaxy Position/Probability array
    s_start = time.time()
    sort_ind = np.lexsort(tuple(sort_prior))
    sort_value, sort_position = [], []
    for ind in sort_ind:
        sort_value.append(value[ind])
        sort_position.append([position[j][ind] for j in range(dim)])
    s_end   = time.time()
    print("Lack {:d} Sort took {:.3f} secs\n".format(lack, s_end-s_start))

    #================================================
    # Cascade Repeated Position
    c_start = time.time()
    all_pos = len(sort_value)
    after_cascade = dict()
    while len(sort_value) > 1:

        # Get reference and target
        tar, tar_val = np.array(sort_position[0], dtype=int), sort_value[0]
        ref, ref_val = np.array(sort_position[1], dtype=int), sort_value[1]
        del sort_position[0], sort_value[0]

        # Determine repeated or not
        if all(np.equal(tar, ref)):
            after_cascade[tuple(tar)] = tar_val + ref_val
        elif (not all(np.equal(tar, ref))) and (len(sort_value) == 1):
            after_cascade[tuple(tar)] = tar_val
            after_cascade[tuple(ref)] = ref_val
        else:
            after_cascade[tuple(tar)] = tar_val

        # Indicator
        if (all_pos - len(sort_value) + 1) % 100  == 0:
            print('{:.6f} %'.format(float(all_pos - len(sort_value) + 1) / all_pos * 100))

    c_end   = time.time()
    print("Lack {:d} Cascade took {:.3f} secs\n".format(lack, c_end-c_start))

    #================================================
    # Save result
    print("Saving result ...\n")
    chdir(out_dir)
    np.save("{:d}d_after_smooth_casacade_dict".format(int(dim-lack)), np.array(after_cascade))
    chdir('../')
