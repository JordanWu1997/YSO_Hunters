#!usr/bin/ipython

'''
#--------------------------------------------------------------------------------
This program is used to execute Fast_Comparator.py.
Catalog in this program is set to be the same dir where you execute this program.
It simply print out what Fast_Comparator.py get with different catalogs.
#--------------------------------------------------------------------------------
latest update: 20181023'''

import os
from sys import argv
from sys import exit

if len(argv) != 2:
    print('Error Usage')
    print('Example: python [program] [cloud\'s name]')
    exit()

name = str(argv[1])
all_candidate = '/home/ken/C2D-SWIRE_20180710/all_candidates.tbl'
HREL_catalog = '/home/ken/C2D-SWIRE_20180710/Converted_catalog/' + 'catalog-' + name +'-HREL.tbl'
program = '/home/ken/C2D-SWIRE_20180710/SOP_Tool_20181117/Fast_Comparator.py'

print('Comparing YSO possible candidates ...')
os.system('python ' + program + ' ' + all_candidate + ' ' + HREL_catalog) 
os.system('python ' + program + ' ' + all_candidate + ' ' + 'catalog-' + name + '-HREL_all_star_removal.tbl')
os.system('python ' + program + ' ' + all_candidate + ' ' + name + '_YSO_candidates.tbl')
os.system('python ' + program + ' ' + all_candidate + ' ' + name + '_GP_to_image_check.tbl')
os.system('python ' + program + ' ' + all_candidate + ' ' + name + '_saturate_candidates.tbl')
    
print('Looking for missing YSO candidates on Hsiehs\'s catalog ...')
os.system('python ' + program  + ' ' + all_candidate + ' ' + name + '_not_count.tbl') 
