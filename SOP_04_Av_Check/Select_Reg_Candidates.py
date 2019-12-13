#!/usr/bin/ipython

'''
------------------------------------------------------------------------------------

---------------------------------------------------------------------------------------
latest update : 2019/07/31 Jordan Wu'''

import numpy as np
from sys import argv, exit
from os import system
from os.path import isfile

if len(argv) != 4:
    exit('\n\tError: Wrong Arguments\
    \n\tExample: [Program] [Input filename] [Reg filename / Index string] [Output filename]\
    \n\t[Reg filename]: file that stores information to pick up candidates\
    \n\t[Index string]: string that stores Indice of slicing objects (separated with \',\')')
else:
    print('Start Selecting ...')

catalog = str(argv[1])
reg_file = str(argv[2])
out_file = str(argv[3])

if isfile(reg_file):
    reg_list = [int(reg) for reg in np.loadtxt(reg_file)]
    print('register ID list: ', reg_list)
else:
    reg_list = reg_file.split(',')
    print('register ID list: ', reg_list)

NR_string = ''
for index in reg_list:
    if index != reg_list[-1]:
        NR_string += 'NR==' + str(index) + '||'
    else:
        NR_string += 'NR==' + str(index)
system('awk \'' + NR_string + '\' ' + catalog + ' > ' + out_file)
