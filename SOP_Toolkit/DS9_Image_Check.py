#!/bin/usr/ipython
'''-------------------------------------------------------------------------------------



---------------------------------------------------------------------------------------
latest update : 2019/10/19 Jordan Wu'''

from sys import argv, exit
import numpy as np
import os

if len(argv) != 3:
    exit('\n\tExample: [program] [start] [end]\n')

start = int(argv[1])
end   = int(argv[2])

unsort_dirs = [name for name in os.listdir(".") if os.path.isdir(name)]
unsort_index = [int(name[:3]) for name in os.listdir(".") if os.path.isdir(name)]

all_dirs = []
for i in range(len(unsort_dirs)):
    all_dirs.append(unsort_dirs[unsort_index.index(i+1)])
inp_dirs = all_dirs[start-1:end]

Band = ['IR1', 'IR2', 'IR3', 'IR4', 'MP1']
Qua_Order = ['K', 'A', 'B', 'C', 'D', 'E' ,'F']

file_list = []
for dirs in inp_dirs:
    index, Qua, Imtype = dirs.split('_')
    
    Ind_list = index
    Qua_list = [Qua_Order.index(qua) for qua in Qua.split(',')]
    
    Im_list  = []
    for im in Imtype.split(','):
        if int(im) == -2:
            Im_list.append(999)
        else:
            Im_list.append(int(im))

    if Im_list == [1] * len(Band):
        name = Band[Qua_list.index(max(Qua_list))] + '_' + Ind_list + 'fits'
    else:
        max_Im_list = np.argwhere(np.array(Im_list) == max(Im_list))[0]
        if len(max_Im_list) == 1:
            name = Band[Im_list.index(max(Im_list))] + '_' + Ind_list + 'fits'
        else:
            qua_list = Qua_list[max_Im_list[0]:max_Im_list[-1]+1]
            name = Band[Qua_list.index(max(qua_list))] + '_' + Ind_list + 'fits'

    file_list.append(dirs + '/' + name)

def fill_zeros(num):
    if num < 10:
        out = '00' + str(num)
    elif num < '100':
        out =  '0' + str(num)
    elif num < '1000':
        out = str(num)
    return out

image_name = fill_zeros(start) + '_TO_' + fill_zeros(end) + '.png'
os.system("ds9 -zscale -crosshair 51 51 physical -zoom 2 " + (' ').join(file_list) + " -saveimage " + image_name)
