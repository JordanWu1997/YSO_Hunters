#!/usr/bin/env python
'''
-------------------------------------------------------------------------------------
Abstract:
    This program is to plot SED for input catalog
    SED band: J, H, Ks, IR1, IR2, IR3, IR4, MP1
    Photometric system: default (UKIDSS + SPITZER)

Example: python [program] [input catalog] [piece-size] [normalize]

Input Variables:
    [input catalog]: input catalog
    [piece-size]: # of SED in ALL_SED_PLOT plot
    [normalize]: True/False (default: False)

-------------------------------------------------------------------------------------
Latest updated: 2020/06/04 Jordan Wu'''

# Load Modules
#=======================================================
from __future__ import print_function
import time
import random
import numpy as np
from os import system, path, chdir
from argparse import ArgumentParser
from All_Variables import *
from Useful_Functions import drawProgressBar
# For non-interactive backend (No request for showing pictures)
import matplotlib
matplotlib.use('Agg')
matplotlib.rc('figure', max_open_warning = 0)
import matplotlib.pyplot as plt

# Variables
#=======================================================
# Bands names ['J', 'H', 'Ks', 'IR1', 'IR2', 'IR3', 'IR4', 'MP1', 'MP2']
# For J, H, Ks, flux must be calculated from magnitude [1594000.0, 1024000.0, 666700.0]
# Wavelength unit: micrometer [1.235, 1.662, 2.159, 3.6, 4.5, 5.8, 8.0, 24.0, 70.0]
# For J, H, Ks, indice are mag indice, others are flux indice [35, 56, 77, 96, 117, 138, 159, 180, 201]
# For IR1-MP2 ['no', 'no', 'no', 100, 121, 142, 163, 184, 205]
coor_ID    = coor_ID
band       = full_band_name
JHK_f0     = f0_UKIDSS
wavelength = full_band_wavelength_UKIDSS_SPITZER
col_index  = mag_ID_2Mass + full_flux_ID[3:]
flux_qua   = ['no'] * 3 + qua_ID_Spitzer_full[3:]

# Functions
#=======================================================
def mag_to_flux_JHK_and_flux_IR1_To_MP1(row):
    '''
    This is to calculate flux from given magnitude
    For JHK bands, there are only magnitudes
    For other bands, there are flux
    '''
    flux_list, qua_list = [], ''
    # JHK band magnitude
    for i in range(len(JHK_f0)):
        if float(row[col_index[i]]) > 0.0:
            flux = JHK_f0[i] * 10**(float(row[col_index[i]])/(-2.5))
        else:
            flux = 0.0
        flux_list.append(flux)
    # IR1-MP1 band flux
    for j in range(len(JHK_f0), len(col_index)):
        if float(row[col_index[j]]) > 0.0:
            flux = float(row[col_index[j]])
        else:
            flux = 0.0
        flux_list.append(flux)
        qua_list += str(row[flux_qua[j]])
    return flux_list, qua_list

def plot_individual_SED(flux_list, qua_list, Norm, index, color='r'):
    '''
    This is to plot SED of individual source
    Note: plt.figure must be specified before this function
    '''
    x, y = [], []
    for i in range(len(wavelength)):
        plt.axvline(wavelength[i], color = 'k', linestyle = '--')
        if flux_list[i] != 0.0:
            x.append(wavelength[i])
            y.append(wavelength[i] * flux_list[i])
    if Norm:
        yN = [ys / max(y) for ys in y]
        plt.loglog(x, yN, '{}o-'.format(color), label=str(index))
        plt.ylabel('Normalized flux * wavelength')
    else:
        plt.loglog(x, y,  '{}o-'.format(color), label=str(index))
        plt.ylabel('wavelength * flux (um * mJy)')
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('wavelength (um)')
    plt.grid(True)

# Main Programs
#=======================================================
if __name__ == '__main__':
    t_start = time.time()

    # # Check inputs
    # if len(argv) != 4:
        # exit('\n\tExample: python [program] [input catalog] [piece-size] [normalize]\
              # \n\t[piece-size]: # of SED in ALL_SED_PLOT plot\
              # \n\t[normalize]: True/False (default: False)\n')

   # Parser arguments
    parser = ArgumentParser(description="Plot SED (Spectral Energy Distribution)",\
                            epilog=" ")
    parser.add_argument("inp_cat", type=str, help="Input catalog to plot SED")
    parser.add_argument("-p", "--piece_num", dest="piece", default=10, type=int, help="Number of SED on a plot")
    parser.add_argument("-n", "--normalize",  dest="norm", action='store_true', help="Normalize to max flux",)
    args = parser.parse_args()
    inp_cat = args.inp_cat
    piece   = args.piece
    Norm    = args.norm

    # Input variables
    print('\nStart plotting SEDs ...\
           \nCatalog: {}\
           \nNorm   : {}\
           \nBands  : {}\
           \nMag_ID : {}\
           \nJHK_f0 (mJy)    : {}\
           \nWavelength (um) : {}\
           \nQua_ID          : {}'
           .format(\
           inp_cat, Norm, str(band), str(wavelength), str(JHK_f0), str(col_index), str(flux_qua)))

    # Check output directories
    if path.isdir('SED_PLOT'):
        system('rm -fr SED_PLOT && mkdir SED_PLOT')
    else:
        system('mkdir SED_PLOT')
    if path.isdir('ALL_SED_PLOT'):
        system('rm -fr ALL_SED_PLOT && mkdir ALL_SED_PLOT')
    else:
        system('mkdir ALL_SED_PLOT')

    # Load catalog
    with open(inp_cat, 'r') as cat:
        data = cat.readlines()

    # Plot individual SED plot
    print('\nMake SED PLOT individually ...')
    chdir('SED_PLOT')
    for i in range(len(data)):
        drawProgressBar(float(i+1) / len(data))
        row = data[i].split()
        ra, dec = row[coor_ID[0]], row[coor_ID[1]]
        flux_list, qua_list = mag_to_flux_JHK_and_flux_IR1_To_MP1(row)
        plt.figure()
        plot_individual_SED(flux_list, qua_list, Norm, i)
        plt.legend(loc='lower right')
        plt.title('{:.7f},  {:.7f}'.format(float(ra), float(dec)))
        plt.savefig('{:d}-{}-SED.png'.format(i+1, qua_list))

    # Generate color of dots on SED
    color_list = []
    if piece <= 10:
        for i in range(piece):
            color_list.append('C'+str(i))
    else:
        for i in range(piece):
            color_list.append('C'+str(i))
        for j in range(10, piece):
            color_list.append((round(random.random(), 3),\
                               round(random.random(), 3),\
                               round(random.random(), 3)))

    # Generate all SED plot
    chdir('../ALL_SED_PLOT')
    cuts = list(np.arange(0, len(data), piece)) + [len(data)]
    print('\n\nMake all SED PLOT ...')
    for h in range(len(cuts)-1):
        plt.figure(figsize=(18,9))
        for i in range(cuts[h], cuts[h+1]):
            row = data[i].split()
            flux_list, qua_list = mag_to_flux_JHK_and_flux_IR1_To_MP1(row)
            plot_individual_SED(flux_list, qua_list, Norm, i, color=color_list[i-cuts[h]])
        plt.legend(loc='lower right')
        plt.title('{} - {}'.format(cuts[h], cuts[h+1]-1))
        plt.savefig('ALL-SED-{:d}.png'.format(h+1))
        drawProgressBar(float(h+1)/((len(data)//piece)+1))
    chdir('../')
    t_end  = time.time()
    print('\n\nWhole {} took {:.3f} secs\n'.format(parser.prog, t_end-t_start))
