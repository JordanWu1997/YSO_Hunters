#!/usr/bin/python
import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from Hsieh_Functions import *
from sys import argv, exit
from os import system, chdir, path

Jaxlim   = Hsieh_Jaxlim
IR1axlim = Hsieh_IR1axlim
IR2axlim = Hsieh_IR2axlim
IR3axlim = Hsieh_IR3axlim
IR4axlim = Hsieh_IR4axlim
MP1axlim = Hsieh_MP1axlim
band_list = ['J', 'IR1', 'IR2', 'IR3', 'IR4', 'MP1']
axlim_list = [Jaxlim, IR1axlim, IR2axlim, IR3axlim, IR4axlim, MP1axlim]

if len(argv) != 8:
    exit('\n\texample: [program] [band1-x] [band2-y] [band3-z] [cubesize] [gal_dict] [shape] [overwrite]\n')

band = [int(argv[1]), int(argv[2]), int(argv[3])]
cube = float(argv[4])
gal_dict = str(argv[5])
shape = str(argv[6])
overwrite = str(argv[7])
image_dir = '{:d}{:d}{:d}_{}_{}_{}_fake_source_tomography'\
        .format(band[0], band[1], band[2], band_list[band[0]], band_list[band[1]], band_list[band[2]])

# Load Galaxy Probability Dictionary
gal_prob_dict = np.load(gal_dict).item()
space_shape = np.load(shape)

# Initialize Storage Directory
if path.isdir(image_dir):
    if overwrite == 'y':
        system('rm -rf ' + image_dir)
        system('mkdir ' + image_dir)
    else:
        exit()
else:
    system('mkdir ' + image_dir)

# Make Fake Source Grid
x_axis = np.linspace(0, space_shape[band[0]]-1, space_shape[band[0]], endpoint=True)
y_axis = np.linspace(0, space_shape[band[1]]-1, space_shape[band[1]], endpoint=True)
z_axis = np.linspace(0, space_shape[band[2]]-1, space_shape[band[2]], endpoint=True)

chdir(image_dir)
t_start = time.time()
print('Start plotting ...')
for i, z in enumerate(z_axis):
    print('{:.3%}'.format(float(i)/len(z_axis)))
    fig = plt.figure(figsize = (8,8))
    ax = fig.add_subplot(111, projection='3d')
    for y in y_axis:
        for x in x_axis:
            # Make Key for Each Fake Source
            key = [-999] * len(axlim_list)
            key[band[0]] = int(x)
            key[band[1]] = int(y)
            key[band[2]] = int(z)
            key = tuple(key)
            if key in gal_prob_dict.keys():
                value = gal_prob_dict[key]
            else:
                value = 0.
            # Plot Scatter
            if value > 1.:
                ax.scatter(x, y, z, s=10, c='red')
            elif value == 1.:
                ax.scatter(x, y, z, s=10, c='gold')
            elif value < 1. and value > 0.:
                ax.scatter(x, y, z, s=10, c='blue')
            else:
                ax.scatter(x, y, z, s=10, c='grey')
    # Save Image
    ax.set_xlabel(band_list[band[0]])
    ax.set_ylabel(band_list[band[1]])
    ax.set_zlabel(band_list[band[2]])
    ax.set_xlim3d(0, space_shape[band[0]])
    ax.set_ylim3d(0, space_shape[band[1]])
    ax.set_zlim3d(0, space_shape[band[2]])
    ax.set_title('{}_{}_{}'.format(band_list[band[0]], band_list[band[1]], band_list[band[2]]))
    plt.savefig('{:0>3d}_{}_{}_{}.png'.format(int(i), band_list[band[0]], band_list[band[1]], band_list[band[2]]))
t_end = time.time()
print('whole process took {:.3f} secs'.format(t_end - t_start))
chdir('../')
