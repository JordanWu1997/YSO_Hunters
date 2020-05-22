#!/usr/bin/python
'''

'''
from __future__ import print_function
from sys import argv, exit
from os import path, system, chdir
# from wpca import WPCA, PCA
from sklearn.decomposition import PCA
from Useful_Functions import *
import numpy as np
import time

# For non-interactive backend (No request for showing pictures)
import matplotlib
matplotlib.use('Agg')
matplotlib.rc('figure', max_open_warning=0)
import matplotlib.pyplot as plt

if len(argv) != 10:
    exit('\n\tError: Wrong Arguments\
    \n\tExample: [program] [dim] [cube size] [sigma] [bond] [ref-D] [lack] [band_inp] [weighted] [cut_style]\
    \n\t[dim]: dimension for smooth (for now only "6")\
    \n\t[cube size]: length of multi-d cube in magnitude unit\
    \n\t[sigma]: standard deviation for gaussian dist. in magnitude\
    \n\t[bond]: boundary radius of gaussian beam unit in cell\
    \n\t[ref-D]: reference dimension which to modulus other dimension to\
    \n\t[lack]: number of lack bands\
    \n\t[band_inp]: band used to do smooth in string e.g. 012345\
    \n\t[weighted]: Use weighted PCA or not (True/False)\
    \n\t[cut_style]: fc (full cut) / sc (simple cut, with interval)\n')

# Input Variables
#==========================================================
dim         = int(argv[1])       # Dimension of position vector
cube        = float(argv[2])     # Beamsize for each cube
sigma       = int(argv[3])       # STD for Gaussian Smooth
bond        = int(argv[4])
refD        = int(argv[5])       # Reference Beam Dimension
lack        = int(argv[6])
band_inp    = str(argv[7])
weighted    = str(argv[8])
cut_style   = str(argv[9])       # Cut style: fc (full cut) / sc (simple cut)

# Check directories
band_id_list = []
for i in range(len(band_inp)):
    band_id_list.append(int(band_inp[i]))
posv_dir = 'GPV_{:d}Dposvec_bin{:.1f}/'.format(dim, cube)
out_dir  = 'GPV_after_smooth_{:d}D_bin{:.1f}_sigma{:d}_bond{:d}_refD{:d}/'.format(dim, cube, sigma, bond, refD)
tomo_dir = 'GPV_after_smooth_{:d}D_bin{:.1f}_sigma{:d}_bond{:d}_refD{:d}_GPtomo/'.format(dim, cube, sigma, bond, refD)

# Main Functions
#==========================================================
def PCA_fit(dim, gal_pos, gal_num, band_inp, weighted, onlyGP_ge1=True):
    # Only include GP >= 1 datapoints
    if onlyGP_ge1:
        gal_pos = gal_pos[gal_num>=1]
        gal_num = gal_num[gal_num>=1]
    # WPCA or PCA
    if weighted == 'True':
        name = 'WPCA'
    else:
        name = 'PCA'
    # Execute
    if path.isfile('{}_components_{}.npy'.format(name, band_inp)):
        components = np.load('{}_components_{}.npy'.format(name, band_inp))
        premean    = np.load('{}_premean_{}.npy'.format(name, band_inp))
        variances  = np.load('{}_variances_{}.npy'.format(name, band_inp))
        var_ratios = np.load('{}_var_ratios_{}.npy'.format(name, band_inp))
        print('Use existed {} model'.format(name))
    else:
        a_start = time.time()
        weight = np.transpose(np.array(len(band_inp) * list(gal_num)).reshape(len(band_inp), len(gal_num)))
        if weighted == 'True':
            pca_result = WPCA(n_components=len(band_inp)).fit(gal_pos, weights=weight)
        else:
            pca_result = PCA(n_components=len(band_inp)).fit(gal_pos)
        components = pca_result.components_
        premean    = pca_result.mean_
        variances  = pca_result.explained_variance_
        var_ratios = pca_result.explained_variance_ratio_
        np.save('{}_components_{}'.format(name, band_inp), components)
        np.save('{}_premean_{}'.format(name, band_inp), premean)
        np.save('{}_variances_{}'.format(name, band_inp), variances)
        np.save('{}_var_ratios_{}'.format(name, band_inp), var_ratios)
        a_end   = time.time()
        print('{} took {:.3f} secs'.format(name, a_end-a_start))
    print(components)
    print('Pre Mean (Centroid of PCA)')
    print(premean)
    print('Explained Variance (Eigenvalue)')
    print(variances)
    print('Var_ratios')
    print(var_ratios)
    return components, premean, variances, var_ratios, name

def generate_pca(bd_id_list, shape, centroid, components, component_n):
    '''
    This is to generate pca line in multi-d space
    '''
    # Set up boundary
    band_upper_bd  = np.array([shape[bd_id] for bd_id in bd_id_list])
    band_lower_bd  = np.array([0.0 for bd_id in bd_id_list])
    pca_round_list = []
    for n in range(component_n):
        # Set up pca axe
        pca_axe = components[n, :]
        if not np.all(np.less_equal(pca_axe, band_lower_bd)):
            pca_axe = -1 * pca_axe
        # Smaller than centroid
        pca_line, pos, i = [centroid], centroid, 1
        # print(pca_axe)
        while np.all(np.greater_equal(pos, band_lower_bd)):
            pos = centroid + (i * pca_axe)
            pca_line.append(pos)
            i += 1
        # Greater than centroid
        pca_axe, pos, j = -1 * pca_axe, centroid, 1
        while np.all(np.less(pos, band_upper_bd)):
            pos = centroid + (j * pca_axe)
            pca_line.append(pos)
            j += 1
        # Store in numpy array (round to closet integer)
        pca_round = np.rint(pca_line)
        # Remove negative element in pca array
        pca_non_neg = []
        for pca_int in pca_round:
            if np.all(pca_int >= np.zeros(len(pca_int))):
                pca_non_neg.append(pca_int)
        pca_non_neg = np.array(pca_non_neg, dtype=int)
        pca_round_list.append(pca_non_neg)
    return pca_round_list

def cal_pca_cut(pca_arr, gal_pos, gal_num, upper, cut_style='sc'):
    '''
    This is to calculate hist along pca line
    Note: No more tolerance
    Note: sc stands for simple cut
          fc stands for full cut
    '''
    # get pca cut
    lower = np.zeros(len(upper))
    pca_bin = []
    for i, pca_pos in enumerate(pca_arr):
        drawProgressBar(float(i+1)/len(pca_arr))
        loc_id = find_pos_id_in_gal_pos(gal_pos, np.array(pca_pos, dtype=int))
        if len(loc_id) == 1:
            num = gal_num[loc_id]
        else:
            num = 0.
        pca_bin.append(num)
    # cut_style
    if cut_style == 'sc':
        for i, dbin in enumerate(pca_bin):
            if dbin > 1.:
                pca_bin[i] = 1.5
            elif dbin < 1. and dbin > 0. :
                pca_bin[i] = 0.5
    elif cut_style == 'fc':
        pass
    pca_bin = np.array(pca_bin)
    return pca_bin

def plot_pca_step(pca, pca_cut, lack, band_inp, var_ratio, name, component_n, cut_style='sc'):
    '''
    This is to plot histogram along pca eigen axis
    sc stands for simple cut
    '''
    plt.figure()
    frame = plt.gca()
    frame.axes.xaxis.set_ticklabels([0])

    if cut_style == 'sc':
        frame.axes.yaxis.set_ticklabels([])
        plt.axhline(1.5, xmax=len(pca), xmin=0, label='GP>1', c='g', ls='--')
        plt.axhline(1.0, xmax=len(pca), xmin=0, label='GP=1', c='b', ls='--')
        plt.axhline(0.5, xmax=len(pca), xmin=0, label='GP<1', c='gold', ls='--')
        plt.axhline(0.0, xmax=len(pca), xmin=0, label='GP=0', c='r', ls='--')
        yscale = 'linear'
        ylabel = 'Galaxy Probability ({})'.format(cut_style)
    elif cut_style == 'fc':
        plt.axhline(1.0, xmax=len(pca), xmin=0, label='GP=1', c='b', ls='--')
        yscale = 'log'
        ylabel = 'log Galaxy Probability ({})'.format(cut_style)

    plt.step(np.arange(0+0.5, len(pca)+0.5, 1), pca_cut, c='k')
    plt.xticks(np.arange(0+0.5, len(pca)+0.5, 1))
    plt.yscale(yscale)
    plt.ylabel(ylabel)
    plt.title('{} Band:{}; e-axis{:d}; var_ratio={:.3f}'.format(cut_style, band_inp, component_n, var_ratio))
    plt.xlabel('Along PC e-axis {:d} (bin={:.1f}mag)'.format(component_n, cube))
    plt.legend()
    plt.savefig('{}_L{:d}_{}_{}_E{}'.format(cut_style, lack, band_inp, name, component_n))

# Main Programs
#==========================================================
if __name__ == '__main__':

    # Load pos/num
    l_start = time.time()
    gal_pos = np.load(out_dir + 'after_smooth_lack_{}_{}_all_cas_pos.npy'.format(lack, band_inp))
    gal_num = np.load(out_dir + 'after_smooth_lack_{}_{}_all_cas_num.npy'.format(lack, band_inp))
    shape   = np.load(posv_dir + 'Shape.npy')
    gal_pos = gal_pos[:, band_id_list]

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

    # Generate wpca array
    g_start  = time.time()
    components, premean, variances, var_ratios, name = PCA_fit(dim, gal_pos, gal_num, band_inp, weighted)
    pca_line_list = generate_pca(band_id_list, shape, premean, components, dim-int(lack))
    pca_cas_list  = []
    for pca_line in pca_line_list:
        _, sort_pca_line = sort_up_array_element(pca_line)
        pca_cas = cascade_array_same_pos(sort_pca_line)
        pca_cas_list.append(pca_cas)
    g_end    = time.time()
    print('\nGenerating pca array took {:.3f} secs'.format(g_end-g_start))

    # Calculate cut along pca line
    c_start  = time.time()
    upper = np.array([shape[bd_id] for bd_id in band_id_list])
    pca_cut_list = []
    for i, pca_cas in enumerate(pca_cas_list):
        print('\ne-axis {:d}'.format(i))
        pca_cut = cal_pca_cut(pca_cas, gal_pos, gal_num, upper, cut_style=cut_style)
        pca_cut_list.append(pca_cut)
    c_end    = time.time()
    print('\nCalculating pca cut took {:.3f} secs'.format(c_end-c_start))

    # Plot step along pca line
    p_start  = time.time()
    for i in range(len(pca_cut_list)):
        plot_pca_step(pca_cas_list[i], pca_cut_list[i], lack, band_inp, var_ratios[i], name, i, cut_style=cut_style)
    chdir('../../')
    p_end    = time.time()
    print('\nPlotting step cut took {:.3f} secs'.format(p_end-p_start))
    print('\n{} {} took {:.3f} secs\n'.format(argv[0], band_inp, p_end-l_start))
