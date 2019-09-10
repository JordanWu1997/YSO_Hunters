#!/usr/bin/ipython
'''
------------------------------------------------------------------------------------

---------------------------------------------------------------------------------------
latest update : 2019/07/30 Jordan Wu'''

#======================================================================================
# Initial Setup and Arguments Check
#======================================================================================
from os import system, path, chdir
from sys import argv, exit

if len(argv) != 6:
    exit('\n\tError: Wrong Arguments\
    \n\tExample: [SOP_Execution.py] [cloud\'s name] [data type] [sort] [sort_ref or \'Default\'] [Binsize]\
    \n\t[data type]: \'flux\' or \'mag\'\
    \n\t[sort option]: True or False\
    \n\t[sort ref]: Table as reference for sorting and comparing\
    \n\t[binsize]: Binsize to calculate multi-Gal Prob')
else:
    print('Excecuting 6D-method ...')

cloud = str(argv[1])
data_type = str(argv[2])
sort_option = str(argv[3])
sort_ref = str(argv[4])
bin_size = str(argv[5])

if sort_ref == 'Default':
    #=======================================================================
    # Default Setting
    #=======================================================================
    ref_path = '/home/ken/C2D-SWIRE_20180710/Table_to_Compare/Table_From_Hsieh/'
    ref_table = ref_path + 'all_candidates.tbl'
    #=======================================================================
else:
    ref_table = sort_ref

# Initialize directories to storage
if path.isdir('./' + cloud + '_6D_BS_' + bin_size):
    system('rm -r ' + cloud + '_6D_BS_' + bin_size)
system('mkdir ' + cloud + '_6D_BS_' + bin_size)

if sort_option == 'True':

    # (1) Initialize directories to storage sorted results
    system('mkdir ' + cloud + '_6D_BS_' + bin_size + '/YSO_5D6D')
    system('mkdir ' + cloud + '_6D_BS_' + bin_size + '/YSO_5D6D/5D')
    system('mkdir ' + cloud + '_6D_BS_' + bin_size + '/YSO_5D6D/6D')
    system('mkdir ' + cloud + '_6D_BS_' + bin_size + '/YSO_5D6D/5D_6D')
    system('mkdir ' + cloud + '_6D_BS_' + bin_size + '/IC_5D6D')
    system('mkdir ' + cloud + '_6D_BS_' + bin_size + '/IC_5D6D/5D_HSIEH')
    system('mkdir ' + cloud + '_6D_BS_' + bin_size + '/IC_5D6D/6D_HSIEH')
    system('mkdir ' + cloud + '_6D_BS_' + bin_size + '/IC_5D6D/5D_6D')

    # (2) Calculate 6D Gal_Prob
    chdir(cloud + '_6D_BS_' + bin_size)
    system('new_dict_6D_method.py ' + '../catalog-' + cloud  + '_Gal_Prob_All.tbl' + ' '  + cloud + ' ' + data_type + ' new ' + bin_size + ' argv')

    # (3) Check
    system('Check_6D_Gal_Prob.py ' + cloud + '_6D_GP_all_out_catalog.tbl' + ' ' + cloud)
    
    # (4) Sort and Compare
    chdir('YSO_5D6D/5D')
    system('Comparator_SWIRE_format.py ' + '../../../' + cloud + '_YSO.tbl' + ' ' + ref_table + ' 5D HSIEH 7 yes no')
    chdir('../6D')
    system('Comparator_SWIRE_format.py ' + '../../' + cloud + '_6D_YSO.tbl' + ' ' + ref_table + ' 6D HSIEH 7 yes no')
    chdir('../5D_6D')
    system('Comparator_SWIRE_format.py ' + '../6D/' + '6D_and_HSIEH.tbl' + ' ' + '../5D/' + '5D_and_HSIEH.tbl ' + ' 6D 5D 7 yes no')
    chdir('../../IC_5D6D/5D_HSIEH')
    system('Comparator_SWIRE_format.py ' + '../../../' + cloud + '_GP_to_image_check.tbl' + ' ' + ref_table + ' 5D HSIEH  7 yes no')
    chdir('../6D_HSIEH')
    system('Comparator_SWIRE_format.py ' + '../../' + cloud + '_6D_GP_to_image_check.tbl' + ' ' + ref_table + ' 6D HSIEH 7 yes no')
    chdir('../5D_6D')
    system('Comparator_SWIRE_format.py ' + '../6D_HSIEH/' + '6D_and_HSIEH.tbl' + ' ' + '../5D_HSIEH/' + '5D_and_HSIEH.tbl' + ' 6D 5D 7 yes no')

else:
    # (1) Calculate 6D Gal_Prob
    chdir(cloud + '_6D_BS_' + bin_size)
    system('new_dict_6D_method.py ' + '../catalog-' + cloud  + '_Gal_Prob_All.tbl' + ' '  + cloud + ' ' + data_type + ' new ' + bin_size + ' argv')
    
    # (2) Sort and Compare
    system('Check_6D_Gal_Prob.py ' + cloud + '_6D_GP_all_out_catalog.tbl' + ' ' + cloud)
    
print('End of calculating 6D galaxy probability ...')
