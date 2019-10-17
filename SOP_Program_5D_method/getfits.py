#!/usr/bin/ipython

'''----------------------------------------------------------------
This program is a part of program for Step6 (Image_Check)

Input : catalog_to_Image_Check with (ra/dec) , wcs , imagetype

Output : Fits_and_shape directory with different bands' mosaics
-------------------------------------------------------------------
latest update : 2018/09/18'''

from os import system, path
from sys import argv, exit

if len(argv) != 4:
    print('Eample: python [catalog] [cloud\'s name] [option]')
    print('option: Saturate / Image_Check / IR1_Check / NAN')
    exit()

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
    path = '/data/public/spitzer/c2d/data.spitzer.caltech.edu/popular/c2d/20071101_enhanced_v1/LUP/MOSAICS/'
else:
    path = '/data/public/spitzer/c2d/data.spitzer.caltech.edu/popular/c2d/20071101_enhanced_v1/'+cloud+'/MOSAICS/'
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
    print str(i+1) + '/' + str(len(coor))
    Qua = "_" + coor[i].split()[4]
    system("mkdir " + str(i+1) + Qua)
    for j in range(len(MOSAIC_li)):
	Ra = coor[i].split()[2]
	Dec = coor[i].split()[3]
	system("getfits " + path + MOSAIC_li[j] + " " + Ra + ", " + Dec + "," + " 100 100 -o " + band[j] + "_" + str(i+1) + "fits &> /dev/null")
    	system("mv " + band[j] + "_"+str(i+1) + "fits " + str(i+1) + Qua)
    system("mv "+str(i+1)+Qua+ " " + cloud + "_" +  option + "_Fits_and_shape")
