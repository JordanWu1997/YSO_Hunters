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

from __future__ import print_function
from sys import argv, exit
from time import time
import os

# Check Inputs
#=========================================================================
if len(argv) != 3:
    exit('\n\tWrong Usage!\
          \n\tExample: [program] [catalog] [MC cloud_name]\n')

# Input Variables
#=========================================================================
cloud_name  = str(argv[2])
RA_ID       = 0
DEC_ID      = 2
MP1_Qua_ID  = 184
GP_OBJ_ID, GP_ID = 241, 242
GPP_OBJ_ID, GPP_ID = 243, 244

# Functions
#=========================================================================
def classify_by_GP(row_list):
    '''
    This is to classify input object by GP and GPP and return object label
    '''
    if row_list[GP_ID] != 'no_count':
        GP = float(row_list[GP_ID])
        if GP <= 1:
            if row_list[GPP_ID] != 'no_count':
                GPP = float(row_list[GPP_ID])
                if GPP > 1:
                    label = 'GP_IC'
                elif GPP <= 1:
                    label = 'YSO'
            else:
                label = 'GP_IC'
        elif GP > 1:
            if row_list[GPP_ID] != 'no_count':
                GPP = float(row_list[GPP_ID])
                if GP <= 1:
                    label = 'GP_IC'
                elif GP > 1:
                    label = 'Galaxy'
            else:
                label = 'Galaxy'
    else:
        label = 'Galaxy'
    return label

# Main Programs
#=========================================================================
if __name__ == '__main__':
    s_start = time.time()

    # Load catalogs
    with open(argv[1], 'r') as cat:
        catalog = cat.readlines()

    # Classify input objects
    YSO, Galaxy, GP_IC = [], [], []
    for i in range(len(catalog)):
        row_list = catalog[i].split()
        label = classify_by_GP(row_list)
        if label == 'YSO':
            YSO.append(row_list)
        elif label == 'Galaxy':
            Galaxy.append(row_list)
        elif label == 'GP_IC':
            GP_IC.append(row_list)

    # Write different object catalogs
    with open(cloud_name + '_6D_YSO.tbl',"w") as out_cat:
        for i in YSO:
            out_cat.write(str(i))
    with open(cloud_name + '_6D_Galaxy.tbl',"w") as out_cat:
        for i in Galaxy:
            out_cat.write(str(i))
    with open(cloud_name + '_6D_GP_to_image_check.tbl',"w") as out_cat:
        for i in GP_IC:
            out_cat.write(str(i))

    # Print out catalog line numbers
    print('The Saturate Candiates in YSO candidates: ')
    os.system('echo | awk \'${:d} == \"S\" {print ${:d}, ${:d}} \' {}_6D_YSO.tbl'.format(MP1_Qua_ID+1, RA_ID+1, DEC_ID+1, cloud_name))
    print('The confident YSO candidates: ')
    os.system('wc ' + cloud_name + '_6D_YSO.tbl')
    print('The confident Galaxy candidates: ')
    os.system('wc ' + cloud_name + '_6D_Galaxy.tbl')
    print('The candidate to image check: ')
    os.system('wc ' + cloud_name + '_6D_GP_to_image_check.tbl')
    s_end   = time.time()
    print('Whole {} took {:.3f} secs'.format(argv[0], s_end - s_start))
