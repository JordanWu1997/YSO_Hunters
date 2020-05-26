#!/usr/bin/python
'''
----------------------------------------------------------------

----------------------------------------------------------------
latest update: Jordan Wu'''
#======================================================================================
# Setup initial environment
#======================================================================================
from __future__ import print_function
from Hsieh_Functions import *
from Useful_Functions import *
import SOP_Program_Path as spp
from sys import argv, exit
import numpy as np
import time

#======================================================================================
# Input variables
#======================================================================================
# Check inputs
if len(argv) != 8:
    exit('\n\tError: Wrong Usage!\
          \n\tExample: [program] [catalog] [cloud\'s name] [inp_data_type] [cube size] [sigma] [bond] [refD]\
          \n\t[catalog]: input catalog for classification\
          \n\t[cloud\'s name]: name of molecular cloud e.g. CHA_II\
          \n\t[inp_data_type]: flux or mag [Note: flux unit "mJy"]\
          \n\t[cube size]: length of multi-d cube in magnitude unit\
          \n\t[sigma]: standard deviation for gaussian dist. in magnitude\
          \n\t[bond]: boundary radius of gaussian beam unit in cell\
          \n\t[ref-D]: reference dimension which to modulus other dimension to\n')

# ARGV Inputs
catalog_name = str(argv[1])
cloud_name   = str(argv[2])
data_type    = str(argv[3])
# Galaxy Bound Quantity
dim   = 6
cube  = float(argv[4])
sigma = int(argv[5])
bond  = int(argv[6])
refD  = int(argv[7])
# Input Catalog Quantity IDs
mag_ID = [35, 98, 119, 140, 161, 182]
qua_ID = [37, 100, 121, 142, 163, 184]
psf_ID = [38, 102, 123, 144, 165, 186]
IR2_ID, IR3_ID, MP1_ID = mag_ID[2], mag_ID[3], mag_ID[5]
# Hsieh's limit
Jaxlim     = Hsieh_Jaxlim
IR1axlim   = Hsieh_IR1axlim
IR2axlim   = Hsieh_IR2axlim
IR3axlim   = Hsieh_IR3axlim
IR4axlim   = Hsieh_IR4axlim
MP1axlim   = Hsieh_MP1axlim
axlim_list = [Jaxlim, IR1axlim, IR2axlim, IR3axlim, IR4axlim, MP1axlim]

#=====================================
#TODO Finish the path in SPP
#=====================================
# Galaxy_Bound_Path
GP_OBJ_ID, GP_ID = 241, 242
GPP_OBJ_ID, GPP_ID = 243, 244
bound_path = spp.Selfmade_6D_GP_Path

# Different suffix for different methods to create bound array
# suffix = 'PCA0'
suffix = 'AlB{:d}'.format(0)

lower_bound_array = '{}GPV_after_smooth_{:d}D_bin{:.1f}_sigma{:d}_bond{:d}_refD{:d}/after_smooth_{:d}D_lower_bounds_{}'.format(\
                    bound_path, dim, cube, sigma, bond, refD, suffix)
upper_bound_array = '{}GPV_after_smooth_{:d}D_bin{:.1f}_sigma{:d}_bond{:d}_refD{:d}/after_smooth_{:d}D_upper_bounds_{}'.format(\
                    bound_path, dim, cube, sigma, bond, refD, suffix)
#=====================================

# Functions
#======================================================================================
def Remove_AGB(mag_list, IR2_mag=2, IR3_mag=3, MP1_mag=5):
    '''
    This is to check if object in input catalog is AGB
    Input datatype: magnitude, int, int, int
    '''
    # Remove AGB
    AGB_flag = 'Not_AGB'
    if (mag_list[IR2_mag] != 'no') and (mag_list[IR3_mag] != 'no') and (mag_list[MP1_mag] != 'no'):
        X23 = mag_list[IR2_mag] - mag_list[IR3_mag]
        Y35 = mag_list[IR3_mag] - mag_list[MP1_mag]
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
    '''
    # Transform input to magnitude
    if data_type == 'flux':
        mag_list = mJy_to_mag(row_list, flux_ID=flux_ID, qua_ID=qua_ID, Qua=Qua, Psf=Psf, system=system)
    elif data_type == 'mag':
        # Command below is for UKIDSS-SWIRE type catalog
        mag_list = mag_to_mag(row_list, mag_ID=mag_ID, qua_ID=qua_ID, Qua=Qua, Psf=Psf, system=system)

    SEQ_vec      = [sort_up_lack999(mag_list[i], axlim_list[i], cube) for i in range(len(axlim_list))]
    AGB_flag     = Remove_AGB(mag_list)
    MP1_Sat_flag = Find_MP1_Saturate(mag_list)
    OBS_num      = len(axlim_list) - SEQ_vec.count(-999)
    OBJ_type     = str(num) + 'bands_'
    Count        = 'no_count'
    POS_vector   = np.array(SEQ_vec)

    if (MP1_Sat_flag == 'MP1_Sat'):
        Count = -999999; OBJ_type += 'MP1_Sat'
    elif (AGB_flag == 'AGB'):
        Count = np.nan; OBJ_type += 'AGB'
    elif (AGB_flag != 'AGB'):
        if (OBS_num < 3):
            Count = np.nan; OBJ_type += 'LESS3BD'
        elif (OBS_num >= 3) and (AGB_flag != 'AGB'):
            if SEQ_vec.count(9999) > 0:
                Count = 9999; OBJ_type += 'Faint'
            elif SEQ_vec.count(-9999) > 0:
                Count = -9999; OBJ_type += 'Bright'
    return POS_vector, OBJ_type, Count

def Check_GP_Lower_Bound(POS_vector, GP_Lower_Bound):
    '''
    This is to check if input is larger than the lower bound of galaxy probability
    '''
    no_lack_id_list = np.arange(0, len(GP_Lower_Bound))[POS_vector != -999]
    GP_Lower_Bound_flag = False
    for no_lack_id in no_lack_id_list:
        if GP_Lower_Bound_flag == True:
            break
        else:
            for bound in GP_Lower_Bound:
                if (POS_vector[no_lack_id] >= bound[no_lack_id]):
                    GP_Lower_Bound_flag = True
                    break
    return GP_Lower_Bound_flag

def Check_GP_Upper_Bound(POS_vector, GP_Upper_Bound):
    '''
    This is to check if input is smaller than the lower bound of galaxy probability
    '''
    no_lack_id_list = np.arange(0, len(GP_Upper_Bound))[POS_vector != -999]
    GP_Upper_Bound_flag = False
    for no_lack_id in no_lack_id_list:
        if GP_Upper_Bound_flag == True:
            break
        else:
            for bound in GP_Upper_Bound:
                if (POS_vector[no_lack_id] <= bound[no_lack_id]):
                    GP_Upper_Bound_flag = True
                    break
    return GP_Upper_Bound_flag

def Classification_Pipeline(GP_Lower_Bound, GP_Upper_Bound, row_list, data_type='flux', Qua=True, GP_PSF=False, system='ukidss'):
    '''
    This is to classify input object and return object type and galaxy probability
    GP_PSF: Galaxy Probability PSF (Considering PSF for c2d catalog)
    '''
    POS_vector, OBJ_type, Count = Cal_Position_Vector(row_list, data_type=data_type, Qua=Qua, Psf=GP_PSF, system='ukidss')
    if (Count != -999999) and (Count != np.nan) and (Count != 9999) and (Count != -9999):
        GP_Lower_Bound_flag = Check_GP_Lower_Bound(POS_vector, GP_Lower_Bound)
        GP_Upper_Bound_flag = Check_GP_Upper_Bound(POS_vector, GP_Upper_Bound)
        if (GP_Lower_Bound_flag) and (GP_Upper_Bound_flag):
            Count = 1e3
            OBJ_type += 'Galaxyc'
        elif (not GP_Lower_Bound_flag) and (GP_Upper_Bound_flag):
            Count = 1e-3
            OBJ_type += 'BYSOc'
        elif (GP_Lower_Bound_flag) and (not GP_Upper_Bound_flag):
            Count = 1e-3
            OBJ_type += 'FYSOc'
    return OBJ_type, Count

def fill_up_list_WI_z(input_list, max_length):
    '''
    This is to fill up list with "z" to prevent list index error
    '''
    if len(input_list) != max_length:
        while len(input_list) <= max_length:
            input_list.append('z')
    return input_list

# Main Programs
#======================================================================================
if __name__ == '__main__':

    # Load catalog and bounds ...
    l_start = time.time()
    print('\nLoading bounds and input catalogs ...')
    GP_Lower_Bound = np.load(lower_bound_array)
    GP_Upper_Bound = np.load(upper_bound_array)
    with open(catalog_name, 'r') as table:
        catalog = table.readlines()
    l_end   = time.time()
    print("\nLoading arrays took {:.3f} secs".format(l_end - l_start))

    # Start calculating 6D galaxy probability and 6D galaxy probability PSF
    t_start = time.time()
    print('\nStart Calculating ...')
    GP_tot_out = []
    for i in range(len(catalog)):
        row_list = catalog[i].split()

        GP_OBJ_type, GP_Count = Classification_Pipeline(\
                                GP_Lower_Bound, GP_Upper_Bound, row_list, data_type='flux', Qua=True, GP_PSF=False, system='ukidss')
        GPP_OBJ_type, GPP_Count = Classification_Pipeline(\
                                GP_Lower_Bound, GP_Upper_Bound, row_list, data_type='flux', Qua=True, GP_PSF=True, system='ukidss')

        row_list = fill_up_list_WI_z(row_list)
        row_list[GP_OBJ_ID], row_list[GP_ID] = str(GP_OBJ_type), str(GPP_Count)
        row_list[GPP_OBJ_ID], row_list[GPP_ID] = str(GPP_OBJ_type), str(GPP_Count)
        GP_tot_out.append('\t'.join(row_list))
        drawProgressBar(float(i+1)/len(catalog))
    t_end = time.time()
    print('\nCalculating 6D_Gal_Prob took {:.3f} secs'.format(t_end - t_start))

    # Save galaxy probability results ...
    s_start = time.time()
    with open(cloud_name + '_6D_GP_out_catalog.tbl', 'w') as GP_tot_out_catalog:
        GP_tot_out_catalog.write('\n'.join(GP_tot_out) + '\n')
    s_end   = time.time()
    print('Saving result took {:.3f} secs'.format(s_end - s_start))

    # Conclude all program time consumption
    print('\n{} all programs took {:.3f} secs\n'.format(s_end - l_start))
