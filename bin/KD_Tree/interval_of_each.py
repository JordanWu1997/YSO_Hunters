#!/usr/bin/python

from sklearn.neighbors import KDTree
import numpy as np
import matplotlib.pyplot as plt
import pickle
from time import sleep
from tqdm import tqdm, trange
from sys import argv , exit
import time 

#path = '/mazu/users/jordan/YSO_Project/SEIP_GP_Bound/GPV_6Dposvec_bin1.0/Lack_pos_num/Lack_000_pos.npy'


if len(argv) != 3:
    exit('\n\t Error Argument : \
            \n\t Example : [program] [catalog] [output name]\
            \n ')

def interval(cat_arr, name) :
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
    ind, dist = tree_copy.query_radius(cat_arr, r = 1.5, return_distance=True)
    print('Finish to load the data\n')
    tEnd = time.time()
    print("It cost %f sec\n" % (tEnd - tStart))
    print(dist)
    print(ind)
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

cat = np.load(argv[1])
interval(cat, argv[2]) 
