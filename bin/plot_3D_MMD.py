#!/home/jeremy/anaconda3/bin/python

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

def process_table(path) :
    output  = []
    table   = open(path, 'r').readlines()
    for line in table :
        output.append([float(line.split()[a]) for a in [35, 98, 119, 140, 161, 182]])
    output  = np.array(output)
    return output

path_lower      = '/mazu/users/jordan/YSO_Project/SEIP_GP_Bound/Test_BD/GPV_after_smooth_6D_bin1.0_sigma2_bond3_refD5/after_smooth_lack_0_012345_6D_lower_bounds_AlB0.npy'
path_upper      = '/mazu/users/jordan/YSO_Project/SEIP_GP_Bound/Test_BD/GPV_after_smooth_6D_bin1.0_sigma2_bond3_refD5/after_smooth_lack_0_012345_6D_upper_bounds_AlB0.npy'
path_galaxy_YSO = '/mazu/users/jordan/YSO_Project/SEIP_GP_Bound/Test_BD/Cloud_Classification_GPM_BD/6D_bin1.0_sigma2_bond3_refD5/PER/AND_PER_Galaxy_all_Hsieh_YSOc.tbl'
path_YSO_YSO    = '/mazu/users/jordan/YSO_Project/SEIP_GP_Bound/Test_BD/Cloud_Classification_GPM_BD/6D_bin1.0_sigma2_bond3_refD5/PER/AND_PER_YSO_all_Hsieh_YSOc.tbl'
path_galaxy_galaxy = '/mazu/users/jordan/YSO_Project/SEIP_GP_Bound/Test_BD/Cloud_Classification_GPM_BD/6D_bin1.0_sigma2_bond3_refD5/PER/DIFF_PER_Galaxy.tbl'

lower           = np.load(path_lower)
upper           = np.load(path_upper)
orig            = np.array([3.5, 8.0, 7.0, 5.0, 5.0, 3.5])
#orig            = np.array([4., 8., 7., 5., 5., 3.5]) # Hseih X lower limit
bound           = np.r_[upper, lower]
bound           = np.array([bound[i] + orig for i in range(len(upper))])

GY = process_table(path_galaxy_YSO)
YY = process_table(path_YSO_YSO)
GG = process_table(path_galaxy_galaxy)
b1 = 3 ; b2 = 4 ; b3 = 6 
band = ['J', 'IR1', 'IR2', 'IR4', 'MP1', 'MP2']

fig = plt.figure()
axis = fig.gca(projection='3d')
print('\n\tNumber of galaxy_YSO : {}'.format(len(GY)))
print('\n\tNUmber of YSO_YSO : {}'.format(len(YY)))
print('\n\tNumber of YSO_galaxy : {}\n'.format(len(GG)))

axis.scatter(bound[:, b1-1], bound[:, b2-1], bound[:, b3-1],label = 'galaxy region' , c = 'b')
axis.scatter(GY[:, b1-1], GY[:, b2-1], GY[:, b3-1], label = 'galaxy_YSO', c = 'r')
#axis.scatter(YY[:, b1-1], YY[:, b2-1], YY[:, b3-1], label = 'YSO_YSO', c = 'g')
#axis.scatter(GG[:, b1-1], GG[:, b2-1], GG[:, b3-1], label = 'galaxy_galaxy', c = 'm')

axis.legend()
plt.title(band[b1-1], fontsize=16)
plt.xlabel(band[b2-1], fontsize=16)
plt.ylabel(band[b3-1], fontsize=16)

plt.show()

