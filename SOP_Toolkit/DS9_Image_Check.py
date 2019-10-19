#!/usr/bin/ipython
'''-------------------------------------------------------------------------------------



---------------------------------------------------------------------------------------
latest update : 2019/10/19 Jordan Wu'''

from sys import argv, exit
import numpy as np
import os

if len(argv) != 4:
    exit('\n\tExample: [program] [start] [end] [option]\
        \n\t[option]: IR1 , All\n')

start = int(argv[1])
end   = int(argv[2])
option = str(argv[3])

unsort_dirs = [name for name in os.listdir(".") if os.path.isdir(name)]
unsort_index = [int(name[:3]) for name in os.listdir(".") if os.path.isdir(name)]

all_dirs = []
for i in range(len(unsort_dirs)):
    all_dirs.append(unsort_dirs[unsort_index.index(i+1)])
inp_dirs = all_dirs[start-1:end]

Band = ['IR1', 'IR2', 'IR3', 'IR4', 'MP1']
Qua_Order = ['U', 'K', 'A', 'B', 'C', 'D', 'E' ,'F']

file_list = []
for dirs in inp_dirs:
    
    index, Qua, Imtype = dirs.split('_')
    Ind_list = index
    Qua_list = [Qua_Order.index(qua) for qua in Qua.split(',')]
    Im_list = [999 if int(im) == -2 else int(im) for im in Imtype.split(',')]

    if option == 'All':
        if Im_list == [1] * len(Band):
            name = Band[Qua_list.index(max(Qua_list))] + '_' + Ind_list + '.fits'
        else:
            where_max_Im = np.where(np.array(Im_list) == max(Im_list))[0]
            if len(where_max_Im) == 1 and Qua_list[where_max_Im[0]] != 'U':
                name = Band[Im_list.index(max(Im_list))] + '_' + Ind_list + '.fits'
            else:
                qua_list = Qua_list[where_max_Im[0]:where_max_Im[-1]+1]
                name = Band[Qua_list.index(max(qua_list))] + '_' + Ind_list + '.fits'
    
    elif option == 'IR1':
        name = Band[0] + '_' + Ind_list + '.fits'

    file_list.append(dirs + '/' + name)

def fill_zeros(num):
    if num < 10:
        out = '00' + str(num)
    elif num < '100':
        out =  '0' + str(num)
    elif num < '1000':
        out = str(num)
    return out

image_name = 'FROM_' + fill_zeros(start) + '_TO_' + fill_zeros(end) + '.png'
os.system("ds9 -zscale -wcs skyformat degree -crosshair 51 51 physical -zoom 2 " + (' ').join(file_list) + " -saveimage " + image_name)
