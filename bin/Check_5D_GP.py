#!/usr/bin/python
'''-------------------------------------------------------------------------
This program is between step5,step6 (Gal_Prob_(N/P)) and step6 (Image_Check)

Input: catalog after galaxy probability calculation

Output: (1)YSO_list: YSO_list candidates for sure
        (2)Galaxy_list: Galaxy_list candidates fo sure
        (3)GP_IC_list: GP with problems to image check
----------------------------------------------------------------------------
latest update: 2020/09/29'''

# Modules
# =========================================================================================
from sys import argv, exit
from All_Variables import *
from Hsieh_Functions import *
from Useful_Functions import *

# Functions
# =========================================================================================
def classify_5D_GP_result(catalog):
    '''
    This is to classify input catalog based on calculcated GP
    '''

    YSO_list = []; Galaxy_list = []; GP_IC_list = []
    for line in catalog:
        columns = line.split()

        # GP1 != no_count, GP2 == no_count
        if columns[GP_ID_5D1] != 'no_count' and columns[GP_ID_5D2] == 'no_count':
            GP1 = float(columns[GP_ID_5D1])
            if GP1 <= 1:
                if columns[GPP_ID_5D1] != 'no_count':
                    GPP1 = float(columns[GPP_ID_5D1])
                    if GPP1 > 1:
                        GP_IC_list.append(line)
                    else:
                        YSO_list.append(line)
                else:
                    GP_IC_list.append(line)
            else:
                Galaxy_list.append(line)

        # GP1 == no_count, GP2 != no_count
        elif columns[GP_ID_5D1] == 'no_count' and columns[GP_ID_5D2] != 'no_count':
            GP2 = float(columns[GP_ID_5D2])
            if GP2 <= 1:
                if columns[GPP_ID_5D2] != 'no_count':
                    GPP2 = float(columns[GPP_ID_5D2])
                    if GPP2 > 1:
                        GP_IC_list.append(line)
                    else:
                        YSO_list.append(line)
                else:
                    GP_IC_list.append(line)
            else:
                Galaxy_list.append(line)

        # GP1 != no_count, GP2 != no_count
        elif columns[GP_ID_5D1] != 'no_count' and columns[GP_ID_5D2] != 'no_count':
            GP1, GP2 = float(columns[GP_ID_5D1]), float(columns[GP_ID_5D2])
            if GP1 > 1 and GP2 > 1:
                Galaxy_list.append(line)
            elif GP1 <= 1 and GP2 <= 1:
                if columns[GPP_ID_5D1] != 'no_count' and columns[GPP_ID_5D2] != 'no_count':
                    GPP1, GPP2 = float(columns[GPP_ID_5D1]), float(columns[GPP_ID_5D2])
                    if GPP1 > 1 or GPP2 > 1:
                        GP_IC_list.append(line)
                    else:
                        YSO_list.append(line)
            elif columns[GPP_ID_5D1] != 'no_count' and columns[GPP_ID_5D2] == 'no_count':
                GPP1 = float(columns[GPP_ID_5D1])
                if  GPP1 > 1:
                    GP_IC_list.append(line)
                else:
                    YSO_list.append(line)
            elif columns[GPP_ID_5D1] == 'no_count' and columns[GPP_ID_5D2] != 'no_count':
                GPP2 = float(columns[GPP_ID_5D2])
                if  GPP2 > 1:
                    GP_IC_list.append(line)
                else:
                    YSO_list.append(line)
            elif columns[GPP_ID_5D1] == 'no_count' and columns[GPP_ID_5D2] == 'no_count':
                GP_IC_list.append(line)
        elif GP1 <= 1 and GP2 > 1:
            if columns[GPP_ID_5D1] != 'no_count':
                GPP1 = float(columns[GPP_ID_5D1])
                if GPP1 > 1:
                    GP_IC_list.append(line)
                else:
                    YSO_list.append(line)
            else:
                GP_IC_list.append(line)
        elif GP1 > 1 and GP2 <= 1:
            if columns[GPP_ID_5D2] != 'no_count':
                GPP2 = float(columns[GPP_ID_5D2])
                if GPP2 > 1:
                    GP_IC_list.append(line)
                else:
                        YSO_list.append(line)
            else:
                GP_IC_list.append(line)

        #GP1 == no_count, GP2 == no_count
        else:
            Galaxy_list.append(line)

        return YSO_list, Galaxy_list, GP_IC_list

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

    # Check inputs
    if len(argv) != 3:
        exit("Example: [program] [input catalog] [MC cloud]")
    inp_cat = str(argv[1])
    mccloud = str(argv[2])

    # Load catalog
    with open(inp_cat, 'r') as inp:
        catalog = inp.readlines()

    # Run classification
    YSO_list, Galaxy_list, GP_IC_list = classify_5D_GP_result(catalog)

    # Store results
    write_catalog(YSO_list, '{}_YSO.tbl'.format(cloud))
    write_catalog(Galaxy_list, '{}_Galaxy.tbl'.format(cloud))
    write_catalog(GP_IC_list, '{}_GP_to_image_check.tbl'.format(cloud))
