#!/usr/bin/python
'''
-------------------------------------------------------------------

Example: [program] [HREL catalog] [cloud's name] [Extinction table]
Input Variables:
    [HREL catalog]:    Catalog to calculate
    [cloud's name]:    Name of cloud
    [Excintion table]: Self_made/Hsieh

-------------------------------------------------------------------
Latest update : 2020/05/26 Jordan Wu'''

# Import Modules
#===================================
from __future__ import print_function
from sys import argv, exit
from os import system
import SOP_Program_Path as spp
import time

# Main Programs
#===================================
if __name__ == '__main__':
    t_start = time.time()

    # Check inputs
    if len(argv) != 4:
        exit('\n\tError: Wrong Arguments\
              \n\tExample: [program] [HREL catalog] [cloud\'s name] [Extinction table]\
              \n\t[Excintion table]: Self_made/Hsieh)\n')
    else:
        print('\nExcecuting Preset Pipeline ...')

    # Step0 : Setup Params
    catalog = str(argv[1])
    cloud   = str(argv[2])
    emap    = str(argv[3])

    # Set extinction table to use
    if emap == 'Hsieh':
        path_Av_table = spp.Hsieh_Av_Table_path #'/home/ken/C2D-SWIRE_20180710/All_Extinction_Table/Tables_From_Hsieh/'
    else:
        path_Av_table = spp.Selfmade_Av_Table_path #'/home/ken/C2D-SWIRE_20180710/All_Extinction_Table/Tables_Self_Made/'

    # Step1: Remove stars
    system('Star_Removal.py ' + catalog + ' ' + cloud + ' ' + 'True')

    # Step2: Deredden (Correct Extinction)
    t_deredden_start = time.time()
    #=======================================================================
    # Default Extinction Map Setting
    #=======================================================================
    #LUP share one Av_table, but not mosaics
    if 'LUP' in cloud:
        cloud1, cloud2 = 'LUP', cloud
    else:
        cloud1, cloud2 = cloud, cloud
    #=======================================================================
    # print('\nStart Extinction Correction ...')
    system('Extinction_Correction.py {}{}_Av_table.tbl {} catalog-{}-HREL_all_star_removal.tbl {}'.format(\
            path_Av_table, cloud1, emap, cloud2, cloud))
    t_deredden_end = time.time()
    # print('Extinction Correction took {:.3f} secs'.format(t_deredden_end - t_deredden_start))

    # Step3: Correct MP1 Saturation
    # MP1 saturate source will be noted with MP1_Q = 'S'
    print('\nStart Finding Saturate Source ...')
    print('For now, spitzer data is lost ...')
    print(str(system('Find_Saturate.py ' + cloud + '_Deredden.tbl ' + cloud)))

    t_end = time.time()
    print("\nWhole Preset process {} took {:.3f} secs".format(argv[0], t_end - t_start))
