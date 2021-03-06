#!/usr/bin/env python
'''
--------------------------------------------------------
Example: [program] [dim] [cube size] [sigma] [bond] [ref-D] [deg_slice] [inclination]
Input Variables:
    [dim]: dimension for smooth (for now only "6")
    [cube size]: length of multi-d cube in magnitude unit
    [sigma]: standard deviation for gaussian dist. in magnitude
    [bond]: boundary radius of gaussian beam unit in cell
    [ref-D]: reference dimension which to modulus other dimension to
    [deg_slice]: number of slices of position angle
    [inclination]: inclination degree of viewing angle

--------------------------------------------------------
Latest update 2020/07/16 Jordan Wu'''

from __future__ import print_function
from sys import argv, exit
from os import system
import time

# Programs' name
#=======================================================
GP2D_Plot = 'Make_Galaxy_Prob_2D_Plot.py'
GP3D_Plot = 'Make_Galaxy_Prob_3D_Plot.py'
GPPCA_Cut = 'Make_Galaxy_Prob_PCA_Cut_Plot.py'
GP3D_Plot_PCA = 'Make_Galaxy_Prob_3D_Plot_With_PCA.py'

# Main Program
#=======================================================
if __name__ == '__main__':
    t_start = time.time()

    if len(argv) != 8:
        exit('\n\tError: Wrong Arguments\
        \n\tExample: [program] [dim] [cube size] [sigma] [bond] [ref-D] [deg_slice] [inclination]\
        \n\t[dim]: dimension for smooth (for now only "6")\
        \n\t[cube size]: length of multi-d cube in magnitude unit\
        \n\t[sigma]: standard deviation for gaussian dist. in magnitude\
        \n\t[bond]: boundary radius of gaussian beam unit in cell\
        \n\t[ref-D]: reference dimension which to modulus other dimension to\
        \n\t[deg_slice]: number of slices of position angle\
        \n\t[inclination]: inclination degree of viewing angle\n')

    # Input variables
    dim        = int(argv[1])       # Dimension of position vector
    cube       = float(argv[2])     # Beamsize for each cube
    sigma      = int(argv[3])       # STD for Gaussian Smooth
    bond       = int(argv[4])
    refD       = int(argv[5])       # Reference Beam Dimension
    deg_slice  = int(argv[6])
    incli      = int(argv[7])

    # Make_Galaxy_Prob_2D_Plot.py
    system('{} {:d} {:.1f} {:d} {:d} {:d}'.format(\
            GP2D_Plot, dim, cube, sigma, bond, refD))

    # Make_Galaxy_Prob_3D_Plot.py
    system('{} {:d} {:.1f} {:d} {:d} {:d} {:d} {:d}'.format(\
            GP3D_Plot, dim, cube, sigma, bond, refD, deg_slice, incli))

    # # Make_Galaxy_Prob_PCA_Cut_Plot.py (Non-weighted, full cut and simple cut)
    # system('{} {:d} {:.1f} {:d} {:d} {:d} {} {} {} {}'.format(\
            # GPPCA_Cut, dim, cube, sigma, bond, refD, '0', ''.join([str(i) for i in range(dim)]), 'False', 'sc'))
    # system('{} {:d} {:.1f} {:d} {:d} {:d} {} {} {} {}'.format(\
            # GPPCA_Cut, dim, cube, sigma, bond, refD, '0', ''.join([str(i) for i in range(dim)]), 'False', 'fc'))

    # # Make_Galaxy_Prob_3D_Plot_With_PCA (Weigthed, Non-weighted)
    # system('{} {:d} {:.1f} {:d} {:d} {:d} {:d} {:d} {} {}'.format(\
            # GP3D_Plot_PCA, dim, cube, sigma, bond, refD, deg_slice, incli, 'False', 'True'))

    t_end   = time.time()
    print('{} took {:.3f} secs'.format(argv[0], t_end-t_start))
