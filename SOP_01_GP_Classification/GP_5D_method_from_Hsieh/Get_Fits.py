#!/usr/bin/env python

'''----------------------------------------------------------------
This program is a part of program for Step6 (Image_Check)

Input : catalog_to_Image_Check with (ra/dec) , wcs , imagetype

Output : Fits_and_shape directory with different bands' mosaics
-------------------------------------------------------------------
latest update : 2019/10/18'''

from os import system, path
from sys import argv, exit
import SOP_Program_Path as spp

if len(argv) != 4:
    exit('\n\tEample: python [catalog] [cloud\'s name] [option] \
          \n\t[option]: Saturate / Image_Check / IR1_Check / NAN\n')

catalog = open(argv[1],'r')
coor = catalog.readlines()
catalog.close()
cloud = str(argv[2])
option = str(argv[3])

if path.isdir(cloud + "_" + option + "_Fits_and_shape"):
    system("rm -r " + cloud + "_" + option + "_Fits_and_shape")

#=======================================
if cloud == 'PER':
    MOSAIC_li = ["PER_ALL_COMB_IRAC1_mosaic.fits","PER_ALL_COMB_IRAC2_mosaic.fits","PER_ALL_COMB_IRAC3_mosaic.fits","PER_ALL_COMB_IRAC4_mosaic.fits","PER_ALL_A_MIPS1_mosaic.fits"]
elif cloud == 'OPH':
    MOSAIC_li = ["OPH_ALL_COMB_IRAC1_mosaic.fits","OPH_ALL_COMB_IRAC2_mosaic.fits","OPH_ALL_COMB_IRAC3_mosaic.fits","OPH_ALL_COMB_IRAC4_mosaic.fits","OPH_ALL_A_MIPS1_mosaic.fits"]

else:
    MOSAIC = ["_COMB_IRAC1_mosaic.fits","_COMB_IRAC2_mosaic.fits","_COMB_IRAC3_mosaic.fits","_COMB_IRAC4_mosaic.fits","_A_MIPS1_mosaic.fits"]
    MOSAIC_li = []
    for element in MOSAIC:
        MOSAIC_li.append(cloud+element)

if 'LUP' in cloud:
    path = spp.Mosaic_path + '/LUP/MOSAICS/'
else:
    path = spp.Mosaic_path + cloud + '/MOSAICS/'
#========================================

if option == 'Saturate':
    system("mkdir " + cloud + "_" + option + "_Fits_and_shape")
elif option == 'Image_Check':
    system("mkdir " + cloud + "_" + option + "_Fits_and_shape")
elif option == 'IR1_Check':
    system("mkdir " + cloud + "_" + option + "_Fits_and_shape")
elif option == 'NAN':
    system("mkdir " + cloud + "_" + option + "_Fits_and_shape")
else:
    exit('Wrong option input')

print('\nGet fitting ...')
band = ["IR1","IR2","IR3","IR4","MP1"]
for i in range(len(coor)):

    # Percentage Indicator
    print(str(i+1) + '/' + str(len(coor)))

    # Assuming i+1 always less than 1000
    if i+1 < 10:
        index = '00' + str(i+1)
    elif i+1 < 100:
        index = '0' + str(i+1)
    elif i+1 < 1000:
        index = str(i+1)

    # Get Fits from Images
    Qua = "_" + coor[i].split()[4]
    system("mkdir " + index + Qua)
    for j in range(len(MOSAIC_li)):
	Ra = coor[i].split()[2]
	Dec = coor[i].split()[3]
	system("getfits " + path + MOSAIC_li[j] + " " + Ra + ", " + Dec + "," + " 100 100 -o " + band[j] + "_" + index + ".fits &> /dev/null")
    	system("mv " + band[j] + "_" + index + ".fits " + index + Qua)
    system("mv " + index + Qua + " " + cloud + "_" +  option + "_Fits_and_shape")
