#!/usr/bin/env python
from glob import glob
from sys import argv

index_list = glob(r'./*_image_check_list.tbl')[0]
with open (index_list, 'r') as f:
    image_check_list = f.readlines()

index, label = [], []
for rows in image_check_list:
    row = rows.split()
    index.append(row[0])
    label.append(row[1])

path = '../'
cloud = str(argv[1])

if label[0] == 'GPP':
    catalog = path + cloud + '_YSOc_PASS_test_6D_GP_to_image_check.tbl'
elif label[0] == 'IR1':
    catalog = path + cloud + '_YSO_candidates.tbl'
elif label[0] == 'SAT':
    catalog = path + cloud + '_saturate_candidates.tbl'
else:
    print('catalog label not found')

with open(catalog, 'r') as cat:
    catalog = cat.readlines()
    select_list = [catalog[int(i)-1] for i in index]

with open(label[0] + '_image_check_list_table.tbl', 'w') as out:
    for select in select_list:
        out.write(select)
