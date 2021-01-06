#!/usr/bin/env python
'''
-------------------------------------------------------------------
This program is a part of program for Step6 (Image_Check)

Input : catalog_to_Image_Check

Output : catalog_to_Image_Check with (ra/dec) , wcs , imagetype

-------------------------------------------------------------------

latest update : 2018/09/18
'''

from sys import argv, exit

if len(argv) != 4:
    exit('\n\tExample: python [catalog] [cloud\'s name] [option] \
          \n\t[option]: Saturate / Image_Check / IR1_Check\n')

cloud   = str(argv[-2])
option  = str(argv[-1])
catalog = open(argv[-3],'r')
catalog = catalog.readlines()

new=[]
for line in catalog:
    line = line.split()
    ra_degree = float(line[0])
    dec_degree = float(line[2])
    Qua = [line[100], line[121], line[142], line[163], line[184]]
    imtype = [line[102], line[123], line[144], line[165], line[186]]
    ra = str("%02d"%int(ra_degree/360*24))+":"+str("%02d"%int(ra_degree/360*24%1*60))+":"+str("%05.2f"%(ra_degree/360*24*60%1*60))
    dec = str("%02d"%int(dec_degree))+":"+str("%02d"%int(abs(dec_degree)%1*60))+":"+str("%05.2f"%(abs(dec_degree)*60%1*60))

    new_line = str(ra_degree) + " " + str(dec_degree) + "\t" + ra + " " + dec + "\t" + ",".join(Qua) + '_' + ",".join(imtype) + "\n"
    new.append(new_line)
    print(new_line)

if option == 'Saturate':
    catalog_tail = '_saturate.tbl'
if option == 'Image_Check':
    catalog_tail = '_image_check.tbl'
if option == 'IR1_Check':
    catalog_tail = '_IR1_check.tbl'

out_ca = open(cloud + '_cans_to_wcs' + catalog_tail,'w')
for i in new:
    out_ca.write(str(i))
out_ca.close()
