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

# Load Data
path_lower      = '/mazu/users/jordan/YSO_Project/SEIP_GP_Bound/Test_BD/GPV_after_smooth_6D_bin1.0_sigma2_bond3_refD5/after_smooth_lack_0_012345_6D_lower_bounds_AlB0.npy'
path_upper      = '/mazu/users/jordan/YSO_Project/SEIP_GP_Bound/Test_BD/GPV_after_smooth_6D_bin1.0_sigma2_bond3_refD5/after_smooth_lack_0_012345_6D_upper_bounds_AlB0.npy'
path_galaxy_YSO = '/mazu/users/jordan/YSO_Project/SEIP_GP_Bound/Test_BD/Cloud_Classification_GPM_BD/6D_bin1.0_sigma2_bond3_refD5/PER/AND_PER_Galaxy_all_Hsieh_YSOc.tbl'
path_YSO_YSO    = '/mazu/users/jordan/YSO_Project/SEIP_GP_Bound/Test_BD/Cloud_Classification_GPM_BD/6D_bin1.0_sigma2_bond3_refD5/PER/AND_PER_YSO_all_Hsieh_YSOc.tbl'
path_galaxy_galaxy = '/mazu/users/jordan/YSO_Project/SEIP_GP_Bound/Test_BD/Cloud_Classification_GPM_BD/6D_bin1.0_sigma2_bond3_refD5/PER/DIFF_PER_Galaxy.tbl'
path_after_smooth_6 = '/mazu/users/jordan/YSO_Project/SEIP_GP_Bound/Test_BD/GPV_after_smooth_6D_bin1.0_sigma2_bond3_refD5/after_smooth_lack_0_012345_all_cas_pos.npy'
path_num = '/mazu/users/jordan/YSO_Project/SEIP_GP_Bound/Test_BD/GPV_after_smooth_6D_bin1.0_sigma2_bond3_refD5/after_smooth_lack_0_012345_all_cas_num.npy'
path_bin_num = '/mazu/users/jordan/YSO_Project/SEIP_GP_Bound/GPV_6Dposvec_bin1.0/Lack_pos_num/Lack_000_num.npy'
path_bin_pos = '/mazu/users/jordan/YSO_Project/SEIP_GP_Bound/GPV_6Dposvec_bin1.0/Lack_pos_num/Lack_000_pos.npy'


lower       = np.load(path_lower)
upper       = np.load(path_upper)
lower_limit = np.array([4., 8.0, 7.0, 5.0, 5.0, 3.5])
upper_limit = np.array([18., 18., 18., 18., 18. , 11.])
bound       = np.r_[upper, lower]
bound       = np.array([bound[i] + lower_limit for i in range(len(bound))])
pos         = np.load(path_after_smooth_6)
num         = np.load(path_num)
bin_pos     = np.load(path_bin_pos)
bin_num     = np.load(path_bin_num)
AS6         = pos[np.where(num>=1)]
bi          = bin_pos[np.where(bin_num>=1)]
AS6         = np.array([AS6[i] + lower_limit for i in range(len(AS6))])
bi          = np.array([bi[i] + lower_limit for i in range(len(bi))])

GY = process_table(path_galaxy_YSO)
YY = process_table(path_YSO_YSO)
GG = process_table(path_galaxy_galaxy)
b1 = 0 ; b2 = 2 ; b3 = 4
band = ['J', 'IR1', 'IR2','IR3', 'IR4', 'MP1']

print('\n\tNumber of YSO_YSO : {}\n'.format(len(YY)))
print('\n\tNumber of galaxy_YSO : {}\n'.format(len(GY)))
print('\n\tNumber of galaxy_galaxy : {}\n'.format(len(GG)))

# Diagram
fig = plt.figure()
axis = fig.gca(projection='3d')

axis.scatter(bound[:, b1], bound[:, b2], bound[:, b3],label = 'galaxy region' , c = 'b', alpha = 0.5)
axis.scatter(GY[:, b1], GY[:, b2], GY[:, b3], label = 'galaxy_YSO', c = 'r')
#axis.scatter(AS6[:, b1], AS6[:, b2], AS6[:, b3], label = 'YSO_YSO', c = 'g')
print(np.shape(GG[np.where(GG[:, b1] < upper_limit[b1])]))
axis.scatter(GG[np.where(GG[:, 5] < upper_limit[5])], GG[np.where(GG[:, b2] < upper_limit[b2])], GG[np.where(GG[:, b3] < upper_limit[b3])], label = 'galaxy_galaxy', c = 'm')
#axis.scatter(bi[:, b1], bi[:, b2], bi[:, b3], label = 'galaxy_galaxy', c = 'r')

axis.legend()
axis.set_zlabel(band[b3], fontsize=16)
axis.set_xlabel(band[b1], fontsize=16)
axis.set_ylabel(band[b2], fontsize=16)


plt.show()


