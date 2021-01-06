#!/usr/bin/env python
'''
----------------------------------------------------------------------
Abstract:
    This program is for cutting diff bands of SPITZER Mosiac WI WCS

Input  : catalog with WCS (RA, DEC) in deg
Output : Fits_and_shape directory with mosaics of different bands
Example: [program] [catalog] [cloud's name]
                   [horizontal_pix_num] [vertical_pix_num] [option]
Input Variables:
    [catalog]            : input catalog
    [cloud's name]       : Name of cloud region of input catalog
    [horizontal_pix_num] : pixel number to cut (must be integer)
    [vertical_pix_num]   : pixel number to cut (must be integer)
    [option]             : Saturate / Image_Check / IR1_Check/ NAN
----------------------------------------------------------------------
latest update: 2020/08/01 Jordan Wu'''

# Load Modules
#======================================================
from __future__ import print_function, division
from astropy import units as u
from astropy.coordinates import SkyCoord
from argparse import ArgumentParser
from os import system, path
from All_Variables import *
from Hsieh_Functions import *
from Useful_Functions import *
import SOP_Program_Path as spp
import time

# Global Variables
#======================================================
# IR1, IR2, IR3, IR4, MP1 (Spitzer Bands)
coor_ID           = coor_ID
qua_ID_Spitzer    = qua_ID_Spitzer
psf_ID_Spitzer    = psf_ID_Spitzer
Spitzer_band_name = Spitzer_band_name

# Functions
#======================================================
def deg_to_hms(Ra_deg, Dec_deg):
    '''
    This is to transform RA/DEC from deg to hhmmss
    '''
    Coord = SkyCoord(ra=Ra_deg*u.degree, dec=Dec_deg*u.degree)
    Ra_hms, Dec_hms = Coord.to_string('hmsdms', sep=(':')).split()
    return Ra_hms, Dec_hms

def generate_MOSAIC_path(cloud):
    '''
    This is to generate Mosiaic path
    '''
    if 'LUP' in cloud:
        path = '{}LUP/MOSAICS/'.format(spp.Mosaic_path)
    else:
        path = '{}{}/MOSAICS/'.format(spp.Mosaic_path, cloud)
    return path

def generate_MOSAIC_ls(cloud):
    '''
    This is to generate Mosaic fits list according
    to different cloud (SPITZER Data)
    '''
    if cloud == 'PER':
        MOSAIC_ls=["PER_ALL_COMB_IRAC1_mosaic.fits",\
                   "PER_ALL_COMB_IRAC2_mosaic.fits",\
                   "PER_ALL_COMB_IRAC3_mosaic.fits",\
                   "PER_ALL_COMB_IRAC4_mosaic.fits",\
                   "PER_ALL_A_MIPS1_mosaic.fits"]
    elif cloud == 'OPH':
        MOSAIC_ls = ["OPH_ALL_COMB_IRAC1_mosaic.fits",\
                     "OPH_ALL_COMB_IRAC2_mosaic.fits",\
                     "OPH_ALL_COMB_IRAC3_mosaic.fits",\
                     "OPH_ALL_COMB_IRAC4_mosaic.fits",\
                     "OPH_ALL_A_MIPS1_mosaic.fits"]
    else:
        MOSAIC = ["_COMB_IRAC1_mosaic.fits",\
                  "_COMB_IRAC2_mosaic.fits",\
                  "_COMB_IRAC3_mosaic.fits",\
                  "_COMB_IRAC4_mosaic.fits",
                  "_A_MIPS1_mosaic.fits"]
        MOSAIC_ls = ['{}{}'.format(cloud, MOS) for MOS in MOSAIC]
    return MOSAIC_ls

# Main Program
#======================================================
if __name__ == '__main__':
    wf_start = time.time()

    # Parser arguments
    parser = ArgumentParser(description="Print out catalog information",\
                            epilog="Purpose: Saturate / Image_Check / IR1_Check/ NAN")
    parser.add_argument("inp_cat", type=str, help="Input catalog")
    parser.add_argument("cloud", type=str, help="Cloud name in SPITZER region")
    parser.add_argument("-hp", "--hor_pix", default=100, dest="hor_pix", type=int, help="Horizontal pixel cut")
    parser.add_argument("-vp", "--ver_pix", default=100, dest="ver_pix", type=int, help="Vertical pixel cut")
    parser.add_argument("-opt", "--option", default="NAN", dest="option", type=str, help="Purpose for FITS image")
    args = parser.parse_args()
    inp_cat = args.inp_cat
    cloud   = args.cloud
    hor_pix = args.hor_pix
    ver_pix = args.ver_pix
    option  = args.option

    # Initialization
    fits_dir = '{}_{}_Fits_and_shape'.format(cloud, option)
    if path.isdir(fits_dir):
        system('rm -r {} && mkdir {}'.format(fits_dir, fits_dir))
    path      = generate_MOSAIC_path(cloud)
    MOSAIC_ls = generate_MOSAIC_ls(cloud)
    with open(inp_cat,'r') as cat:
        catalog = cat.readlines()

    # From WCS To Fits
    new_rows = []
    print('\nGet SPITZER image cut WI WCS (# to cut: {:d})'.format(len(catalog)))
    for i, row in enumerate(catalog):
        drawProgressBar(float(i+1)/len(catalog))
        cols = row.split()

        # Transform from deg to hhmmss
        Qua  = [cols[ID] for ID in qua_ID_Spitzer]
        Psf  = [cols[ID] for ID in psf_ID_Spitzer]
        Ra_deg, Dec_deg = float(cols[coor_ID[0]]), float(cols[coor_ID[1]])
        Ra_hms, Dec_hms = deg_to_hms(Ra_deg, Dec_deg)
        new_row = "{}\t{}\t{}\t{}\t{}\t{}\n".format(\
                   Ra_deg, Dec_deg, Ra_hms, Dec_hms, "".join(Qua), "".join(Psf))
        new_rows.append(new_row)

        # Get fits according to WCS
        qdir_name = "{:d}_{}".format(i+1, "".join(Qua))
        system("mkdir {}".format(qdir_name))
        for j in range(len(MOSAIC_ls)):
            fits_name = "{}_{:d}.fits".format(Spitzer_band_name[j], i+1)
            system("getfits -o {} {}{} {}, {} {:d} {:d} &> /dev/null".format(\
                    fits_name, path, MOSAIC_ls[j], Ra_hms, Dec_hms, hor_pix, ver_pix))
            system("mv {} {}".format(fits_name, qdir_name))
        system("mv {} {}".format(qdir_name, fits_dir))

    # Save tables ...
    print('\nStore WCS table ...')
    with open('{}_cans_to_wcs.tbl'.format(cloud), 'w') as out_cat:
        for row in new_rows:
            out_cat.write(row)
    wf_end   = time.time()
    print('{} took {:.3f} secs\n'.format(parser.prog, wf_end-wf_start))
