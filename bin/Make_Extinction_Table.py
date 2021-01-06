#!/usr/bin/env python
'''
#==================================

This Program is from Jacob and revised by Jordan.

#==================================
Jordan Wu 20190806'''

import numpy as np
from astropy.io import fits as pyfits
from astropy import wcs
from sys import argv, exit

if len(argv) != 3:
    exit('\n\tError: Wrong Arguments\
    \n\tExample: [Program] [Extinction Map] [Output Filename]\n')
else:
    print('Making Extinction Tables ...')

image = str(argv[1])
output = str(argv[2])

hdu = pyfits.open(image)
header = hdu[0].header
emap = hdu[0].data

# reshape data
x_pix = range(emap.shape[1])
y_pix = range(emap.shape[0])
xv_pix, yv_pix = np.meshgrid(x_pix, y_pix)
xv_pix = xv_pix.flatten()
yv_pix = yv_pix.flatten()
emap = emap.flatten()
emap[np.isnan(emap)] = 0.0

# Convert pixel to wcs
w = wcs.WCS(header)
pixcrd = np.array([xv_pix, yv_pix])
pixcrd = np.transpose(pixcrd)
world = w.wcs_pix2world(pixcrd, 1)
world = np.transpose(world)
emap_table = np.array([world[0], world[1], emap])
emap_table = np.transpose(emap_table)

# Save Av and position into table.
np.savetxt(output, emap_table, fmt="%1.4f")
