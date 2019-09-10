#!/usr/bin/ipython

'''
-------------------------------------------------------------------

-------------------------------------------------------------------
latest update : 20190730 Jordan Wu'''

import os
import time
from sys import argv
from sys import exit

if len(argv) != 3:
    exit('\n\tError: Wrong Arguments\
    \n\tExample: [SOP_Execution.py] [Input table or \"Default\"] [cloud\'s name]\n')
else:
    print('Excecuting 5D-method ...')

cloud = str(argv[2])
filename = str(argv[1])

tStart = time.time()
# Step0: Calculate Gal Prob N/P and determine if the object is YSO
if filename == 'Default':
    #=======================================================================
    # Default Setting
    #=======================================================================
    os.system('Gal_Prob_Execution.py ' + cloud + '_saturate_correct_file.tbl ' + cloud)
    #=======================================================================
else:
    os.system('Gal_Prob_Execution.py ' + filename + '  ' + cloud)

# Step1: Image Check for 
# 1. Gal Prob Irreliable candidates
# 2. Saturate source in YSO candidates
# 3. Final YSO candidates's IR1 check (which exclude (2))
print('Image Checking ...')

# (1)Gal Prob P UNCERTAIN
os.system('degree_to_wcs.py ' + cloud + '_GP_to_image_check.tbl ' + cloud + ' Image_Check')
os.system('getfits.py ' + cloud + '_cans_to_wcs_image_check.tbl ' + cloud + ' Image_Check')

# (2)Saturate candidates in YSO candidates
print('\nThe Saturate Candiates in YSO candidates:')
os.system('echo | awk \'$185 == \"S\" {print $1, $3} \' '+ cloud + '_YSO.tbl')
os.system('echo | awk \'$185 == \"S\" \' '+ cloud + '_YSO.tbl' + ' > ' + cloud + '_saturate_candidates.tbl')
os.system('degree_to_wcs.py ' + cloud + '_saturate_candidates.tbl ' + cloud + ' Saturate')
os.system('getfits.py ' + cloud + '_cans_to_wcs_saturate.tbl ' + cloud + ' Saturate')

# (3)All YSO candidate's IR1 check excluding (2)
os.system('echo | awk \'$185 != \"S\" \' '+ cloud + '_YSO.tbl' + ' > ' + cloud + '_YSO_candidates.tbl')
os.system('degree_to_wcs.py ' + cloud + '_YSO_candidates.tbl ' + cloud + ' IR1_Check')
os.system('getfits.py ' + cloud + '_cans_to_wcs_IR1_check.tbl ' + cloud + ' IR1_Check')

# (4)Remove deg_to_wcs_catalog
os.system('rm '+ cloud + '_cans_to_wcs_image_check.tbl')
os.system('rm '+ cloud + '_cans_to_wcs_saturate.tbl')
os.system('rm '+ cloud + '_cans_to_wcs_IR1_check.tbl')

tEnd = time.time()
print("Whole 5D calculation process took %f sec" % (tEnd - tStart))
