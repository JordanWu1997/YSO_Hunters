#!/usr/bin/python
'''

'''
from __future__ import print_function
from sys import argv, exit
from os import path, system, chdir
from Useful_Functions import *
from Hsieh_Functions import *
import numpy as np
import time

# For non-interactive backend (No request for showing pictures)
import matplotlib
matplotlib.use('Agg')
matplotlib.rc('figure', max_open_warning=0)
import matplotlib.pyplot as plt

if len(argv) != 10:
    exit('\n\tError: Wrong Arguments\
    \n\tExample: [program] [dim] [cube size] [sigma] [bond] [ref-D] [band_inp] [L_step] [probe_band] [cut_style]\
    \n\t[dim]: dimension for smooth (for now only "6")\
    \n\t[cube size]: length of multi-d cube in magnitude unit\
    \n\t[sigma]: standard deviation for gaussian dist. in magnitude\
    \n\t[bond]: boundary radius of gaussian beam unit in cell\
    \n\t[ref-D]: reference dimension which to modulus other dimension to\
    \n\t[band_inp]: band used to do smooth in string e.g. 012345\
    \n\t[L_step]: step length for shifting origin (unit: cells)\
    \n\t[probe_band]: band used to scan along (or "default")\
    \n\t[cut_style]: fc (full cut) / sc (simple cut, set (GP>1)=1)\n')

# Input Variables
#==========================================================
dim         = int(argv[1])       # Dimension of position vector
cube        = float(argv[2])     # Beamsize for each cube
sigma       = int(argv[3])       # STD for Gaussian Smooth
bond        = int(argv[4])       #
refD        = int(argv[5])       # Reference Beam Dimension
band_inp    = str(argv[6])       #
L_step      = int(argv[7])       # Step length for shifting origin
probe_band  = int(argv[8])       # Band for scanning along
cut_style   = str(argv[9])       # Cut style: fc (full cut) / sc (simple cut)

posv_dir = 'GPV_{:d}Dposvec_bin{:.1f}/'.format(dim, cube)
out_dir  = 'GPV_after_smooth_{:d}D_bin{:.1f}_sigma{:d}_bond{:d}_refD{:d}/'.format(dim, cube, sigma, bond, refD)
tomo_dir = 'GPV_after_smooth_{:d}D_bin{:.1f}_sigma{:d}_bond{:d}_refD{:d}_GPtomo/'.format(dim, cube, sigma, bond, refD)

# Main Functions
#==========================================================
def generate_probe(start, along_bd_id):
    '''
    This is to generate probe array along the band with most cells
    '''
    probe_array = np.arange(0, along_bd_id+1, 1)
    return probe_array

def cal_probe_cut(probe_arr, gal_pos, gal_num, cut_style='sc'):
    '''
    This is to calculate hist along the band with most cells
    Note: sc stands for simple cut
          fc stands for full cut
    '''
    # get pca cut
    probe_cut = []
    for i, probe_pos in enumerate(probe_arr):
        # drawProgressBar(float(i+1)/len(probe_arr))
        loc_id = find_pos_id_in_gal_pos(gal_pos, probe_pos)
        if len(loc_id) == 1:
            num = gal_num[loc_id]
        else:
            num = 0.
        probe_cut.append(num)
    # cut_style
    if cut_style == 'sc':
        for i in range(len(probe_cut)):
            value = probe_cut[i]
            if value > 1.:
                probe_cut[i] = 1.5
            elif value < 1. and value > 0. :
                probe_cut[i] = 0.5
    elif cut_style == 'fc':
        pass
    probe_cut = np.array(probe_cut)
    return probe_cut

def plot_probe_step(probe_arr, probe_cut, xlabel, title, save_name, cut_style='sc'):
    '''
    This is to plot histogram along the band with most cells
    sc stands for simple cut
    '''
    plt.figure()
    frame = plt.gca()
    frame.axes.xaxis.set_ticklabels([0])

    if cut_style == 'sc':
        frame.axes.yaxis.set_ticklabels([])
        plt.axhline(1.5, xmax=len(probe_arr), xmin=0, label='GP>1', c='g', ls='--')
        plt.axhline(1.0, xmax=len(probe_arr), xmin=0, label='GP=1', c='b', ls='--')
        plt.axhline(0.5, xmax=len(probe_arr), xmin=0, label='GP<1', c='gold', ls='--')
        plt.axhline(0.0, xmax=len(probe_arr), xmin=0, label='GP=0', c='r', ls='--')
        yscale = 'linear'
        ylabel = 'Galaxy Probability ({})'.format(cut_style)
    elif cut_style == 'fc':
        plt.axhline(1.0, xmax=len(probe_arr), xmin=0, label='GP=1', c='b', ls='--')
        yscale = 'log'
        ylabel = 'log Galaxy Probability ({})'.format(cut_style)

    plt.step(np.arange(0+0.5, len(probe_arr)+0.5, 1), probe_cut, c='k')
    plt.xticks(np.arange(0+0.5, len(probe_arr)+0.5, 1))
    plt.yscale(yscale)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.legend()
    plt.savefig(save_name)

# Main Programs
#==========================================================
if __name__ == '__main__':

    # Load pos/num
    l_start = time.time()
    gal_pos = np.load(out_dir + 'after_smooth_lack_{}_{}_all_cas_pos.npy'.format(dim-len(band_inp), band_inp))
    gal_num = np.load(out_dir + 'after_smooth_lack_{}_{}_all_cas_num.npy'.format(dim-len(band_inp), band_inp))
    shape   = np.load(posv_dir + 'Shape.npy')
    bands   = band_name

    # Check existence of output directory
    if not path.isdir(tomo_dir):
        system('mkdir {}'.format(tomo_dir))
    chdir(tomo_dir)
    if not path.isdir('{:d}D_{}_probe_cut'.format(len(band_inp), band_inp)):
        system('mkdir {}'.format('{:d}D_{}_probe_cut'.format(len(band_inp), band_inp)))
    chdir('{:d}D_{}_probe_cut'.format(len(band_inp), band_inp))
    l_end   = time.time()
    print('\nExecuting {}'.format(argv[0]))
    print('\nLoading {} gal pos/num took {:.3f} secs'.format(band_inp, l_end-l_start))

    # Probe scanning and Parameters
    if probe_band == 'default':
        along_bd_id = np.argmax(shape)[0]
    else:
        along_bd_id = int(probe_band)
    print('\nProbing along {} band: {:d} cells'.format(band_name[along_bd_id], shape[along_bd_id]))
    xlabel  = 'Along {} band (cell={:d}; bin={:.1f}mag)'.format(band_name[along_bd_id], shape[along_bd_id], cube)
    p_bdinp = ''
    for inp in band_inp:
        if int(inp) != along_bd_id:
            p_bdinp += inp

    # Start dim-1 probing origin calculation
    c_start = time.time()
    origin_array = np.array([np.zeros(len(band_inp))], dtype=int)
    for band in p_bdinp:
        new_origin_list = []
        for i in range(shape[int(band)]):
            if i % L_step == 0:
                # Scanning by shifting start probing points
                for origin in origin_array:
                    shift = np.array(np.zeros(len(origin)), dtype=int)
                    shift[int(band)] = i
                    start = origin + shift
                    new_origin_list.append(start)
        origin_array = np.array(new_origin_list)
    c_end   = time.time()
    print('\nCalculating origin shift took {:.3f} secs'.format(c_end-c_start))

    # Plot step diagram
    p_start = time.time()
    print('\nPlotting step diagrams ... #{:d}'.format(len(origin_array)))
    for i in range(len(origin_array)):
        # Assign titles and savefig names
        indice = ['{:0>3d}'.format(origin_array[i][j]) for j in range(len(origin_array[i])) if j != along_bd_id]
        svname = '{}{:d}_{}'.format(cut_style, along_bd_id, '_'.join(indice))
        title  = '{} smooth_bond={:d}'.format(svname, bond)
        # Calculate and Plot ...
        probe_arr = generate_probe(origin_array[i], along_bd_id)
        probe_cut = cal_probe_cut(probe_arr, gal_pos, gal_num, cut_style=cut_style)
        plot_probe_step(probe_arr, probe_cut, xlabel, title, svname, cut_style=cut_style)
        # Progress Indicator
        drawProgressBar(float(i+1)/len(origin_array))
    p_end   = time.time()
    print('\nPlotting took {:.3f} secs'.format(p_end-p_start))
    print('\n{} {} took {:.3f} secs\n'.format(argv[0], band_inp, p_end-l_start))
