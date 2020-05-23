#!/usr/bin/python
'''-------------------------------------------------------------------------
This program is to check 6d galaxy probability and sort the candidates

Input: catalog after galaxy probability (P)  calculation

Output: (1)YSO: YSO candidates for sure
        (2)Galaxy: Galaxy candidates fo sure
        (3)GP_IC: GP with problems to image check
----------------------------------------------------------------------------
latest update: 2018/12/11'''

import os
from sys import argv
from sys import exit

if len(argv) != 3:
    exit('Wrong Usage!\nExample: ipython [program] [catalog] [MC cloud]')

cloud = str(argv[2])
catalog = open(argv[1], 'r')
cat = catalog.readlines()

#-----------------------------------------------------------------------------------------------------------

YSO = []; Galaxy = []; GP_IC = []
for i in range(len(cat)):
    row_prob = cat[i].split()

    if row_prob[242] != 'no_count':
        GP = float(row_prob[242])
        if GP <= 1:
            if row_prob[244] != 'no_count':
                GPP = float(row_prob[244])
                if GPP > 1:
                    GP_IC.append(cat[i])
                elif GPP <= 1:
                    YSO.append(cat[i])
            else:
                GP_IC.append(cat[i])

        elif GP > 1:
            if row_prob[244] != 'no_count':
                GPP = float(row_prob[244])
                if GP <= 1:
                    GP_IC.append(cat[i])
                elif GP > 1:
                    Galaxy.append(cat[i])
            else:
                Galaxy.append(cat[i])
    else:
        Galaxy.append(cat[i])

#-----------------------------------------------------------------------------------------------------------

out_ca = open(cloud + '_6D_YSO.tbl',"w")
for i in YSO:
    out_ca.write(str(i))
out_ca.close()

out_ca = open(cloud + '_6D_Galaxy.tbl',"w")
for i in Galaxy:
    out_ca.write(str(i))
out_ca.close()

out_cat = open(cloud + '_6D_GP_to_image_check.tbl',"w")
for i in GP_IC:
    out_cat.write(str(i))
out_cat.close()

#-----------------------------------------------------------------------------------------------------------
print('The Saturate Candiates in YSO candidates: ')
os.system('echo | awk \'$185 == \"S\" {print $1, $3} \' '+ cloud + '_6D_YSO.tbl')
print('The confident YSO candidates: ')
os.system('wc ' + cloud + '_6D_YSO.tbl')
print('The confident Galaxy candidates: ')
os.system('wc ' + cloud + '_6D_Galaxy.tbl')
print('The candidate to image check ')
os.system('wc ' + cloud + '_6D_GP_to_image_check.tbl')
#-----------------------------------------------------------------------------------------------------------
