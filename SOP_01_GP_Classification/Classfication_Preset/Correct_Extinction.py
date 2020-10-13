#!/usr/bin/python
'''
-------------------------------------------------------------------
This program is for step2 (extinction_correction)

Input : Av_table, c2d HREL catalog

Output : Deredden.tbl

Note : Av_table's header must be removed before starting

Usage Example: [Program] [Av_table] [catalog] [cloud Name]
Input variables:
        [Av Table]:  table contains specific cloud region Av values
        [Av table type]: "Self_made" or "Hsieh"
        [catalog]:   input catalog to do extinction correction
        [cloud name] brief name of cloud e.g. CHA_II
-------------------------------------------------------------------
Latest update : 2020/05/25 Jordan Wu'''

# Import Modules
#=============================================
from __future__ import print_function
from sys import argv, exit
from math import pi,sin,cos
from All_Variables import *
from Hsieh_Functions import *
from Useful_Functions import *
import numpy as np
import time

# Global Variables
#=============================================
parameter  = C_av_list         # parameters [band, flux index, mag index, C_av(Exctintion_coef)]
Av_coor_ID = Av_coor_ID        # RA, Dec on extinction table
Av_ID      = Av_ID[0]
coor_ID    = coor_ID           # RA, Dec on input table
mag_ID     = full_mag_ID       # [33, 54, 75, 96, 117, 138, 159, 180, 201]
flux_ID    = full_flux_ID      # [35, 56, 77, 98, 119, 140, 161, 182, 203]
tolerance  = 0.5               # Radius to distinguish source point on Av_table (in radian)

# Functions
#=============================================
def deg_to_rad(degree):
    radian = degree / 180 * pi
    return radian

def calculate_min_angular_dist(Ra_catalog_degree, Dec_catalog_degree, Av_table_lines, tolerance):
    '''
    This is to calculate angular distance from input to point on Av table
    minlist: Store distance of possible point sources from Av table
    min_info_list: Store information of all possible points
    '''
    # Transform from degree to rad for numpy trigonometric functions
    Ra_catalog_rad  = deg_to_rad(Ra_catalog_degree)
    Dec_catalog_rad = deg_to_rad(Dec_catalog_degree)
    # Loop through all Av table
    minlist, min_info_list = [], []
    for line in Av_table_lines:
        line = line.split()
        # Check if input object in Av table
        if ((Ra_catalog_degree  - float(line[Av_coor_ID[0]])) > -tolerance) and\
           ((Ra_catalog_degree  - float(line[Av_coor_ID[0]])) <  tolerance) and\
           ((Dec_catalog_degree - float(line[Av_coor_ID[1]])) > -tolerance) and\
           ((Dec_catalog_degree - float(line[Av_coor_ID[1]])) <  tolerance):
            # Calculate distance(angular) on spherical coordinate
            Ra_table_rad, Dec_table_rad  = deg_to_rad(float(line[0])), deg_to_rad(float(line[1]))
            diffX = cos(Ra_catalog_rad) * cos(Dec_catalog_rad) - cos(Ra_table_rad) * cos(Dec_table_rad)
            diffY = cos(Ra_catalog_rad) * sin(Dec_catalog_rad) - cos(Ra_table_rad) * sin(Dec_table_rad)
            diffZ = sin(Dec_catalog_rad) - sin(Dec_table_rad)
            # Calculate Squared distance
            SQdistance = diffX ** 2 + diffY ** 2 + diffZ ** 2
            minlist.append(SQdistance)
            min_info_list.append(line)
    return minlist, min_info_list

def store_Av_info_to_list(far_line, minlist, min_info_list, not_found_list, flux_ID=flux_ID, mag_ID=mag_ID):
    '''
    This is to store Av value and correct mag/flux to input line
    not_found_list: list to store lines that not found in Av table
    '''
    if len(min_info_list) != 0:
        # Find Av value
        minSQ        = min(minlist)
        minnumber    = minlist.index(minSQ)
        correct_line = min_info_list[minnumber]
        Av = correct_line[Av_tbl_col_ID]
        # Store Av value on catalog
        far_line[Av_ID] = Av
        for i, band in enumerate(parameter):
            flux = float(far_line[flux_ID[i]])
            mag  = float(far_line[mag_ID[i]])
            C_av = float(band[1])
            # Start Flux Correction
            if flux > 0.0:
                Av = float(Av)
                new_far_flux = str(flux * 10 ** (Av * C_av/2.5))
            else:
                new_far_flux = str(0.0) #str(flux)
            far_line[flux_ID[i]] = new_far_flux
            # Start Magnitude Correction
            if mag > 0.0:
                Av = float(Av)
                new_far_mag = str(mag - C_av * Av) #from def of Av, Cv
            else:
                new_far_mag = str(0.0) #str(mag)
            far_line[mag_ID[i]] = new_far_mag
        new_far_line = "\t".join(far_line)
    else:
        # If Av value not found
        for j, band in enumerate(parameter):
            far_line[mag_ID[j]] = 'NOT_FOUND'
        new_far_line = 'NOT_FOUND'
        not_found_list.append("\t".join(far_line))
    return new_far_line, not_found_list

# Main Programs
#=============================================
if __name__ == '__main__':
    t_start = time.time()

    # Check inputs
    if len(argv) != 5:
        exit('\n\tError: Wrong Arguments\
            \n\tExample: [Program] [Av_table] [Av_table_type] [catalog] [cloud\'s Name]\
            \n\t[Av table]: table contains specific cloud region Av values\
            \n\t[Av table type]: "Self_made" or "Hsieh"\
            \n\t[catalog]: input catalog to do extinction correction\
            \n\t[cloud\'s name] brief name of cloud e.g. CHA_II\n')

    # Input variables
    Av_tbl_name   = str(argv[1])      # Name of input extinction table
    Av_tbl_type   = str(argv[2])      # Type of extinction table selfmade or Hsieh's
    catalog_name  = str(argv[3])      # Name of input catalog
    cloud_name    = str(argv[4])      # Cloud name

    if Av_tbl_type == 'Hsieh':
        Av_tbl_col_ID = Av_tbl_col_ID[1]
    else:
        # Here 0 for new made Av table (Default)
        Av_tbl_col_ID = Av_tbl_col_ID[0]

    # Print out info from inputs
    print('\nCatalog: {}\
           \nAv table: {}\
           \nAv table type: {}\
           \nAv_ID on Catalog (write): {:d}\
           \nAv_ID on Av table (read): {:d}\
           \nCloud name: {}\
           \nRadius of tolerance (rad): {:.1f}\n'.format(\
           catalog_name, Av_tbl_name, Av_tbl_type, Av_ID, Av_tbl_col_ID, cloud_name, tolerance))

    # Load Av table and read files
    with open(Av_tbl_name, 'r') as Av_table:
        Av_table_lines = Av_table.readlines()
    with open(catalog_name, 'r') as catalogs:
        catalog = catalogs.readlines()

    # Main Calculation
    print('Start Correcting Extinction ...')
    not_found_list, new_far_line_list = [], []
    for i, objects in enumerate(catalog):
        objects = objects.split()
        Ra_catalog_degree  = float(objects[coor_ID[0]])
        Dec_catalog_degree = float(objects[coor_ID[1]])
        minlist, min_info_list = calculate_min_angular_dist(Ra_catalog_degree, Dec_catalog_degree, Av_table_lines, tolerance)
        far_line, not_found_list = store_Av_info_to_list(objects, minlist, min_info_list, not_found_list)
        if far_line != 'NOT_FOUND':
            new_far_line_list.append(far_line)
        drawProgressBar(float(i+1)/len(catalog))

    # Print out not found list
    print('\nNOT FOUND INPUTS:')
    for not_found in not_found_list:
        not_found = not_found.split()
        print('RA:{}, DEC:{} Not on this extinction map'.format(not_found[coor_ID[0]], not_found[coor_ID[1]]))

    # Write results
    print('\nSave Extinction Correction result ...')
    with open(cloud_name + '_Deredden.tbl','w') as out_Avfar:
        out_Avfar.write("\n".join(new_far_line_list) + "\n")
    if len(not_found_list) != 0:
        with open(cloud_name + '_AvNotFound.tbl','w') as out_NotFound:
            out_NotFound.write("\n".join(not_found_list) + "\n")
    t_end   = time.time()
    print('\nWhole {} process took {:.3f} secs'.format(argv[0], t_end-t_start))
