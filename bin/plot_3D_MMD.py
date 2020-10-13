#!/usr/bin/python
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from itertools import combinations
from os import system, chdir, path
from All_Variables import *

def process_table(path):
    '''
    This is to get 6D magnitude from input table
    '''
    output = []
    with open(path, 'r') as table:
        for line in table.readlines():
            output.append([float(line.split()[a]) for a in mag_ID_6D])
    output = np.array(output)
    return output

# Load Data
path_GD_num = './after_smooth_lack_0_012345_all_cas_num.npy'
path_GD_pos = './after_smooth_lack_0_012345_all_cas_pos.npy'
path_lower  = './after_smooth_lack_0_012345_6D_lower_bounds_AlB0.npy'
path_upper  = './after_smooth_lack_0_012345_6D_upper_bounds_AlB0.npy'
path_new_YSO = './all_new_YSO.tbl'
path_new_LYSO = './all_new_LYSO.tbl'
path_new_UYSO = './all_new_UYSO.tbl'
path_new_NULYSO = './all_new_NULYSO.tbl'
path_YSO_YSO = './all_YSO_and_Hsieh.tbl'
path_galaxy_YSO = 'all_YSO_not_Hsieh.tbl'
path_5D_GD_num = './after_smooth_lack_0_012345_all_cas_num.npy' # C2D
path_5D_GD_pos = './after_smooth_lack_0_012345_all_cas_pos.npy' # C2D

lower       = np.load(path_lower)
upper       = np.load(path_upper)
lower_limit = np.array([4., 8., 7., 5., 5., 3.5])
upper_limit = np.array([18., 18., 18., 18., 18. , 11.])
bound       = np.r_[upper, lower]
bound       = np.array([bound[i] + lower_limit for i in range(len(bound))])

GD_num      = np.load(path_GD_num)
GD_pos      = np.load(path_GD_pos)[GD_num >= 1.]
GD_pos      = np.array([GD_pos[i] + lower_limit for i in range(len(GD_pos))])

GD_num_5D   = np.load(path_5D_GD_num)
GD_pos_5D   = np.load(path_5D_GD_pos)[GD_num_5D >= 1.]
GD_pos_5D   = np.array([GD_pos_5D[i] + lower_limit for i in range(len(GD_pos_5D))])

NY    = process_table(path_new_YSO)
NLY   = process_table(path_new_LYSO)
NUY   = process_table(path_new_UYSO)
NNULY = process_table(path_new_NULYSO)
YY    = process_table(path_YSO_YSO)
GY    = process_table(path_galaxy_YSO)
print(len(NY), len(NLY), len(NUY), len(NNULY))
print(len(NY), len(YY), len(GY))

out_dir = '3D_MMD'
if not path.isdir(out_dir):
    system('mkdir {}'.format(out_dir))
chdir(out_dir)

band = ['J', 'IR1', 'IR2','IR3', 'IR4', 'MP1']
for comb in combinations([0, 1, 2, 3, 4, 5], 3):
    print(comb)
    b1, b2, b3 = tuple(comb)
    # b1 = 2 ; b2 = 4 ; b3 = 5
    fig = plt.figure()
    axis = fig.gca(projection='3d')
    axis.scatter(bound[:, b1], bound[:, b2], bound[:, b3],label='BD', c='b', alpha=0.5)
    axis.scatter(GD_pos[:, b1], GD_pos[:, b2], GD_pos[:,b3], label='GD', c='g', alpha=0.5)
    # axis.scatter(GD_pos_5D[:, b1], GD_pos_5D[:, b2], GD_pos_5D[:, b3], label='GD_5D', c='g', alpha=0.5)
    # axis.scatter(GY[:, b1], GY[:, b2], GY[:, b3], label='new_YSO', c='r', alpha=0.1)
    # axis.scatter(NLY[:, b1], NLY[:, b2], NLY[:, b3], label='new_YSO_LYSO', c='y', alpha=0.5)
    # axis.scatter(NUY[:, b1], NUY[:, b2], NUY[:, b3], label='new_YSO_UYSO', c='purple', alpha=0.5)
    # axis.scatter(NNULY[:, b1], NNULY[:, b2], NNULY[:, b3], label='new_YSO_NULYSO', c='cyan', alpha=0.5)
    axis.scatter(YY[:, b1], YY[:, b2], YY[:, b3], label='YSO_and_Hsieh_YSO', c='lime', alpha=0.5)
    axis.scatter(GY[:, b1], GY[:, b2], GY[:, b3], label='YSO_not_Hsieh_YSO', c='orange', alpha=0.5)
    axis.legend()
    axis.set_xlabel(band[b1], fontsize=16)
    axis.set_ylabel(band[b2], fontsize=16)
    axis.set_zlabel(band[b3], fontsize=16)
    plt.savefig('{:d}{:d}{:d}.png'.format(b1, b2, b3))
