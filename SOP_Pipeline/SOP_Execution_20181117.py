#!/usr/bin/ipython

'''
-------------------------------------------------------------------
This program is for running all program in order to get YSO candidates

Input : c2d HREL catalog

Output : YSO candidates, candidates to image check, Galaxy candidates

-------------------------------------------------------------------
latest update : 20190303 Jordan Wu'''

import os
import time
from sys import argv
from sys import exit

if len(argv) != 4:
    print('Error: Wrong Usage')
    print('Example: python [SOP_Execution.py] [HREL catalog] [cloud\'s name] [skip]')
    print('skip: True/False to skip star_removal and deredden processes')
    exit()

tStart = time.time()

#-------------------------------------------------------------------------

#Step0 : SETUP
catalog = str(argv[1])
cloud = str(argv[2])
skip = str(argv[3])
path = '/home/ken/C2D-SWIRE_20180710' + '/SOP_Program_20181117/'
path_Av_table = '/home/ken/C2D-SWIRE_20180710' + '/Backup_Av_table_20180826/'
path_Av_table_PER = '/home/ken/'

#-------------------------------------------------------------------------

if skip == "False":

    #Step1: Remove stars
    os.system('python ' + path + 'Star_Removal.py ' + catalog + ' ' + cloud + ' ' + 'True')

    #Step2: Deredden (Correct Extinction) 
    t_deredden_start = time.time()

    #LUP share one Av_table, but not mosaics
    if 'LUP' in cloud:
        cloud1, cloud2 = 'LUP', cloud
        print('Extinction Map: ' + path_Av_table + cloud1 + '_Av_table.tbl')

    # New extinction map of Perseus from Shih-Ping Lai 2018.12
    elif cloud == 'PER':
        path_Av_table = path_Av_table_PER
        cloud1, cloud2 = cloud, cloud
        print('Extinction Map: ' + path_Av_table + cloud1 + '_Av_table.tbl')

    else:
        cloud1, cloud2 = cloud, cloud
        print('Extinction Map: ' + path_Av_table + cloud1 + '_Av_table.tbl')

    os.system('python ' + path + 'Extinction_Correction.py ' + path_Av_table + cloud1 + '_Av_table.tbl ' + 'catalog-' + cloud2 + '-HREL_all_star_removal.tbl ' + cloud)
    
    t_deredden_end = time.time() 
    print('Extinction Correction took %f sec' % (t_deredden_end - t_deredden_start))

else:
    pass

#-------------------------------------------------------------------------

#Step3: Correct MP1 Saturation

os.system('python ' + path + 'Find_Saturate.py ' + cloud + '_Deredden.tbl ' + cloud) 
# MP1 saturate source will be noted with MP1_Q = 'S'

#-------------------------------------------------------------------------

#Step4: Calculate Gal Prob N/P and determine if the object is YSO
os.system('python ' + path + 'Gal_Prob_Execution.py ' + cloud + '_saturate_correct_file.tbl ' + cloud)

#-------------------------------------------------------------------------

#Step5: Image Check for (1)Gal Prob UNCERTAIN, (2)Saturate source in YSO candidates, (3)Final YSO candidates's IR1 check ( except for (2))

print('Image Checking ...')

#(1)Gal Prob P UNCERTAIN
os.system('python ' + path + 'degree_to_wcs.py ' + cloud + '_GP_to_image_check.tbl ' + cloud + ' Image_Check')
os.system('python ' + path + 'getfits.py ' + cloud + '_cans_to_wcs_image_check.tbl ' + cloud + ' Image_Check')

#(2)Saturate candidates in YSO candidates
print('The Saturate Candiates in YSO candidates: ')
os.system( 'echo | awk \'$185 == \"S\" {print $1, $3} \' '+ cloud + '_YSO.tbl')
os.system( 'echo | awk \'$185 == \"S\" \' '+ cloud + '_YSO.tbl' + ' > ' + cloud + '_saturate_candidates.tbl')
os.system('python ' + path + 'degree_to_wcs.py ' + cloud + '_saturate_candidates.tbl ' + cloud + ' Saturate')
os.system('python ' + path + 'getfits.py ' + cloud + '_cans_to_wcs_saturate.tbl ' + cloud + ' Saturate')

#(3)All YSO candidate's IR1 check except (2)
os.system( 'echo | awk \'$185 != \"S\" \' '+ cloud + '_YSO.tbl' + ' > ' + cloud + '_YSO_candidates.tbl')
os.system('python ' + path + 'degree_to_wcs.py ' + cloud + '_YSO_candidates.tbl ' + cloud + ' IR1_Check')
os.system('python ' + path + 'getfits.py ' + cloud + '_cans_to_wcs_IR1_check.tbl ' + cloud + ' IR1_Check')

#(4)Remove deg_to_wcs_catalog
os.system('rm '+ cloud + '_cans_to_wcs_image_check.tbl')
os.system('rm '+ cloud + '_cans_to_wcs_saturate.tbl')
os.system('rm '+ cloud + '_cans_to_wcs_IR1_check.tbl')

#-------------------------------------------------------------------------

tEnd = time.time()
print("This process took %f sec" % (tEnd - tStart))

#=========================================================================
#Step6: Calculate 6D galaxy probability
os.system('6D_SOP_Execution.py ' + cloud)
#=========================================================================
