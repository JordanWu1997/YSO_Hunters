#!/usr/bin/ipython
'''-------------------------------------------------------------------------------------



---------------------------------------------------------------------------------------
latest update : 2019/10/19 Jordan Wu'''

from sys import argv, exit
import numpy as np
import os

if len(argv) != 5:
    exit('\n\tExample: [program] [start] [end] [option] [make_check_list]\
        \n\t[option]: IR1/All\
        \n\t[make_check_list]: True/False\n')

start = int(argv[1])
end   = int(argv[2])
option = str(argv[3]).capitalize()

unsort_dirs = [name for name in os.listdir(".") if os.path.isdir(name)]
unsort_index = [int(name[:3]) for name in os.listdir(".") if os.path.isdir(name)]

all_dirs = []
for i in range(len(unsort_dirs)):
    all_dirs.append(unsort_dirs[unsort_index.index(i+1)])
inp_dirs = all_dirs[start-1:end]

Band = ['IR1', 'IR2', 'IR3', 'IR4', 'MP1']
Qua_Order = ['U', 'K', 'A', 'B', 'C', 'D', 'E' ,'F']

file_list = []
check_band = []
for dirs in inp_dirs:

    index, Qua, Imtype = dirs.split('_')
    Ind_list = index
    Qua_list = [Qua_Order.index(qua) for qua in Qua.split(',')]
    Im_list = [999 if int(im) == -2 else int(im) for im in Imtype.split(',')]

    if option == 'All':
        if Im_list == [1] * len(Band):
            band = Band[Qua_list.index(max(Qua_list))]
            name = band + '_' + Ind_list + '.fits'
        else:
            where_max_Im = np.where(np.array(Im_list) == max(Im_list))[0]
            if len(where_max_Im) == 1 and Qua_list[where_max_Im[0]] != 'U':
                band = Band[Im_list.index(max(Im_list))]
                name = band + '_' + Ind_list + '.fits'
            else:
                qua_list = Qua_list[where_max_Im[0]:where_max_Im[-1]+1]
                band = Band[Qua_list.index(max(qua_list))]
                name = band + '_' + Ind_list + '.fits'

    elif option == 'IR1':
        band = Band[0]
        name = band + '_' + Ind_list + '.fits'

    file_list.append(dirs + '/' + name)
    check_band.append(band)

def fill_zeros(num):
    if num < 10:
        out = '00' + str(num)
    elif num < '100':
        out =  '0' + str(num)
    elif num < '1000':
        out = str(num)
    return out

image_name = 'FROM_' + fill_zeros(start) + '_TO_' + fill_zeros(end) + '.png'
os.system("ds9 -zscale -wcs skyformat degree -crosshair 51 51 physical -zoom 2 " + (' ').join(file_list) + " -saveimage " + image_name + " &")

#=================================================================
# Interactive check list making procedures
#=================================================================
Make_Check_list = str(argv[4]).capitalize()
if Make_Check_list == 'True':

    print("\nStart making checklist ...")
    print("option: [GPP, IR1, SAT]")
    check_option = raw_input("Image Check Option: ").upper()

    rows = []
    for i in range(start, end+1):
        print('\n' + fill_zeros(i))

        sure = 'no'
        while sure != 'yes':
            number  = fill_zeros(i)
            label   = str(check_option)
            band    = str(check_band[i-start])
            comment = raw_input("Comment: ").upper()
            result  = raw_input("YSO: (Y/G) ").upper()
            sure    = raw_input("Are you sure? [Default: Yes)] ") or "yes"
            rows.append('\t'.join([number, label, band, comment, result]) + '\n')

    with open(check_option + '_image_check_list.tbl', 'a+') as out:
        for row in rows:
            out.write(row)
else:
    print("\nEnd of Image Check ...\n")
