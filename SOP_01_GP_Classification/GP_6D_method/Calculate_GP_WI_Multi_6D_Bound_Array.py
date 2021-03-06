#!/usr/bin/env python
'''
----------------------------------------------------------------
Example: [program] [catalog] [cloud\'s name] [inp_data_type] [galaxy lower bd] [galaxy upper bd] [dim] [cube size] [sigma] [bond] [refD]
Input Variables:
    [catalog]: input catalog for classification
    [cloud's name]: name of molecular cloud e.g. CHA_II
    [inp_data_type]: flux or mag [Note: flux unit "mJy"]
    [galaxy lower bd]: direct point to file or "default"
    [galaxy upper bd]: direct point to file or "default"
    [dim]: dimension of magnitude space (for now only "6")\
    [cube size]: length of multi-d cube in magnitude unit
    [sigma]: standard deviation for gaussian dist. in magnitude
    [bond]: boundary radius of gaussian beam unit in cell
    [ref-D]: reference dimension which to modulus other dimension to
----------------------------------------------------------------
Latest update: 2020/11/11 Jordan Wu'''

# Import Modules
#======================================================================================
from __future__ import print_function
from sys import argv, exit
import numpy as np
import time
import copy
from All_Variables import *
from Hsieh_Functions import *
from Useful_Functions import *
import SOP_Program_Path as spp

# Global Variables
#======================================================================================
band_ID    = [0, 3, 4, 5, 6, 7]
# GP_OBJ_ID, GP_ID = GP_OBJ_ID_6D, GP_ID_6D
# GPP_OBJ_ID, GPP_ID = GPP_OBJ_ID_6D, GPP_ID_6D
# POS_VEC_ID = GP_KEY_ID_6D

# JHK photometry system
JHK_system = 'ukidss' #'2mass'
axlim_list = [full_axlim_list[i] for i in band_ID]
name_list  = [full_band_name[i] for i in band_ID]
MP1_mag_ID = np.nan
IR2_mag_ID = np.nan
IR3_mag_ID = np.nan
if 'MP1' in name_list:
    MP1_mag_ID = name_list.index('MP1')
if 'IR2' in name_list:
    IR2_mag_ID = name_list.index('IR2')
if 'IR3' in name_list:
    IR3_mag_ID = name_list.index('IR3')
MP1_qua_ID = qua_ID_Spitzer[4]

# Functions
#======================================================================================
def Remove_AGB(mag_list, IR2_mag_ID=IR2_mag_ID, IR3_mag_ID=IR3_mag_ID, MP1_mag_ID=MP1_mag_ID):
    '''
    This is to check if object in input catalog is AGB
    Input datatype: magnitude, int, int, int
    '''
    # Remove AGB
    AGB_flag = 'Not_AGB'
    if (IR2_mag_ID is not np.nan) and (IR3_mag_ID is not np.nan) and (MP1_mag_ID is not np.nan):
        if (mag_list[IR2_mag_ID] != 'no') and (mag_list[IR3_mag_ID] != 'no') and (mag_list[MP1_mag_ID] != 'no'):
            X23 = mag_list[IR2_mag_ID] - mag_list[IR3_mag_ID]
            Y35 = mag_list[IR3_mag_ID] - mag_list[MP1_mag_ID]
            if index_AGB(X23, Y35, [0, 0, 2, 5], [-1, 0, 2, 2]) < 0:
                AGB_flag = 'AGB'
    return AGB_flag

def Find_MP1_Saturate(row_list, MP1_qua_ID=MP1_qua_ID):
    '''
    This is to check if object in input catalog is saturate in MP1 band
    '''
    MP1_Sat_flag = 'Not_MP1_Sat'
    if row_list[MP1_qua_ID] == 'S':
        MP1_Sat_flag = 'MP1_Sat'
    return MP1_Sat_flag

# def Generate_Galaxy_Populated_Region(GP_Lower_Bound, GP_Upper_Bound, fixed_ax):
    # '''
    # This is to generate galaxy populated region by filled all points \
    # between two upper/lower boundaries.
    # '''
    # galaxy_populated_region = []
    # same_galaxy_num = 0
    # for lower, upper in zip(GP_Lower_Bound, GP_Upper_Bound):
        # if not np.all(lower == upper):
            # WO_fixed_ax = list(lower[:fixed_ax]) + list(lower[fixed_ax+1:])
            # for fixed_ax_pos in range(lower[fixed_ax], upper[fixed_ax]+1):
                # WI_fixed_ax = copy.deepcopy(WO_fixed_ax)
                # WI_fixed_ax.insert(fixed_ax, fixed_ax_pos)
                # galaxy_populated_region.append(np.array(WI_fixed_ax))
        # else:
            # galaxy_populated_region.append(lower)
            # same_galaxy_num += 1
    # return galaxy_populated_region, same_galaxy_num

# def Check_Within_GP_Bound(POS_vector, Galaxy_Populated_Region):
    # '''
    # This is to check if input is within galaxy populated region \
    # (galaxy boundary)
    # '''
    # no_lack_POSv = POS_vector[POS_vector != -999]
    # GP_Within_Bound_flag = False
    # for bound in Galaxy_Populated_Region:
        # no_lack_bound = bound[POS_vector != -999]
        # if np.all(no_lack_POSv == no_lack_bound):
            # GP_Within_Bound_flag = True
            # break
    # return GP_Within_Bound_flag

def Cal_Position_Vector(row_list, data_type, Qua=True, Psf=False):
    '''
    This is to calculate position vector and object types
    Count:
        "no_count"  : LESS3BD
        "no_count"  : AGB
        1e-5        : MP1_Sat
        1e-4        : Bright
        1e-3        : YSO
        1e4         : Faint
        1e3         : Galaxy
    '''
    # Transform input to magnitude
    if data_type == 'flux':
        mag_list = mJy_to_mag(row_list, flux_ID=flux_ID_6D, f0_list=f0_list_6D, qua_ID=qua_ID_6D, Qua=Qua, psf_ID=psf_ID_6D, Psf=Psf)
    elif data_type == 'mag':
        # Command below is for UKIDSS-SWIRE type catalog
        mag_list = mag_to_mag(row_list, mag_ID=mag_ID_6D, qua_ID=qua_ID_6D, Qua=Qua, psf_ID=psf_ID_6D, Psf=Psf)

    SEQ_vec      = [sort_up_lack999(mag_list[i], axlim_list[i], cube) for i in range(len(mag_list))]
    AGB_flag     = Remove_AGB(mag_list)
    MP1_Sat_flag = Find_MP1_Saturate(row_list)
    OBS_num      = len(axlim_list) - SEQ_vec.count(-999)
    OBJ_type     = str(OBS_num) + 'bands_'
    Count        = 'init'
    POS_vector   = np.array(SEQ_vec)

    if OBS_num < 3:
        Count = 'no_count'; OBJ_type += 'LESS3BD'
    else:
        if (AGB_flag == 'AGB'):
            Count = 'no_count'; OBJ_type += 'AGB'
        elif (AGB_flag == 'Not_AGB'):
            if (MP1_Sat_flag == 'MP1_Sat'):
                Count = 1e-5; OBJ_type += 'MP1_Sat'
            elif (SEQ_vec.count(-9999) > 0):
                Count = 1e-4; OBJ_type += 'Bright'
            elif (SEQ_vec.count(9999) > 0):
                Count = 1e4;  OBJ_type += 'Faint'
    return POS_vector, OBJ_type, Count

def Check_Boundary_Position_Along_Axis(POS_vector, GP_Lower_Bound, GP_Upper_Bound, fixed_ax):
    '''
    This is to find the location of boundary on probing axis
    '''
    POS_vector_ax, POS_ax = np.delete(POS_vector, fixed_ax), POS_vector[fixed_ax]
    GP_Lower_Bound_ax = np.delete(GP_Lower_Bound, fixed_ax, axis=1)
    GP_Upper_Bound_ax = np.delete(GP_Upper_Bound, fixed_ax, axis=1)
    # Find boundary point on probing axis
    POS_bd_ax, indicator = [], 0
    lack_ind = np.where(POS_vector_ax==-999)
    for i in range(len(GP_Lower_Bound_ax)):
        Lbd = GP_Lower_Bound_ax[i]
        Ubd = GP_Upper_Bound_ax[i]
        for ind in lack_ind:
            Lbd[ind], Ubd[ind] = -999, -999
        # Find corresponding points in galaxy populated region -> TBD
        if np.all(POS_vector_ax == Lbd) and np.all(POS_vector_ax == Ubd):
            POS_bd_ax.append(GP_Lower_Bound[i, fixed_ax])
            POS_bd_ax.append(GP_Upper_Bound[i, fixed_ax])
            break
        indicator += 1
    # If no corresponding boundary point
    if (indicator == len(GP_Lower_Bound_ax)):
        POS_bd_ax = np.nan
    return POS_bd_ax, POS_ax

def Assign_GP_num_and_objtype(POS_bd_ax, POS_ax):
    '''
    This is to assign GP value and object type based on the location on probing axis
    (1) Outside galaxy-populated region (at bright end)   -> BYSO
    (2) Within  galaxy-populated region (in the middle)   -> Galaxy
    (3) On both upper & lower boundary overlapped region  -> IGalaxy
    (3) Outside galaxy-populated region (at faint end)    -> FYSO
    (4) Not be coverd by any boundary (Isolated)          -> IYSO
    (5) No information on the fixed axis (No information) -> Other

    This code is modified from Jeremy Yang's work
    '''
    # No corresponding boundary -> Isolated YSO (IYSO)
    # Lack on fixed axis
    if POS_ax == -999:
        count = 0.
        label = 'Other'
    # Isolated
    elif POS_bd_ax is np.nan:
        count = 1e-3
        label = 'IYSOc'
    # POS=Lower POS=Upper -> Isolated galaxy / In the fringe of galaxy region (IGalaxy)
    elif (POS_bd_ax[0] == POS_ax) and (POS_bd_ax[1] == POS_ax):
        count = 1e3
        label = 'IGalaxyc'
    # POS<Lower bd -> Outside galaxy region (BYSO)
    elif (POS_bd_ax[0] > POS_ax):
        count = 1e-3
        label = 'BYSOc'
    # POS>Upper bd -> Outside galaxy region (FYSO)
    elif (POS_bd_ax[1] < POS_ax):
        count = 1e6
        label = 'FYSOc'
    # WITHIN galaxy region -> Galaxy (Galaxy)
    else:
        count = 1e3
        label = 'Galaxyc'
    return label, count

# def Classification_Pipeline(Galaxy_Populated_Region, row_list, data_type='mag', Qua=True, GP_PSF=False):
    # '''
    # This is to classify input object and return object type and galaxy probability
    # GP_PSF: Galaxy Probability PSF (Considering PSF for c2d catalog)
    # Count:
        # "not_count" : LESS3BD
        # "not_count" : AGB
        # 1e-5        : MP1_Sat
        # 1e-4        : Bright
        # 1e-3        : YSO
        # 1e4         : Faint
        # 1e3         : Galaxy
    # '''
    # POS_vector, OBJ_type, Count = Cal_Position_Vector(row_list, data_type=data_type, Qua=Qua, Psf=GP_PSF)
    # if Count == 'init':
        # GP_Within_Bound_flag = Check_Within_GP_Bound(POS_vector, Galaxy_Populated_Region)
        # if GP_Within_Bound_flag:
            # Count = 1e3;  OBJ_type += 'Galaxyc'
        # else:
            # Count = 1e-3; OBJ_type += 'YSOc'
    # return OBJ_type, Count, POS_vector

def Classification_Pipeline(GP_Lower_Bound, GP_Upper_Bound, row_list, fixed_ax=0, data_type='mag', Qua=True, GP_PSF=False):
    '''
    This is to classify input object and return object type and galaxy probability
    GP_PSF: Galaxy Probability PSF (Considering PSF for c2d catalog)
    Count:
        "not_count" : LESS3BD
        "not_count" : AGB
        1e-5        : MP1_Sat
        1e-4        : Bright
        1e-3        : YSO
        1e4         : Faint
        1e3         : Galaxy
    '''
    POS_vector, OBJ_type, Count = Cal_Position_Vector(row_list, data_type=data_type, Qua=Qua, Psf=GP_PSF)
    if Count == 'init':
        POS_bd_ax, POS_ax = Check_Boundary_Position_Along_Axis(POS_vector, GP_Lower_Bound, GP_Upper_Bound, fixed_ax)
        AOBJ_type, Count = Assign_GP_num_and_objtype(POS_bd_ax, POS_ax)
        OBJ_type += AOBJ_type
    return OBJ_type, Count, POS_vector

# Main Programs
#======================================================================================
if __name__ == '__main__':
    t_start = time.time()

    # Check inputs
    if len(argv) != 10:
        exit('\n\tError: Wrong Usage!\
            \n\tExample: [program] [catalog] [cloud\'s name] [inp_data_type] \
            \n\t\t [bound_path] [dim] [cube size] [sigma] [bond] [refD]\
            \n\t[catalog]: input catalog for classification\
            \n\t[cloud\'s name]: name of molecular cloud e.g. CHA_II\
            \n\t[inp_data_type]: flux or mag [Note: flux unit "mJy"]\
            \n\t[bound_path]: absolute path to GP directory\
            \n\t[dim]: dimension of magnitude space (for now only "6")\
            \n\t[cube size]: length of multi-d cube in magnitude unit\
            \n\t[sigma]: standard deviation for gaussian dist. in magnitude\
            \n\t[bond]: boundary radius of gaussian beam unit in cell\
            \n\t[ref-D]: reference dimension which to modulus other dimension to\n')
    else:
        print('\nStart calculating GP with 6D bound array ...')

    # Input variables
    catalog_name = str(argv[1])
    cloud_name   = str(argv[2])
    data_type    = str(argv[3])
    bound_path   = str(argv[4])
    dim          = int(argv[5])
    cube         = float(argv[6])
    sigma        = int(argv[7])
    bond         = int(argv[8])
    refD         = int(argv[9])

    # Load catalog and bounds ...
    l_start = time.time()
    print('\nLoading input catalogs ...')
    with open(catalog_name, 'r') as table:
        catalog = table.readlines()

    # Load all boundaries
    GP_Lower_Bound_list = []
    GP_Upper_Bound_list = []
    GP_OBJ_ID_list, GP_ID_list = [], []
    GPP_OBJ_ID_list, GPP_ID_list = [], []
    POS_VEC_ID_list = []
    for bd_band_ax in range(dim):
        # Setup output
        GP_OBJ_ID, GP_ID = eval('GP_OBJ_ID_6D_{:d}'.format(bd_band_ax)), eval('GP_ID_6D_{:d}'.format(bd_band_ax))
        GPP_OBJ_ID, GPP_ID = eval('GPP_OBJ_ID_6D_{:d}'.format(bd_band_ax)), eval('GPP_ID_6D_{:d}'.format(bd_band_ax))
        POS_VEC_ID = eval('GP_KEY_ID_6D_{:d}'.format(bd_band_ax))
        # Lower bound array
        lower_bound_array = '{}/GPV_after_smooth_{:d}D_bin{:.1f}_sigma{:d}_bond{:d}_refD{:d}/after_smooth_lack_{:d}_{}_{:d}D_lower_bounds_AlB{}.npy'.format(\
                                bound_path, dim, cube, sigma, bond, refD, 0,\
                                ''.join([str(i) for i in range(dim)]), dim, bd_band_ax)
        # Upper bound array
        upper_bound_array = '{}/GPV_after_smooth_{:d}D_bin{:.1f}_sigma{:d}_bond{:d}_refD{:d}/after_smooth_lack_{:d}_{}_{:d}D_upper_bounds_AlB{}.npy'.format(\
                                bound_path, dim, cube, sigma, bond, refD, 0,\
                                ''.join([str(i) for i in range(dim)]), dim, bd_band_ax)
        # Load all bound arrray
        GP_Lower_Bound = np.load(lower_bound_array)
        GP_Upper_Bound = np.load(upper_bound_array)
        # Append to list
        GP_Lower_Bound_list.append(GP_Lower_Bound)
        GP_Upper_Bound_list.append(GP_Upper_Bound)
        GP_OBJ_ID_list.append(GP_OBJ_ID)
        GP_ID_list.append(GP_ID)
        GPP_OBJ_ID_list.append(GPP_OBJ_ID)
        GPP_ID_list.append(GPP_ID)
        POS_VEC_ID_list.append(POS_VEC_ID)
    l_end   = time.time()
    print("Loading catalog and galaxy boundary took {:.3f} secs".format(l_end - l_start))

    # Start calculating 6D galaxy probability and 6D galaxy probability PSF
    c_start = time.time()
    print('\nStart Calculating 6D GP/GPP...')
    GP_tot_out = []
    for i in range(len(catalog)):
        row_list = catalog[i].split()
        row_list = fill_up_list_WI_z(row_list, max_column_num=max_column_num)
        for j in range(dim):
            GP_OBJ_type, GP_Count, Pos_vector = Classification_Pipeline(\
                                                GP_Lower_Bound_list[j], GP_Upper_Bound_list[j],\
                                                row_list, data_type='mag', Qua=True, GP_PSF=False,\
                                                fixed_ax=j)
            GPP_OBJ_type, GPP_Count, Pos_vector = Classification_Pipeline(\
                                                GP_Lower_Bound_list[j], GP_Upper_Bound_list[j],\
                                                row_list, data_type='mag', Qua=True, GP_PSF=True,\
                                                fixed_ax=j)
            row_list[GP_OBJ_ID_list[j]], row_list[GP_ID_list[j]] = str(GP_OBJ_type), str(GP_Count)
            row_list[GPP_OBJ_ID_list[j]], row_list[GPP_ID_list[j]] = str(GPP_OBJ_type), str(GPP_Count)
            row_list[POS_VEC_ID_list[j]] = (','.join([str(PV) for PV in Pos_vector]))
        GP_tot_out.append('\t'.join(row_list))
        drawProgressBar(float(i+1)/len(catalog))
    c_end   = time.time()
    print('\nCalculating 6D_Gal_Prob took {:.3f} secs'.format(c_end - c_start))

    # Save galaxy probability results ...
    s_start = time.time()
    with open('{}_6D_multi_BD_GP_out_catalog.tbl'.format(cloud_name), 'w') as GP_tot_out_catalog:
        GP_tot_out_catalog.write('\n'.join(GP_tot_out) + '\n')
    s_end   = time.time()
    print('Saving result took {:.3f} secs'.format(s_end - s_start))

    # Conclude all program time consumption
    t_end   = time.time()
    print('\nWhole {} process took {:.3f} secs\n'.format(str(argv[0]), t_end - t_start))
