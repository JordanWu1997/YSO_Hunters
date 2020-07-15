#!/usr/bin/python
'''-----------------------------------------------------------------------------------
This program is for calculating 6D galaxy probability (P) by GP Dict

Example: [program] [dimension] [cube size] [GP_dict] [input catalog] [cloud name] [datatype] [qua]

Input Variables:
    [dimension]:     dim of magnitude space (for now only "6")
    [cube size]:     length of cube (unit: mag)
    [GP_dict]:       Galaxy probability dictionary (specific file or "default")
    [input catalog]: must include magnitudes
    [cloud name]:    cloud name of input catalog
    [datatype]:      "mag" or "flux" input data in magnitude or flux (mJy)
    [qua]:           if qua label is taken into calculation (True/False)

# Note:
    For Assignment of GP value and objecttype, check README.md

--------------------------------------------------------------------------------------
latest update: 2019/07/14 Jordan Wu'''

# Import Modules
#==============================================================================
from __future__ import print_function
from sys import argv, exit
from All_Variables import *
from Hsieh_Functions import *
from Useful_Functions import *
import SOP_Program_Path as spp
from Calculate_GP_WI_6D_Bound_Array import Remove_AGB
import numpy as np
import time

# Global Variables
#==============================================================================
band_ID    = [0, 3, 4, 5, 6, 7]
band_name  = band_name
psf_ID     = psf_ID
flux_ID    = flux_ID
mag_ID     = mag_ID
MP1_ID     = qua_ID_Spitzer[4]
JHK_system = 'ukidss'
# Use Limit Stored in Hsieh_Functions
Jaxlim   = Hsieh_Jaxlim
Ksaxlim  = Hsieh_Ksaxlim
Haxlim   = [0, 0]         # Not Mentioned in Hsieh
IR1axlim = Hsieh_IR1axlim
IR2axlim = Hsieh_IR2axlim
IR3axlim = Hsieh_IR3axlim
IR4axlim = Hsieh_IR4axlim
MP1axlim = Hsieh_MP1axlim
all_axlim  = [Jaxlim, Ksaxlim, Haxlim, IR1axlim, IR2axlim, IR3axlim, IR4axlim, MP1axlim]
axlim_list = [all_axlim[i] for i in band_ID]
# Galaxy Probability IDs
GP_OBJ_ID, GP_ID = 241, 242
GPP_OBJ_ID, GPP_ID = 243, 244
KEY_ID = 245
max_column_num = 246

# Functions
#==============================================================================
def GP_Dict_Pipeline(line, mag_list, PSF_list, cube, axlim_list=axlim_list):
    '''
    This is to generate objecttype and count by input magnitude list
    '''
    # Extract information from catalogs and set default values to output
    SEQ_vector = [sort_up_lack999(mag_list[i], axlim_list[i], cube) for i in range(len(axlim_list))]
    AGB_flag   = Remove_AGB(mag_list)
    Num        = dim - SEQ_vector.count(-999)
    Ob_type    = '{:d}bands_'.format(Num)
    Count      = 'no_count'
    KEY        = 'NO_KEY'
    # Remove AGB
    if AGB_flag == 'AGB':
        Count = 'no_count'
        Ob_type += 'AGB'
    else:
        # More than 3 band detection
        if Num >= 3:
            KEY, Key_array = tuple(SEQ_vector), np.array(SEQ_vector)
            ind_array = np.argwhere(Key_array==-999)
            # Faint sources
            if 9999 in SEQ_vector:
                Count    = 1e4
                Ob_type += 'Faint'
            # Bright sources
            elif -9999 in SEQ_vector:
                Count    = 1e-4
                Ob_type += 'Bright'
            # Use GP Dict
            else:
                try:
                    Count    = eval('L{}_Dict'.format(dim-Num))[KEY]
                    Ob_type += 'Lack_{}'.format(''.join([band_name[int(ind_array[i])]\
                                                    for i in range(len(ind_array))]))
                except KeyError:
                    Count    = 1e-3
                    Ob_type += '{:d}D_NOGALAXY_'.format(Num)
    # Avoid log(0)
    if Count == 0.0:
        Count = 1e-9
    # Find saturate candidates
    if lines[MP1_ID] == "S":
        Count = 1e-4
    # Record bandfill band number
    Ob_type += "bandfill=" + str(PSF_list.count("-2"))
    return Ob_type, Count, KEY

# Main Program
#======================================================
if __name__ == '__main__':
    t_start = time.time()

    # Check Input Variables
    if len(argv) != 8:
        exit('\n\tWrong Usage!\
              \n\tExample: [program] [dimension] [cube size] [GP_dict] [input catalog] [cloud name] [datatype] [qua]\
              \n\t[dimension]: dim of magnitude space (for now only "6")\
              \n\t[cube size]: length of cube (unit: mag)\
              \n\t[GP_dict]: Galaxy probability dictionary (specific file or "default")\
              \n\t[input catalog]: must include magnitudes if datatype is "mag"\
              \n\t[cloud name]: cloud name of input catalog\
              \n\t[datatype]: "mag" or "flux" input data in magnitude or flux (mJy)\
              \n\t[qua]: if qua label is taken into calculation (True/False)\n')

    # Input Variables
    dim          = int(argv[1])
    cube         = float(argv[2])
    GP_Dict_Path = str(argv[3])
    inp_catalog  = str(argv[4])
    Cloud_name   = str(argv[5])
    datatype     = str(argv[6])
    qualabel     = bool(argv[7] == 'True')

    # Load GP dict
    print('\nLoading GP_Dict ...')
    # Setup Galaxy Probability Dictionary Path
    if GP_Dict_Path == 'default':
        path = spp.Selfmade_6D_GP_Dict_path
    else:
        path = GP_Dict_Path
    print('GP_Dict: {}'.format(path))
    L0_Dict = np.load(path + 'all_detect_grid_Full_6d.npy').item()
    L1_Dict = np.load(path + 'all_detect_grid_Full_5d.npy').item()
    L2_Dict = np.load(path + 'all_detect_grid_Full_4d.npy').item()
    L3_Dict = np.load(path + 'all_detect_grid_Full_3d.npy').item()

    # Load Cloud Catalog
    print('Loading input catalog ...')
    with open(inp_catalog, 'r') as inp:
        catalog = inp.readlines()

    # Start calculating 6D Galaxy probabilty / Galaxy probability P
    print('Calculating 6D Galaxy Probability..')
    out_line = []
    for i in range(len(catalog)):
        drawProgressBar(float(i+1)/len(catalog))

        # Unit transformation
        lines = catalog[i].split()
        if datatype == 'flux':
            GP_mag_list  = mJy_to_mag(lines, flux_ID=flux_ID, Qua=qualabel, system=JHK_system)
            GPP_mag_list = mJy_to_mag(lines, flux_ID=flux_ID, Qua=qualabel, Psf=True, system=JHK_system)
        elif datatype == 'mag':
            GP_mag_list  = mag_to_mag(lines, mag_ID=mag_ID, Qua=qualabel, system=JHK_system)
            GPP_mag_list = mag_to_mag(lines, mag_ID=mag_ID, Qua=qualabel, Psf=True, system=JHK_system)
        else:
            exit('Input type error')

        # Generate GP/GPP from pipeline procedure
        PSF_list = [int(lines[psf_ID[i]]) for i in range(len(GP_mag_list))]
        GP_Ob_type,  GP_Count, KEY = GP_Dict_Pipeline(lines, GP_mag_list, PSF_list, cube)
        GPP_Ob_type, GPP_Count, _  = GP_Dict_Pipeline(lines, GPP_mag_list, PSF_list, cube)
        # Create some empty columns and Write GP/GPP type/value
        lines = fill_up_list_WI_z(lines, max_column_num=max_column_num)
        lines[GP_OBJ_ID]  = str(GP_Ob_type)
        lines[GP_ID]      = str(GP_Count)
        lines[GPP_OBJ_ID] = str(GPP_Ob_type)
        lines[GPP_ID]     = str(GPP_Count)
        lines[KEY_ID]     = str(','.join([str(ele) for ele in KEY]))
        out_line.append('\t'.join(lines))

    # Save to output catalog
    with open('{}_6D_GP_all_out_catalog.tbl'.format(Cloud_name), 'w') as out_catalog:
        out_lines = '\n'.join(out_line) + '\n'
        out_catalog.write(out_lines)
    t_end   = time.time()
    print('\n{} took {:.3f} secs\n'.format(str(argv[0]), t_end - t_start))
