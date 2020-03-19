#!/usr/bin/python
'''

'''
from __future__ import print_function
from sys import argv, exit
from os import path, system, chdir
from numba import jit
from sklearn.decomposition import PCA
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
def cascade_array(sort_pos):
    '''
    Use this to find out sources locate in same position and cascade them
    '''
    #================================================
    # Input
    after_cascade_pos = []
    start = 0
    end   = 0
    for i in range(len(sort_pos)-1):
        #================================================
        # Indicator
        #if i % 1000 == 0 and i>999:
        #    print(float(i+1)/len(sort_value))
        #================================================
        # Get reference and target
        tar, ref = sort_pos[i], sort_pos[i+1]
        end += 1
        #================================================
        # Determine repeated or not
        if not np.all(np.equal(tar, ref)):
            after_cascade_pos.append(sort_pos[start])
            start = end
    #================================================
    # Include the last term
    after_cascade_pos.append(sort_pos[start])
    return after_cascade_pos

def PCA_fit(dim, gal_pos):
    if path.isfile('PCA_components.npy'):
        components = np.load('PCA_components.npy')
        var_ratios = np.load('PCA_var_ratios.npy')
        print('Use existed PCA model')
    else:
        a_start = time.time()
        pca = PCA(n_components=dim)
        pca.fit(gal_pos)
        components = pca.components_
        var_ratios = pca.explained_variance_ratio_
        np.save('PCA_components', components)
        np.save('PCA_var_ratios', var_ratios)
        a_end   = time.time()
        print('PCA took {:.3f} secs\n'.format(a_end-a_start))
    print(components)
    print('Var_ratios')
    print(var_ratios)
    return components, var_ratios

def generate_pca(dim, bd_id_list, shape, components):
    '''
    This is to generate pca line in multi-d space
    '''
    band_bd  = min([shape[bd_id] for bd_id in bd_id_list])
    pca_axe0 = components[0,:]
    pca_line, pos, i = [], [0]*dim, 0
    while round(max(pos)) < band_bd:
        pos = i * pca_axe0
        pca_line.append(pos)
        i += 1
    pca_line  = np.array(pca_line)
    pca_round = np.rint(pca_line)
    return pca_round

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

def cal_pca_cut(pca_arr, gal_pos, gal_num, simple_cut=True):
    '''
    This is to calculate hist along pca line
    '''
    pca_bin = []
    for i, pca in enumerate(pca_arr):
        drawProgressBar(float(i+1)/len(pca_arr))
        loc_id = find_gal_pos(gal_pos, pca)
        if len(loc_id) == 1:
            pca_bin.append(gal_num[loc_id])
        else:
            pca_bin.append(0.)
    if simple_cut:
        for i, dbin in enumerate(pca_bin):
            if dbin > 1.:
                pca_bin[i] = 1.5
            elif dbin > 0.:
                pca_bin[i] = 0.5
    pca_bin = np.array(pca_bin)
    return pca_bin

def plot_pca_step(pca, pca_cut, lack, band_inp):
    '''
    This is to plot histogram along pca line
    '''
    plt.figure()
    plt.axhline(1.5, xmax=len(pca), xmin=0, label='GP>1', c='g', ls='--')
    plt.axhline(1.0, xmax=len(pca), xmin=0, label='GP=1', c='b', ls='--')
    plt.axhline(0.5, xmax=len(pca), xmin=0, label='GP<1', c='gold', ls='--')
    plt.axhline(0.0, xmax=len(pca), xmin=0, label='GP=0', c='r', ls='--')
    plt.step(np.arange(0+0.5, len(pca)+0.5, 1), pca_cut, c='k')
    plt.xticks(np.arange(0+0.5, len(pca)+0.5, 1))
    frame1 = plt.gca()
    frame1.axes.xaxis.set_ticklabels([0])
    frame1.axes.yaxis.set_ticklabels([])
    plt.title('Band: {}'.format(band_inp))
    plt.xlabel('Along PC Line (bin={:.1f}mag)'.format(cube))
    plt.ylabel('Galaxy Probability')
    plt.legend()
    plt.savefig('PCA_Cut_L{}_{}'.format(lack, band_inp))

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
    if not path.isdir('pca_cut'):
        system('mkdir {}'.format('pca_cut'))
    chdir('pca_cut')
    l_end   = time.time()
    print('\nExecuting {}'.format(argv[0]))
    print('\nLoading {} gal pos/num took {:.3f} secs'.format(band_inp, l_end-l_start))
    # Generate pca array
    g_start  = time.time()
    components, var_ratios = PCA_fit(dim, gal_pos)
    pca_line = generate_pca(dim, band_id_list, shape, components)
    pca_cas  = cascade_array(pca_line)
    pca_arr  = np.array(pca_cas, dtype=int)
    g_end    = time.time()
    print('\nGenerating pca array took {:.3f} secs'.format(g_end-g_start))
    # Calculate cut along pca line
    c_start  = time.time()
    pca_cut  = cal_pca_cut(pca_arr, gal_pos, gal_num)
    c_end    = time.time()
    print('\nCalculating pca cut took {:.3f} secs'.format(c_end-c_start))
    # Plot step pcaram along pca line
    p_start  = time.time()
    plot_pca_step(pca_arr, pca_cut, lack, band_inp)
    chdir('../../')
    p_end    = time.time()
    print('Plotting step cut took {:.3f} secs\n'.format(p_end-p_start))
    print('{} {} took {:.3f} secs\n'.format(argv[0], band_inp, p_end-l_start))
