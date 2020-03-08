#!/usr/bin/python
'''----------------------------------------------------------------
-------------------------------------------------------------------
latest update :  Jordan Wu'''

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
import matplotlib.pyplot as plt

if len(argv) != 6:
    exit('\n\tError: Wrong Arguments\
    \n\tExample: [program] [dim] [cube size] [sigma] [bond] [ref-D]\
    \n\t[dim]: dimension for smooth (for now only "6")\
    \n\t[cube size]: length of multi-d cube in magnitude unit\
    \n\t[sigma]: standard deviation for gaussian dist. in magnitude\
    \n\t[bond]: boundary radius of gaussian beam unit in cell\
    \n\t[ref-D]: reference dimension which to modulus other dimension to\n')

#=======================================================
# Input variables
band_name  = band_name
dim        = int(argv[1])       # Dimension of position vector
cube       = float(argv[2])     # Beamsize for each cube
sigma      = int(argv[3])       # STD for Gaussian Smooth
bond       = int(argv[4])
refD       = int(argv[5])       # Reference Beam Dimension

shape_dir  = 'GPV_{:d}Dposvec_bin{:.1f}/'.format(dim, cube)
smooth_dir = 'GPV_after_smooth_{:d}D_bin{:.1f}_sigma{:d}_bond{:d}_refD{:d}/'.format(dim, cube, sigma, bond, refD)
output_dir = 'GPV_after_smooth_{:d}D_bin{:.1f}_sigma{:d}_bond{:d}_refD{:d}_GPtomo/'.format(dim, cube, sigma, bond, refD)
all_shape  = np.load(shape_dir + 'Shape.npy')
print('\n', all_shape)

# Check storage directory
if not path.isdir(output_dir):
    system('mkdir {}'.format(output_dir))

#=======================================================
# Functions
def update_num(gal_pos, gal_num):
    '''
    Update gal_num to a cube array with gal_pos
    '''
    bd1_pos, bd2_pos, bd3_pos = gal_pos[:, bd_ind[0]], gal_pos[:, bd_ind[1]], gal_pos[:, bd_ind[2]]
    bd1_len, bd2_len, bd3_len = shape[0], shape[1], shape[2]
    cube_array = np.zeros((bd1_len, bd2_len, bd3_len))
    for i in range(len(gal_pos)):
        if gal_num[i] > 1.:
            cube_array[bd1_pos[i], bd2_pos[i], bd3_pos[i]] = 2
        elif gal_num[i] == 1.:
            cube_array[bd1_pos[i], bd2_pos[i], bd3_pos[i]] = 1
        else:
            cube_array[bd1_pos[i], bd2_pos[i], bd3_pos[i]] = gal_num[i]
    return cube_array

def plot_along_bd1(cube_array, shape, bd_name):

    '''
    Plot 2D plot along band 1
    '''
    for i in range(cube_array.shape[0]):
        drawProgressBar(float(i+1)/cube_array.shape[0])
        plt.figure()
        plt.imshow(cube_array[i, :, :], origin='lower')
        plt.title('{} = {:d}'.format(bd_name[0], i))
        plt.xlabel('{} ({:d})'.format(bd_name[2], shape[2]))
        plt.ylabel('{} ({:d})'.format(bd_name[1], shape[1]))
        plt.xticks(np.arange(0-0.5, shape[2]+0.5, 1))
        plt.yticks(np.arange(0-0.5, shape[1]+0.5, 1))
        frame1 = plt.gca()
        frame1.axes.xaxis.set_ticklabels([0])
        frame1.axes.yaxis.set_ticklabels([0])
        plt.tight_layout()
        plt.grid()
        plt.savefig('{}_{:0>3d}'.format(bd_name[0], i))
        plt.clf()

def plot_along_bd2(cube_array, shape, bd_name):
    '''
    Plot 2D plot along band 2
    '''
    for j in range(cube_array.shape[1]):
        drawProgressBar(float(j+1)/cube_array.shape[1])
        plt.figure()
        plt.imshow(cube_array[:, j, :], origin='lower')
        plt.title('{} = {:d}'.format(bd_name[1], j))
        plt.xlabel('{} ({:d})'.format(bd_name[2], shape[2]))
        plt.ylabel('{} ({:d})'.format(bd_name[0], shape[0]))
        plt.xticks(np.arange(0-0.5, shape[2]+0.5, 1))
        plt.yticks(np.arange(0-0.5, shape[0]+0.5, 1))
        frame1 = plt.gca()
        frame1.axes.xaxis.set_ticklabels([0])
        frame1.axes.yaxis.set_ticklabels([0])
        plt.tight_layout()
        plt.grid()
        plt.savefig('{}_{:0>3d}'.format(bd_name[1], j))
        plt.clf()

def plot_along_bd3(cube_array, shape, bd_name):
    '''
    Plot 2D plot along band 3
    '''
    for k in range(cube_array.shape[2]):
        drawProgressBar(float(k+1)/cube_array.shape[2])
        plt.figure()
        plt.imshow(cube_array[:, :, k], origin='lower')
        plt.title('{} = {:d}'.format(bd_name[2], k))
        plt.xlabel('{} ({:d})'.format(bd_name[1], shape[1]))
        plt.ylabel('{} ({:d})'.format(bd_name[0], shape[0]))
        plt.xticks(np.arange(0-0.5, shape[1]+0.5, 1))
        plt.yticks(np.arange(0-0.5, shape[0]+0.5, 1))
        frame1 = plt.gca()
        frame1.axes.xaxis.set_ticklabels([0])
        frame1.axes.yaxis.set_ticklabels([0])
        plt.tight_layout()
        plt.grid()
        plt.savefig('{}_{:0>3d}'.format(bd_name[2], k))
        plt.clf()

#=======================================================
# Main Programs
m_start = time.time()
# Just for debugging test: band_ind_list = np.array([0, 1, 2])
band_ind_list = np.arange(0, dim, 1)
for comb in combinations(band_ind_list, 3):

    #=======================================================
    # Generate band input
    band_ind = ''
    for band in comb:
        band_ind += str(band)
    bd_ind, shape, bd_name = [], [], []
    for ind in band_ind:
        bd_ind.append(int(ind))
        shape.append(all_shape[int(ind)])
        bd_name.append(band_name[int(ind)])
    print('\n# band: ' + band_ind)

    #=======================================================
    # Load galaxy pos/num
    l_start = time.time()
    gal_pos = np.load(smooth_dir + 'after_smooth_lack_{:d}_{}_all_cas_pos.npy'.format(dim-len(band_ind), band_ind))
    gal_num = np.load(smooth_dir + 'after_smooth_lack_{:d}_{}_all_cas_num.npy'.format(dim-len(band_ind), band_ind))
    cube_array = update_num(gal_pos, gal_num)
    l_end   = time.time()
    #print('Loading took {:.3f} secs'.format(l_end-l_start))

    #=======================================================
    # Start plotting
    p_start = time.time()
    chdir(output_dir)
    tomo_dir = 'tomo_{}/'.format(band_ind)
    if not path.isdir(tomo_dir):
        system('mkdir {}'.format(tomo_dir))
    chdir(tomo_dir)

    axis_dir = 'axis_{}/'.format(bd_ind[0])
    if not path.isdir(axis_dir):
        system('mkdir {}'.format(axis_dir))
    print('axis-0')
    chdir(axis_dir)
    plot_along_bd1(cube_array, shape, bd_name)
    chdir('../')
    system('convert -delay 20 -loop 0 {}*.png {}_axis_{}.gif'.format(axis_dir, band_ind, bd_ind[0]))

    axis_dir = 'axis_{}/'.format(bd_ind[1])
    if not path.isdir(axis_dir):
        system('mkdir {}'.format(axis_dir))
    chdir(axis_dir)
    print('\naxis-1')
    plot_along_bd2(cube_array, shape, bd_name)
    chdir('../')
    system('convert -delay 20 -loop 0 {}*.png {}_axis_{}.gif'.format(axis_dir, band_ind, bd_ind[1]))

    axis_dir = 'axis_{}/'.format(bd_ind[2])
    if not path.isdir(axis_dir):
        system('mkdir {}'.format(axis_dir))
    chdir(axis_dir)
    print('\naxis-2')
    plot_along_bd3(cube_array, shape, bd_name)
    chdir('../')
    system('convert -delay 20 -loop 0 {}*.png {}_axis_{}.gif'.format(axis_dir, band_ind, bd_ind[2]))

    chdir('../../')
    p_end   = time.time()
    print('\nPlotting took {:.3f} secs'.format(p_end-p_start))

#=======================================================
m_end   = time.time()
print('\nWhole Process took {:.3f} secs\n'.format(m_end-m_start))
