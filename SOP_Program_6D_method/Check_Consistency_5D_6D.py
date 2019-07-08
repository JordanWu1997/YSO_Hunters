#!/usr/bin/ipython

'''
#-----------------------------------------------
Thiis program is for YSO Hnuter project.

input : catalog with 5DGP, 6DGP
output: consistency check result col_index [247]

*minor change: no label for consistency check 
#-----------------------------------------------
Lastest Upload 20190301 Jordan Wu
'''

from os import system
from sys import argv
from sys import exit
import numpy as np

#Part 0: Load the catalog with all GP/GPP to compare
catalog = open(str(argv[1]), 'r')
candidates = catalog.readlines()
catalog.close()

cloud = str(argv[2])

#Part 1: Consistent Check
New_catalog = []
GP_inc = []
GPP_inc = []

if system('rm ' + cloud + '_consistency_check -r') == 256:
    system('mkdir ' + cloud + '_consistency_check')
else:
    system('rm ' + cloud + '_consistency_check -r')
    system('mkdir ' + cloud + '_consistency_check')

for row in candidates:
    cand = row.split()
    consist = 'CTC'
    # Select 6DGP lack J band (identical to 5DGP)
    if '5bands_Lack_J' in cand[241]:
        if cand[242] != 'no_count' and cand[236] != 'no_count':
            if (float(cand[242])<=1e-3 and float(cand[236])<=1e-3) or (abs(float(cand[242])-float(cand[236]))<1e-5):
                consist += '_GP_pass'
            else:
                GP_inc.append(row)
                consist += '_GP_fail'
        else:
            if cand[242] == cand[241]:
                consist += '_GP_pass'
            else:
                consist += '_GP_fail'
    else:
        consist += '_none'

#    try:
#        cand[247] = consist
#    except IndexError:
#        cand.append('z')
#        cand[247] = consist
#
#    New_row = row + '\t' + consist
#    New_catalog.append(str(New_row))

out = open(cloud + '_consistency_check/' + cloud + '_catalog_after_check.tbl', 'w')
for ele in New_catalog:
    out.write(ele)
out.close()

out = open(cloud + '_consistency_check/' + cloud + '_catalog_GP_inc.tbl', 'w')
for inc in GP_inc:
    out.write(inc)
out.close()
