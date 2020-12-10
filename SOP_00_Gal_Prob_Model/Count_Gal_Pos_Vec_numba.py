#!/usr/bin/python
'''
-------------------------------------------------------
Example: [program] [input catalog] [catalog format] [datatype] [qua] [dimension] [cube size] [band_ID]
Input variables:
    [input catalog]: must include magnitudes
    [cat_forat]:     format of catalog (SEIP_JACOB/C2D_HSIEH)
    [datatype]:      "mag" or "flux" input data in magnitude or flux (mJy)
    [qualabel]:      if qua label is taken into calculation (True/False)
    [dimension]:     dim of magnitude space (for now only "6")
    [cube size]:     length of multi-d cube in magnitude unit
    [band_ID]:       band index to use in calculation (default: 034567)

-------------------------------------------------------
Latest update 2020.11.11 Jordan Wu'''

# Load Modules
#======================================================
from __future__ import print_function
import time
import numpy as np
from numba import jit
from sys import argv, exit
from os import chdir, system, path
from argparse import ArgumentParser
from All_Variables import *
from Hsieh_Functions import *
from Useful_Functions import *

# Global Variables
#======================================================
# JHK photometry system
JHK_system = 'ukidss' #'2mass'

# Functions
#======================================================
def Remove_AGB(mag_list, IR2_mag_ID, IR3_mag_ID, MP1_mag_ID):
    '''
    This is to check if object in input catalog is AGB
    Input datatype: magnitude, int, int, int
    '''
    # Initialize AGB flag
    AGB_flag = 'Not_AGB'
    # Remove AGB if IR2, IR3, MP1 band all exists in input
    if (IR2_mag_ID is not np.nan) and (IR3_mag_ID is not np.nan) and (MP1_mag_ID is not np.nan):
        if (mag_list[IR2_mag_ID] != 'no') and (mag_list[IR3_mag_ID] != 'no') and (mag_list[MP1_mag_ID] != 'no'):
            X23 = mag_list[IR2_mag_ID] - mag_list[IR3_mag_ID]
            Y35 = mag_list[IR3_mag_ID] - mag_list[MP1_mag_ID]
            if index_AGB(X23, Y35, [0, 0, 2, 5], [-1, 0, 2, 2]) < 0:
                AGB_flag = 'AGB'
    return AGB_flag

@jit(nopython=True)
def filter_bright_faint(pos_vec_array):
    '''
    This is to filter out bright, faint and sources we want
    Note: np.any can't do well
    '''
    bright = []
    faint  = []
    source = []
    for i in range(len(pos_vec_array)):
        pos_vec_array_sub = pos_vec_array[i]
        # Filiter out Bright/Faint Sources
        if np.shape(np.where(pos_vec_array_sub == -9999)[0])[0] > 0:
            bright.append(pos_vec_array_sub)
        elif np.shape(np.where(pos_vec_array_sub == 9999)[0])[0] > 0:
            faint.append(pos_vec_array_sub)
        else:
            source.append(pos_vec_array_sub)
    return bright, faint, source

@jit(nopython=True)
def cascade_array_pos(sort_position):
    '''
    Use this to find out sources locate in same position and cascade them
    Note: No tuple() support in numba, No format() support in numba
    '''
    # Input
    after_cascade_pos = []
    after_cascade_value = []
    start = 0
    end   = 0
    for i in range(len(sort_position)-1):
        # Get reference and target
        tar, ref = sort_position[i], sort_position[i+1]
        end += 1
        # Determine repeated or not
        if not np.all(np.equal(tar, ref)):
            after_cascade_pos.append(sort_position[start])
            after_cascade_value.append(end-start)
            start = end
    # Include the last term
    after_cascade_pos.append(sort_position[start])
    after_cascade_value.append(len(sort_position)-start)
    return after_cascade_pos, after_cascade_value

# Main Program
#======================================================
if __name__ == '__main__':

    # # Check inputs
    # if len(argv) != 7:
        # exit('\n\tError: Wrong Arguments\
        # \n\tExample: [program] [input catalog] [catalog format] [datatype] [qua] [dimension] [cube size]\
        # \n\t[input catalog]: must include magnitudes\
        # \n\t[catalog format]: format of catalog (SEIP_JACOB/C2D_HSIEH)\
        # \n\t[datatype]: "mag" or "flux" input data in magnitude or flux (mJy)\
        # \n\t[qua]: if qua label is taken into calculation (True/False)\
        # \n\t[dimension]: dim of magnitude space (for now only "6")\
        # \n\t[cube size]: length of multi-d cube in magnitude unit\n')
    # # Input variables
    # inpcat    = str(argv[1])
    # catformat = str(argv[2])
    # datatype  = str(argv[3])
    # qualabel  = bool(argv[4] == 'True')
    # dim       = int(argv[5])
    # cube      = float(argv[6])

    parser = ArgumentParser(description='Count binning galaxy position vector in multi-dimensional magnitude space',\
                            epilog='Band index: J[0], H[1], K[2], IR1[3], IR2[4], IR3[5], IR4[6], MP1[7]; Default: 034567')
    parser.add_argument('input_catalog', type=str, help='Input catalog (must include magnitudes if datatype is "mag")')
    parser.add_argument('cat_format', type=str, help='format of catalog (SEIP_JACOB/C2D_HSIEH)')
    parser.add_argument('datatype', type=str, help='"mag" or "flux" input data in magnitude or flux (mJy)')
    parser.add_argument('qualabel', type=str, help='if qua label is taken into calculation (True/False)')
    parser.add_argument('dimension', type=int, help='dim of magnitude space (for now only "6")')
    parser.add_argument('cube_size', type=float, help='length of multi-d cube (unit: magnitude)')
    parser.add_argument('-band_ID', '--band_index', type=str, dest='band_IDs', help='Band index to use in calculation (e.g. 012345)')

    args = parser.parse_args()
    inpcat    = args.input_catalog
    catformat = args.cat_format
    datatype  = args.datatype
    qualabel  = (args.qualabel == 'True')
    dim       = args.dimension
    cube      = args.cube_size
    band_IDs  = args.band_IDs

    if band_IDs is None:
        band_ID = band_ID
    else:
        band_ID = [int(ID) for ID in band_IDs]

    # For 6D GP (J, IR1, IR2, IR3, IR4, MP1)
    if catformat == 'SEIP_JACOB':
        flux_ID = band_ID
        mag_ID  = band_ID
    # For 6D GP (J, IR1, IR2, IR3, IR4, MP1)
    elif catformat == 'C2D_HSIEH':
        flux_ID = [full_flux_ID[ID] for ID in band_ID]
        mag_ID  = [full_mag_ID[ID] for ID in band_ID]
    else:
        exit('Wrong catalog format ...')

    # Setup parameters
    axlim_list = [full_axlim_list[ID] for ID in band_ID]
    name_list  = [full_band_name[ID] for ID in band_ID]
    MP1_mag_ID = np.nan
    IR2_mag_ID = np.nan
    IR3_mag_ID = np.nan
    if 'MP1' in name_list:
        MP1_mag_ID = name_list.index('MP1')
    if 'IR2' in name_list:
        IR2_mag_ID = name_list.index('IR2')
    if 'IR3' in name_list:
        IR3_mag_ID = name_list.index('IR3')

    # Check Directory
    if path.isdir('GPV_' + str(dim) + 'Dposvec_bin' + str(cube)):
        system('rm -fr GPV_' + str(dim) + 'Dposvec_bin' + str(cube))
        system('mkdir GPV_' + str(dim) + 'Dposvec_bin' + str(cube))
    else:
        system('mkdir GPV_' + str(dim) + 'Dposvec_bin' + str(cube))

    qua_ID = [full_qua_ID[ID] for ID in band_ID]
    bins_list = [int(round((full_axlim_list[i][1] - full_axlim_list[i][0]) / cube)) + 1 for i in band_ID]
    # Print out input information
    print('\nJHK system: {}\ncubesize: {:.1f}\nflux_ID: {}\nmag_ID: {}\nQua/Qua_ID: {}, {}\nShape: {}'.format(\
           JHK_system, cube, str(flux_ID), str(mag_ID), str(qualabel), str(qua_ID), str(bins_list)))

    # Load Galaxy Catalog
    l_start = time.time()
    print("\nLoading input catalog ...")
    with open(str(argv[1]), 'r') as catalogs:
        catalog = catalogs.readlines()
    l_end   = time.time()
    print("Loading catalog took {:.3f} secs\n".format(l_end-l_start))

    # Calculate Galaxy Position Vector
    c_start = time.time()
    pos_vec = []
    for i in range(len(catalog)):
        drawProgressBar(float(i+1)/len(catalog))
        # Unit transformation
        line = catalog[i]
        lines = line.split()
        if datatype == 'flux':
            mag_list = mJy_to_mag(lines, flux_ID=flux_ID, f0_list=f0_list, qua_ID=qua_ID, Qua=qualabel)
        elif datatype == 'mag':
            mag_list = mag_to_mag(lines, mag_ID=mag_ID, qua_ID=qua_ID, Qua=qualabel)
        else:
            exit('Input type error')
        SEQ_vector = [sort_up_lack999(mag_list[i], axlim_list[i], cube) for i in range(len(axlim_list))]
        AGB_flag   = Remove_AGB(mag_list, IR2_mag_ID, IR3_mag_ID, MP1_mag_ID)
        if AGB_flag != 'AGB':
            pos_vec.append(SEQ_vector)
    c_end   = time.time()
    print("\n\nCalculate all sources position in n-dim space took {:.3f} secs\n".format(c_end-c_start))

    # Galaxy filter
    f_start = time.time()
    pos_vec_array = np.array(pos_vec)
    bright, faint, source = filter_bright_faint(pos_vec_array)
    source_array = np.array(source)
    f_end   = time.time()
    print("Filter out bright and faint sources took {:.3f} secs\n".format(f_end-f_start))

    # Sort Input Galaxy Position/Probability array
    u_start = time.time()
    position_t = np.transpose(source_array)
    sort_ind = np.lexsort(tuple(position_t))
    sort_position = np.array(source_array[sort_ind], dtype=int)
    uni_pos, uni_num = cascade_array_pos(sort_position)
    uni_pos_array = np.array(uni_pos)
    uni_num_array = np.array(uni_num)
    u_end   = time.time()
    print("Sort sources took {:.3f} secs\n".format(u_end-u_start))

    # Save Galaxy Position Vector, Bright, Faint
    s_start = time.time()
    chdir('GPV_' + str(dim) + 'Dposvec_bin' + str(cube))
    np.save('Gal_Position_vectors', uni_pos_array)
    np.save('Gal_Position_numbers', uni_num_array)
    np.save('Bright', bright)
    np.save('Faint', faint)
    np.save('Shape', np.array(bins_list))
    chdir('../')
    s_end   = time.time()
    print("Saving Galaxy Position took {:.3f} secs\n".format(s_end-s_start))
