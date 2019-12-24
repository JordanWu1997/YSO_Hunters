#!/usr/bin/python

'''
-------------------------------------------------------------------




-------------------------------------------------------------------
latest update : 20190730 Jordan Wu'''

import os
import time
from sys import argv
from sys import exit
import SOP_Program_Path as spp

if len(argv) != 4:
    exit('\n\tError: Wrong Arguments\
    \n\tExample: [SOP_Execution.py] [HREL catalog] [cloud\'s name] [Extinction table]\
    \n\t[Excintion table]: New/Old (Self-made / from Hsieh)\n')
else:
    print('Excecuting Preset ...')

tStart = time.time()

# Step0 : Setup Params
catalog = str(argv[1])
cloud = str(argv[2])
emap = str(argv[3])

if emap == 'Old':
    path_Av_table = spp.Hsieh_Av_Table_path #'/home/ken/C2D-SWIRE_20180710/All_Extinction_Table/Tables_From_Hsieh/'
else:
    path_Av_table = spp.Selfmade_Av_Table_path #'/home/ken/C2D-SWIRE_20180710/All_Extinction_Table/Tables_Self_Made/'

tStart = time.time()
# Step1: Remove stars
os.system('Star_Removal.py ' + catalog + ' ' + cloud + ' ' + 'True')

# Step2: Deredden (Correct Extinction)
t_deredden_start = time.time()

#=======================================================================
# Default Extinction Map Setting
#=======================================================================
#LUP share one Av_table, but not mosaics
if 'LUP' in cloud:
    cloud1, cloud2 = 'LUP', cloud
    print('Extinction Map: ' + path_Av_table + cloud1 + '_Av_table.tbl')
else:
    cloud1, cloud2 = cloud, cloud
    print('Extinction Map: ' + path_Av_table + cloud1 + '_Av_table.tbl')
#=======================================================================

print('Start Extinction Correction ...')
os.system('Extinction_Correction.py ' + path_Av_table + cloud1 + '_Av_table.tbl ' + 'catalog-' + cloud2 + '-HREL_all_star_removal.tbl ' + cloud + ' ' + emap)

t_deredden_end = time.time()
print('Extinction Correction took %f sec' % (t_deredden_end - t_deredden_start))

# Step3: Correct MP1 Saturation
# MP1 saturate source will be noted with MP1_Q = 'S'
os.system('Find_Saturate.py ' + cloud + '_Deredden.tbl ' + cloud)

tEnd = time.time()
print("Whole Preset process took %f sec" % (tEnd - tStart))
