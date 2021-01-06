#!/usr/bin/env python
from sys import argv, exit
import matplotlib.pyplot as plt
from tqdm import tqdm, trange
import numpy as np
'''
if len(argv) != 4 :
    exit('\t\n Error Argument : \
            \t\n [program] [catalog] [radius] [hist_slice_number(15)]\
            \n ')

cat = np.load(argv[1])
radius = float(argv[2])
ind = []
'''
def occupied(path, radius) :
    cat = np.load(path)
    ind = []
    # Find the point which length between the target point is lower than redius
    print('\nStart to identify the point')
    for point in tqdm(cat) :
        hist = 0
        for i in range(len(point)) :
            if point[i][2] <= radius :
                hist += 1
        ind.append([point[i][0], hist])
    ind = np.array(ind)
    #np.save('bin0.2', ind)
    #print(ind)
    # Calculate the full number in radius
    print('\nStart to calculate the full number of the points in the range for each target\n' )
    full = 12
    print('There are {} points inside the range\n'.format(full))

    # Histogram
    print('========================================================\n')
    print('Histogram\n')
    fig = plt.figure()
    bins = np.linspace(0, full+0.5, num = float(25) + 1)
    print(bins)
    #bins = np.linspace(int(np.min(ind[:, 1])), int(np.max(ind[:, 1])), num = float(argv[3]) + 1)
    print('\n Total number of compact points : {}\n'.format(int(len(ind[:, 1]))))
    hist, b = np.histogram(ind[:, 1], bins)
    plt.hist(ind[:, 1], bins = bins)
    new_ticks = np.linspace(0, np.max(hist), num = float(5) + 1)
    new_y = []
    for y in new_ticks :
        new_y.append('{:.0%}'.format(y/len(ind[:, 1])))
    #name = 'hist_occupied_bin1.0_lack_3_'+ path[-7:-4] + '.png'
    name = 'hist_occupied_bin0.2_lack_0'
    fig.savefig(name+'_num.png')
    plt.yticks(new_ticks, new_y)
    fig.savefig(name+'_percentage.png')
    #plt.show()

# main
'''
l = []
for i in range(6) :
    for j in range(6) :
        for k in range(6) :
            if i < j and j < k :
                l.append(str(i) + str(j) + str(k))
'''
#for line in l :
#    print('Run '+line)
#    occupied('/home/jeremy/intervals_length/catalog/total_intervals/intervals_lack_3/bin1.0/intervals_bin1.0_lack_3_'+line+'.npy', 1)
occupied('/home/jeremy/intervals_length/catalog/total_intervals/intervals_lack_0/intervals_bin0.2_lack_0.npy', 1)

