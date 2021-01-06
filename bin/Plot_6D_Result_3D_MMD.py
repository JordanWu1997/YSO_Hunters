#!/usr/bin/env python
'''

'''

# Modules
#=====================================================================
import matplotlib.pyplot as plt
import numpy as np
from sys import exit, argv
from mpl_toolkits.mplot3d import Axes3D
from itertools import combinations
from os import system, chdir, path
from All_Variables import *

# Functions
#======================================================================
def process_table(path):
    '''
    This is to get 6D magnitude from input table
    '''
    output = []
    with open(path, 'r') as table:
        for line in table.readlines():
            output.append([float(line.split()[a]) for a in mag_ID_6D])
    output = np.array(output)
    return output

# Main Program
#======================================================================
if __name__ == '__main__':

    # Check inputs
    if len(argv) != 5:
        exit('\n\tWrong Input Argument!\
              \n\tExample: [program] [galaxy model] [GP method] [input catalog] [details]\
              \n\t[galaxy model]: catalog for galaxy model ["SEIP"/"SWIRE_2MASS_BR"/"2MASS"]\
              \n\t[GP method]: method to classify YSO ["GD"/"BD"]\
              \n\t[input catalog]: catalog for classification ["Original_HREL"/""]\
              \n\t[details]: detailed description for plotting [e.g. "6D_bin0.5_sigma2_bond0_refD5"]\n')
    else:
        print('Start plotting ...')

    mazu_path     = '/mazu/users/jordan/YSO_Project'
    out_par       = '/home/jordan/YSO_Project/Result'
    galaxy_model  = str(argv[1]) #'SWIRE' #SEIP #SWIRE_2MASS_BR
    GP_method     = str(argv[2]) #'BD' # GD
    input_catalog = str(argv[3]) #'Original_HREL' # ''
    details       = str(argv[4])  #'6D_bin0.5_sigma2_bond0_refD5'

    # Assign path variables
    GD_pos_num_path     = '{}/{}_GP_Bound/GPV_after_smooth_{}'.format(mazu_path, galaxy_model, details)
    BD_lower_upper_path = '{}/{}_GP_Bound/GPV_after_smooth_{}'.format(mazu_path, galaxy_model, details)
    All_YSO_path        = '{}/{}_GP_Bound/Cloud_Classification_GPM_{}_{}/{}/All_YSO'.format(\
                           mazu_path, galaxy_model, GP_method, input_catalog, details)
    out_prefix          = '{}_{}_{}_{}'.format(galaxy_model, GP_method, input_catalog, details)
    out_dir             = '{}/3D_MMD_{}_BDGY'.format(out_par, out_prefix)
    out_title           = out_prefix

    # Assign path variables
    path_GD_num     = '{}/after_smooth_lack_0_012345_all_cas_num.npy'.format(GD_pos_num_path)
    path_GD_pos     = '{}/after_smooth_lack_0_012345_all_cas_pos.npy'.format(GD_pos_num_path)
    path_lower      = '{}/after_smooth_lack_0_012345_6D_lower_bounds_AlB0.npy'.format(BD_lower_upper_path)
    path_upper      = '{}/after_smooth_lack_0_012345_6D_upper_bounds_AlB0.npy'.format(BD_lower_upper_path)
    path_new_YSO    = '{}/all_new_YSO.tbl'.format(All_YSO_path)
    path_new_LYSO   = '{}/all_new_LYSO.tbl'.format(All_YSO_path)
    path_new_UYSO   = '{}/all_new_UYSO.tbl'.format(All_YSO_path)
    path_new_NULYSO = '{}/all_new_NULYSO.tbl'.format(All_YSO_path)
    path_YSO_YSO    = '{}/all_YSO_and_Hsieh.tbl'.format(All_YSO_path)
    path_galaxy_YSO = '{}/all_YSO_not_Hsieh.tbl'.format(All_YSO_path)
    # path_5D_GD_num = './after_smooth_lack_0_012345_all_cas_num.npy' # C2D
    # path_5D_GD_pos = './after_smooth_lack_0_012345_all_cas_pos.npy' # C2D

    # Load BD boundary
    lower       = np.load(path_lower)
    upper       = np.load(path_upper)
    lower_limit = np.array([Hsieh_Jaxlim[0], Hsieh_IR1axlim[0], Hsieh_IR2axlim[0], Hsieh_IR3axlim[0], Hsieh_IR4axlim[0], Hsieh_MP1axlim[0]])
    upper_limit = np.array([Hsieh_Jaxlim[1], Hsieh_IR1axlim[1], Hsieh_IR2axlim[0], Hsieh_IR3axlim[0], Hsieh_IR4axlim[0], Hsieh_MP1axlim[0]])
    bound       = np.r_[upper, lower]
    bound       = np.array([bound[i] + lower_limit for i in range(len(bound))])

    # Load GD pos/num
    GD_num      = np.load(path_GD_num)
    GD_pos      = np.load(path_GD_pos)[GD_num >= 1.]
    GD_pos      = np.array([GD_pos[i] + lower_limit for i in range(len(GD_pos))])
    # GD_num_5D   = np.load(path_5D_GD_num)
    # GD_pos_5D   = np.load(path_5D_GD_pos)[GD_num_5D >= 1.]
    # GD_pos_5D   = np.array([GD_pos_5D[i] + lower_limit for i in range(len(GD_pos_5D))])

    # Load All YSO
    NY    = process_table(path_new_YSO)
    NLY   = process_table(path_new_LYSO)
    NUY   = process_table(path_new_UYSO)
    NNULY = process_table(path_new_NULYSO)
    YY    = process_table(path_YSO_YSO)
    GY    = process_table(path_galaxy_YSO)
    print(len(NY), len(NLY), len(NUY), len(NNULY))
    print(len(NY), len(YY), len(GY))

    # Initialize output directory
    if not path.isdir(out_dir):
        system('mkdir {}'.format(out_dir))
    chdir(out_dir)
    band = band_name_6D #['J', 'IR1', 'IR2','IR3', 'IR4', 'MP1']
    for comb in combinations([0, 1, 2, 3, 4, 5], 3):
        print(comb)
        b1, b2, b3 = tuple(comb)
        fig = plt.figure()
        axis = fig.gca(projection='3d')
        axis.scatter(bound[:, b1], bound[:, b2], bound[:, b3],label='BD', c='b', alpha=0.5)
        #axis.scatter(GD_pos[:, b1], GD_pos[:, b2], GD_pos[:,b3], label='GD', c='g', alpha=0.5)
        #axis.scatter(GD_pos_5D[:, b1], GD_pos_5D[:, b2], GD_pos_5D[:, b3], label='GD_5D', c='g', alpha=0.5)
        #axis.scatter(NY[:, b1], NY[:, b2], NY[:, b3], label='new_YSO', c='r', alpha=0.1)
        #axis.scatter(NLY[:, b1], NLY[:, b2], NLY[:, b3], label='new_YSO_LYSO', c='y', alpha=0.5)
        #axis.scatter(NUY[:, b1], NUY[:, b2], NUY[:, b3], label='new_YSO_UYSO', c='purple', alpha=0.5)
        #axis.scatter(NNULY[:, b1], NNULY[:, b2], NNULY[:, b3], label='new_YSO_NULYSO', c='cyan', alpha=0.5)
        #axis.scatter(YY[:, b1], YY[:, b2], YY[:, b3], label='YSO_and_Hsieh_YSO', c='lime', alpha=0.1)
        axis.scatter(GY[:, b1], GY[:, b2], GY[:, b3], label='YSO_not_Hsieh_YSO', c='orange', alpha=0.5)
        axis.legend()
        axis.set_xlabel(band[b1], fontsize=16)
        axis.set_ylabel(band[b2], fontsize=16)
        axis.set_zlabel(band[b3], fontsize=16)
        axis.set_title(out_title)
        plt.savefig('{:d}{:d}{:d}{}.png'.format(b1, b2, b3, out_prefix))
        #plt.show()
