#!/usr/bin/python
'''
----------------------------------------------------------
Example: [program] [cloud\'s name]

Input Variables:
    [cloud\'s name]: name of molecular cloud e.g. CHA_II
----------------------------------------------------------
latest update: 2019/07/28 Jordan Wu'''

# Import Modules
#======================================================
from __future__ import print_function
from glob import glob
from sys import argv, exit
import numpy as np
import warnings

# Functions
#======================================================
def get_list_number(list_name):
    '''
    This is to get total number of line in input list
    '''
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        inplist = np.loadtxt(list_name, dtype=str)
    if len(inplist.shape) == 1:
        if inplist.shape[0] == 0:
            number = 0
        else:
            number = 1
    else:
        number = len(inplist)
    return number

# Main Program
#======================================================
if __name__ == '__main__':

    # Check input
    if len(argv) != 2:
        exit('\n\tError: Wrong Usage!\
              \n\tExample: [program] [cloud\'s name]\
              \n\t[cloud\'s name]: name of molecular cloud e.g. CHA_II\n')

    # Input paramters
    cloud     = str(argv[1])
    YSO       = get_list_number(glob('*_YSO.tbl')[0])
    GALA      = get_list_number(glob('*_Galaxy.tbl')[0])
    GPIC      = get_list_number(glob('*_GP_to_image_check.tbl')[0])
    OTHER     = get_list_number(glob('*_2_5D_GP_others.tbl')[0])
    GPIC_YSO  = get_list_number(glob('AND_*_GP_IC_all_Hsieh_YSOc.tbl')[0])
    OTHER_YSO = get_list_number(glob('AND_*_2_5D_OTHERS_all_Hsieh_YSOc.tbl')[0])
    GALA_YSO  = get_list_number(glob('AND_*_Galaxy_all_Hsieh_YSOc.tbl')[0])
    YSO_YSO   = get_list_number(glob('AND_*_YSO_all_Hsieh_YSOc.tbl')[0])
    Hsieh_YSO = YSO_YSO + GALA_YSO + GPIC_YSO + OTHER_YSO

    # Table head
    print(' ')
    print('| {:10} | {:10} | {:10} | {:10} | {:10} |'.format('-'*10, '-'*10, '-'*10, '-'*10, '-'*10))

    # Confusion Matrix
    print('| {:10} | {:10} | {:10} | {:10} | {:10} |'.format(cloud, 'YSO', 'Galaxy', 'IC', 'Other'))
    print('| {:10} | {:10} | {:10} | {:10} | {:10} |'.format('-'*10, '-'*10, '-'*10, '-'*10, '-'*10))
    print('| {:10} | {:10} | {:10} | {:10} | {:10} |'.format('H&L YSO', str(YSO_YSO), \
                                                              str(GALA_YSO), str(GPIC_YSO), str(OTHER_YSO)))
    print('| {:10} | {:10} | {:10} | {:10} | {:10} |'.format('H&L NYSO', str(YSO-YSO_YSO), str(GALA-GALA_YSO),\
                                                              str(GPIC-GPIC_YSO), str(OTHER-OTHER_YSO)))
    print('| {:10} | {:10} | {:10} | {:10} | {:10} |'.format('-'*10, '-'*10, '-'*10, '-'*10, '-'*10))

    # Precision and Recall of YSO (WI/WO IC^HSIEH YSO)
    print('  {:23}: {:9}%'.format('Precis WO IC^HSIEH YSO', '{:.3f}'.format(float(YSO_YSO)/YSO*100.)))
    print('  {:23}: {:9}%'.format('Recall WO IC^HSIEH YSO', '{:.3f}'.format(float(YSO_YSO)/Hsieh_YSO*100.)))
    print('  {:23}: {:9}%'.format('Precis WI IC^HSIEH YSO', '{:.3f}'.format(float(YSO_YSO+GPIC_YSO)/(YSO+GPIC_YSO)*100.)))
    print('  {:23}: {:9}%'.format('Recall WI IC^HSIEH YSO', '{:.3f}'.format(float(YSO_YSO+GPIC_YSO)/Hsieh_YSO*100.)))
    print(' ')
