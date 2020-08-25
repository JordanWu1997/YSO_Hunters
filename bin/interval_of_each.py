#!/home/jeremy/anaconda3/bin/python

from sklearn.neighbors import KDTree
import numpy as np
import matplotlib.pyplot as plt
import pickle
from time import sleep
from tqdm import tqdm, trange
from sys import argv , exit
import time 

#path = '/mazu/users/jordan/YSO_Project/SEIP_GP_Bound/GPV_6Dposvec_bin1.0/Lack_pos_num/Lack_000_pos.npy'

'''
if len(argv) != 4:
    exit('\n\t Error Argument : \
            \n\t Example : [program] [catalog] [bin_size] [name]\
            \n ')
'''
def interval(path, name) :
    cat_arr = np.load(path)
    print('\nStart finding intervals for '+name+' \n')
    tStart = time.time()
    time.sleep(2)
    tree = KDTree(cat_arr, leaf_size=2)
    s = pickle.dumps(tree)
    tree_copy = pickle.loads(s)
    tEnd = time.time()
    print('KD tree is finish\n')
    print("It cost %f sec\n" % (tEnd - tStart))
    print('Load distance and index\n')
    tStart = time.time()
    time.sleep(2)
    dist, ind = tree_copy.query(cat_arr, k=len(cat_arr))
    print('Finish to load the data\n')
    tEnd = time.time()
    print("It cost %f sec\n" % (tEnd - tStart))

    print("Start to re-arrange the array\n")
    fin = []
    for i in tqdm(range(len(cat_arr))) :
        point = []
        for j in range(len(ind[i]) - 1) :
            point.append([ind[i][0], ind[i][j+1], dist[i][j+1]])
        fin.append(point)
    fin = np.array(fin)
    #print(fin)
    np.save(name, fin)
    #np.save('catalog_of_interval_bin{}'.format(argv[2]), fin)
l = []
n = 3
for i in range(6) :
    for j in range(6) :
        for k in range(6) :
            if i < j and j < k :
                l.append(str(i) + str(j) + str(k))
interval('/mazu/users/jordan/YSO_Project/SEIP_GP_Bound/GPV_6Dposvec_bin0.2/Lack_pos_num/Lack_000_pos.npy', 'intervals_bin0.2_lack_0.npy') 
#for line in l :
#    interval('/home/jeremy/intervals_length/catalog/band_lack_3/bin0.5/band_bin0.5_'+line+'.npy', 'intervals_bin0.5_lack_3_'+ line +'.npy')
#    interval('/mazu/users/jordan/YSO_Project/SEIP_GP_Bound/GPV_6Dposvec_bin1.0/Band_pos_num/Lack_3_'+ line +'_pos.npy','intervals_Lack_3_'+ line +'_pos.npy') 
