#!/usr/bin/ipython

from sys import argv
from SOP_Program_Path import *

cloud = str(argv[1])
cat_prefix  = ['GPP', 'IR1', 'SAT']
dir_suffix = ['_Image_Check_Fits_and_shape/', '_IR1_Check_Fits_and_shape/', '_Saturate_Fits_and_shape/']
cat_list = [cloud + dir_suffix[i] + cat_prefix[i] + '_image_check_list.tbl' for i in range(len(cat_prefix))]


#===============
with open(Hsieh_YSO_Coor_path + 'HL_YSOs_' + cloud + '_coord.dat', 'r') as cat:
    hsieh_coors = cat.readlines()
round_hsieh_coors = []
for coor in hsieh_coors:
    ra, dec = coor.split()
    ra7, dec7 = round(float(ra), 7), round(float(dec), 7)
    round_hsieh_coors.append([ra7, dec7])
#===============

def is_hsieh_YSO(ra, dec, ref_list):
    '''
    ref_list: [[ra1, dec1], [ra2, dec2], ... ]
    '''
    for ref in ref_list:
        ra0, dec0 = ref
        if round(float(ra), 7) == float(ra0) and round(float(dec), 7) == float(dec0):
            hsieh_YSO = 'YES'
        else:
            hsieh_YSO = 'NO'
    return hsieh_YSO

def make_table(ind, ra, dec, evans, hsieh, result, 6DGP, 6DGPTYPE, label, band, comment, mag)
    '''
    mag = (J, IR1, IR2, IR3, IR4, MP1)
    '''
    output = '\t'.join(ind + ra + dec+ evans + hsieh + result.strip('\n') + 6D_GP + 6DGPTYPE + label + band + comment + str(mag))
    return output


for cat in cat_list:
    with open(cat, 'r') as f:
        catalog = f.readlines()
    for rows in catalog:
        row = row.split()
        ra, dec = row[0], row[2]
        evans   = row[16]
        result  = row
