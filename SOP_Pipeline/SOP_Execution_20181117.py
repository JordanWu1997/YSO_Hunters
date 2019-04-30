#!/usr/bin/ipython

'''
-------------------------------------------------------------------
This program is for running all program in order to get YSO candidates

Input : (1) w/o 6D calculation: c2d HREL catalog
        (2) w/i 6D calculation: c2d HREL catalog after calculating magnitudes

Output: (1) w/o 6D calculation: 
            1. 5D YSO candidates, candidates to image check, Galaxy candidates
        (2) w/i 6D calculation:
            1. 5D YSO candidates, candidates to image check, Galaxy candidates
            2. 6D YSO candidates, candidates to image check, Galaxy candidates
            3. optionally, comparison between 5D, 6D, Hsieh's catalog

NOTE: (1) **Remove 6D gal prob counting function for temp.
      (2) add new extinction correction for mag
-------------------------------------------------------------------
latest update : 20190430 Jordan Wu'''

import os
import time
from sys import argv
from sys import exit

if len(argv) != 5:
    exit('Error: Wrong Usage\n\
    Example: python [SOP_Execution.py] [HREL catalog] [cloud\'s name] [skip] [datatype]\n\
    skip: True/False to skip star_removal and deredden processes\n\
    datatype: flux/mag input datatype for EXTINCTION CORRECTION (defualt:flux)\n\
    Warning: Input catalog must with magnitudes if 6D-OPTION is True')

tStart = time.time()

#-------------------------------------------------------------------------

#Step0 : SETUP
catalog = str(argv[1])
cloud = str(argv[2])
skip = bool(argv[3])
datatype = str(argv[4])

path = '/home/ken/C2D-SWIRE_20180710' + '/SOP_Program_20181117/'
path_Av_table = '/home/ken/C2D-SWIRE_20180710' + '/Backup_Av_table_20180826/'
path_Av_table_PER = '/home/ken/'

#-------------------------------------------------------------------------

if ~skip:

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

    #=======================================================================
    if datatype == 'flux':
        os.system('python ' + path + 'Extinction_Correction.py ' + path_Av_table + cloud1 + '_Av_table.tbl ' + 'catalog-' + cloud2 + '-HREL_all_star_removal.tbl ' + cloud)
    else:
        print('mag ...')
        os.system('python ' + path + 'Extinction_Correction_mag.py ' + path_Av_table + cloud1 + '_Av_table.tbl ' + 'catalog-' + cloud2 + '-HREL_all_star_removal.tbl ' + cloud)
    #=======================================================================

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
