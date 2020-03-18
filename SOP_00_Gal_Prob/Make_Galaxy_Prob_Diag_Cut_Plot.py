#!/usr/bin/python
'''

'''
from __future__ import print_function
from sys import argv, exit
from os import path, system, chdir
from numba import jit
from Useful_Functions import *
import matplotlib.pyplot as plt
import numpy as np
import time

if len(argv) != 8:
    exit('\n\tError: Wrong Arguments\
    \n\tExample: [program] [dim] [cube size] [sigma] [bond] [ref-D] [lack] [band_inp]\
    \n\t[dim]: dimension for smooth (for now only "6")\
    \n\t[cube size]: length of multi-d cube in magnitude unit\
    \n\t[sigma]: standard deviation for gaussian dist. in magnitude\
    \n\t[bond]: boundary radius of gaussian beam unit in cell\
    \n\t[ref-D]: reference dimension which to modulus other dimension to\
    \n\t[lack]: number of lack bands\
    \n\t[band_inp]: band used to do smooth in string e.g. 012345\n')

# Input Variables
#==========================================================
dim         = int(argv[1])       # Dimension of position vector
cube        = float(argv[2])     # Beamsize for each cube
sigma       = int(argv[3])       # STD for Gaussian Smooth
bond        = int(argv[4])
refD        = int(argv[5])       # Reference Beam Dimension
lack        = int(argv[6])
band_inp    = str(argv[7])
band_id_list = []
for i in range(len(band_inp)):
    band_id_list.append(int(band_inp[i]))
posv_dir = 'GPV_{:d}Dposvec_bin{:.1f}/'.format(dim, cube)
out_dir  = 'GPV_after_smooth_{:d}D_bin{:.1f}_sigma{:d}_bond{:d}_refD{:d}/'.format(dim, cube, sigma, bond, refD)
tomo_dir = 'GPV_after_smooth_{:d}D_bin{:.1f}_sigma{:d}_bond{:d}_refD{:d}_GPtomo/'.format(dim, cube, sigma, bond, refD)

# Main Functions
#==========================================================
def generate_diag(dim, bd_id_list, shape):
    '''
    This is to generate diagonal line in multi-d space
    '''
    band_bd  = min([shape[bd_id] for bd_id in bd_id_list])
    diagonal = [[i]*dim for i in range(band_bd)]
    diagonal = np.array(diagonal)
    return diagonal

@jit(nopython=True)
def find_gal_pos(gal_pos, target):
    '''
    This is to find if target in galaxy position array
    '''
    id_list = []
    for i in range(len(gal_pos)):
        if np.all(np.equal(gal_pos[i], target)):
            id_list.append(i)
    id_array = np.array(id_list)
    return id_array

def cal_diag_cut(diagonal, gal_pos, gal_num, simple_cut=True):
    '''
    This is to calculate hist along diagonal line
    '''
    diag_bin = []
    for i, diag in enumerate(diagonal):
        drawProgressBar(float(i+1)/len(diagonal))
        loc_id = find_gal_pos(gal_pos, diag)
        if len(loc_id) == 1:
            diag_bin.append(gal_num[loc_id])
        else:
            diag_bin.append(0.)
    if simple_cut:
        for i, dbin in enumerate(diag_bin):
            if dbin > 1.:
                diag_bin[i] = 1.5
            elif dbin > 0.:
                diag_bin[i] = 0.5
    diag_bin = np.array(diag_bin)
    return diag_bin

def plot_diag_step(diagonal, diag_cut, lack, band_inp):
    '''
    This is to plot histogram along diagonal line
    '''
    plt.figure()
    plt.axhline(1.5, xmax=len(diagonal), xmin=0, label='GP>1', c='g', ls='--')
    plt.axhline(1.0, xmax=len(diagonal), xmin=0, label='GP=1', c='b', ls='--')
    plt.axhline(0.5, xmax=len(diagonal), xmin=0, label='GP<1', c='gold', ls='--')
    plt.axhline(0.0, xmax=len(diagonal), xmin=0, label='GP=0', c='r', ls='--')
    plt.step(np.arange(0+0.5, len(diagonal)+0.5, 1), diag_cut, c='k')
    plt.xticks(np.arange(0+0.5, len(diagonal)+0.5, 1))
    frame1 = plt.gca()
    frame1.axes.xaxis.set_ticklabels([0])
    frame1.axes.yaxis.set_ticklabels([])
    plt.title('Band: {}'.format(band_inp))
    plt.xlabel('Along Diagonal Line (bin={:.1f}mag)'.format(cube))
    plt.ylabel('Galaxy Probability')
    plt.legend()
    plt.savefig('DiagCut_L{}_{}'.format(lack, band_inp))

# Main Programs
#==========================================================
if __name__ == '__main__':
    # Load pos/num
    l_start = time.time()
    gal_pos = np.load(out_dir + 'after_smooth_lack_{}_{}_all_cas_pos.npy'.format(lack, band_inp))#[:1000]
    gal_num = np.load(out_dir + 'after_smooth_lack_{}_{}_all_cas_pos.npy'.format(lack, band_inp))#[:1000]
    shape   = np.load(posv_dir + 'Shape.npy')
    # Check existence of output directory
    if not path.isdir(tomo_dir):
        system('mkdir {}'.format(tomo_dir))
    chdir(tomo_dir)
    if not path.isdir('diag_cut'):
        system('mkdir {}'.format('diag_cut'))
    chdir('diag_cut')
    l_end   = time.time()
    print('\nExecuting {}'.format(argv[0]))
    print('\nLoading {} gal pos/num took {:.3f} secs'.format(band_inp, l_end-l_start))
    # Generate diagonal array
    g_start  = time.time()
    diagonal = generate_diag(dim, band_id_list, shape)
    g_end    = time.time()
    print('Generating diag array took {:.3f} secs'.format(g_end-g_start))
    # Calculate cut along diagonal line
    c_start  = time.time()
    diag_cut = cal_diag_cut(diagonal, gal_pos, gal_num)
    c_end    = time.time()
    print('\nCalculating diag cut took {:.3f} secs'.format(c_end-c_start))
    # Plot step diagram along diagonal line
    p_start  = time.time()
    plot_diag_step(diagonal, diag_cut, lack, band_inp)
    chdir('../../')
    p_end    = time.time()
    print('Plotting step cut took {:.3f} secs\n'.format(p_end-p_start))
    print('{} {} took {:.3f} secs\n'.format(argv[0], band_inp, p_end-l_start))
