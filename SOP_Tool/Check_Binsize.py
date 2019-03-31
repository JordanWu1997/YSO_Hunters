#!/usr/bin/ipython
'''
-------------------------------------------------------------------
This program is for selecting galaxy sample with GP<=1

Input : c2d_no_star_catalog (Galaxy samples)

Output :(1) galaxy catalog with galaxy probability
        (2) galaxy candidate catalog which GP<=1
-------------------------------------------------------------------
latest update : 20190330 Jordan Wu'''

from sys import argv
from os import system

#path = '/home/ken/C2D-SWIRE_20180710/SOP_Program_20181117/'
path = '/home/ken/C2D-SWIRE_20180710/SOP_Program_6D_20190224/'

catalog = str(argv[-1])
system('ipython ' + path + 'new_dict_6D_method.py ' + catalog + ' Galaxy_Sample')

print('\nThe number of Galaxy candidate that GP<=1 ...')
system('awk \'($243!~/no_count/)&&($243<=\"1.0\") {print $243}\' '+ 'Galaxy_Sample_6D_GP_all_out_catalog.tbl | wc')
print('\nGalaxy candidate that GP=<1 ...')
system('awk \'($243!~/no_count/)&&($243<=\"1.0\") {print $243}\' '+ 'Galaxy_Sample_6D_GP_all_out_catalog.tbl')
system('awk \'($243!~/no_count/)&&($243<=\"1.0\")\' '+ 'Galaxy_Sample_6D_GP_all_out_catalog.tbl > GP_LESS_1.tbl')
