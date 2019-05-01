#!/usr/bin/ipython

'''-------------------------------------------------------------------
This program is for getting fits from catalog with ra, dec in deg

Input : catalog with ra, dec in deg

Output : Fits_and_shape directory with mosaics of different bands

*minor change: (1)name option is added
               (2)save option is added
----------------------------------------------------------------------
latest update: 2019/03/04 by Jordan Wu'''

from sys import argv
from sys import exit
from os import system

if len(argv) != 8:
    print('Example: python [program] [catalog] [cloud\'s name] [Output Name] [horizontal_pix_num] [vertical_pix_num] [option] [save table]')
    print('Require: [horizontal_pix_num] [vertical_pix_num] must both be integers')
    print(' option: Saturate / Image_Check / IR1_Check/ NAN')
    print(' save table: save transformed RA DEC table [yes/no]')
    exit()

cloud = str(argv[2])
name = str(argv[3])
option = str(argv[6])
save = str(argv[7])
catalog = open(argv[1],'r')
catalog = catalog.readlines()

print('Convert deg to hh:mm:ss ...\n')

new=[]
for line in catalog:
    line = line.split()
    ra_degree = float(line[0])
    dec_degree = float(line[2])
    Qua = [line[100], line[121], line[142], line[163], line[184]]
    imtype = [line[102], line[123], line[144], line[165], line[186]]
    ra = str("%02d" % int(ra_degree/360*24)) + ":" + str("%02d" % int(ra_degree/360*24%1*60)) + ":" + str("%05.2f" % (ra_degree/360*24*60%1*60))
    dec = str("%02d" % int(dec_degree)) + ":" + str("%02d" % int(abs(dec_degree)%1*60)) + ":" + str("%05.2f" % (abs(dec_degree)*60%1*60))

    new_line = str(ra_degree) + " " + str(dec_degree) + "\t" + ra + " " + dec + "\t" + "".join(Qua) + "".join(imtype) + "\n"
    new.append(new_line)
    print(new_line)

out_ca = open(name + '_cans_to_wcs.tbl','w')
for i in new:
    out_ca.write(str(i))
out_ca.close()

print('Conversion Complete ...\n')

#--------------------------------------------------------------------------------------------------------------------------------

coor = open(name + '_cans_to_wcs.tbl', 'r')
coor = coor.readlines()

print('Getfitting ...\n')

if cloud == 'PER':
    MOSAIC_li=["PER_ALL_COMB_IRAC1_mosaic.fits","PER_ALL_COMB_IRAC2_mosaic.fits","PER_ALL_COMB_IRAC3_mosaic.fits","PER_ALL_COMB_IRAC4_mosaic.fits","PER_ALL_A_MIPS1_mosaic.fits"]
else:
    MOSAIC=["_COMB_IRAC1_mosaic.fits","_COMB_IRAC2_mosaic.fits","_COMB_IRAC3_mosaic.fits","_COMB_IRAC4_mosaic.fits","_A_MIPS1_mosaic.fits"]
    MOSAIC_li = []
    for element in MOSAIC:
        MOSAIC_li.append(cloud+element)

#--------------------------------------------------------------------------------------------------------------------------------

band=["IR1","IR2","IR3","IR4","MP1"]

if 'LUP' in cloud:
    path = '/data/public/spitzer/c2d/data.spitzer.caltech.edu/popular/c2d/20071101_enhanced_v1/LUP/MOSAICS/'
else:
    path = '/data/public/spitzer/c2d/data.spitzer.caltech.edu/popular/c2d/20071101_enhanced_v1/'+cloud+'/MOSAICS/'

if option != 'NAN':
    system("rm -r " + name + "_" + option + "_Fits_and_shape")
    system("mkdir " + name + "_" + option + "_Fits_and_shape")
else:
    option = ''
    system("rm -r " + name + "_" + option + "_Fits_and_shape")
    system("mkdir " + name + "_" + option + "_Fits_and_shape")

#--------------------------------------------------------------------------------------------------------------------------------

hor_num = str(argv[4])
ver_num = str(argv[5])

print('number of candidates: %s' % str(len(coor)))
print('----------------------')
for i in range(len(coor)):
    print(str(i+1)+'/'+str(len(coor)))
    Qua = "_"+coor[i].split()[4]
    system("mkdir "+str(i+1)+Qua)

    for j in range(len(MOSAIC_li)):
        Ra = coor[i].split()[2]
        Dec = coor[i].split()[3]
        system("getfits " + path + MOSAIC_li[j] + " " + Ra + ", " + Dec + "," + " " + hor_num + " " +ver_num + " -o "+band[j] + "_" + str(i+1) + ".fits &> /dev/null")
        system("mv " + band[j] + "_" + str(i+1) + ".fits " + str(i+1) + Qua)
    system("mv " + str(i+1) + Qua + " " + name  + "_" +  option + "_Fits_and_shape")

#--------------------------------------------------------------------------------------------------------------------------------

if save == 'no':
    system('rm '+ name + '_cans_to_wcs.tbl')
elif save == 'yes':
    pass

print('----------------------')
print('Procedure is complete ...')
