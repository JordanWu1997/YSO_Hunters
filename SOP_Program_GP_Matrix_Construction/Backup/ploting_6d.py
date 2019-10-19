import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from os import system, chdir
###import data
sixd = np.load("./result0.2/all_detect_grid_Full_6d.npy").item()
###start choosing bands
bands = ['J', 'IR1', 'IR2', 'IR3', 'IR4', 'MP1']
system('mkdir 6d_plot_0.2')
chdir('6d_plot_0.2')
for band1 in range(6):
    for band2 in range(band1):
        z = np.zeros((100,100))
###Get datas
        for i in sixd.keys():
            inin = i.strip('( )')
            g = inin.split(',')
            z[int(g[band2])][int(g[band1])] += float(sixd[i])
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_xlabel(str(bands[band2]))
        ax.set_ylabel(str(bands[band1]))
        plt.imshow(z, vmin = np.mean(z), vmax = np.mean(z)+5*np.std(z))
        plt.colorbar()
        #plt.show()
        plt.savefig(str(bands[band2] + '-' + bands[band1]))
