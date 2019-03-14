#!/usr/bin/ipython

'''
-------------------------------------------------------------------
This program is for step4 (MP1_Saturate)

Input : c2d HREL catalog after extinction correction

Output : catalog with (1)quality == 'U', source that are not saturate but undetected
                      (2)quality == 'S', source that might be saturate or undetected
                                         still need to image check
-------------------------------------------------------------------
latest update : 2018/09/06
'''

from os import system
from sys import argv
from sys import exit
import pyfits


if len(argv) != 3:
    print('Error: Wrong Usage')
    print('Example: ipython Find_Saturate.py [catalog] [cloud\'s name]')
    exit()

catalog = open(argv[-2])
cloud = argv[-1]
catalog = catalog.readlines()

if "LUP" in cloud:
    mosaic_path = "/data/public/spitzer/c2d/data.spitzer.caltech.edu/popular/c2d/20071101_enhanced_v1/" + "LUP" + "/MOSAICS/"
    mosaic_band_li = ["_COMB_IRAC1_mosaic.fits","_COMB_IRAC2_mosaic.fits","_COMB_IRAC3_mosaic.fits","_COMB_IRAC4_mosaic.fits","_A_MIPS1_mosaic.fits"]

elif cloud == "PER":
    mosaic_path = "/data/public/spitzer/c2d/data.spitzer.caltech.edu/popular/c2d/20071101_enhanced_v1/" + "PER" + "/MOSAICS/"
    mosaic_band_li = ["_ALL_COMB_IRAC1_mosaic.fits","_ALL_COMB_IRAC2_mosaic.fits","_ALL_COMB_IRAC3_mosaic.fits","_ALL_COMB_IRAC4_mosaic.fits","_ALL_A_MIPS1_mosaic.fits"]

else:
    mosaic_path = "/data/public/spitzer/c2d/data.spitzer.caltech.edu/popular/c2d/20071101_enhanced_v1/" + str(cloud) + "/MOSAICS/"
    mosaic_band_li = ["_COMB_IRAC1_mosaic.fits","_COMB_IRAC2_mosaic.fits","_COMB_IRAC3_mosaic.fits","_COMB_IRAC4_mosaic.fits","_A_MIPS1_mosaic.fits"]

name = " "
mosaic_name_li = []

for band in mosaic_band_li:
    name = str(cloud) + band
    mosaic_name_li.append(name)

band_li = ['IR1','IR2','IR3','IR4','MP1']

# array that store different band's mosaic
mosaic_li = []
for i in range(len(mosaic_name_li)):
    fi = pyfits.open(mosaic_path + mosaic_name_li[i])
    fits = fi[0].data
    mosaic_li.append(fits)

# Indice
imtype_in = [102,123,144,165,186]
Qua_in = [100,121,142,163,184]

# Source's pixel value larger than that is classified 'saturate'
band_cut_li=[50,50,300,300,800]

FWHM_in = [1.66,1.72,1.88,1.98,6] #arcsec
pixel_size = 1.22 #arcsec

# Saturae Radius 3sigma
SatR_li = []
for i in range(len(FWHM_in)):
    SatR = []
    R_pix = FWHM_in[i]/2.35*3/1.22
    for m in range(-10, 10):
	for n in range(-10, 10):
            #Region of Saturate
	    if m**2 + n**2 < R_pix**2:
                SatR.append([m,n])
    SatR_li.append(SatR)

cats = open('step','w')
new_catalog = []
for i in range(len(catalog)):
    line = catalog[i]
    line = line.split()
        
    # Remove sources only detected in 2mass
    if line[16] != '2mass':
        # save cats with ra and dec in new_catalog
        cats.write(line[0] + "\t" + line[2] + "\n")
        new_catalog.append(line)
cats.close()


for i in range(len(mosaic_li)):
    system('sky2xy '+ mosaic_path + mosaic_name_li[i] + ' @step > ' + band_li[i] + '_sources_pix')
    cats = open(band_li[i] + '_sources_pix','r')
    cats = cats.readlines()
	
    for j in range(len(cats)):
	pos_line = cats[j].split()
	
        if len(pos_line) == 8:
	    break
	
        pos_pix = [round(float(pos_line[4])),round(float(pos_line[5]))]
	for k in range(len(SatR_li[i])):
	    vec = SatR_li[i][k]
	    
            if new_catalog[j][Qua_in[i]] == "U" or new_catalog[j][Qua_in[i]] == "N":
	        
                if mosaic_li[i][int(pos_pix[1] + vec[1])][int(pos_pix[0] + vec[0])] > band_cut_li[i]:
		    new_catalog[j][Qua_in[i]] = "S"

output = open(str(cloud) + '_saturate_correct_file.tbl','w')
output.write("\n".join(["\t".join(line) for line in new_catalog]))

system('rm step *pix')
