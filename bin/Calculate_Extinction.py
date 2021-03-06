#!/usr/bin/env python
'''
Abstract:
    This is a program for calculate the extinction of each source with NICER
Usage:
    calculate_extinction.py [coord_table] [mag_table] [err_mag_table] [Rv] [bin size]
    Available Rv: WD55B, WD31B
    Four files would be generated:
        1. Av of each input source.
        Av_table = [[Av1, stdev1],
                    [Av2, stdev2],
                    [Av3, stdev3],
                    ...]
        2. The plot of the histogram of Av of input sources.
        3. extinction map, a fits image file.
        4. extinction map in table format.
        table =[[RA, DEC, Av1, stdev1],
                [RA, DEC, Av2, stdev2],
                [RA, DEC, Av3, stdev3],
                ...]
Editor:
    JW Wang, Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20180815
####################################
update log
20180815 version alpha 1
    1. The code works
20180823 version alpha 2
    2. Add a option for Rv
'''
import numpy as np
from pnicer import ApparentMagnitudes as AM
from astropy.coordinates import *
from astropy.io import fits as pyfits
from astropy import wcs
import matplotlib.pyplot as plt
from extinction_curves_lib import WD_55B_twomass, WD_31B
from sys import argv
import time
import DL_conf

#--------------------------------------------
# main code
if __name__ == "__main__":
    # measure time
    start_time = time.time()
    #--------------------------------------------
    # Load argv
    if len(argv) != 6:
        print ("Wrong number of arguments")
        print ("Usage: calculate_extinction.py [coord_table] [mag_table] [err_mag_table] [Rv] [bin size in arcmin]")
        print ("Available Rv: WD55B, WD31B")
        exit(1)
    coord_table_name = argv[1]
    mag_table_name = argv[2]
    err_mag_table_name = argv[3]
    Rv = argv[4]
    bin_size = float(argv[5])/60.
    #--------------------------------------------
    # Load files
    science_coord = np.loadtxt(coord_table_name, dtype = float)
    science_coord_shape = science_coord.shape
    science_coord = SkyCoord(science_coord, frame='icrs', unit='deg')
    science_mag = np.loadtxt(mag_table_name, dtype = float)
    science_err_mag = np.loadtxt(err_mag_table_name, dtype = float)
    control_coord = np.loadtxt("{0}/ELAIS_N1_NICER_control_image/star_coord.txt".format(DL_conf.path_of_data), dtype = float)
    control_coord = SkyCoord(control_coord, frame='icrs', unit='deg')
    control_mag = np.loadtxt("{0}/ELAIS_N1_NICER_control_image/twomass_mag.txt".format(DL_conf.path_of_data), dtype = float)
    control_err_mag = np.loadtxt("{0}/ELAIS_N1_NICER_control_image/err_twomass_mag.txt".format(DL_conf.path_of_data), dtype = float)
    # Read source which is allOBS in JHK band only
    index_science_allOBS = np.where((science_mag[:,0] != 0) & (science_mag[:,1] != 0) &(science_mag[:,2] != 0))
    index_control_allOBS = np.where((control_mag[:,0] != 0) & (control_mag[:,1] != 0) &(control_mag[:,2] != 0))
    science_coord = science_coord[index_science_allOBS]
    science_mag = science_mag[index_science_allOBS]
    science_mag = np.transpose(science_mag)
    science_err_mag = science_err_mag[index_science_allOBS]
    science_err_mag = np.transpose(science_err_mag)
    control_coord = control_coord[index_control_allOBS]
    control_coord = control_coord[:len(control_coord)//4]
    control_mag = control_mag[index_control_allOBS]
    control_mag = control_mag[:len(control_mag)//4]
    control_mag = np.transpose(control_mag)
    control_err_mag = control_err_mag[index_control_allOBS]
    control_err_mag = control_err_mag[:len(control_err_mag)//4]
    control_err_mag = np.transpose(control_err_mag)
    #--------------------------------------------
    # Calculate the extinction
    # Initialize
    mag_names = ["J"  , "H"   , "Ks"   ]
    extvec = []
    if Rv == 'WD55B':
        extvec = [  WD_55B_twomass[0][3],
                    WD_55B_twomass[1][3],
                    WD_55B_twomass[2][3]]
    elif Rv == 'WD31B':
        extvec = [  WD_31B[0][3],
                    WD_31B[1][3],
                    WD_31B[2][3]]
    else:
        print ('Wrong Rv value')
        print ('Available Rv: WD55B, WD31B')
        exit()
    science = AM(magnitudes = science_mag,
                errors = science_err_mag,
                extvec = extvec,
                coordinates = science_coord,
                names = mag_names)
    control = AM(magnitudes = control_mag,
                errors = control_err_mag,
                extvec = extvec,
                coordinates = control_coord,
                names = mag_names)
    ext_nicer = science.nicer(control=control)
    #--------------------------------------------
    # Save the Av of each sources
    Av_nicer=ext_nicer.extinction
    var_Av_nicer = ext_nicer.variance
    std_Av_nicer = np.sqrt(var_Av_nicer)
    Av = np.array([Av_nicer , std_Av_nicer])
    Av = np.transpose(Av)
    all_Av = np.zeros(science_coord_shape)
    all_Av[index_science_allOBS, 0] = Av_nicer
    all_Av[index_science_allOBS, 1] = std_Av_nicer
    # Output 1
    np.savetxt('{0}_Av.dat'.format(coord_table_name[:-10]), all_Av, fmt="%1.4f")
    # Save extinction map
    #                                pixel size(degree)                       gaussian in pixel
    nicer_emap = ext_nicer.build_map(bandwidth = bin_size, metric="gaussian", sampling=5        , use_fwhm=True)
    nicer_emap_name = '{0}emap_{1:.0f}arcsec'.format(coord_table_name[:-9], bin_size * 3600)
    # Output 2
    nicer_emap.save_fits(path="./{0}.fits".format(nicer_emap_name))
    #----------------------------------
    # Convert extinction map to extinction table
    # Load data
    hdu = pyfits.open('{0}.fits'.format(nicer_emap_name))
    header = hdu[1].header
    emap = hdu[1].data
    err_emap = hdu[2].data
    # reshape data
    x_pix = range(emap.shape[1])
    y_pix = range(emap.shape[0])
    xv_pix, yv_pix = np.meshgrid(x_pix, y_pix)
    xv_pix = xv_pix.flatten()
    yv_pix = yv_pix.flatten()
    emap = emap.flatten()
    err_emap = err_emap.flatten()
    # Convert pixel to wcs
    w = wcs.WCS(header)
    pixcrd = np.array([xv_pix, yv_pix])
    pixcrd = np.transpose(pixcrd)
    world = w.wcs_pix2world(pixcrd, 1)
    world = np.transpose(world)
    emap_table = np.array([world[0], world[1], emap, err_emap])
    emap_table = np.transpose(emap_table)
    # Save Av and position into table.
    # Output 3
    np.savetxt("{0}.txt".format(nicer_emap_name), emap_table, fmt="%1.4f")
    #-----------------------------------
    # measure time
    elapsed_time = time.time() - start_time
    print ("Exiting Main Program, spending ", elapsed_time, "seconds.")
