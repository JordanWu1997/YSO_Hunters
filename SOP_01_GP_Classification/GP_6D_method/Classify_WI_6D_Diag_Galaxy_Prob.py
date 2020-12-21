#!/usr/bin/python
'''
-------------------------------------------------------------------------
This program is to check 6d galaxy probability and sort the candidates

Input: catalog after galaxy probability (P)  calculation

Output: (1)YSO: YSO candidates for sure
        (2)Galaxy: Galaxy candidates fo sure
        (3)GP_IC: GP with problems to image check

Major_Update at 2020: Make it more general and simpler
-------------------------------------------------------------------------
latest update: 20200524 Jordan Wu'''

# Import Modules
#=========================================================================
from __future__ import print_function
from sys import argv, exit
import time
from os import system
from Useful_Functions import *
from All_Variables import *

# Global Variables
#=========================================================================
RA_ID              = coor_ID[0]
DEC_ID             = coor_ID[1]
MP1_Qua_ID         = qua_ID_Spitzer[4]
GP_OBJ_ID, GP_ID   = GP_OBJ_ID_6D_Diag, GP_ID_6D_Diag
GPP_OBJ_ID, GPP_ID = GPP_OBJ_ID_6D_Diag, GPP_ID_6D_Diag

# Functions
#=========================================================================
def classify_by_GP(row_list):
    '''
    This is to classify input object by GP and GPP and return object label
    Count:
    Count:
        "not_count" : LESS3BD
        "not_count" : AGB
        1e-5        : MP1_Sat
        1e-4        : Bright
        1e-3        : YSO
        1e4         : Faint
        1e3         : Galaxy
    '''
    GP = row_list[GP_ID]
    if GP != 'no_count':
        GP = float(row_list[GP_ID])
        if GP < 1.:
            GPP = row_list[GPP_ID]
            if GPP != 'no_count':
                GPP = float(row_list[GPP_ID])
                if GPP >= 1.:
                    label = 'GP_IC'
                else:
                    label = 'YSO'
            else:
                label = 'YSO'
        else:
            label = 'GALAXY'
    else:
        label = 'OTHER'
    return label

# Main Programs
#=========================================================================
if __name__ == '__main__':
    s_start = time.time()

    # Check inputs
    if len(argv) != 3:
        exit('\n\tWrong Usage!\
              \n\tExample: [program] [catalog] [MC cloud_name]\n')

    # Input Variables
    catalog_name = str(argv[1])
    cloud_name   = str(argv[2])

    # Load catalogs
    with open(catalog_name, 'r') as cat:
        catalog = cat.readlines()

    print('\nStart classifying ...')
    # Classify input objects
    YSOc, Galaxyc, GP_IC, Others = [], [], [], []
    for i in range(len(catalog)):
        row_list = catalog[i].split()
        label = classify_by_GP(row_list)
        if label == 'YSO':
            YSOc.append(catalog[i])
        elif label == 'GALAXY':
            Galaxyc.append(catalog[i])
        elif label == 'GP_IC':
            GP_IC.append(catalog[i])
        else:
            Others.append(catalog[i])
        drawProgressBar(float(i+1)/len(catalog))

    # Write different object catalogs
    # Note "NO NEED \n when write since there already is one from loading catalog"
    with open('{}_6D_YSO.tbl'.format(cloud_name), "w") as out_cat:
        for line in YSOc:
            out_cat.write('{}'.format(line))
    with open('{}_6D_Galaxy.tbl'.format(cloud_name), "w") as out_cat:
        for line in Galaxyc:
            out_cat.write('{}'.format(line))
    with open('{}_6D_GP_to_image_check.tbl'.format(cloud_name), "w") as out_cat:
        for line in GP_IC:
            out_cat.write('{}'.format(line))
    with open('{}_6D_GP_others.tbl'.format(cloud_name), "w") as out_cat:
        for line in Others:
            out_cat.write('{}'.format(line))

    # Print out catalog line numbers
    system('echo "\nThe Saturate Candiates in YSO candidates:" && awk \'${:d}==\"S\" {{ print ${:d}, ${:d} }}\' {}_6D_YSO.tbl'.format(\
                                                 MP1_Qua_ID+1, RA_ID+1, DEC_ID+1, cloud_name))
    system('echo "The YSO Candiates:" && wc -l {}_6D_YSO.tbl'.format(cloud_name))
    system('echo "The Galaxy Candidates:" && wc -l {}_6D_Galaxy.tbl'.format(cloud_name))
    system('echo "The Image Check Candidates:" && wc -l {}_6D_GP_to_image_check.tbl'.format(cloud_name))
    system('echo "The Others:" && wc -l {}_6D_GP_others.tbl'.format(cloud_name))
    s_end   = time.time()
    print('Whole {} process took {:.3f} secs'.format(argv[0], s_end - s_start))
