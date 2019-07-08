#!/usr/bin/ipython
'''----------------------------------------------------------------
This program is origionally from Ken
This program is for plotting projection of different dimensional GP arrays
-------------------------------------------------------------------
latest update : 2019/05/12 Jordan Wu'''

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sys import argv, exit
from os import system, chdir, path
from os.path import isdir

# Input Check
if len(argv) == 2 or len(argv) == 6:
    print('Input Check pass ...')
else:
    exit('Example:\n\
            (1) [python] [program] [option]\n\
            (2) [python] [program] [option] [binsize] [lower_lim] [upper_lim] [unit of lim]\n\
            option: old/new/latest UKIDSS CATALOG: WO COND/WI COND/WI COND AND NEW BOUND\n\
            unit of lim: std/value in standard deviation or in exact values')

# Select model, binsize, and bound of output images
# Input W/I command line argv
if str(argv[-1])=='argv':
    Binsize = str(argv[2])
    lower = float(argv[3])
    upper = float(argv[4])
    unit = str(argv[5])
# Input W/I python input
else:
    Binsize = str(input('binsize = '))
    lower = float(input('Lower limit of value = '))
    upper = float(input('Upper limit of value = '))
    unit = str(raw_input('bound unit (std/value) = '))

if str(argv[1]) == 'old':
    path = '/home/ken/new_mg/GPV_SOP_Program/result' + Binsize + '/'
    title = 'UKIDSS catalog WO condition '
elif str(argv[1]) == 'new':
    path = '/home/ken/new_mg/GPV_SOP_Program/result_condition_' + Binsize + '/'
    title = 'UKIDSS catalog WI condition '
elif str(argv[1]) == 'latest':
    path = '/home/ken/new_mg/GPV_SOP_Program/' ###################### TO BE CONTINUED ...
    title = 'UKIDSS catalog WI condition, WI new_boundary '
else:
    exit('Wrong model selection ...')
title += (';bs='+ Binsize + ' ;value: ' + str(lower) + '~' + str(upper) + ' ' + unit)

# Load data
print('Array path: ' + path)
data = path + 'all_detect_grid_Full_6d.npy'
sixd = np.load(data).item()

# Parameter
cube = float(Binsize)
if str(argv[1]) != 'latest':
    Jaxlim =   [4.0, 18.0]
    IR1axlim = [8.0, 18.0]
    IR2axlim = [7.0, 18.0]
    IR3axlim = [5.0, 18.0]
    IR4axlim = [5.0, 18.0]
    MP1axlim = [3.5, 11.0]
else:
    # NEW BOUNDARY WI UKIDSS CATALOG
    Jaxlim =   [3.5, 22.0]
    IR1axlim = [8.0, 20.0]
    IR2axlim = [7.0, 19.0]
    IR3axlim = [5.0, 18.0]
    IR4axlim = [5.0, 18.0]
    MP1axlim = [3.5, 12.0]

bands = ['J', 'IR1', 'IR2', 'IR3', 'IR4', 'MP1']
band_lim_list = [Jaxlim, IR1axlim, IR2axlim, IR3axlim, IR4axlim, MP1axlim]
bin_num_list = []
for i in range(len(bands)):
    bin_num_list.append(int((band_lim_list[i][1]-band_lim_list[i][0])/cube))

# Start choosing bands
if isdir('6d_plot_' + str(Binsize)):
    system('rm -fr ' + '6d_plot_' + str(Binsize))
    system('mkdir 6d_plot_' + str(Binsize))
else:
    system('mkdir 6d_plot_' + str(Binsize))

chdir('6d_plot_' + str(Binsize))
for band1 in range(6):
    for band2 in range(band1):
        print(band2, band1)
        z = np.zeros((bin_num_list[band2]+1, bin_num_list[band1]+1))
        
        # Get data
        for key in sixd.keys():
            inin = key.strip('( )')
            g = inin.split(',')
            z[int(g[band2])][int(g[band1])] += float(sixd[key])
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        if unit == 'std':
            plt.imshow(z, vmin = np.mean(z) + lower*np.std(z), vmax = np.mean(z) + upper*np.std(z))
        elif unit == 'value':
            plt.imshow(z, vmin = lower, vmax = upper)

        ax.set_title(title)
        ax.set_xlabel(str(bands[band1]))
        ax.set_ylabel(str(bands[band2]))
        ax.set_xticks(np.arange(0, bin_num_list[band1], 5))
        ax.set_yticks(np.arange(0, bin_num_list[band2], 5))
        ax.set_xticklabels(np.arange(1, bin_num_list[band1]+1, 5))
        ax.set_yticklabels(np.arange(1, bin_num_list[band2]+1, 5))
        ax.set_xticks(np.arange(-0.5, bin_num_list[band1], 1), minor=True);
        ax.set_yticks(np.arange(-0.5, bin_num_list[band2], 1), minor=True);
        ax.grid(which='minor', color='w', linestyle='-')
        
        plt.colorbar()
        plt.savefig(str(bands[band2] + '-' + bands[band1]))
