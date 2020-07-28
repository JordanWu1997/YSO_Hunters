#!/usr/bin/python

from __future__ import print_function
from glob import glob
from sys import argv, exit
import numpy as np
import warnings

def get_list_number(list_name):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        inplist = np.loadtxt(list_name, dtype=str)
    number = len(inplist)
    return number

if __name__ == '__main__':

    if len(argv) != 2:
        exit('\n\tError: Wrong Usage!\
              \n\tExample: [program] [cloud\'s name]\
              \n\t[cloud\'s name]: name of molecular cloud e.g. CHA_II\n')

    cloud = str(argv[1])

    YSO   = get_list_number(glob('*_6D_YSO.tbl')[0])
    GALA  = get_list_number(glob('*_6D_Galaxy.tbl')[0])
    GPIC  = get_list_number(glob('*_6D_GP_to_image_check.tbl')[0])
    OTHER = get_list_number(glob('*_6D_GP_others.tbl')[0])

    GPIC_YSO  = get_list_number(glob('AND_*_6D_GP_IC_all_Hsieh_YSOc.tbl')[0])
    OTHER_YSO = get_list_number(glob('AND_*_6D_OTHERS_all_Hsieh_YSOc.tbl')[0])
    GALA_YSO  = get_list_number(glob('AND_*_Galaxy_all_Hsieh_YSOc.tbl')[0])
    YSO_YSO   = get_list_number(glob('AND_*_YSO_all_Hsieh_YSOc.tbl')[0])

    print(' ')
    print('| {:10} | {:10} | {:10} | {:10} | {:10} |'.format('-'*10, '-'*10, '-'*10, '-'*10, '-'*10))
    print('| {:10} | {:10} | {:10} | {:10} | {:10} |'.format(cloud, 'YSO', 'Galaxy', 'IC', 'Other'))
    print('| {:10} | {:10} | {:10} | {:10} | {:10} |'.format('-'*10, '-'*10, '-'*10, '-'*10, '-'*10))
    print('| {:10} | {:10} | {:10} | {:10} | {:10} |'.format('H&L YSO', str(YSO_YSO), \
                                                              str(GALA_YSO), str(GPIC_YSO), str(OTHER_YSO)))
    print('| {:10} | {:10} | {:10} | {:10} | {:10} |'.format('H&L NYSO', str(YSO-YSO_YSO), str(GALA-GALA_YSO),\
                                                              str(GPIC-GPIC_YSO), str(OTHER-OTHER_YSO)))
    print('| {:10} | {:10} | {:10} | {:10} | {:10} |'.format('-'*10, '-'*10, '-'*10, '-'*10, '-'*10))
    print(' ')
