#! /home/jeremy/anaconda3/bin/python

import numpy as np
from sys import argv, exit
from tqdm import tqdm, trange

if len(argv) != 4 :
    exit('\n\t Error Argument : \
            \n\t Example : [program] [boundary_path] [YSO_path] [bin_size]\
            \n ')


def process_table(path) :
    output  = []
    table   = open(path, 'r').readlines()
    for line in table :
        output.append([float(line.split()[a]) for a in [35, 98, 119, 140, 161, 182]])
    output  = np.array(output)
    return output

def check_pos(obj, bound) :
    YSO_type = []
    for axis in range(6) :
        band = ['J', 'IR1', 'IR2', 'IR3', 'IR4', 'MP1']
        print('\n\tStart '+band[axis]+' band\n')
        for point in tqdm(obj) :
            ax = np.delete(point, axis)
            for BD in bound :
                limit = []
                b = np.delete(BD, axis)
                print(ax, b)
                if np.all(ax, b) == True :
                    limit.append(BD)

            if len(limit) == 2 :
                if limit[0][ax] > limit[1][ax] :
                    up = limit[0][ax] 
                    low = limit[1][ax]
                elif limit[0][ax] == limit[1][ax] :
                    up = limit[0][ax]
                    low = up
                else :
                    up = limit[1][ax]
                    low = limit[0][ax]
            else :
                YSO_type.append('nonBD')

            if point[ax] > up :
                YSO_type.append('U')
            elif point[ax] < up and point[ax] > low :
                YSO_type.append('L')
            else :
                YSO_type.append('M')
    return YSO_type

path_lower      = argv[1] + '/after_smooth_lack_0_012345_6D_lower_bounds_AlB0.npy'
path_upper      = argv[1] + '/after_smooth_lack_0_012345_6D_upper_bounds_AlB0.npy'
lower       = np.load(path_lower)
upper       = np.load(path_upper)
lower_limit = np.array([4., 8.0, 7.0, 5.0, 5.0, 3.5])
upper_limit = np.array([18., 18., 18., 18., 18. , 11.])
bound       = np.r_[upper, lower]
boundary    = lower_limit + float(argv[3]) * np.array([bound[i]  for i in range(len(bound))])
#YSO = process_table(argv[2])

fin = check_pos(YSO, boundary)

np.save('test_YSO_type', fin)



