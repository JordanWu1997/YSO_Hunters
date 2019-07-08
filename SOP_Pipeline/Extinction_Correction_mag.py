#!/usr/bin/ipython
'''
-------------------------------------------------------------------
This program is for step2 (extinction_correction) MAGNITUDE VER.

Input : Av_table, c2d HREL catalog with MAGNITUDE

Output : Deredden.tbl

Note : Av_table's header must be removed before starting
-------------------------------------------------------------------
latest update : 2019/04/30 Jordan Wu
'''

from sys import argv
from sys import exit
from math import pi,sin,cos
from numpy import arcsin, log10

if len(argv) != 4:
    print('Help: ')
    print('Example: python Extinctin_Correction.py [Av_table] [catalog] [cloud\'s name]')
    exit()
else:
    pass

#parameters [band, mag_index(w/i UKIDSS), C_av(Extinction_coef), f0_value(mJy)]
parameter=[['J',35,0.2741,1594000.0],
          ['H',56,0.1622,1024000.0],
          ['K',77,0.1119,666700.0],
          ['IR1',98,0.0671,280900.0],
          ['IR2',119,0.0543,179700.0],
          ['IR3',140,0.0444,115000.0],
          ['IR4',161,0.0463,64130.0],
          ['MP1',182,0.0259,7140.0]]#,
          #['MP2',201,0]]

#radius to distinguish source point on Av_table
tolerance = 0.5
print('tolerance = '+str(tolerance)+' rad')

Av_table = open(argv[1], 'r')
catalog = open(argv[2])
cloud = str(argv[3])

#-----------------------------------------------------------
Av_table_lines = Av_table.readlines()
catalog = catalog.readlines()
object_num = len(catalog)

#Name of output catalog
out_Avfar = open(cloud+'_Deredden.tbl','w')
#----------------------------------------latest Update------

num = 1
for objects in catalog:
    print(str(num)+'/'+str(object_num)); num+=1

    Ra_catalog_degree = float(objects.split()[0])
    Dec_catalog_degree = float(objects.split()[2])

    Ra_catalog_rad = Ra_catalog_degree/360*2*pi
    Dec_catalog_rad = Dec_catalog_degree/360*2*pi

    #to store possible point sources' distance from Av_table
    minlist=[]
    #store all possible points' information
    min_info_list=[]

    for line in Av_table_lines:

        if -tolerance < Ra_catalog_degree-float(line.split()[0]) < tolerance and -tolerance < Dec_catalog_degree-float(line.split()[1]) < tolerance:

            Ra_table_rad = float(line.split()[0])/360*2*pi
            Dec_table_rad =float(line.split()[1])/360*2*pi

            #calculate distance(angular) on spherical coordinate
            diffX = cos(Ra_catalog_rad) * cos(Dec_catalog_rad) - cos(Ra_table_rad) * cos(Dec_table_rad)
            diffY = cos(Ra_catalog_rad) * sin(Dec_catalog_rad) - cos(Ra_table_rad) * sin(Dec_table_rad)
            diffZ = sin(Dec_catalog_rad) - sin(Dec_table_rad)

            #Squared distance
            SQdistance = diffX**2 + diffY**2 + diffZ**2

            minlist.append(SQdistance)
            min_info_list.append(line)

    if len(min_info_list) != 0:

        minSQ = min(minlist)
        minnumber = minlist.index(minSQ)

        correct_line = min_info_list[minnumber]
        Av = correct_line.split()[6]

        #Store Av value on catalog
        object_data = objects.split()
        object_data[17] = Av
        far_line = object_data

        for band in parameter:
#====================================================================
            mag = float(far_line[band[1]])
            C_av = float(band[2])
            if mag > 0.0: 
                Av = float(Av)
                new_far_mag = str(mag - C_av*Av) #from def of Av, Cv
            else:
                new_far_mag = str(mag)
            far_line[band[1]] = new_far_mag
#====================================================================
    else:
        print('Not on this extinction map')

    new_far_line = "\t".join(far_line) + "\n"
    out_Avfar.write(new_far_line)
out_Avfar.close()
