#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
import math as math

def Get_Mean_Mid_Std(filename):
    hdul = fits.open(filename)
    image = hdul[0].data
    flat_image = image.flatten()
    flat_image = flat_image[np.invert(np.isnan(flat_image))]
    value = []
    for i in range(len(flat_image)):
        if not np.isnan(flat_image[i]):
            value.append(flat_image[i])
    mean = np.mean(value)
    med = np.median(value)
    std = np.std(value)
    return flat_image, mean, med, std

All_flat = []
fig, axe = plt.subplots(2,4,figsize=(16,8))

flat_image, mean, med, std = Get_Mean_Mid_Std('CHA_II_300asec_Av.fits')
axe[0,0].hist(flat_image, bins=np.arange(0, 21, 1))
axe[0,0].axvline(mean, c='k', ls='--', label='mean=%.2f'%mean)
axe[0,0].axvline(med , c='k', ls='-' , label='med =%.2f'%med)
axe[0,0].set_title('CHA_II_Av_Map; std=%.2f'%std)
axe[0,0].set_xticks(np.arange(0, 21, 2))
axe[0,0].legend()
All_flat += list(flat_image)

flat_image, mean, med, std = Get_Mean_Mid_Std('LUP_I_300asec_Av.fits')
axe[0,1].hist(flat_image, bins=np.arange(0, 21, 1))
axe[0,1].axvline(mean, c='k', ls='--', label='mean=%.2f'%mean)
axe[0,1].axvline(med , c='k', ls='-' , label='med =%.2f'%med)
axe[0,1].set_title('LUP_I_Av_Map; std=%.2f'%std)
axe[0,1].set_xticks(np.arange(0, 21, 2))
axe[0,1].legend()
All_flat += list(flat_image)

flat_image, mean, med, std = Get_Mean_Mid_Std('LUP_III_300asec_Av.fits')
axe[1,0].hist(flat_image, bins=np.arange(0, 21, 1))
axe[1,0].axvline(mean, c='k', ls='--', label='mean=%.2f'%mean)
axe[1,0].axvline(med , c='k', ls='-' , label='med =%.2f'%med)
axe[1,0].set_title('LUP_III_Av_Map; std=%.2f'%std)
axe[1,0].set_xticks(np.arange(0, 21, 2))
axe[1,0].legend()
All_flat += list(flat_image)

flat_image, mean, med, std = Get_Mean_Mid_Std('LUP_IV_300asec_Av.fits')
axe[1,1].hist(flat_image, bins=np.arange(0, 21, 1))
axe[1,1].axvline(mean, c='k', ls='--', label='mean=%.2f'%mean)
axe[1,1].axvline(med , c='k', ls='-' , label='med =%.2f'%med)
axe[1,1].set_title('LUP_IV_Av_Map; std=%.2f'%std)
axe[1,1].set_xticks(np.arange(0, 21, 2))
axe[1,1].legend()
All_flat += list(flat_image)

flat_image, mean, med, std = Get_Mean_Mid_Std('OPH_300asec_Av.fits')
axe[0,2].hist(flat_image, bins=np.arange(0, 21, 1))
axe[0,2].axvline(mean, c='k', ls='--', label='mean=%.2f'%mean)
axe[0,2].axvline(med , c='k', ls='-' , label='med =%.2f'%med)
axe[0,2].set_title('OPH_Av_Map; std=%.2f'%std)
axe[0,2].set_xticks(np.arange(0, 21, 2))
axe[0,2].legend()
All_flat += list(flat_image)

flat_image, mean, med, std = Get_Mean_Mid_Std('PER_300asec_Av.fits')
axe[1,2].hist(flat_image, bins=np.arange(0, 21, 1))
axe[1,2].axvline(mean, c='k', ls='--', label='mean=%.2f'%mean)
axe[1,2].axvline(med , c='k', ls='-' , label='med =%.2f'%med)
axe[1,2].set_title('PER_Av_Map; std=%.2f'%std)
axe[1,2].set_xticks(np.arange(0, 21, 2))
axe[1,2].legend()
All_flat += list(flat_image)

flat_image, mean, med, std = Get_Mean_Mid_Std('SER_300asec_Av.fits')
axe[0,3].hist(flat_image, bins=np.arange(0, 21, 1))
axe[0,3].axvline(mean, c='k', ls='--', label='mean=%.2f'%mean)
axe[0,3].axvline(med , c='k', ls='-' , label='med =%.2f'%med)
axe[0,3].set_title('SER_Av_Map; std=%.2f'%std)
axe[0,3].set_xticks(np.arange(0, 21, 2))
axe[0,3].legend()
All_flat += list(flat_image)

All_flat = np.array(All_flat)
mean, med, std = np.mean(All_flat), np.median(All_flat), np.std(All_flat)
axe[1,3].hist(All_flat, bins=np.arange(0, 21, 1), color='orange')
axe[1,3].axvline(mean, c='k', ls='--', label='mean=%.2f'%mean)
axe[1,3].axvline(med , c='k', ls='-' , label='med =%.2f'%med)
axe[1,3].set_title('All_Av_Map; std=%.2f'%std)
axe[1,3].set_xticks(np.arange(0, 21, 2))
axe[1,3].legend()

plt.tight_layout()
plt.savefig('All_Mean_Av.png')
plt.show()
