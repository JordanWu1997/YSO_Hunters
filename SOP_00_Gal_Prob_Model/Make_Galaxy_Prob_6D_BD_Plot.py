#!/usr/bin/env python
'''
----------------------------------------------------------------

Example: [program] [dim] [cube size] [sigma] [bond] [ref-D] [suffix]
Input variables:
    [dim]:       dimension for smooth (for now only "6")
    [cube size]: length of multi-d cube in magnitude unit
    [sigma]:     standard deviation for gaussian dist. in magnitude
    [bond]:      boundary radius of gaussian beam unit in cell
    [ref-D]:     reference dimension which to modulus other dimension to
    [suffix]:    suffix to bound array ("default" is "AlB0")
----------------------------------------------------------------
latest update:  2020.05.26 Jordan Wu'''

# Import Modules
#=======================================================
from __future__ import print_function
import time
import numpy as np
from sys import argv, exit
from os import system, chdir, path
from itertools import combinations
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
ctick_params = [[0.0, '=0'],\
                [1.0, '<1'],\
                [2.0, '=1'],\
                [3.0, '>1'],\
                [4.0, 'LB'],\
                [5.0, 'LB=UB'],\
                [6.0, 'UB']]

# Functions
#=======================================================
def generate_diff_comb_band_params(comb):
    '''
    This is to generate band parameters for different input combinations
    band_ind: band indice stored in "str"
    bd_id:    band indice stored in "int" in a LIST
    shape:    shape of selected 3 band dimensional magnitude space, stored in LIST
    bd_name:  name of band store in "str" in a LIST
    '''
    band_ind = ''
    for band in comb:
        band_ind += str(band)
    bd_ind, shape, bd_name = [], [], []
    for ind in band_ind:
        bd_ind.append(int(ind))
        shape.append(all_shape[int(ind)])
        bd_name.append(band_name[int(ind)])
    return band_ind, bd_ind, shape, bd_name

def update_num(gal_pos, gal_num, shape, ctick_params=ctick_params):
    '''
    Update gal num to a cube array with gal pos
    '''
    # Assign num for diff conditions
    val_list  = [params[0] for params in ctick_params]
    tick_list = [params[1] for params in ctick_params]
    E0_val = val_list[tick_list.index('=0')]
    G1_val = val_list[tick_list.index('>1')]
    E1_val = val_list[tick_list.index('=1')]
    L1_val = val_list[tick_list.index('<1')]
    bd1_pos, bd2_pos, bd3_pos = gal_pos[:, 0], gal_pos[:, 1], gal_pos[:, 2]
    bd1_len, bd2_len, bd3_len = shape[0], shape[1], shape[2]
    cube_array = E0_val * np.ones((bd1_len, bd2_len, bd3_len))
    for i in range(len(gal_num)):
        if gal_num[i] > 1.:
            cube_array[bd1_pos[i], bd2_pos[i], bd3_pos[i]] = G1_val
        elif gal_num[i] == 1.:
            cube_array[bd1_pos[i], bd2_pos[i], bd3_pos[i]] = E1_val
        elif gal_num[i] < 1.:
            cube_array[bd1_pos[i], bd2_pos[i], bd3_pos[i]] = L1_val
    return cube_array

def update_num_from_bounds(cube_array, lower_bound, upper_bound, ctick_params=ctick_params):
    '''
    Update lower/upper bound to previous 3D cube array
    '''
    lbd1_pos, lbd2_pos, lbd3_pos = lower_bound[:, 0], lower_bound[:, 1], lower_bound[:, 2]
    ubd1_pos, ubd2_pos, ubd3_pos = upper_bound[:, 0], upper_bound[:, 1], upper_bound[:, 2]
    val_list  = [params[0] for params in ctick_params]
    tick_list = [params[1] for params in ctick_params]
    LB_val    = val_list[tick_list.index('LB')]
    UB_val    = val_list[tick_list.index('UB')]
    LBUB_val  = val_list[tick_list.index('LB=UB')]
    for i in range(len(lower_bound)):
        cube_array[lbd1_pos[i], lbd2_pos[i], lbd3_pos[i]] = LB_val
    for i in range(len(upper_bound)):
        if cube_array[ubd1_pos[i], ubd2_pos[i], ubd3_pos[i]] == LB_val:
            cube_array[ubd1_pos[i], ubd2_pos[i], ubd3_pos[i]] = LBUB_val
        else:
            cube_array[ubd1_pos[i], ubd2_pos[i], ubd3_pos[i]] = UB_val
    return cube_array

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

def plot_along_bd(cube_array, shape, bd_name, bd_axis, ctick_params=ctick_params, base_cmap='hot'):
    '''
    Plot 2D plot along specific band
    '''
    # Local variables
    ctick_list  = [params[0] for params in ctick_params]
    clabel_list = [params[1] for params in ctick_params]
    N_session   = len(ctick_list)
    t_bd_id     = bd_axis
    x_bd_id     = bd_axis - 1
    y_bd_id     = bd_axis - 2
    for i in range(cube_array.shape[bd_axis]):
        # Indicator
        drawProgressBar(float(i+1)/cube_array.shape[bd_axis])
        # Select sliced cube array
        if bd_axis == 0:
            plot_cube_array = cube_array[i, :, :]
        elif bd_axis == 1:
            plot_cube_array = cube_array[:, i, :].T
        elif bd_axis == 2:
            plot_cube_array = cube_array[:, :, i]
        else:
            exit('Wrong input band index')
        # Plot 2D slice along band
        fig, axe = plt.subplots()
        cax = axe.imshow(plot_cube_array, origin='lower',\
                         cmap=discrete_cmap(N_session, base_cmap),\
                         vmin=min(ctick_list)-0.5, vmax=max(ctick_list)+0.5)
        cbar = fig.colorbar(cax, ticks=ctick_list, label='GP')
        cbar.ax.set_yticklabels(clabel_list)
        axe.set_title('{} = {:d}'.format(bd_name[t_bd_id], i))
        axe.set_xlabel('{} ({:d})'.format(bd_name[x_bd_id], shape[x_bd_id]))
        axe.set_ylabel('{} ({:d})'.format(bd_name[y_bd_id], shape[y_bd_id]))
        axe.set_xticks(np.arange(0-0.5, shape[x_bd_id]+0.5, 1))
        axe.set_yticks(np.arange(0-0.5, shape[y_bd_id]+0.5, 1))
        axe.xaxis.set_ticklabels([0])
        axe.yaxis.set_ticklabels([0])
        axe.grid()
        plt.tight_layout()
        plt.savefig('{}_{:0>3d}'.format(bd_name[t_bd_id], i))
        plt.clf()

# Main Programs
#=======================================================
if __name__ == '__main__':
    m_start = time.time()

    # Check inputs
    if len(argv) != 7:
        exit('\n\tError: Wrong Arguments\
            \n\tExample: [program] [dim] [cube size] [sigma] [bond] [ref-D] [suffix]\
            \n\t[dim]: dimension for smooth (for now only "6")\
            \n\t[cube size]: length of multi-d cube in magnitude unit\
            \n\t[sigma]: standard deviation for gaussian dist. in magnitude\
            \n\t[bond]: boundary radius of gaussian beam unit in cell\
            \n\t[ref-D]: reference dimension which to modulus other dimension to\
            \n\t[suffix]: suffix to bound array ("default" is "AlB0")\n')

    # Input variables
    dim        = int(argv[1])       # Dimension of position vector
    cube       = float(argv[2])     # Beamsize for each cube
    sigma      = int(argv[3])       # STD for Gaussian Smooth
    bond       = int(argv[4])
    refD       = int(argv[5])       # Reference Beam Dimension
    suffix     = str(argv[6])       # Suffix of bound array
    ddim       = 6                  # Specific dimensional data to plot (projection: ddim -> 3D)
    shape_dir  = 'GPV_{:d}Dposvec_bin{:.1f}/'.format(dim, cube)
    smooth_dir = 'GPV_after_smooth_{:d}D_bin{:.1f}_sigma{:d}_bond{:d}_refD{:d}/'.format(dim, cube, sigma, bond, refD)
    output_dir = 'GPV_after_smooth_{:d}D_bin{:.1f}_sigma{:d}_bond{:d}_refD{:d}_GPtomo/'.format(dim, cube, sigma, bond, refD)

    # Load and print out input information
    if suffix == 'default': suffix = 'AlB0'
    all_shape = np.load(shape_dir + 'Shape.npy')
    print('\nGalaxy Prob Data shape: {}\
           \nPlot Galaxy Prob Data Dim: {:d}D\
           \nGalaxy Prob Bound Suffix: {}'.format(str(all_shape), ddim, suffix))

    # Check storage directory
    if not path.isdir(output_dir):
        system('mkdir {}'.format(output_dir))

    # Generate diff band combinations
    band_ind_list = np.arange(0, dim, 1)
    for comb in combinations(band_ind_list, 3):

        # Generate band input
        band_ind, bd_ind, shape, bd_name = generate_diff_comb_band_params(comb)
        print('\n# band: ' + band_ind)

        # Load galaxy pos/num
        if ddim == dim:
            gal_pos = np.load('{}after_smooth_lack_{:d}_{}_all_cas_pos.npy'.format(\
                                smooth_dir, 0, ''.join([str(i) for i in range(ddim)])))\
                                [:, [bd_ind[0], bd_ind[1], bd_ind[2]]]
            gal_num = np.load('{}after_smooth_lack_{:d}_{}_all_cas_num.npy'.format(\
                                smooth_dir, 0, ''.join([str(i) for i in range(ddim)])))
        else:
            gal_pos = np.load('{}after_smooth_lack_{:d}_{}_all_cas_pos.npy'.format(\
                                smooth_dir, dim-len(band_ind), band_ind))
            gal_num = np.load('{}after_smooth_lack_{:d}_{}_all_cas_num.npy'.format(\
                                smooth_dir, dim-len(band_ind), band_ind))

        # 6D galaxy bound
        lower_bound = np.load('{}after_smooth_lack_0_{}_{}D_lower_bounds_{}.npy'.format(\
                                smooth_dir, ''.join([str(i) for i in range(dim)]), dim, suffix))
        upper_bound = np.load('{}after_smooth_lack_0_{}_{}D_upper_bounds_{}.npy'.format(\
                                smooth_dir, ''.join([str(i) for i in range(dim)]), dim, suffix))

        # Merge repeated position in bound array
        _, sort_lower_bound = sort_up_array_element(lower_bound[:, [bd_ind[0], bd_ind[1], bd_ind[2]]])
        _, sort_upper_bound = sort_up_array_element(upper_bound[:, [bd_ind[0], bd_ind[1], bd_ind[2]]])
        lower_bound = np.array(cascade_array_same_pos(sort_lower_bound))
        upper_bound = np.array(cascade_array_same_pos(sort_upper_bound))
        num_array   = update_num(gal_pos, gal_num, shape)
        cube_array  = update_num_from_bounds(num_array, lower_bound, upper_bound)

        # Start plotting
        p_start = time.time()
        chdir(output_dir)
        tomo_dir = 'tomo_{}/'.format(band_ind)
        if not path.isdir(tomo_dir):
            system('mkdir {}'.format(tomo_dir))
        chdir(tomo_dir)

        print('\naxis-0')
        axis_dir = 'axis_{}_WI_BD/'.format(bd_ind[0])
        if not path.isdir(axis_dir):
            system('mkdir {}'.format(axis_dir))
        chdir(axis_dir)
        plot_along_bd(cube_array, shape, bd_name, 0)
        chdir('../')
        system('convert -delay 20 -loop 0 {}*.png {}_axis_{}_{}.gif'.format(axis_dir, band_ind, bd_ind[0], 'WI_BD'))

        print('\naxis-1')
        axis_dir = 'axis_{}_WI_BD/'.format(bd_ind[1])
        if not path.isdir(axis_dir):
            system('mkdir {}'.format(axis_dir))
        chdir(axis_dir)
        plot_along_bd(cube_array, shape, bd_name, 1)
        chdir('../')
        system('convert -delay 20 -loop 0 {}*.png {}_axis_{}_{}.gif'.format(axis_dir, band_ind, bd_ind[1], 'WI_BD'))

        print('\naxis-2')
        axis_dir = 'axis_{}_WI_BD/'.format(bd_ind[2])
        if not path.isdir(axis_dir):
            system('mkdir {}'.format(axis_dir))
        chdir(axis_dir)
        plot_along_bd(cube_array, shape, bd_name, 2)
        chdir('../')
        system('convert -delay 20 -loop 0 {}*.png {}_axis_{}_{}.gif'.format(axis_dir, band_ind, bd_ind[2], 'WI_BD'))
        chdir('../../')
        p_end   = time.time()
        print('\nPlotting took {:.3f} secs'.format(p_end-p_start))

    m_end   = time.time()
    print('\nWhole {} process took {:.3f} secs\n'.format(str(argv[0]), m_end-m_start))
