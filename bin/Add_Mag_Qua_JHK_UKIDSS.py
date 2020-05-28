#!/usr/bin/python
'''
This program is to replace qua label in catalogs
'''

from __future__ import print_function
import time
import numpy as np
from sys import argv, exit
from os import system
from Useful_Functions import *

if len(argv) != 3:
    exit('\n\tWrong Input Argument!\
            \n\tExample: python [program] [input table] [output file name]')

# For now it's J, H, K
qua_list = [37, 58, 79]
catalog = str(argv[1])
output_name = str(argv[2])

print('\nReplacing ...')
with open(catalog, 'r') as cat:
    data = cat.readlines()

t_start = time.time()
out_catalog = []
for i in range(len(data)):
    row = data[i].split()
    for qua_id in qua_list:
        if row[qua_id] == 'N':
            row[qua_id] = 'A_fake'
    new_row = '\t'.join(row) + '\n'
    out_catalog.append(new_row)
    drawProgressBar(float(i+1)/len(data))
t_end   = time.time()
print('\nReplace Qua label took {:.3f} secs'.format(t_end-t_start))

with open(output_name, 'w') as out:
    for row in out_catalog:
        out.write(row)
system('wc ' + output_name)
