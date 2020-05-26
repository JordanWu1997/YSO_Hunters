#!/usr/bin/python
'''
-------------------------------------------------------------------
This program is for step4 (MP1_Saturate)

Input: c2d HREL catalog after extinction correction

Output: catalog with (1)quality == 'U', source that are not saturate but undetected
                     (2)quality == 'S', source that might be saturate or undetected
                                        still need to image check

Example: [program] [catalog] [cloud's name]
-------------------------------------------------------------------
Latest update: 2019/05/26 Jordan Wu'''

# Import Modules
#======================================================
from os import system
from sys import argv, exit
import pyfits
import SOP_Program_Path as spp
from Hsiehs_Function import *

# Global Variables
#=======================================================
# Band name list
band_li     = ['IR1','IR2','IR3','IR4','MP1']
imtype_in   = [102, 123, 144, 165, 186]
Qua_in      = [100, 121, 142, 163, 184]
# Source's pixel value larger than that is classified 'saturate'
band_cut_li = [50, 50, 300, 300, 800]
FWHM_in     = [1.66, 1.72, 1.88, 1.98, 6] # arcsec
pixel_size  = 1.22 # arcsec
coor_ID     = coor_ID  # RA, Dec on input table
# Functions
#======================================================
def generate_mosaic_name_list(cloud):
    '''
    Generate different mosaic name and path for different input cloud
    '''
    if "LUP" in cloud:
        mosaic_path = spp.Mosaic_path + "LUP" + "/MOSAICS/"
        mosaic_band_li = ["_COMB_IRAC1_mosaic.fits", \
                          "_COMB_IRAC2_mosaic.fits", \
                          "_COMB_IRAC3_mosaic.fits", \
                          "_COMB_IRAC4_mosaic.fits", \
                          "_A_MIPS1_mosaic.fits"]
    elif cloud == "PER":
        mosaic_path = spp.Mosaic_path + "PER" + "/MOSAICS/"
        mosaic_band_li = ["_ALL_COMB_IRAC1_mosaic.fits", \
                          "_ALL_COMB_IRAC2_mosaic.fits", \
                          "_ALL_COMB_IRAC3_mosaic.fits", \
                          "_ALL_COMB_IRAC4_mosaic.fits", \
                          "_ALL_A_MIPS1_mosaic.fits"]
    elif cloud == "OPH":
        mosaic_path = spp.Mosaic_path + "OPH" + "/MOSAICS/"
        mosaic_band_li = ["_ALL_COMB_IRAC1_mosaic.fits", \
                          "_ALL_COMB_IRAC2_mosaic.fits", \
                          "_ALL_COMB_IRAC3_mosaic.fits", \
                          "_ALL_COMB_IRAC4_mosaic.fits", \
                          "_ALL_A_MIPS1_mosaic.fits"]
    else:
        mosaic_path = spp.Mosaic_path + str(cloud) + "/MOSAICS/"
        mosaic_band_li = ["_COMB_IRAC1_mosaic.fits", \
                          "_COMB_IRAC2_mosaic.fits", \
                          "_COMB_IRAC3_mosaic.fits", \
                          "_COMB_IRAC4_mosaic.fits", \
                          "_A_MIPS1_mosaic.fits"]

    mosaic_name_list = ['{}{}'.format(cloud, band) for band in mosaic_band_li]
    return mosaic_path, mosaic_name_list

def load_mosaic(mosaic_path, mosaic_name_list):
    '''
    array that store different band's mosaic
    '''
    mosaic_li = []
    for i in range(len(mosaic_name_li)):
        mosaic_fits = pyfits.open('{}{}'.format(mosaic_path, mosaic_name_li[i]))[0].data
        mosaic_li.append(mosaic_fits)
    return mosaic_li

def generate_saturate_region_for_all_bands(FWHM_in):
    '''
    Saturate Radius 3sigma
    '''
    SatR_li = []
    for i in range(len(FWHM_in)):
        SatR = []
        R_pix = FWHM_in[i] / 2.35 * 3 / 1.22
        for m in range(-10, 10):
            for n in range(-10, 10):
                # Region of given pixel radius
                if ((m ** 2 + n ** 2) < (R_pix ** 2)):
                    SatR.append([m,n])
        SatR_li.append(SatR)
    return SatR_li

# Main Programs
#======================================================
if __name__ == '__main__':

    # Check inputs
    if len(argv) != 3:
        exit('\n\tError: Wrong Usage\
              \n\tExample: [program] [catalog] [cloud\'s name]\n')

    # Input variables
    catalog_name = str(argv[1])
    cloud        = str(argv[2])

    # Load input catalog
    with open(catalog_name, 'r') as inp:
        catalog = inp.readlines()

    # Write out RA, DEC for input catalog
    with open('step', 'w') as cats:
        for i in range(len(catalog)):
            line = catalog[i].split()
            # Must remove sources that only detected in 2mass from previous steps
            cats.write('{}\t{}\n'.format(line[coor_ID[0]], line[coor_ID[1]]))

    # Load mosaic
    mosaic_path, mosaic_name_li = generate_mosaic_name_list(cloud)
    mosaic_li = load_mosaic(mosaic_path, mosaic_name_li)

    # Generate saturate check region
    SatR_li = generate_saturate_region_for_all_bands(FWHM_in)

    # Check if object is saturate
    for i in range(len(mosaic_li)):
        # Transform from sky coordinate to pixel xy coordinate
        system('sky2xy '+ mosaic_path + mosaic_name_li[i] + ' @step > ' + band_li[i] + '_sources_pix')
        # Load pixel xy coordinate table
        with open(band_li[i] + '_sources_pix','r') as coor_table:
            cats = coor_table.readlines()

        for j in range(len(cats)):
            pos_line = cats[j].split()
            if len(pos_line) == 8:
                break
            pos_pix = [round(float(pos_line[4])), round(float(pos_line[5]))]
            for k in range(len(SatR_li[i])):
                vec = SatR_li[i][k]
                if (catalog[j][Qua_in[i]] == "U") or (catalog[Qua_in[i]] == "N"):
                    if (mosaic_li[i][int(pos_pix[1] + vec[1])][int(pos_pix[0] + vec[0])] > band_cut_li[i]):
                        catalog[j][Qua_in[i]] = "S"

    # Save result and remove temporary step files
    system('rm step *pix')
    with open('{}_saturate_correct_file.tbl'.format(cloud), 'w') as output:
        new_catalog = ["\t".join(line) for line in catalog]
        output.write("\n".join(new_catalog) + "\n")
