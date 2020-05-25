#!/usr/bin/python
'''
------------------------------------------------------------------------------------------------------------
Example: [program] [dim] [cube size] [sigma] [bond] [ref-D] [band_inp] [fixed_band_id] [lower_bd] [upper_bd] [n_thread]
    Input Variables:
    [dim]:           dimension for smooth (for now only "6")
    [cube size]:     length of multi-d cube in magnitude unit
    [sigma]:         standard deviation for gaussian dist. in magnitude
    [bond]:          boundary radius of gaussian beam unit in cell
    [ref-D]:         reference dimension which to modulus other dimension to
    [band_inp]:      band used to do smooth in string e.g. 012345
    [fixed_band_id]: index of band that fixed when calculating with different origins
    [lower_bd]:      bound of input bands except fixed one (unit:cell) e.g. "0,0,0,0,0" or "default"
    [upper_bd]:      bound of input bands except fixed one (unit:cell) e.g. "9,9,9,9,9" or "default"
    [n_thread]:      number of thread for parallel computation
------------------------------------------------------------------------------------------------------------
Latest Updated: 2020.05.26 Jordan Wu'''

# Import Modules
#==========================================================
from __future__ import print_function
from sys import argv, exit
from os import chdir
from Useful_Functions import *
from Hsieh_Functions import *
from joblib import Parallel, delayed
import numpy as np
import time

# Functions
#==========================================================
def generate_6D_origins_on_plane(band_inp, sc_fixed_bd, sc_lower_bd, sc_upper_bd):
    '''
    This is used to generate origins on specific plane (fixed one band)
    This is especially for 6D case, for more/less dimension, number of list element must be modified
    '''
    bd_list = []
    for i in range(len(sc_lower_bd)):
        # Note upper_bd here already out of the 6D space, no needs to +1 in np.arange func
        bd_list.append(np.arange(sc_lower_bd[i], sc_upper_bd[i], 1))
    origin_list = []
    xx = np.meshgrid(bd_list[0], bd_list[1], bd_list[2], bd_list[3], bd_list[4])
    x0, x1, x2, x3, x4 = xx[0], xx[1], xx[2], xx[3], xx[4]
    xx0, xx1, xx2, xx3, xx4 = x0.flatten(), x1.flatten(), x2.flatten(), x3.flatten(), x4.flatten()
    for j in range(len(x0.flatten())):
        new_origin = [xx0[j], xx1[j], xx2[j], xx3[j], xx4[j]]
        new_origin.insert(sc_fixed_bd, 0)
        origin_list.append(np.array(new_origin))
    return origin_list

def generate_probe_line(origin, probe_vec, band_upper_bd):
    '''
    This is used to generate line array along probe vector direction
    Here assuming probe vector components are "all positive" or "all negative"
    Here input origin should start on "0" of the fixed band
    '''
    # Initialize probe vector direction
    probe_vec = np.array(probe_vec)
    if np.all(np.less_equal(probe_vec, np.zeros(len(band_upper_bd)))):
        probe_vec = -1 * probe_vec
    # Prevent infinite loops
    if np.any(np.less(probe_vec, np.zeros(len(band_upper_bd)))):
        exit('Wrong probe vector ...')
    # Larger than origin
    probe_line, pos, i = [], origin, 1
    while np.all(np.less(pos, band_upper_bd-0.5)):
        probe_line.append(pos)
        pos = origin + (i * probe_vec)
        i += 1
    # Round and store in array
    probe_round = np.rint(probe_line)
    probe_line  = np.array(probe_round, dtype=int)
    return probe_line

def get_gp_along_line(probe_line, gal_pos, gal_num):
    '''
    This is used to get galaxy probability along probe line
    '''
    gp_along_line = []
    for i in range(len(probe_line)):
        probe_pos = probe_line[i]
        loc_id = find_pos_id_in_gal_pos(gal_pos, probe_pos)
        if (len(loc_id) == 1):
            num = float(gal_num[loc_id])
        elif (len(loc_id) == 0):
            num = 0.
        else:
            exit('Wrong loc_id ...')
        gp_along_line.append(num)
    gp_along_line = np.array(gp_along_line)
    return gp_along_line

def find_gp_boundary(probe_line, gp_along_line):
    '''
    This is used to find two boundary end in one probe cut set
    '''
    ids = np.array([i for i in range(len(gp_along_line))], dtype=int)
    loc_GE1_id = ids[gp_along_line >= 1.0]
    if (len(loc_GE1_id) != 0) and (len(loc_GE1_id) != len(gp_along_line)):
        lower_gp_bound = probe_line[loc_GE1_id[0]]
        upper_gp_bound = probe_line[loc_GE1_id[-1]]
    elif (len(loc_GE1_id) == len(gp_along_line)):
        lower_gp_bound = probe_line[0]
        upper_gp_bound = probe_line[-1]
    else:
        lower_gp_bound = [np.nan] * len(probe_line[0])
        upper_gp_bound = [np.nan] * len(probe_line[0])
    return lower_gp_bound, upper_gp_bound

def find_bd_of_diff_origins(index, len_origin, origin, probe_vec, band_upper_bd, gal_pos, gal_num, gp_lower_bd_list, gp_upper_bd_list):
    '''
    This is to combine all above functions (for parallel computation)
    '''
    # Main calculation
    probe_line    = generate_probe_line(origin, probe_vec, band_upper_bd)
    gp_along_line = get_gp_along_line(probe_line, gal_pos, gal_num)
    gp_lower_bd, gp_upper_bd = find_gp_boundary(probe_line, gp_along_line)
    if np.nan not in gp_lower_bd:
        gp_lower_bd_list.append(gp_lower_bd)
        gp_upper_bd_list.append(gp_upper_bd)
    # Indicator
    if (index >= 100) and (index % 100 == 0):
        print('{} / {}'.format(index, len_origin))

# Main Program
#==========================================================
if __name__ == '__main__':
    s_start = time.time()

    # Check inputs
    if len(argv) != 11:
        exit('\n\tError: Wrong Arguments\
        \n\tExample: [program] [dim] [cube size] [sigma] [bond] [ref-D] [band_inp] [fixed_band_id] [lower_bd] [upper_bd] [n_thread]\
        \n\t[dim]: dimension for smooth (for now only "6")\
        \n\t[cube size]: length of multi-d cube in magnitude unit\
        \n\t[sigma]: standard deviation for gaussian dist. in magnitude\
        \n\t[bond]: boundary radius of gaussian beam unit in cell\
        \n\t[ref-D]: reference dimension which to modulus other dimension to\
        \n\t[band_inp]: band used to do smooth in string e.g. 012345\
        \n\t[fixed_band_id]: index of band that fixed when calculating with different origins\
        \n\t[lower_bd]: bound of input bands except fixed one (unit:cell) e.g. "0,0,0,0,0" or "default"\
        \n\t[upper_bd]: bound of input bands except fixed one (unit:cell) e.g. "9,9,9,9,9" or "default"\
        \n\t[n_thread]: number of thread for parallel computation\n')

    # Input variables
    dim         = int(argv[1])       # Dimension of position vector
    cube        = float(argv[2])     # Beamsize for each cube
    sigma       = int(argv[3])       # STD for Gaussian Smooth
    bond        = int(argv[4])       # Bond for Gaussian Smooth
    refD        = int(argv[5])       # Reference Beam Dimension
    band_inp    = str(argv[6])       # Input band ids
    sc_fixed_bd = int(argv[7])       # Fixed band id
    n_thread    = int(argv[10])      # Number of threads to parallel computation
    posv_dir    = 'GPV_{:d}Dposvec_bin{:.1f}/'.format(dim, cube)
    out_prefix  = 'GPV_after_smooth_{:d}D_bin{:.1f}_sigma{:d}_bond{:d}_refD{:d}'.format(dim, cube, sigma, bond, refD)
    out_dir     = '{}/'.format(out_prefix)

    # Load arrays for calculations
    probe_vec0    = [0] * (len(band_inp)-1); probe_vec0.insert(sc_fixed_bd, 1)
    gal_pos       = np.load(out_dir + 'after_smooth_lack_{}_{}_all_cas_pos.npy'.format(dim-len(band_inp), band_inp))
    gal_num       = np.load(out_dir + 'after_smooth_lack_{}_{}_all_cas_num.npy'.format(dim-len(band_inp), band_inp))
    shape         = np.load(posv_dir + 'Shape.npy')
    band_upper_bd = np.array([int(shape[int(ind)]) for ind in band_inp])
    band_lower_bd = np.array([0 for ind in band_inp])
    sc_lower_bd   = [0 for i in range(len(band_inp)-1)]
    sc_upper_bd   = [shape[int(i)] for i in band_inp if int(i) != sc_fixed_bd]

    # Use different origins to find boundaries
    origin_list = generate_6D_origins_on_plane(band_inp, sc_fixed_bd, sc_lower_bd, sc_upper_bd)
    len_origin  = len(origin_list)
    print('\nFixed band id: {}\nOrigins lower bound: {}\nOrigins upper bound: {}\n# of origins: {:d}\n'.format(\
            sc_fixed_bd, sc_lower_bd, sc_upper_bd, len_origin))

    # Parallel Computing (Note: require='sharedmen' is essential for list parallel)
    gp_lower_bd_list, gp_upper_bd_list = [], []
    Parallel(n_jobs=n_thread, require='sharedmem')\
            (delayed(find_bd_of_diff_origins)\
            (i, len_origin, origin_list[i], probe_vec0, band_upper_bd, gal_pos, gal_num, gp_lower_bd_list, gp_upper_bd_list)\
            for i in range(len_origin))

    # Non-Parallel method (Just for backup)
    # gp_lower_bd_list, gp_upper_bd_list = [], []
    # for i, origin in enumerate(origin_list):
        # find_bd_of_diff_origins(origin, probe_vec0, band_upper_bd, gal_pos, gal_num)
        # drawProgressBar(float(i+1)/len(origin_list))

    # Store boundaries
    gp_lower_bounds = np.array(gp_lower_bd_list)
    gp_upper_bounds = np.array(gp_upper_bd_list)
    chdir(out_dir)
    np.save('after_smooth_{:d}D_lower_bounds_AlB{:d}'.format(dim, sc_fixed_bd), gp_lower_bounds)
    np.save('after_smooth_{:d}D_upper_bounds_AlB{:d}'.format(dim, sc_fixed_bd), gp_upper_bounds)
    chdir('../')

    # Print out result ...
    s_end   = time.time()
    print('\nFinding {:d}D boundary took {:.3f} secs\
           \nAverage time for each probe: {:.3f} secs\n'.format(dim, s_end - s_start, (s_end-s_start)/len(origin_list)))
