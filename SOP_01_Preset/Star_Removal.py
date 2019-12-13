#!/usr/bin/ipython

'''-------------------------------------------------------------------
This program is for step1 (star_removal)

Input : c2d HREL catalog

Output : catalog with star, zero, 2mass, one, two, red1, red2 removal
----------------------------------------------------------------------
latest update : 2019/01/02'''

import os
from sys import argv, exit

if len(argv) != 4:
    print('Error: Wrong Usage')
    print('Example: python Star_Removal.py [catalog] [cloud\'s name] [data-Option]')
    print('data-Option: True/False to delete all data except all_removal catalog')
    exit()

table = str(argv[1])
cloud = str(argv[2])
objecttype_ID = 17
print('catalog = '+table)

table1 = 'tables/catalog-' + cloud + '-HREL' + '_star_removal.tbl'
table2 = 'tables/catalog-' + cloud + '-HREL' + '_star_zero_removal.tbl'
table3 = 'tables/catalog-' + cloud + '-HREL' + '_star_zero_2mass_removal.tbl'
table4 = 'tables/catalog-' + cloud + '-HREL' + '_star_zero_2mass_one_removal.tbl'
table5 = 'tables/catalog-' + cloud + '-HREL' + '_star_zero_2mass_one_two_removal.tbl'
table6 = 'tables/catalog-' + cloud + '-HREL' + '_star_zero_2mass_one_two_red1_removal.tbl'
table7 = 'tables/catalog-' + cloud + '-HREL' + '_star_zero_2mass_one_two_red1_red2_removal.tbl'

table8 = 'catalog-' + cloud + '-HREL' + '_all_star_removal.tbl'
table9 = cloud + '_star.tbl'

if os.path.isdir('tables'):
    os.system('rm -r tables')
os.system('mkdir tables')

os.system('awk \'${:d}!=\"star\"\'  {} > {}'.format(objecttype_ID, table,  table1))
os.system('awk \'${:d}!=\"zero\"\'  {} > {}'.format(objecttype_ID, table1, table2))
os.system('awk \'${:d}!=\"2mass\"\' {} > {}'.format(objecttype_ID, table2, table3))
os.system('awk \'${:d}!=\"one\"\'   {} > {}'.format(objecttype_ID, table3, table4))
os.system('awk \'${:d}!=\"two\"\'   {} > {}'.format(objecttype_ID, table4, table5))
os.system('awk \'${:d}!=\"red1\"\'  {} > {}'.format(objecttype_ID, table5, table6))
os.system('awk \'${:d}!=\"red2\"\'  {} > {}'.format(objecttype_ID, table6, table7))
os.system('awk \'${:d}==\"star\"\'  {} > {}'.format(objecttype_ID, table,  table9))

print('The number of objects in the catalog:')
os.system('wc -l ' + table )
os.system('wc -l ' + table1)
os.system('wc -l ' + table2)
os.system('wc -l ' + table3)
os.system('wc -l ' + table4)
os.system('wc -l ' + table5)
os.system('wc -l ' + table6)
os.system('wc -l ' + table7)

os.system('cp ' + table7 + ' ' + table8)

if argv[3] == 'True':
    os.system('rm -r tables')
