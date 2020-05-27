#!/usr/bin/ipython
'''-------------------------------------------------------------------------
This program is between step5,step6 (Gal_Prob_(N/P)) and step6 (Image_Check)

Input: catalog after galaxy probability calculation

Output: (1)YSO: YSO candidates for sure
        (2)Galaxy: Galaxy candidates fo sure
        (3)GP_IC: GP with problems to image check
----------------------------------------------------------------------------
latest update: 2018/11/18'''

from sys import argv
from sys import exit

if len(argv) != 3:
    print('Wrong Usage!')
    print("Example: ipython Check_Prob.py [catalog] [MC cloud]")
    exit()

cloud = str(argv[2])
catalog = open(argv[1])
cat = catalog.readlines()

YSO = []; Galaxy = []; GP_IC = []

for i in range(len(cat)):
    row_prob = cat[i].split()

    #GP1 != no_count, GP2 == no_count
    if row_prob[234] != 'no_count' and row_prob[236] == 'no_count':
        GP1 = float(row_prob[234])
        if GP1 <= 1:
            if row_prob[238] != 'no_count':
                GPP1 = float(row_prob[238])
                if GPP1 > 1:
                    GP_IC.append(cat[i])
                else:
                    YSO.append(cat[i])
            else:
                GP_IC.append(cat[i])
        else:
            Galaxy.append(cat[i])

    #GP1 == no_count, GP2 != no_count
    elif row_prob[234] == 'no_count' and row_prob[236] != 'no_count':
        GP2 = float(row_prob[236])
        if GP2 <= 1:
            if row_prob[240] != 'no_count':
                GPP2 = float(row_prob[240])
                if GPP2 > 1:
                    GP_IC.append(cat[i])
                else:
                    YSO.append(cat[i])
            else:
                GP_IC.append(cat[i])
        else:
            Galaxy.append(cat[i])

    #GP1 != no_count, GP2 != no_count
    elif row_prob[234] != 'no_count' and row_prob[236] != 'no_count':
        GP1, GP2 = float(row_prob[234]), float(row_prob[236])
        if GP1 > 1 and GP2 > 1:
            Galaxy.append(cat[i])
        elif GP1 <= 1 and GP2 <= 1:
            if row_prob[238] != 'no_count' and row_prob[240] != 'no_count':
                GPP1, GPP2 = float(row_prob[238]), float(row_prob[240])
                if GPP1 > 1 or GPP2 > 1:
                    GP_IC.append(cat[i])
                else:
                    YSO.append(cat[i])
            elif row_prob[238] != 'no_count' and row_prob[240] == 'no_count':
                GPP1 = float(row_prob[238])
                if  GPP1 > 1:
                    GP_IC.append(cat[i])
                else:
                    YSO.append(cat[i])
            elif row_prob[238] == 'no_count' and row_prob[240] != 'no_count':
                GPP2 = float(row_prob[240])
                if  GPP2 > 1:
                    GP_IC.append(cat[i])
                else:
                    YSO.append(cat[i])
            elif row_prob[238] == 'no_count' and row_prob[240] == 'no_count':
                GP_IC.append(cat[i])
        elif GP1 <= 1 and GP2 > 1:
            if row_prob[238] != 'no_count':
                GPP1 = float(row_prob[238])
                if GPP1 > 1:
                    GP_IC.append(cat[i])
                else:
                    YSO.append(cat[i])
            else:
                GP_IC.append(cat[i])
        elif GP1 > 1 and GP2 <= 1:
            if row_prob[240] != 'no_count':
                GPP2 = float(row_prob[240])
                if GPP2 > 1:
                    GP_IC.append(cat[i])
                else:
                    YSO.append(cat[i])
            else:
                GP_IC.append(cat[i])

    #GP1 == no_count, GP2 == no_count
    else:
        Galaxy.append(cat[i])

out_ca = open(cloud + '_YSO.tbl',"w")
for i in YSO:
    out_ca.write(str(i))
out_ca.close()

out_ca = open(cloud + '_Galaxy.tbl',"w")
for i in Galaxy:
    out_ca.write(str(i))
out_ca.close()

out_cat=open(cloud + '_GP_to_image_check.tbl',"w")
for i in GP_IC:
    out_cat.write(str(i))
out_cat.close()
