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
Latest Updated: 2020.09.19 Jordan Wu'''

# Import Modules
#==========================================================
from __future__ import print_function
from sys import argv, exit
from os import chdir
from argparse import ArgumentParser
from joblib import Parallel, delayed
import numpy as np
import time
from All_Variables import *
from Useful_Functions import *
from Hsieh_Functions import *

# Functions
#==========================================================
def generate_origins_on_plane(shape, band_inp, sc_fixed_bd, sc_lower_bd, sc_upper_bd):
    '''
    This is used to generate origins on specific plane (fixed one band)
    This is especially for 6D case, for more/less dimension, number of list element must be modified
    '''
    # Generate boundary list of each band
    bd_list = []
    for i in range(len(sc_lower_bd)):
        # Note upper_bd here already out of the 6D space, no needs to +1 in np.arange func
        bd_list.append(list(np.arange(sc_lower_bd[i], sc_upper_bd[i], 1)))
    # Generate origins and put -999 to lack band
    xx  = eval('np.meshgrid{}'.format(tuple([bd for bd in bd_list])))
    XX  = np.array([xx[i].flatten() for i in range(len(xx))])
    XXT = np.transpose(XX)
    fixed_bd_ID = band_inp.index(str(sc_fixed_bd))
    origin_list = []
    for i in range(len(XXT)):
        new_origin = list(XXT[i])
        new_origin.insert(fixed_bd_ID, 0)
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

def get_gp_along_line(lack_ind_list, probe_line, gal_pos, gal_num):
    '''
    This is used to get galaxy probability along probe line
    '''
    gp_along_line = []
    for i in range(len(probe_line)):
        # Assign -999 to lack band
        probe_pos = list(probe_line[i])
        for lack_ind in lack_ind_list:
            probe_pos.insert(lack_ind, -999)
        probe_pos = np.array(probe_pos)
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

# def get_gp_along_line_and_delete_pos(probe_line, gal_pos, gal_num):
    # '''
    # This is used to get galaxy probability along probe line
    # But this took forever to replace gal_pos, gal_num
    # '''
    # gp_along_line = []
    # for i in range(len(probe_line)):
        # probe_pos = probe_line[i].reshape(1, len(probe_line[i]))
        # loc_id = find_pos_id_in_gal_pos(gal_pos, probe_pos)
        # loc_id = find_pos_id_in_gal_pos_KD_Tree(gal_pos, probe_pos)
        # if (len(loc_id) == 1):
            # num = float(gal_num[loc_id])
            # gal_pos = np.delete(gal_pos, loc_id[0])
            # gal_num = np.delete(gal_num, loc_id[0])
        # elif (len(loc_id) == 0):
            # num = 0.
        # else:
            # exit('Wrong loc_id ...')
        # gp_along_line.append(num)
    # gp_along_line = np.array(gp_along_line)
    # return gp_along_line

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

def find_bd_of_diff_origins(index, len_origin, origin, probe_vec, \
                            lack_ind_list, band_upper_bd, gal_pos, \
                            gal_num, gp_lower_bd_list, gp_upper_bd_list):
    '''
    This is to combine all above functions (for parallel computation)
    '''
    # Main calculation
    probe_line    = generate_probe_line(origin, probe_vec, band_upper_bd)
    gp_along_line = get_gp_along_line(lack_ind_list, probe_line, gal_pos, gal_num)
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
    p_start = time.time()

    # Check inputs
    parser = ArgumentParser(description='Find galaxy boundary in multi-D magnitude space', \
                            epilog='For indice for input band and fixed band: J[0], IR1[1], IR2[2], IR3[3], IR4[4], MP1[5]')
    parser.add_argument('dim', type=int, help='Dim of input position vector')
    parser.add_argument('cube', type=float, help='Length of binning size (One decimal place)')
    parser.add_argument('sigma', type=int, help='Standard deviation of gaussian smooth (unit: bin)')
    parser.add_argument('bond', type=int, help='Cutoff radius of guassian smooth (unit: bin)')
    parser.add_argument('refD', type=int, help='Reference dimension for gaussian smooth')
    parser.add_argument('band_inp', type=str, help='Indice of bands to use (e.g 12345)')
    # parser.add_argument('sc_fixed_band', type=int, help='Index of band fixed to generate plane to find boundary')
    parser.add_argument('-n_th', '--Number_of_Thread', type=int, dest='n_thread', default=10, \
                        help='Number of thread for parallel computation')
    parser.add_argument('-posv_dir', '--Position_Vector_Directory', type=str, dest='posv_dir', \
                        help='Directory that stores galaxy position vector and mutl-D space shape')
    parser.add_argument('-out_dir', '--Output_Directory', dest='out_dir', \
                        type=str, help='Directory that stores output boundaries')

    # Load input from parser
    args        = parser.parse_args()
    dim         = args.dim
    cube        = args.cube
    sigma       = args.sigma
    bond        = args.bond
    refD        = args.refD
    band_inp    = args.band_inp
    # sc_fixed_bd = args.sc_fixed_band
    n_thread    = args.n_thread
    posv_dir    = args.posv_dir
    out_dir     = args.out_dir
    if posv_dir is None:
        posv_dir = 'GPV_{:d}Dposvec_bin{:.1f}/'.format(dim, cube)
    if out_dir is None:
        out_prefix  = 'GPV_after_smooth_{:d}D_bin{:.1f}_sigma{:d}_bond{:d}_refD{:d}'.format(dim, cube, sigma, bond, refD)
        out_dir     = '{}/'.format(out_prefix)
    print('\nGalaxy Position Vector Directory: {}\
           \nOutput Boundary Directory:        {}'.format(posv_dir, out_dir))

    # Load arrays for calculations
    # probe_vec0    = [0] * (len(band_inp)-1); probe_vec0.insert(sc_fixed_bd, 1)
    probe_vec0    = [1] * dim
    shape         = np.load(posv_dir + 'Shape.npy')
    band_upper_bd = np.array([int(shape[int(ind)]) for ind in band_inp])
    band_lower_bd = np.array([0 for ind in band_inp])

    sc_lower_bd_list, sc_upper_bd_list = [], []
    for i in range(dim):
        sc_fixed_bd = i
        sc_lower_bd = [0 for i in range(len(band_inp)-1)]
        sc_upper_bd = [shape[int(i)] for i in band_inp if int(i) != sc_fixed_bd]
        sc_lower_bd_list.append(sc_lower_bd)
        sc_upper_bd_list.append(sc_upper_bd)

    # Generate lack band index list
    all_ind_list  = [i for i in range(dim)]
    inp_ind_list  = [int(band_inp[i]) for i in range(len(band_inp))]
    lack_ind_list = []
    for ind in all_ind_list:
        if ind not in inp_ind_list:
            lack_ind_list.append(ind)

    # Galaxy position vector and number (Remove pos with num < 1.0 to increase efficiency)
    print('\nLoad galaxy position vectors and correspoding values ...')
    gal_pos = np.load(out_dir + 'after_smooth_lack_{}_{}_all_cas_pos.npy'.format(dim-len(band_inp), band_inp))
    gal_num = np.load(out_dir + 'after_smooth_lack_{}_{}_all_cas_num.npy'.format(dim-len(band_inp), band_inp))
    gal_pos = gal_pos[gal_num >= 1.0]
    gal_num = gal_num[gal_num >= 1.0]

    # Use different origins to find boundaries
    print('\nGenerate origins on multi-D magnitude space ...')
    origin_lists = []
    tot_len_origin = 0
    for i in range(dim):
        sc_fixed_bd = i
        origin_list = generate_origins_on_plane(shape, band_inp, sc_fixed_bd, sc_lower_bd_list[i], sc_upper_bd_list[i])
        len_origin  = len(origin_list)
        print('\nFixed band id: {}\nOrigins lower bound: {}\nOrigins upper bound: {}\n# of origins: {:d}'.format(\
                sc_fixed_bd, sc_lower_bd, sc_upper_bd, len_origin))
        origin_lists += origin_list
        tot_len_origin += len_origin
    print('\nTotal {:d} direction:\nOrigins lower bound: {}\nOrigins upper bound: {}\n# of origins: {:d}'.format(\
            dim, sc_lower_bd, sc_upper_bd, tot_len_origin))
    p_end   = time.time()
    print('\nGenerate mult-d origins took {:.3f} secs'.format(p_end-p_start))

    # Parallel Computing (Note: require='sharedmen' is essential for list parallel)
    s_start = time.time()
    print('\nStart finding boundary ...\n')
    gp_lower_bd_list, gp_upper_bd_list = [], []
    Parallel(n_jobs=n_thread, require='sharedmem')\
            (delayed(find_bd_of_diff_origins)\
            (i, tot_len_origin, origin_lists[i], probe_vec0, lack_ind_list, \
            band_upper_bd, gal_pos, gal_num, gp_lower_bd_list, gp_upper_bd_list)\
            for i in range(tot_len_origin))

    # Store boundaries
    gp_lower_bounds = np.array(gp_lower_bd_list)
    gp_upper_bounds = np.array(gp_upper_bd_list)
    chdir(out_dir)
    np.save('after_smooth_lack_{:d}_{}_{:d}D_lower_bounds_AlDiag'.format(\
            dim-len(band_inp), band_inp, dim, sc_fixed_bd), gp_lower_bounds)
    np.save('after_smooth_lack_{:d}_{}_{:d}D_upper_bounds_AlDiag'.format(\
            dim-len(band_inp), band_inp, dim, sc_fixed_bd), gp_upper_bounds)
    chdir('../')

    # Print out result ...
    s_end   = time.time()
    print('\nWhole Finding {:d}D boundary took {:.3f} secs\
           \nAverage time for each probe: {:.3f} secs\n'.format(\
           dim, s_end-p_start, (s_end-s_start)/len(origin_list)))
