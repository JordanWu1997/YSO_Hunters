#!/usr/bin/env python
'''-------------------------------------------------------------------------
This program is between step5,step6 (Gal_Prob_(N/P)) and step6 (Image_Check)

Input: catalog after galaxy probability calculation

Output: (1)YSO_list: YSO_list candidates for sure
        (2)Galaxy_list: Galaxy_list candidates fo sure
        (3)GP_IC_list: GP with problems to image check
----------------------------------------------------------------------------
latest update: 2020/10/11'''

# Modules
# =========================================================================================
from sys import argv, exit
import time
from os import system
from All_Variables import *
from Hsieh_Functions import *
from Useful_Functions import *

# Global Variables
#=========================================================================
MP1_Qua_ID = qua_ID_Spitzer[4]
RA_ID      = coor_ID[0]
DEC_ID     = coor_ID[1]

# Functions
# =========================================================================================
def classify_2GPs_result(catalog, GP1_ID=GP_ID_5D1, GPP1_ID=GPP_ID_5D1, GP2_ID=GP_ID_5D2, GPP2_ID=GPP_ID_5D2):
    '''
    This is to classify input catalog based on calculcated GP
    '''

    YSO_list = []; Galaxy_list = []; GP_IC_list = []; Other_list = []
    for line in catalog:
        columns = line.split()

        # GP1 != no_count, GP2 == no_count
        if columns[GP1_ID] != 'no_count' and columns[GP2_ID] == 'no_count':
            GP1 = float(columns[GP1_ID])
            if GP1 <= 1.:
                if columns[GPP1_ID] != 'no_count':
                    GPP1 = float(columns[GPP1_ID])
                    if GPP1 > 1.:
                        GP_IC_list.append(line)
                    else:
                        YSO_list.append(line)
                else:
                    GP_IC_list.append(line)
            else:
                Galaxy_list.append(line)

        # GP1 == no_count, GP2 != no_count
        elif columns[GP1_ID] == 'no_count' and columns[GP2_ID] != 'no_count':
            GP2 = float(columns[GP2_ID])
            if GP2 <= 1.:
                if columns[GPP2_ID] != 'no_count':
                    GPP2 = float(columns[GPP2_ID])
                    if GPP2 > 1.:
                        GP_IC_list.append(line)
                    else:
                        YSO_list.append(line)
                else:
                    GP_IC_list.append(line)
            else:
                Galaxy_list.append(line)

        # GP1 != no_count, GP2 != no_count
        elif columns[GP1_ID] != 'no_count' and columns[GP2_ID] != 'no_count':
            GP1, GP2 = float(columns[GP1_ID]), float(columns[GP2_ID])
            if GP1 > 1. and GP2 > 1.:
                Galaxy_list.append(line)
            elif GP1 <= 1. and GP2 <= 1.:
                if columns[GPP1_ID] != 'no_count' and columns[GPP2_ID] != 'no_count':
                    GPP1, GPP2 = float(columns[GPP1_ID]), float(columns[GPP2_ID])
                    if GPP1 > 1. or GPP2 > 1.:
                        GP_IC_list.append(line)
                    else:
                        YSO_list.append(line)
                elif columns[GPP1_ID] != 'no_count' and columns[GPP2_ID] == 'no_count':
                    GPP1 = float(columns[GPP1_ID])
                    if GPP1 > 1.:
                        GP_IC_list.append(line)
                    else:
                        YSO_list.append(line)
                elif columns[GPP1_ID] == 'no_count' and columns[GPP2_ID] != 'no_count':
                    GPP2 = float(columns[GPP2_ID])
                    if GPP2 > 1.:
                        GP_IC_list.append(line)
                    else:
                        YSO_list.append(line)
                elif columns[GPP1_ID] == 'no_count' and columns[GPP2_ID] == 'no_count':
                    GP_IC_list.append(line)
            elif GP1 <= 1. and GP2 > 1.:
                if columns[GPP1_ID] != 'no_count':
                    GPP1 = float(columns[GPP1_ID])
                    if GPP1 > 1.:
                        GP_IC_list.append(line)
                    else:
                        YSO_list.append(line)
                else:
                    GP_IC_list.append(line)
            elif GP1 > 1. and GP2 <= 1.:
                if columns[GPP2_ID] != 'no_count':
                    GPP2 = float(columns[GPP2_ID])
                    if GPP2 > 1.:
                        GP_IC_list.append(line)
                    else:
                        YSO_list.append(line)
                else:
                    GP_IC_list.append(line)

        # GP1 == no_count, GP2 == no_count
        else:
            Other_list.append(line)

    return YSO_list, Galaxy_list, GP_IC_list, Other_list

def write_catalog(List, output):
    '''
    This is to write catalog based on input list
    '''
    # Store results
    with open(output, 'w') as out:
        for ele in List:
            out.write(str(ele))

# Main Programs
# =========================================================================================
if __name__ == '__main__':
    ck_start = time.time()

    # Check inputs
    if len(argv) != 4:
        exit("\n\tExample: [program] [input catalog] [MC cloud] [output name]\
              \n\t[input catalog]: must include 2 different GP(GPP)\
              \n\t[MC cloud]: name of cloud of input catalog\
              \n\t[output name]: output suffix (or 'default')\n")

    inp_cat    = str(argv[1])
    cloud_name = str(argv[2])
    out_name   = str(argv[3])

    # Load catalog
    with open(inp_cat, 'r') as inp:
        catalog = inp.readlines()

    # Run classification
    YSO_list, Galaxy_list, GP_IC_list, Other_list = classify_2GPs_result(catalog)
    print(len(YSO_list), len(Galaxy_list), len(GP_IC_list))

    # Store results
    if out_name == 'default':
        write_catalog(YSO_list, '{}_2_5D_YSO.tbl'.format(cloud_name))
        write_catalog(Galaxy_list, '{}_2_5D_Galaxy.tbl'.format(cloud_name))
        write_catalog(GP_IC_list, '{}_2_5D_GP_to_image_check.tbl'.format(cloud_name))
        write_catalog(Other_list, '{}_2_5D_GP_others.tbl'.format(cloud_name))
    else:
        write_catalog(YSO_list, '{}_2_5D_YSO.tbl'.format(out_name))
        write_catalog(Galaxy_list, '{}_2_5D_Galaxy.tbl'.format(out_name))
        write_catalog(GP_IC_list, '{}_2_5D_GP_to_image_check.tbl'.format(out_name))
        write_catalog(Other_list, '{}_2_5D_GP_others.tbl'.format(out_name))

    # Print out catalog line numbers
    system('echo "\nThe Saturate Candiates in YSO candidates:" && awk \'${:d}==\"S\" {{ print ${:d}, ${:d} }}\' {}_2_5D_YSO.tbl'.format(\
                                                                                        MP1_Qua_ID+1, RA_ID+1, DEC_ID+1, cloud_name))
    system('echo "The YSO Candiates:" && wc -l {}_2_5D_YSO.tbl'.format(cloud_name))
    system('echo "The Galaxy Candidates:" && wc -l {}_2_5D_Galaxy.tbl'.format(cloud_name))
    system('echo "The Image Check Candidates:" && wc -l {}_2_5D_GP_to_image_check.tbl'.format(cloud_name))
    system('echo "The Others:" && wc -l {}_2_5D_GP_others.tbl'.format(cloud_name))
    ck_end   = time.time()
    print('Whole {} process took {:.3f} secs'.format(argv[0], ck_end - ck_start))
