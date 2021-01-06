#!/usr/bin/env python
'''
----------------------------------------------------------------

Example: program [Shape array] [GD dict]
                 [BD lower array] [BD upper array]
                 [YSO catalog]
                 [Output directory]

Input Variables:
    [Shape_name]      : Shape that stores multi-D space size
    [GD_dict_name]    : Dictionary from GD method
    [BD_l_array_name] : Lower bound array from BD method
    [BD_u_array_name] : Upper bound array from BD method
    [YSO_catalog_name]: YSO catalog containing position vector
    [out_dir]         : Out directory to store tomographys

----------------------------------------------------------------
Latest update 2020/08/05 Jordan Wu
'''

# Import Modules
#=======================================================
from __future__ import print_function, division
import time
import warnings
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
#=======================================================i
warnings.simplefilter(action='ignore', category=(FutureWarning, UserWarning))
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
    YSO_pos_list = []
    for YSO in YSO_catalog:
        YSO_pos_str = YSO.split()[KEY_ID].split(',')
        YSO_pos_int = [int(YSO_pos) for YSO_pos in YSO_pos_str]
        YSO_pos_list.append(YSO_pos_int)
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

def Check_GP_Lower_Bound(POS_vector, GP_Lower_Bound):
    '''
    This is to check if input is larger than the lower bound of galaxy probability
    '''
    no_lack_id_list = np.arange(0, len(POS_vector))[POS_vector != -999]
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
    no_lack_id_list = np.arange(0, len(POS_vector))[POS_vector != -999]
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

def fill_region_WI_LU_BD_bounds(shape, lower_bound_pos, upper_bound_pos):
    '''
    This is ignore for now
    '''
    pass

def sort_up_and_assign_num(pos_array, num_array, bd_ind, option):
    '''
    This is to sort up pos array and assign num array according to option
    '''
    # Remove lack, bright, faint
    no_lack_pos_list = []
    for pos in pos_array[:, [bd_ind[0], bd_ind[1], bd_ind[2]]]:
        if (-999 in pos) or (-9999 in pos) or (9999 in pos):
            continue
        else:
            no_lack_pos_list.append(pos)
    no_lack_pos_array = np.array(no_lack_pos_list)
    # Check length of pos_array
    out_pos, out_num = [], []
    if len(no_lack_pos_array) != 0:
        sort_id, sort_pos = sort_up_array_element(no_lack_pos_array)
        if ('GD' in option) or ('YSO' in option):
            # Repeat ones should be cascades
            sort_num = num_array[sort_id]
            casc_pos, casc_num = cascade_array(sort_pos, sort_num)
            out_pos, out_num = casc_pos, casc_num
        elif ('BD' in option):
            # Repeat ones should be excluded
            sort_num = num_array[sort_id]
            out_pos, out_num = sort_pos, sort_num
    out_pos_array, out_num_array = np.array(out_pos), np.array(out_num)
    return out_pos_array, out_num_array

def update_num_to_cube_array(inp_shape, inp_pos, inp_num):
    '''
    Update inp_num according to inp_pos to a cube array in inp_shape
    '''
    # Assign num for diff conditions
    bd1_len, bd2_len, bd3_len = inp_shape[0], inp_shape[1], inp_shape[2]
    cube_array = 0.0 * np.ones((bd1_len, bd2_len, bd3_len))
    if inp_shape != []:
        bd1_pos, bd2_pos, bd3_pos = inp_pos[:, 0], inp_pos[:, 1], inp_pos[:, 2]
        cube_array = 0.0 * np.ones((bd1_len, bd2_len, bd3_len))
        for i in range(len(inp_pos)):
            cube_array[bd1_pos[i], bd2_pos[i], bd3_pos[i]] = inp_num[i]
    return cube_array

def generate_cube_and_desc(proj_shape, inp_pos_list, inp_num_list, inp_desc_list, bd_ind):
    '''
    This is to generate cube and desc base on input pos/num and desc
    '''
    out_cube_list, out_desc_list = [], []
    if len(inp_pos_list) != 0:
        for i in range(len(inp_pos_list)):
            pos, num, desc = inp_pos_list[i], inp_num_list[i], inp_desc_list[i]
            sort_pos, sort_num = sort_up_and_assign_num(pos, num, bd_ind, desc)
            if len(sort_pos) != 0:
                cube = update_num_to_cube_array(proj_shape, sort_pos, sort_num)
                out_cube_list.append(cube)
                out_desc_list.append(desc)
    return out_cube_list, out_desc_list

def get_cbar_label(inp_desc):
    '''
    This is to get color bar label based on input description
    '''
    cbar_label = None
    if 'GD' in inp_desc:
        cbar_label = 'GP #'
    elif 'BD' in inp_desc:
        cbar_label = 'Bound = 1.0'
    elif 'YSO' in inp_desc:
        cbar_label = 'YSO # = 1.0'
    return cbar_label

def get_imshow_max(inp_desc):
    '''
    This is to get max value for imshow
    '''
    imshow_max = None
    if 'GD' in inp_desc:
        imshow_max = 5
    elif 'BD'in inp_desc:
        imshow_max = 1
    elif 'YSO' in inp_desc:
        imshow_max = 1
    return imshow_max

def discrete_cmap(N, base_cmap=None):
    '''
    Create an N-bin discrete colormap from the specified input map
    Author: jakevdp/discrete_cmap.py
    Link: https://gist.github.com/jakevdp/91077b0cae40f8f8244a
    '''
    # Note that if base_cmap is a string or None, you can simply do
    #    return plt.cm.get_cmap(base_cmap, N)
    # The following works for string, None, or a colormap instance:
    base = plt.cm.get_cmap(base_cmap)
    color_list = base(np.linspace(0, 1, N))
    cmap_name = base.name + str(N)
    return base.from_list(cmap_name, color_list, N)

def plot_along_band(shape, inp_cube_list, inp_desc_list, bd_name, aband_axis):
    '''
    This is to plot 2D plot along specific band
    '''
    # Set up band id and axe list
    t_bd_id = aband_axis
    x_bd_id = aband_axis - 1
    y_bd_id = aband_axis - 2
    axe_list = ['{:d}{:d}{:d}'.format(1, len(inp_desc_list), i+1) for i in range(len(inp_desc_list))]
    print('Plot along axis-{:d} (fig: {})'.format(ax, axe_list))

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

        # Start plotting fig
        fig  = plt.figure(figsize=(6*len(axe_list), 6))
        for j in range(len(axe_list)):
            axe  = fig.add_subplot(axe_list[j])
            cax  = axe.imshow(plot_slice_list[j], origin='lower',\
                              vmin=-0.5, vmax=get_imshow_max(inp_desc_list[j])+0.5, \
                              cmap=discrete_cmap(get_imshow_max(inp_desc_list[j])+1, base_cmap='hot'))
            cbar = fig.colorbar(cax, ticks=np.arange(0, get_imshow_max(inp_desc_list[j])+1, 1),\
                                label=get_cbar_label(inp_desc_list[j]))
            cbar.ax.set_yticklabels(list(np.arange(0, get_imshow_max(inp_desc_list[j])+1)))
            axe.set_title('{}\n{} = {:d}'.format(inp_desc_list[j], bd_name[t_bd_id], i))
            axe.set_xlabel('{} ({:d})'.format(bd_name[x_bd_id], shape[x_bd_id]))
            axe.set_ylabel('{} ({:d})'.format(bd_name[y_bd_id], shape[y_bd_id]))
            axe.set_xticks(np.arange(0-0.5, shape[x_bd_id]+0.5, 1))
            axe.set_yticks(np.arange(0-0.5, shape[y_bd_id]+0.5, 1))
            tick_res = 5
            x_tick_list = []
            for tick in range(shape[x_bd_id]):
                if tick % tick_res == 0 and tick >= tick_res:
                    x_tick_list.append(tick)
                else:
                    x_tick_list.append(' ')
            y_tick_list = []
            for tick in range(shape[y_bd_id]):
                if tick % tick_res == 0 and tick >= tick_res:
                    y_tick_list.append(tick)
                else:
                    y_tick_list.append(' ')
            axe.xaxis.set_ticklabels(x_tick_list)
            axe.yaxis.set_ticklabels(y_tick_list)
            axe.grid()
        plt.tight_layout()
        plt.savefig('{}_{:0>3d}'.format(bd_name[t_bd_id], i))
        plt.clf()

# Main Programs
#=======================================================
if __name__ == '__main__':
    mk_start = time.time()

    # Check inputs
    parser = ArgumentParser(description='Make tomography that contains GD, BD or YSO respectively', \
                            epilog='Note: If you want to fill region boundary covered,\
                                    please include "fill" in BDDesc option. \
                                    Multiple input BD, GD or YSO is allowed, but please remember\
                                    to add flag in the front of every optional argument.\
                                    Please at least choose one out of GD, BD and YSO')
    parser.add_argument('Shape_array', type=str, help='Shape that stores multi-D space size')
    parser.add_argument('-out_dir', '--Out_directory', dest='out_dir', default='output_tomo',\
                        help='Out directory to store tomographys')
    parser.add_argument('-GD', '--GDlist', action='append', dest='GD_list',\
                        help='GD method Galaxy probabilty dictionary')
    parser.add_argument('-GDDesc', '-GDDesclist', action='append', dest='GDDesc_list',\
                        help='Describe GD dictionary (Recommended: GD)')
    parser.add_argument('-BDlower', '--BDlowerlist', action='append', dest='BDl_list',\
                        help='BD method lower bound array')
    parser.add_argument('-BDupper', '--BDupperlist', action='append', dest='BDu_list',\
                        help='BD method upper bound array')
    parser.add_argument('-BDDesc', '--BDDesclist', action='append', dest='BDDesc_list',\
                        help='Describe BD boundary (Recommended: BD)')
    parser.add_argument('-YSO', '--YSOlist', action='append', dest='YSO_list',\
                        help='YSO catalog with position vector')
    parser.add_argument('-YSODesc', '--YSODesclist', action='append', dest='YSODesc_list',\
                        help='Describe YSO catalog (Recommeded: YSO + method')

    # Load input from parser
    args              = parser.parse_args()
    Shape_name        = args.Shape_array
    out_dir           = args.out_dir
    GD_dict_name_list = args.GD_list
    GDDesc_list       = args.GDDesc_list
    BD_l_name_list    = args.BDl_list
    BD_u_name_list    = args.BDu_list
    BDDesc_list       = args.BDDesc_list
    YSO_name_list     = args.YSO_list
    YSODesc_list      = args.YSODesc_list
    print('\n', args)

    # Load shape/pos/num/decs list
    Shape =  np.load(Shape_name)
    GD_pos_list, GD_num_list, GD_Desc_list = [], [], []
    if GD_dict_name_list is not None:
        for i in range(len(GD_dict_name_list)):
            GD_dict_name = GD_dict_name_list[i]
            GD_pos, GD_num = load_GD_dict(GD_dict_name)
            GD_pos_list.append(GD_pos)
            GD_num_list.append(GD_num)
            GD_Desc_list.append(GDDesc_list[i])
    BD_Desc_list = []
    BD_l_pos_list, BD_u_pos_list = [], []
    BD_tot_pos_list, BD_tot_num_list = [], []
    if BD_l_name_list is not None:
        for i in range(len(BD_l_name_list)):
            BD_l_name = BD_l_name_list[i]
            BD_u_name = BD_u_name_list[i]
            # TODO filll region within bounds
            # if 'fill' in BDDesc_list[i]: else:
            # BD_l_pos  = np.load(BD_l_name)
            # BD_u_pos  = np.load(BD_u_name)
            BD_tot_pos, BD_tot_num = load_BD_bounds(BD_l_name, BD_u_name)
            BD_tot_pos_list.append(BD_tot_pos)
            BD_tot_num_list.append(BD_tot_num)
            BD_Desc_list.append(BDDesc_list[i])

    YSO_pos_list, YSO_num_list, YSO_Desc_list = [], [], []
    if YSO_name_list is not None:
        for i in range(len(YSO_name_list)):
            YSO_catalog_name = YSO_name_list[i]
            YSO_pos, YSO_num = load_YSO_catalog(YSO_catalog_name)
            YSO_pos_list.append(YSO_pos)
            YSO_num_list.append(YSO_num)
            YSO_Desc_list.append(YSODesc_list[i])
    # Try different bands combination
    band_ind_list = np.arange(0, len(band_name), 1)
    # band_ind_list = [0, 1, 3]
    for comb in combinations(band_ind_list, 3):
        print('\n3D comb: {}'.format(str(comb)))
        bd_ind = list(comb)
        band_ind = ''.join([str(i) for i in comb])

        # Generate cube/desc list
        Proj_shape = Shape[bd_ind]
        inp_cube_list, inp_desc_list = [], []
        GD_cube_list, GD_desc_list = generate_cube_and_desc(Proj_shape, GD_pos_list, GD_num_list, GD_Desc_list, bd_ind)
        BD_cube_list, BD_desc_list = generate_cube_and_desc(Proj_shape, BD_tot_pos_list, BD_tot_num_list, BD_Desc_list, bd_ind)
        YSO_cube_list, YSO_desc_list = generate_cube_and_desc(Proj_shape, YSO_pos_list, YSO_num_list, YSO_Desc_list, bd_ind)

        inp_cube_list = GD_cube_list + BD_cube_list + YSO_cube_list
        inp_desc_list = GD_desc_list + BD_desc_list + YSO_desc_list
        # Generate output directory
        if not path.isdir(out_dir):
            system('mkdir {}'.format(out_dir))
        chdir(out_dir)
        tomo_dir = 'tomo_{}/'.format(band_ind)
        if not path.isdir(tomo_dir):
            system('mkdir {}'.format(tomo_dir))
        chdir(tomo_dir)

        # Plot along axis
        for ax in range(3):
            axis_dir = 'axis_{}'.format(bd_ind[ax])
            if not path.isdir(axis_dir):
                system('mkdir {}'.format(axis_dir))
            chdir(axis_dir)
            if len(inp_cube_list) != 0:
                plot_along_band(Proj_shape, inp_cube_list, inp_desc_list, band_name, ax)
                chdir('../')
                print('\nGenerate .gif file ...')
                system('convert -delay 50 -loop 0 {}/*.png {}_axis_{}.gif'.format(axis_dir, band_ind, bd_ind[ax]))
            else:
                print('\nNo Plottable Pos ...\n')
                break
        chdir('../../')

    mk_end   = time.time()
    print('\nWhole {} process took {:.3f} secs\n'.format(parser.prog, mk_end-mk_start))
