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

path = '/home/ken/C2D-SWIRE_20180710/SOP_Program_20181117/'
catalog = str(argv[-1])
system('ipython ' + path + 'multi-d_Prob_J_MP1.py ' + catalog)
system('ipython ' + path + 'multi-d_Prob_IR1_MP1.py')
system('rm step')
system('awk \'($235!~/no_count/||$237!~/no_count/)&&($235<=\"1.0\"||$237<=\"1.0\") {print $235,$237}\' Out_catalog > GP_LESS_1.tbl')

print('\nGalaxy candidate that GP=<1 ...')
system('cat GP_LESS_1.tbl')

print('\nThe number of Galaxy candidate that GP<=1 ...')
system('wc GP_LESS_1.tbl')
