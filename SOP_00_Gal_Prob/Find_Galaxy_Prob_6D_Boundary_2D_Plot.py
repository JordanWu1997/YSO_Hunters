#!/usr/bin/python
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
from Hsieh_Functions import *
from Useful_Functions import *
# For non-interactive backend (No request for showing pictures)
import matplotlib
matplotlib.use('Agg')
matplotlib.rc('figure', max_open_warning = 0)
import matplotlib.pyplot as plt

# Input Variables
#=======================================================
band_name  = band_name
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

def update_num(gal_pos, gal_num, shape):
    '''
    Update gal num to a cube array with gal pos
    '''
    bd1_pos, bd2_pos, bd3_pos = gal_pos[:, 0], gal_pos[:, 1], gal_pos[:, 2]
    bd1_len, bd2_len, bd3_len = shape[0], shape[1], shape[2]
    cube_array = np.zeros((bd1_len, bd2_len, bd3_len))
    for i in range(len(gal_pos)):
        if gal_num[i] > 1.:
            cube_array[bd1_pos[i], bd2_pos[i], bd3_pos[i]] = 2.0
        elif gal_num[i] == 1.:
            cube_array[bd1_pos[i], bd2_pos[i], bd3_pos[i]] = 1.2
        elif gal_num[i] < 1.:
            cube_array[bd1_pos[i], bd2_pos[i], bd3_pos[i]] = 0.5
    return cube_array

def update_num_from_bounds(cube_array, lower_bound, upper_bound):
    '''
    Update lower/upper bound to previous 3D cube array
    '''
    lbd1_pos, lbd2_pos, lbd3_pos = lower_bound[:, 0], lower_bound[:, 1], lower_bound[:, 2]
    ubd1_pos, ubd2_pos, ubd3_pos = upper_bound[:, 0], upper_bound[:, 1], upper_bound[:, 2]
    for i in range(len(lower_bound)):
        cube_array[lbd1_pos[i], lbd2_pos[i], lbd3_pos[i]] = 3.0
    for i in range(len(upper_bound)):
        print(ubd1_pos[i], ubd2_pos[i], ubd3_pos[i])
        #cube_array[ubd1_pos[i], ubd2_pos[i], ubd3_pos[i]] = 4.0
    return cube_array

def plot_along_bd(cube_array, shape, bd_name, bd_axis):
    '''
    Plot 2D plot along specific band
    '''
    for i in range(cube_array.shape[bd_axis]):
        drawProgressBar(float(i+1)/cube_array.shape[bd_axis])

        fig, axe = plt.subplots()
        if bd_axis == 0:
            cax = axe.imshow(cube_array[i, :, :], origin='lower', vmin=0, vmax=2, cmap='hot')
            axe.set_title('{} = {:d}'.format(bd_name[0], i))
            axe.set_xlabel('{} ({:d})'.format(bd_name[2], shape[2]))
            axe.set_ylabel('{} ({:d})'.format(bd_name[1], shape[1]))
            axe.set_xticks(np.arange(0-0.5, shape[2]+0.5, 1))
            axe.set_yticks(np.arange(0-0.5, shape[1]+0.5, 1))
        elif bd_axis == 1:
            cax = axe.imshow(cube_array[:, i, :], origin='lower', vmin=0, vmax=2, cmap='hot')
            axe.set_title('{} = {:d}'.format(bd_name[1], i))
            axe.set_xlabel('{} ({:d})'.format(bd_name[2], shape[2]))
            axe.set_ylabel('{} ({:d})'.format(bd_name[0], shape[0]))
            axe.set_xticks(np.arange(0-0.5, shape[2]+0.5, 1))
            axe.set_yticks(np.arange(0-0.5, shape[0]+0.5, 1))
        elif bd_axis == 2:
            cax = axe.imshow(cube_array[:, :, i], origin='lower', vmin=0, vmax=2, cmap='hot')
            axe.set_title('{} = {:d}'.format(bd_name[2], i))
            axe.set_xlabel('{} ({:d})'.format(bd_name[1], shape[1]))
            axe.set_ylabel('{} ({:d})'.format(bd_name[0], shape[0]))
            axe.set_xticks(np.arange(0-0.5, shape[1]+0.5, 1))
            axe.set_yticks(np.arange(0-0.5, shape[0]+0.5, 1))

        axe.xaxis.set_ticklabels([0])
        axe.yaxis.set_ticklabels([0])
        cbar = fig.colorbar(cax, ticks=[0.0, 0.5, 1.2, 2.0], label='GP')
        cbar.ax.set_yticklabels(['=0', '< 1.', '=1.', '> 1'])
        axe.grid()
        plt.tight_layout()
        plt.savefig('{}_{:0>3d}'.format(bd_name[0], i))
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

    # Load and print out input information
    if suffix == 'default': suffix = 'AlB0'
    all_shape = np.load(shape_dir + 'Shape.npy')
    print('\nGalaxy Prob Data shape: {}\
           \nPlot Galaxy Prob Data Dim: {:d}D\
           \nGalaxy Prob Bound Suffix: {}'.format(str(all_shape), ddim, suffix))

    # Check storage directory
    if not path.isdir(output_dir):
        system('mkdir {}'.format(output_dir))

    # Just for debugging test: band_ind_list = np.array([0, 1, 2])
    band_ind_list = np.arange(0, dim, 1)
    for comb in combinations(band_ind_list, 3):

        # Generate band input
        band_ind, bd_ind, shape, bd_name = generate_diff_comb_band_params(comb)
        print('\n# band: ' + band_ind)

        # Load galaxy pos/num
        # l_start = time.time()
        if ddim == dim:
            gal_pos = np.load('{}after_smooth_lack_{:d}_{}_all_cas_pos.npy'.format(smooth_dir, 0, ''.join([str(i) for i in range(ddim)])))
            gal_num = np.load('{}after_smooth_lack_{:d}_{}_all_cas_num.npy'.format(smooth_dir, 0, ''.join([str(i) for i in range(ddim)])))
            gal_pos = gal_pos[:, [bd_ind[0], bd_ind[1], bd_ind[2]]]
        else:
            gal_pos = np.load('{}after_smooth_lack_{:d}_{}_all_cas_pos.npy'.format(smooth_dir, dim-len(band_ind), band_ind))
            gal_num = np.load('{}after_smooth_lack_{:d}_{}_all_cas_num.npy'.format(smooth_dir, dim-len(band_ind), band_ind))

        lower_bound = np.load('{}after_smooth_6D_lower_bounds_{}.npy'.format(smooth_dir, suffix))
        upper_bound = np.load('{}after_smooth_6D_upper_bounds_{}.npy'.format(smooth_dir, suffix))
        lower_bound = lower_bound[:, [bd_ind[0], bd_ind[1], bd_ind[2]]]
        upper_bound = upper_bound[:, [bd_ind[0], bd_ind[1], bd_ind[2]]]
        cube_array  = update_num(gal_pos, gal_num, shape)
        cube_array  = update_num_from_bounds(cube_array, lower_bound, upper_bound)
        # l_end   = time.time()
        # print('Loading took {:.3f} secs'.format(l_end-l_start))

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
    print('\nWhole Process took {:.3f} secs\n'.format(m_end-m_start))
