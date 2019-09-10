#!/usr/bin/ipython

'''
------------------------------------------------------------------------------------

---------------------------------------------------------------------------------------
latest update : 2019/07/30 Jordan Wu'''

from os import system, path, chdir
from sys import argv, exit

if len(argv) != 4:
    exit('\n\tError: Wrong Arguments\
    \n\tExample: [SOP_Execution.py] [cloud\'s name] [binsize] [Av_bound]\
    \n\t[binsize]: Binsize to calculate multi-Gal Prob\
    \n\t[Av_bound]: Boundary of extinction value')

cloud = str(argv[1])
binsize = str(argv[2])
Av_bound = str(argv[3])

system('cat ' + cloud +  '_6D_GP_to_image_check.tbl' + ' ' + cloud + '_6D_YSO.tbl' + ' > 6D_ALGO_YSOc.tbl')

if path.isdir(cloud + '_Extinction_Test_Av_' + Av_bound):
    system('rm -r ' + cloud + '_Extinction_Test_Av_' + Av_bound)
system('mkdir ' + cloud + '_Extinction_Test_Av_' + Av_bound)
chdir(cloud + '_Extinction_Test_Av_' + Av_bound)
system('mkdir ' + cloud + '_YSOc_PASS_Extinction_Test')
system('mkdir ' + cloud + '_YSOc_FAIL_Extinction_Test')

# PASS_Extinction_Test
# (1) Sort Data
chdir(cloud + '_YSOc_PASS_Extinction_Test')
system('cp ' + '../../6D_ALGO_YSOc.tbl ' + './')
system('awk \'$18>' + str(float(Av_bound)) + '\'' + ' 6D_ALGO_YSOc.tbl > 6D_ALGO_YSOc_PASS_test.tbl')

# (2) Run GP Check For Candidates Passed Tests
Pass = open('6D_ALGO_YSOc_PASS_test.tbl', 'r').readlines()
if len(Pass) != 0:
    system('new_dict_6D_method.py ' + '6D_ALGO_YSOc_PASS_test.tbl ' + cloud + '_YSOc_PASS_test' + ' mag new ' + binsize + ' argv')
    system('Check_6D_Gal_Prob.py ' + cloud + '_YSOc_PASS_test_6D_GP_all_out_catalog.tbl' + ' ' + cloud + '_YSOc_PASS_test')

    system('degree_to_wcs.py ' + cloud + '_YSOc_PASS_test_6D_GP_to_image_check.tbl ' + cloud + ' Image_Check')
    system('getfits.py ' + cloud + '_cans_to_wcs_image_check.tbl ' + cloud + ' Image_Check')
    system('echo | awk \'$185 == \"S\" \' '+ cloud + '_YSOc_PASS_test_6D_YSO.tbl' + ' > ' + cloud + '_saturate_candidates.tbl')
    system('degree_to_wcs.py ' + cloud + '_saturate_candidates.tbl ' + cloud + ' Saturate')
    system('getfits.py ' + cloud + '_cans_to_wcs_saturate.tbl ' + cloud + ' Saturate')
    system('echo | awk \'$185 != \"S\" \' '+ cloud + '_YSOc_PASS_test_6D_YSO.tbl' + ' > ' + cloud + '_YSO_candidates.tbl')
    system('degree_to_wcs.py ' + cloud + '_YSO_candidates.tbl ' + cloud + ' IR1_Check')
    system('getfits.py ' + cloud + '_cans_to_wcs_IR1_check.tbl ' + cloud + ' IR1_Check')
    system('rm '+ cloud + '_cans_to_wcs_image_check.tbl')
    system('rm '+ cloud + '_cans_to_wcs_saturate.tbl')
    system('rm '+ cloud + '_cans_to_wcs_IR1_check.tbl')

#=======================================================
# (3) If All Candidates Fail Test => Print Out Message
else:
    print('=================================================')
    print('\nNo One Pass Extinction Test Av=%s\n' % Av_bound)
    print('=================================================')
#=======================================================

# FAIL_Extinction_Test
# (1) Sort Data
chdir('../' + cloud + '_YSOc_FAIL_Extinction_Test')
system('cp ' + '../../6D_ALGO_YSOc.tbl ' + './')
system('awk \'$18<=' + str(float(Av_bound)) + '\'' + ' 6D_ALGO_YSOc.tbl > 6D_ALGO_YSOc_FAIL_test.tbl')
system('new_dict_6D_method.py ' + '6D_ALGO_YSOc_FAIL_test.tbl ' + cloud + '_YSOc_FAIL_test' + ' mag new ' + binsize + ' argv')
system('Check_6D_Gal_Prob.py ' + cloud + '_YSOc_FAIL_test_6D_GP_all_out_catalog.tbl' + ' ' + cloud + '_YSOc_FAIL_test')
# (2) Get Image
system('degree_to_wcs.py ' + cloud + '_YSOc_FAIL_test_6D_GP_to_image_check.tbl ' + cloud + ' Image_Check')
system('getfits.py ' + cloud + '_cans_to_wcs_image_check.tbl ' + cloud + ' Image_Check')
system('echo | awk \'$185 == \"S\" \' '+ cloud + '_YSOc_FAIL_test_6D_YSO.tbl' + ' > ' + cloud + '_saturate_candidates.tbl')
system('degree_to_wcs.py ' + cloud + '_saturate_candidates.tbl ' + cloud + ' Saturate')
system('getfits.py ' + cloud + '_cans_to_wcs_saturate.tbl ' + cloud + ' Saturate')
system('echo | awk \'$185 != \"S\" \' '+ cloud + '_YSOc_FAIL_test_6D_YSO.tbl' + ' > ' + cloud + '_YSO_candidates.tbl')
system('degree_to_wcs.py ' + cloud + '_YSO_candidates.tbl ' + cloud + ' IR1_Check')
system('getfits.py ' + cloud + '_cans_to_wcs_IR1_check.tbl ' + cloud + ' IR1_Check')
system('rm '+ cloud + '_cans_to_wcs_image_check.tbl')
system('rm '+ cloud + '_cans_to_wcs_saturate.tbl')
system('rm '+ cloud + '_cans_to_wcs_IR1_check.tbl')
