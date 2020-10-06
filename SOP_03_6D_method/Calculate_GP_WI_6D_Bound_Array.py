#!/usr/bin/python
'''
----------------------------------------------------------------
Example: [program] [catalog] [cloud\'s name] [inp_data_type] [galaxy lower bd] [galaxy upper bd] [cube size] [sigma] [bond] [refD]
Input Variables:
    [catalog]: input catalog for classification
    [cloud's name]: name of molecular cloud e.g. CHA_II
    [inp_data_type]: flux or mag [Note: flux unit "mJy"]
    [galaxy lower bd]: direct point to file or "default"
    [galaxy upper bd]: direct point to file or "default"
    [band_inp]: band used to do smooth in string e.g. 012345
    [cube size]: length of multi-d cube in magnitude unit
    [sigma]: standard deviation for gaussian dist. in magnitude
    [bond]: boundary radius of gaussian beam unit in cell
    [ref-D]: reference dimension which to modulus other dimension to
----------------------------------------------------------------
Latest update: 2020/05/26 Jordan Wu'''

# Import Modules
#======================================================================================
from __future__ import print_function
from sys import argv, exit
import numpy as np
import time
from All_Variables import *
from Hsieh_Functions import *
from Useful_Functions import *
import SOP_Program_Path as spp

# Global Variables
#======================================================================================
# band_ID    = [0, 3, 4, 5, 6, 7]
# GP_OBJ_ID, GP_ID = GP_OBJ_ID_6D, GP_ID_6D
# GPP_OBJ_ID, GPP_ID = GPP_OBJ_ID_6D, GPP_ID_6D

POS_VEC_ID = GP_KEY_ID_6D
# JHK photometry system
JHK_system = 'ukidss' #'2mass'
all_axlim  = full_axlim
axlim_list = [full_axlim[i] for i in band_ID]
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

def Cal_Position_Vector(row_list, data_type, Qua=True, Psf=False, system="ukidss"):
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
        mag_list = mJy_to_mag(row_list, flux_ID=flux_ID, qua_ID=qua_ID, Qua=Qua, Psf=Psf, system=system)
    elif data_type == 'mag':
        # Command below is for UKIDSS-SWIRE type catalog
        mag_list = mag_to_mag(row_list, mag_ID=mag_ID, qua_ID=qua_ID, Qua=Qua, Psf=Psf, system=system)

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

# def Check_GP_Lower_Bound(POS_vector, GP_Lower_Bound):
    # '''
    # This is to check if input is larger than the lower bound of galaxy probability
    # '''
    # no_lack_id_list = np.arange(0, len(POS_vector))[POS_vector != -999]
    # GP_Lower_Bound_flag = False
    # for no_lack_id in no_lack_id_list:
        # if GP_Lower_Bound_flag == True:
            # break
        # else:
            # for bound in GP_Lower_Bound:
                # if (POS_vector[no_lack_id] >= bound[no_lack_id]):
                    # GP_Lower_Bound_flag = True
                    # break
    # return GP_Lower_Bound_flag

# def Check_GP_Upper_Bound(POS_vector, GP_Upper_Bound):
    # '''
    # This is to check if input is smaller than the lower bound of galaxy probability
    # '''
    # no_lack_id_list = np.arange(0, len(POS_vector))[POS_vector != -999]
    # GP_Upper_Bound_flag = False
    # for no_lack_id in no_lack_id_list:
        # if GP_Upper_Bound_flag == True:
            # break
        # else:
            # for bound in GP_Upper_Bound:
                # if (POS_vector[no_lack_id] <= bound[no_lack_id]):
                    # GP_Upper_Bound_flag = True
                    # break
    # return GP_Upper_Bound_flag

def Check_GP_Lower_Bound(POS_vector, GP_Lower_Bound):
    '''
    This is to check if input is larger than the lower bound of galaxy probability
    '''
    no_lack_POSv = POS_vector[POS_vector != -999]
    GP_Lower_Bound_flag = False
    for bound in GP_Lower_Bound:
        no_lack_bound = bound[POS_vector != -999]
        if np.all(no_lack_POSv >= no_lack_bound):
            GP_Lower_Bound_flag = True
            break
    return GP_Lower_Bound_flag

def Check_GP_Upper_Bound(POS_vector, GP_Upper_Bound):
    '''
    This is to check if input is smaller than the lower bound of galaxy probability
    '''
    no_lack_POSv = POS_vector[POS_vector != -999]
    GP_Upper_Bound_flag = False
    for bound in GP_Upper_Bound:
        no_lack_bound = bound[POS_vector != -999]
        if np.all(no_lack_POSv <= no_lack_bound):
            GP_Upper_Bound_flag = True
            break
    return GP_Upper_Bound_flag

def Classification_Pipeline(GP_Lower_Bound, GP_Upper_Bound, row_list, data_type='mag', Qua=True, GP_PSF=False, system='ukidss'):
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
    POS_vector, OBJ_type, Count = Cal_Position_Vector(row_list, data_type=data_type, Qua=Qua, Psf=GP_PSF, system='ukidss')
    if Count == 'init':
        GP_Lower_Bound_flag = Check_GP_Lower_Bound(POS_vector, GP_Lower_Bound)
        GP_Upper_Bound_flag = Check_GP_Upper_Bound(POS_vector, GP_Upper_Bound)
        if (GP_Lower_Bound_flag) and (GP_Upper_Bound_flag):
            Count = 1e3;  OBJ_type += 'Galaxyc'
        elif (not GP_Lower_Bound_flag) and (GP_Upper_Bound_flag):
            Count = 1e-3; OBJ_type += 'LYSOc'
        elif (GP_Lower_Bound_flag) and (not GP_Upper_Bound_flag):
            Count = 1e-3; OBJ_type += 'UYSOc'
        else:
            Count = 1e-3; OBJ_type += 'IYSO'
    return OBJ_type, Count, POS_vector

def fill_up_list_WI_z(input_list, max_column_num=max_column_num):
    '''
    This is to fill up list with "z" to prevent list index error
    '''
    if len(input_list) != max_column_num:
        while len(input_list) <= max_column_num:
            input_list.append('z')
    return input_list

# Main Programs
#======================================================================================
if __name__ == '__main__':
    t_start = time.time()

    # Check inputs
    if len(argv) != 12:
        exit('\n\tError: Wrong Usage!\
            \n\tExample: [program] [catalog] [cloud\'s name] [inp_data_type] \\\
            \n\t\t [galaxy lower bd] [galaxy upper bd] [dim] [band_inp] [cube size] [sigma] [bond] [refD]\
            \n\t[catalog]: input catalog for classification\
            \n\t[cloud\'s name]: name of molecular cloud e.g. CHA_II\
            \n\t[inp_data_type]: flux or mag [Note: flux unit "mJy"]\
            \n\t[galaxy lower bd]: direct point to file or "default"\
            \n\t[galaxy upper bd]: direct point to file or "default"\
            \n\t[dim]: dimension of magnitude space (for now only "6")\
            \n\t[band_inp]: band used to do smooth in string e.g. 012345\
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
    galaxy_lower = str(argv[4])
    galaxy_upper = str(argv[5])
    dim          = int(argv[6])
    band_inp     = str(argv[7])
    bd_band_ax   = int(band_inp[0]) # Default first band of input bands
    cube         = float(argv[8])
    sigma        = int(argv[9])
    bond         = int(argv[10])
    refD         = int(argv[11])
    bound_path   = spp.Selfmade_6D_GP_BD_path

    # Lower bound array
    if galaxy_lower == 'default':
        suffix = 'AlB{:d}'.format(bd_band_ax) # suffix = 'PCA0'
        lower_bound_array = '{}GPV_after_smooth_{:d}D_bin{:.1f}_sigma{:d}_bond{:d}_refD{:d}/\
                            after_smooth_lack_{:d}_{}_{:d}D_lower_bounds_{}'.format(\
                            bound_path, dim, cube, sigma, bond, refD, dim-len(band_inp), band_inp, dim, suffix)
    else:
        lower_bound_array = galaxy_lower

    # Upper bound array
    if galaxy_upper == 'default':
        suffix = 'AlB{:d}'.format(bd_band_ax) # suffix = 'PCA0'
        upper_bound_array = '{}GPV_after_smooth_{:d}D_bin{:.1f}_sigma{:d}_bond{:d}_refD{:d}/\
                            after_smooth_lack_{:d}_{}_{:d}D_upper_bounds_{}'.format(\
                            bound_path, dim, cube, sigma, bond, refD, dim-len(band_inp), band_inp, dim, suffix)
    else:
        upper_bound_array = galaxy_upper

    # Load catalog and bounds ...
    l_start = time.time()
    print('\nLoading bounds and input catalogs ...')
    GP_Lower_Bound = np.load(lower_bound_array)
    GP_Upper_Bound = np.load(upper_bound_array)
    with open(catalog_name, 'r') as table:
        catalog = table.readlines()
    l_end   = time.time()
    print("Loading arrays took {:.3f} secs".format(l_end - l_start))

    # Start calculating 6D galaxy probability and 6D galaxy probability PSF
    t_start = time.time()
    print('\nStart Calculating 6D GP/GPP...')
    GP_tot_out = []
    for i in range(len(catalog)):
        row_list = catalog[i].split()
        GP_OBJ_type, GP_Count, Pos_vector = Classification_Pipeline(\
                                GP_Lower_Bound, GP_Upper_Bound, row_list, data_type='mag', Qua=True, GP_PSF=False, system='ukidss')
        GPP_OBJ_type, GPP_Count, _ = Classification_Pipeline(\
                                GP_Lower_Bound, GP_Upper_Bound, row_list, data_type='mag', Qua=True, GP_PSF=True, system='ukidss')
        row_list = fill_up_list_WI_z(row_list)
        row_list[GP_OBJ_ID], row_list[GP_ID] = str(GP_OBJ_type), str(GP_Count)
        row_list[GPP_OBJ_ID], row_list[GPP_ID] = str(GPP_OBJ_type), str(GPP_Count)
        row_list[POS_VEC_ID] = (','.join([str(PV) for PV in Pos_vector]))
        GP_tot_out.append('\t'.join(row_list))
        drawProgressBar(float(i+1)/len(catalog))
    t_end   = time.time()
    print('\nCalculating 6D_Gal_Prob took {:.3f} secs'.format(t_end - t_start))

    # Save galaxy probability results ...
    s_start = time.time()
    with open('{}_6D_BD_GP_out_catalog.tbl'.format(cloud_name), 'w') as GP_tot_out_catalog:
        GP_tot_out_catalog.write('\n'.join(GP_tot_out) + '\n')
    s_end   = time.time()
    print('Saving result took {:.3f} secs'.format(s_end - s_start))

    # Conclude all program time consumption
    t_end   = time.time()
    print('\nWhole {} process took {:.3f} secs\n'.format(str(argv[0]), t_end - t_start))
