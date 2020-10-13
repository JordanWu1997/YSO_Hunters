#!/usr/bin/python
'''
----------------------------------------------------------------
Example: [program] [dim] [cube size] [sigma] [bond] [ref-D] [num_slice] [inclination]
Input Variables:
    [dim]:         dimension for smooth (for now only "6")
    [cube size]:   length of multi-d cube in magnitude unit
    [sigma]:       standard deviation for gaussian dist. in magnitude
    [bond]:        boundary radius of gaussian beam unit in cell
    [ref-D]:       reference dimension which to modulus other dimension to
    [deg_slice]:   number of slices of position angle
    [inclination]: inclination degree of viewing angle
----------------------------------------------------------------
Latest update: 20200526 Jordan Wu'''

# Load Modules
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
from mpl_toolkits.mplot3d import Axes3D

# Global Variables
#=======================================================

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

def sort_inp_gal(gal_pos, gal_num):
    '''
    sort gal_pos, gal_num and then return list after sorting
    '''
    out_pos, out_num = [], []
    for i in range(len(gal_num)):
        if gal_num[i] >= 1.:
            out_pos.append(gal_pos[i])
            out_num.append(gal_num[i])
    return out_pos, out_num

def plot_3d_scatter(pos_array, num_array, shape, bd_ind, bd_name, sl_num, incli):
    '''
    Plot 2D plot along band 3
    '''
    bd0, bd1, bd2 = pos_array[:, 0], pos_array[:, 1], pos_array[:, 2]
    bd0_g1, bd1_g1, bd2_g1 = bd0[num_array>1.], bd1[num_array>1.], bd2[num_array>1.]
    bd0_e1, bd1_e1, bd2_e1 = bd0[num_array==1.], bd1[num_array==1.], bd2[num_array==1.]
    for i, deg in enumerate(np.linspace(0, 360, sl_num, endpoint=False)):
        drawProgressBar(float(i+1)/sl_num)
        fig = plt.figure(figsize=(12, 8))
        ax  = fig.add_subplot(111, projection='3d')
        #ax.scatter(bd0, bd1, bd2, s=0.5, alpha=0.8)
        ax.scatter(bd0_e1, bd1_e1, bd2_e1, s=dot_size, c='g', alpha=0.5, label='Scatter (GP=1)')
        ax.scatter(bd0_g1, bd1_g1, bd2_g1, s=dot_size, c='steelblue', alpha=0.5, label='Scatter (GP>1)')
        ax.set_title('{}{}{}_{}'.format(bd_name[0], bd_name[1], bd_name[2], bd_name[0]))
        ax.set_xlabel('{} ({:d})'.format(bd_name[0], shape[0]))
        ax.set_ylabel('{} ({:d})'.format(bd_name[1], shape[1]))
        ax.set_zlabel('{} ({:d})'.format(bd_name[2], shape[2]))
        ax.set_xticks(np.arange(0-0.5, shape[0]+0.5, 1))
        ax.set_yticks(np.arange(0-0.5, shape[1]+0.5, 1))
        ax.set_zticks(np.arange(0-0.5, shape[2]+0.5, 1))
        ax.w_xaxis.set_ticklabels([0])
        ax.w_yaxis.set_ticklabels([0])
        ax.w_zaxis.set_ticklabels([0])
        ax.view_init(incli, deg)
        ax.legend()
        plt.savefig('{}{}{}_{:0>3d}'.format(bd_name[0], bd_name[1], bd_name[2], i))
        plt.clf()

# Main Programs
#=======================================================
if __name__ == '__main__':
    m_start = time.time()

    # Check inputs
    if len(argv) != 8:
        exit('\n\tError: Wrong Arguments\
        \n\tExample: [program] [dim] [cube size] [sigma] [bond] [ref-D] [deg_slice] [inclination]\
        \n\t[dim]: dimension for smooth (for now only "6")\
        \n\t[cube size]: length of multi-d cube in magnitude unit\
        \n\t[sigma]: standard deviation for gaussian dist. in magnitude\
        \n\t[bond]: boundary radius of gaussian beam unit in cell\
        \n\t[ref-D]: reference dimension which to modulus other dimension to\
        \n\t[deg_slice]: number of slices of position angle\
        \n\t[inclination]: inclination degree of viewing angle\n')

    # Input variables
    band_name  = band_name
    dim        = int(argv[1])        # Dimension of position vector
    cube       = float(argv[2])      # Beamsize for each cube
    sigma      = int(argv[3])        # STD for Gaussian Smooth
    bond       = int(argv[4])
    refD       = int(argv[5])        # Reference Beam Dimension
    deg_slice  = int(argv[6])
    incli      = int(argv[7])
    ddim       = 6                   # Specific dimensional data to plot
    dot_size   = 0.5 * (cube/0.2)**3 # Size of scatter dots (refer to cube=0.2 case)
    shape_dir  = 'GPV_{:d}Dposvec_bin{:.1f}/'.format(dim, cube)
    smooth_dir = 'GPV_after_smooth_{:d}D_bin{:.1f}_sigma{:d}_bond{:d}_refD{:d}/'.format(dim, cube, sigma, bond, refD)
    output_dir = 'GPV_after_smooth_{:d}D_bin{:.1f}_sigma{:d}_bond{:d}_refD{:d}_GPtomo/'.format(dim, cube, sigma, bond, refD)

    # Load and print out input information
    all_shape  = np.load(shape_dir + 'Shape.npy')
    print('\nGalaxy Prob Data shape: {}\
           \nPlot Galaxy Prob Data Dim: {:d}D'.format(str(all_shape), ddim))

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
            gal_pos = np.load('{}after_smooth_lack_{:d}_{}_all_cas_pos.npy'.format(smooth_dir, 0, ''.join([str(i) for i in range(ddim)])))
            gal_num = np.load('{}after_smooth_lack_{:d}_{}_all_cas_num.npy'.format(smooth_dir, 0, ''.join([str(i) for i in range(ddim)])))
            gal_pos = gal_pos[:, [bd_ind[0], bd_ind[1], bd_ind[2]]]
        else:
            gal_pos = np.load('{}after_smooth_lack_{:d}_{}_all_cas_pos.npy'.format(smooth_dir, dim-len(band_ind), band_ind))
            gal_num = np.load('{}after_smooth_lack_{:d}_{}_all_cas_num.npy'.format(smooth_dir, dim-len(band_ind), band_ind))
        out_pos, out_num = sort_inp_gal(gal_pos, gal_num)            # only include gp>=1 data points
        pos_array, num_array = np.array(out_pos), np.array(out_num)  # transform to arrays

        # Start plotting
        p_start = time.time()
        chdir(output_dir)
        tomo_dir = 'tomo_{}/'.format(band_ind)
        if not path.isdir(tomo_dir):
            system('mkdir {}'.format(tomo_dir))
        chdir(tomo_dir)
        all_dir  = 'all_{}_n{:d}_i{:d}/'.format(band_ind, deg_slice, incli)
        if not path.isdir(all_dir):
            system('mkdir {}'.format(all_dir))
        chdir(all_dir)
        plot_3d_scatter(pos_array, num_array, shape, bd_ind, bd_name, deg_slice, incli)
        chdir('../')
        system('convert -delay 100 -loop 0 {}*.png {}_all_{}_n{:d}_i{:d}.gif'.format(all_dir, band_ind, bd_ind[0], deg_slice, incli))
        chdir('../../')
        p_end   = time.time()
        print('\nPlotting took {:.3f} secs'.format(p_end-p_start))

    #=======================================================
    m_end   = time.time()
    print('\nWhole {} process took {:.3f} secs\n'.format(str(argv[0]), m_end-m_start))
