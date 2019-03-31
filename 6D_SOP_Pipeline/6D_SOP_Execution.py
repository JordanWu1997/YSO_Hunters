#!/usr/bin/ipython
'''------------------------------------------------------------------------------------
This program is for 6-d galaxy probability (P)

Input : catalog with 
        (1)5-d galaxy probablity
        (2)galaxy probability P

Output: catalog with 
        (1)6-d galaxy probability
        (2)6-d galaxy probability

*Output Directory YSO_6D contains:
        YSO/IC (ImageCheck)
        (1)5D: old algorithm compared with Hsieh's candidates
        (2)6D: new algorithm compared with Hsieh's candidates
        (3)5D_6D: old algorithm compared with new algorithm
---------------------------------------------------------------------------------------
latest update : 2019/03/02 Jordan Wu'''

#======================================================================================
# Initial Setup and Arguments Check
#======================================================================================
from os import system, path, chdir
from sys import argv, exit

path_P0 = '/home/ken/C2D-SWIRE_20180710/SOP_Program_6D_20190224/'
path_P1 = '/home/ken/C2D-SWIRE_20180710/Table_to_Compare/Table_From_Hsieh/' 
table_0 = path_P1 + 'all_candidates.tbl'

if len(argv) == 5:
    print('Start calculating ...')
else:
    exit('Error: Wrong Usage!\n \
          Exmaple: python [program] [catalog] [cloud\'s name] [data_type] [sort]\n \
          data_type: flux or mag (default=flux)\n \
          sort: yes or no')

table = str(argv[1])
cloud = str(argv[2])
data_type = str(argv[3])
sort = str(argv[4])

if sort == 'yes':
    #======================================================================================
    # Calculate 6D Gal_Prob
    #======================================================================================
    chdir(cloud + '_6D')
    #table = '../catalog-CHA_II_Gal_Prob_All.tbl'
    system('new_dict_6D_method.py ' + table + ' ' + cloud + ' ' + data_type)

    #======================================================================================
    # Sort and Compare
    #======================================================================================
    system('Check_6D_Gal_Prob.py ' + cloud + '_6D_GP_all_out_catalog.tbl' + ' ' + cloud)

    #======================================================================================
    # Initialize directories to storage
    #======================================================================================
    if path.isdir('./' + cloud + '_6D'):
        system('rm -r ' + cloud + '_6D')
    else:
        pass

    system('mkdir ' + cloud + '_6D')
    system('mkdir ' + cloud + '_6D/YSO_5D6D')
    system('mkdir ' + cloud + '_6D/YSO_5D6D/5D')
    system('mkdir ' + cloud + '_6D/YSO_5D6D/6D')
    system('mkdir ' + cloud + '_6D/YSO_5D6D/5D_6D')
    system('mkdir ' + cloud + '_6D/IC_5D6D')
    system('mkdir ' + cloud + '_6D/IC_5D6D/5D_HSIEH')
    system('mkdir ' + cloud + '_6D/IC_5D6D/6D_HSIEH')
    system('mkdir ' + cloud + '_6D/IC_5D6D/5D_6D')

    chdir('YSO_5D6D/5D')
    system('Comparator_SWIRE_format.py ' + '../../../' + cloud + '_YSO.tbl' + ' ' + table_0 + ' 5D HSIEH 7 yes no')
    chdir('../6D')
    system('Comparator_SWIRE_format.py ' + '../../' + cloud + '_6D_YSO.tbl' + ' ' + table_0 + ' 6D HSIEH 7 yes no')
    chdir('../5D_6D')
    system('Comparator_SWIRE_format.py ' + '../6D/' + '6D_and_HSIEH.tbl' + ' ' + '../5D/' + '5D_and_HSIEH.tbl ' + ' 6D 5D 7 yes no')

    chdir('../../IC_5D6D/5D_HSIEH')
    system('Comparator_SWIRE_format.py ' + '../../../' + cloud + '_GP_to_image_check.tbl' + ' ' + table_0 + ' 5D HSIEH  7 yes no')
    chdir('../6D_HSIEH')
    system('Comparator_SWIRE_format.py ' + '../../' + cloud + '_6D_GP_to_image_check.tbl' + ' ' + table_0 + ' 6D HSIEH 7 yes no')
    chdir('../5D_6D')
    system('Comparator_SWIRE_format.py ' + '../6D_HSIEH/' + '6D_and_HSIEH.tbl' + ' ' + '../5D_HSIEH/' + '5D_and_HSIEH.tbl' + ' 6D 5D 7 yes no')

else:
    #======================================================================================
    # Calculate 6D Gal_Prob
    #======================================================================================
    #table = '../catalog-CHA_II_Gal_Prob_All.tbl'
    system('new_dict_6D_method.py ' + table + ' ' + cloud + ' ' + data_type)

    #======================================================================================
    # Sort and Compare
    #======================================================================================
    system('Check_6D_Gal_Prob.py ' + cloud + '_6D_GP_all_out_catalog.tbl' + ' ' + cloud)
    
    print('End of calculating 6D galaxy probability ...')
