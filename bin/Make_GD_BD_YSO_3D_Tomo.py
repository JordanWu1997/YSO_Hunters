#!/usr/bin/python
'''
----------------------------------------------------------------

Example: program [Shape array] [GD dict]
                 [BD lower array] [BD upper array]
                 [YSO catalog] [YSO method] [Output directory]

Input Variables:
    [Shape_name]      : Shape that stores multi-D space size
    [GD_dict_name]    : Dictionary from GD method
    [BD_l_array_name] : Lower bound array from BD method
    [BD_u_array_name] : Upper bound array from BD method
    [YSO_catalog_name]: YSO catalog containing position vector
    [YSO_method]      : Method to get YSO catalog (GD/BD)
    [out_dir]         : Out directory to store tomographys

----------------------------------------------------------------
Latest update 2020/08/05 Jordan Wu
'''

# Import Modules
#=======================================================
from __future__ import print_function
import time
import numpy as np
from sys import argv, exit
from os import system, chdir, path
from itertools import combinations
from argparse import ArgumentParser
from All_Variables import *
from Hsieh_Functions import *
from Useful_Functions import *
# For non-interactive backend (No request for showing pictures)
import matplotlib
matplotlib.use('Agg')
matplotlib.rc('figure', max_open_warning = 0)
import matplotlib.pyplot as plt

# Global Variables
#=======================================================
band_name = band_name
KEY_ID    = 245

# Functions
#=======================================================
# Load YSO catalog
def load_YSO_catalog(YSO_catalog_name, KEY_ID=245):
    '''
    This is to load pos vector on YSO catalog
    '''
    with open(YSO_catalog_name, 'r') as YSO_cat:
        YSO_catalog = YSO_cat.readlines()
    YSO_pos_list  = [YSO.split()[KEY_ID].split(',') for YSO in YSO_catalog]
    YSO_pos_array = np.array(YSO_pos_list)
    YSO_num_array = np.ones(len(YSO_pos_array))
    return YSO_pos_array, YSO_num_array

def load_GD_dict(GD_dict_name):
    '''
    This is to load pos/num on GD dictionary
    '''
    GD_dict = np.load(GD_dict_name, allow_pickle=True, encoding='bytes').item()
    GD_keys, GD_values = GD_dict.keys(), GD_dict.values()
    GD_pos_list = [np.array(key) for key in GD_keys]
    GD_num_list = GD_values
    GD_pos_array = np.array(GD_pos_list)
    GD_num_array = np.array(GD_num_list)
    return GD_pos_array, GD_num_array

def load_BD_bounds(BD_l_array_name, BD_u_array_name):
    '''
    This is to load boundary on BD l/u array
    Note: this only return combined total BD array
    '''
    BD_l_array = np.load(BD_l_array_name)
    BD_u_array = np.load(BD_u_array_name)
    BD_tot_pos_array = np.append(BD_l_array, BD_u_array, axis=0)
    BD_tot_num_array = np.ones(len(BD_tot_pos_array))
    return BD_tot_pos_array, BD_tot_num_array

##TODO
def fill_region_WI_BD_bounds():
    '''
    This is ignored for now ...
    '''
    pass

def sort_up_and_assign_num(pos_array, num_array, bd_ind, option):
    '''
    This is to sort up pos array and assign num array according to option
    '''
    sort_id, sort_pos = sort_up_array_element(pos_array[:, [bd_ind[0], bd_ind[1], [bd_ind[2]]]])
    if option == 'GD' or option == 'YSO':
        # Repeat ones should be cascades
        sort_num = num_array[sort_id]
        casc_pos, casc_num = cascade_array(sort_pos, sort_num)
        out_pos, out_num = casc_pos, casc_num
    elif option == 'BD':
        # Repeat ones should be excluded
        sort_num = num_array[sort_id]
        out_pos, out_num = sort_pos, sort_num
    return out_pos, out_num

def update_num_to_cube_array(inp_shape, inp_pos, inp_num):
    '''
    Update inp_num according to inp_pos to a cube array in inp_shape
    '''
    # Assign num for diff conditions
    bd1_pos, bd2_pos, bd3_pos = inp_pos[:, 0], inp_pos[:, 1], inp_pos[:, 2]
    bd1_len, bd2_len, bd3_len = inp_shape[0], inp_shape[1], inp_shape[2]
    cube_array = 0.0 * np.ones((bd1_len, bd2_len, bd3_len))
    for i in range(len(inp_pos)):
        cube_array[bd1_pos[i], bd2_pos[i], bd3_pos[i]] = inp_num[i]
    return cube_array

def get_cbar_label(inp_desc):
    '''
    This is to get color bar label based on input description
    '''
    cbar_label = None
    if inp_desc == 'GD':
        cbar_label = 'GP #'
    elif inp_desc == 'BD':
        cbar_label = 'Bound'
    elif inp_desc == 'YSO':
        cbar_label = 'YSO #'
    return cbar_label

def plot_along_band(shape, inp_title_list, inp_cube_list, inp_desc_list, bd_name, aband_axis):
    '''
    This is to plot 2D plot along specific band
    '''
    # Set up band id
    t_bd_id = aband_axis
    x_bd_id = aband_axis - 1
    y_bd_id = aband_axis - 2

    # Along band axis
    for i in range(inp_cube_list[0].shape[aband_axis]):
        drawProgressBar(float(i+1)/inp_cube_list[0].shape[aband_axis])

        # Select sliced input cube array
        if aband_axis == 0:
            plot_slice_list = [inp_cube[i, :, :] for inp_cube in inp_cube_list]
        elif aband_axis == 1:
            plot_slice_list = [inp_cube[:, i, :].T for inp_cube in inp_cube_list]
        elif aband_axis == 2:
            plot_slice_list = [inp_cube[:, :, i] for inp_cube in inp_cube_list]
        else:
            exit('Wrong input band index')

        # Start plotting
        # fig & axe1
        fig  = plt.figure()
        axe1 = plt.add_subplot(131)
        cax1 = axe1.imshow(plot_slice_list[0], origin='lower')
        cbar = fig.colorbar(cax, label=get_cmap(inp_desc_list[0]))
        axe1.set_title('{}: {} = {:d}'.format(inp_title_list[0], bd_name[t_bd_id], i))
        axe1.set_xlabel('{} ({:d})'.format(bd_name[x_bd_id], shape[x_bd_id]))
        axe1.set_ylabel('{} ({:d})'.format(bd_name[y_bd_id], shape[y_bd_id]))
        axe1.set_xticks(np.arange(0-0.5, shape[x_bd_id]+0.5, 1))
        axe1.set_yticks(np.arange(0-0.5, shape[y_bd_id]+0.5, 1))
        axe1.xaxis.set_ticklabels([0])
        axe1.yaxis.set_ticklabels([0])
        axe1.grid()

        # axe2
        axe2 = plt.add_subplot(132)
        cax2 = axe2.imshow(plot_slice_list[1], origin='lower')
        cbar = fig.colorbar(cax, label=get_cmap(inp_desc_list[1]))
        axe2.set_title('{}: {} = {:d}'.format(inp_title_list[1], bd_name[t_bd_id], i))
        axe2.set_xlabel('{} ({:d})'.format(bd_name[x_bd_id], shape[x_bd_id]))
        axe2.set_ylabel('{} ({:d})'.format(bd_name[y_bd_id], shape[y_bd_id]))
        axe2.set_xticks(np.arange(0-0.5, shape[x_bd_id]+0.5, 1))
        axe2.set_yticks(np.arange(0-0.5, shape[y_bd_id]+0.5, 1))
        axe2.xaxis.set_ticklabels([0])
        axe2.yaxis.set_ticklabels([0])
        axe2.grid()

        # axe3
        axe3 = plt.add_subplot(133)
        cax3 = axe3.imshow(plot_slice_list[2], origin='lower')
        cbar = fig.colorbar(cax, label=get_cmap(inp_desc_list[2]))
        axe3.set_title('{}: {} = {:d}'.format(inp_title_list[2], bd_name[t_bd_id], i))
        axe3.set_xlabel('{} ({:d})'.format(bd_name[x_bd_id], shape[x_bd_id]))
        axe3.set_ylabel('{} ({:d})'.format(bd_name[y_bd_id], shape[y_bd_id]))
        axe3.set_xticks(np.arange(0-0.5, shape[x_bd_id]+0.5, 1))
        axe3.set_yticks(np.arange(0-0.5, shape[y_bd_id]+0.5, 1))
        axe3.xaxis.set_ticklabels([0])
        axe3.yaxis.set_ticklabels([0])
        axe3.grid()

        # save fig
        plt.tight_layout()
        plt.savefig('{}_{:0>3d}'.format(bd_name[t_bd_id], i))
        plt.clf()

# Main Programs
#=======================================================
if __name__ == '__main__':
    m_start = time.time()

    # Check inputs
    parser = ArgumentParser(description='Make tomography that contains GD, BD, YSO respectively')
    parser.add_argument("Shape_array", type=str, help="Shape that stores multi-D space size")
    parser.add_argument("GD_dictionary", type=str, help="Dictionary from GD method")
    parser.add_argument("BD_lower_array", type=str, help="Lower bound array from BD method")
    parser.add_argument("BD_upper_array", type=str, help="Upper bound array from BD method")
    parser.add_argument("YSO_catalog", type=str, help="YSO catalog containing position vector")
    parser.add_argument("YSO_method", type=str, help="Method to get YSO catalog (GD/BD)")
    parser.add_argument("Out_directory", type=str, help="Out directory to store tomographys")

    # Load input from parser
    args             = parser.parse_args()
    Shape_name       = args.Shape_array
    GD_dict_name     = args.GD_dictionary
    BD_l_array_name  = args.BD_lower_array
    BD_u_array_name  = args.BD_upper_array
    YSO_catalog_name = args.YSO_catalog
    YSO_method       = args.YSO_method
    out_directory    = args.Out_dir

    # Load pos/num array from inputs
    Shape            = np.load(Shape_name)
    GD_pos, GD_num   = load_GD_dict(GD_dict_name)
    BD_pos, BD_num   = load_BD_bounds(BD_l_array_name, BD_u_array_name)
    YSO_pos, YSO_num = load_YSO_catalog(YSO_catalog_name)

    # Try different bands combination
    band_ind_list = np.arange(0, len(band_name), 1)
    for comb in combinations(band_ind_list, 3):
        print(comb)
        bd_ind = list(comb)
        band_ind = ''.join([str(i) for i in comb])

        # Sort up pos and assign new num
        GD_sort_pos, GD_sort_num   = sort_up_and_assign_num(GD_pos, GD_num, bd_ind, 'GD')
        BD_sort_pos, BD_sort_num   = sort_up_and_assign_num(BD_pos, BD_num, bd_ind, 'BD')
        YSO_sort_pos, YSO_sort_num = sort_up_and_assign_num(YSO_pos, YSO_num, bd_ind, 'GD')
        Proj_shape = Shape[bd_ind]

        # Generate 3D cube with value (num)
        GD_cube  = update_num_to_cube_array(Proj_shape, GD_sort_pos, GD_sort_num)
        BD_cube  = update_num_to_cube_array(Proj_shape, BD_sort_pos, BD_sort_num)
        YSO_cube = update_num_to_cube_array(Proj_shape, YSO_sort_pos, YSO_sort_num)

        # Generate list of objects prepared to be plotted
        inp_title_list = ['GD', 'BD', '{}_YSO'.format(YSO_method)]
        inp_cube_list  = [GD_cube, BD_cube, YSO_cube]
        inp_desc_list  = ['GD', 'BD', 'YSO']

        # Generate output directory
        if not path.isdir(out_dir):
            system('mkdir {}'.format(out_dir))
        chdir(out_dir)

        # Generate tomo dir for all combinations
        tomo_dir = 'tomo_{}/'.format(band_ind)
        if not path.isdir(tomo_dir):
            system('mkdir {}'.format(tomo_dir))
        chdir(tomo_dir)

        # Plot along axis-0
        print('axis-0')
        axis_dir = 'axis_{}/'.format(bd_ind[0])
        if not path.isdir(axis_dir):
            system('mkdir {}'.format(axis_dir))
        chdir(axis_dir)
        plot_along_band(Shape, inp_title_list, inp_cube_list, inp_desc_list, band_name, 0)
        chdir('../')
        system('convert -delay 20 -loop 0 {}*.png {}_axis_{}.gif'.format(axis_dir, band_ind, bd_ind[0]))

        # Plot along axis-1
        print('\naxis-1')
        axis_dir = 'axis_{}/'.format(bd_ind[1])
        if not path.isdir(axis_dir):
            system('mkdir {}'.format(axis_dir))
        chdir(axis_dir)
        plot_along_band(Shape, inp_title_list, inp_cube_list, inp_desc_list, band_name, 1)
        chdir('../')
        system('convert -delay 20 -loop 0 {}*.png {}_axis_{}.gif'.format(axis_dir, band_ind, bd_ind[1]))

        # Plot along axis-2
        print('\naxis-2')
        axis_dir = 'axis_{}/'.format(bd_ind[2])
        if not path.isdir(axis_dir):
            system('mkdir {}'.format(axis_dir))
        chdir(axis_dir)
        plot_along_band(Shape, inp_title_list, inp_cube_list, inp_desc_list, band_name, 2)
        chdir('../')
        system('convert -delay 20 -loop 0 {}*.png {}_axis_{}.gif'.format(axis_dir, band_ind, bd_ind[2]))
        chdir('../../')

    m_end   = time.time()
    print('\nWhole {} process took {:.3f} secs\n'.format(parser.prog, m_end-m_start))
