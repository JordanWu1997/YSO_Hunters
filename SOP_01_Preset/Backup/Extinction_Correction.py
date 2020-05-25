#!/usr/bin/python
'''
-------------------------------------------------------------------
This program is for step2 (extinction_correction)

Input : Av_table, c2d HREL catalog

Output : Deredden.tbl

Note : Av_table's header must be removed before starting
-------------------------------------------------------------------
latest update : 2019/5/01 Jordan Wu'''

from sys import argv
from sys import exit
from math import pi,sin,cos
from numpy import arcsin

if len(argv) != 5:
    exit('\n\tError: Wrong Arguments\
    \n\tExample: [Program] [Av_table] [catalog] [cloud\'s Name] [Table Format]\
    \n\t[Table Format] old/new : Hsieh\'s style/new style\n')

# parameters [band, flux index, mag index, C_av(Exctintion_coef)]
parameter = [['J',  0.2741],
            [ 'H',  0.1622],
            [ 'K',  0.1119],
            ['IR1', 0.0671],
            ['IR2', 0.0543],
            ['IR3', 0.0444],
            ['IR4', 0.0463],
            ['MP1', 0.0259],
            ['MP2', 0]]

Av_coor_ID = [0, 1]  # RA, Dec on extinction table
Av_ID      = [17]
coor_ID    = [0, 2]  # RA, Dec on input table
mag_ID     = [33, 54, 75, 96, 117, 138, 159, 180, 201]
flux_ID    = [35, 56, 77, 98, 119, 140, 161, 182, 203]

# Set up input table and catalogs
Av_table = open(str(argv[1]), 'r')
catalogs = open(str(argv[2]), 'r')
cloud    = str(argv[3])

# Set up input table format
tbl_format, Av_col = str(argv[4]), 0
if tbl_format != 'Old':
    Av_col = 2
else:
    Av_col = 6

# Read Files
Av_table_lines = Av_table.readlines()
catalog = catalogs.readlines()
Av_table.close()
catalogs.close()
object_num = len(catalog)

# Name of output catalog
out_Avfar = open(cloud+'_Deredden.tbl','w')

# Radius to distinguish source point on Av_table (in radian)
tolerance = 0.5
print('tolerance = '+str(tolerance)+' rad')

num = 1
not_found = []
for objects in catalog:
    print(str(num)+'/'+str(object_num)); num+=1

    Ra_catalog_degree = float(objects.split()[coor_ID[0]])
    Dec_catalog_degree = float(objects.split()[coor_ID[1]])

    Ra_catalog_rad = Ra_catalog_degree/360*2*pi
    Dec_catalog_rad = Dec_catalog_degree/360*2*pi

    # Store distance of possible point sources from Av_table
    minlist=[]
    # Store information of all possible points
    min_info_list=[]

    for line in Av_table_lines:

        if -tolerance < Ra_catalog_degree-float(line.split()[Av_coor_ID[0]]) < tolerance and -tolerance < Dec_catalog_degree-float(line.split()[Av_coor_ID[1]]) < tolerance:

            Ra_table_rad = float(line.split()[0])/360*2*pi
	    Dec_table_rad =float(line.split()[1])/360*2*pi

            # Calculate distance(angular) on spherical coordinate
            diffX = cos(Ra_catalog_rad) * cos(Dec_catalog_rad) - cos(Ra_table_rad) * cos(Dec_table_rad)
	    diffY = cos(Ra_catalog_rad) * sin(Dec_catalog_rad) - cos(Ra_table_rad) * sin(Dec_table_rad)
	    diffZ = sin(Dec_catalog_rad) - sin(Dec_table_rad)

            # Calculate Squared distance
            SQdistance = diffX**2 + diffY**2 + diffZ**2
            minlist.append(SQdistance)
	    min_info_list.append(line)

    object_data = objects.split()
    far_line = object_data

    if len(min_info_list) != 0:

        minSQ = min(minlist)
        minnumber = minlist.index(minSQ)
        correct_line = min_info_list[minnumber]
        Av = correct_line.split()[Av_col]

        # Store Av value on catalog
        far_line[Av_ID[0]] = Av

        for i, band in enumerate(parameter):

            flux = float(far_line[flux_ID[i]])
            mag  = float(far_line[mag_ID[i]])
            C_av = float(band[1])

            #=============================
            # Flux Correction
            #=============================
            if flux < 0.0:
                new_far_flux = str(flux)
            else:
                Av = float(Av)
                new_far_flux = str(flux*10**(Av*C_av/2.5))
            far_line[flux_ID[i]] = new_far_flux

            #=============================
            # Magnitude Correction
            #=============================
            if mag > 0.0:
                Av = float(Av)
                new_far_mag = str(mag - C_av*Av) #from def of Av, Cv
            else:
                new_far_mag = str(mag)
            far_line[mag_ID[i]] = new_far_mag

        new_far_line = "\t".join(far_line) + "\n"

    else:
        for j, band in enumerate(parameter):
            far_line[mag_ID[j]] = 'NOT_FOUND'
        not_found.append("\t".join(far_line))
        print('RA:{}, DEC:{} Not on this extinction map'.format(object_data[coor_ID[0]], object_data[coor_ID[1]]))

    out_Avfar.write(new_far_line)
out_Avfar.close()
if len(not_found) != 0:
    with open(cloud+'_AvNotFound.tbl','w') as out_NotFound:
        out_NotFound.write("\n".join(not_found) + "\n")
