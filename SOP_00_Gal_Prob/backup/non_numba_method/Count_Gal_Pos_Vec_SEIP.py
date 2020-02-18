#!/usr/bin/python
from __future__ import print_function
import time
import numpy as np
from sys import argv, exit
from os import chdir, system, path
from Hsieh_Functions import *

if len(argv) != 5:
    exit('\n\tError: Wrong Arguments\
    \n\tExample: [program] [input catalog] [mag/flux] [dimension] [cube size]\
    \n\t[input catalog]: must include magnitudes\
    \n\t[mag/flux]: input data in magnitude or flux (mJy)\
    \n\t[dimension]: dim of magnitude space (for now only "6")\
    \n\t[cube size]: length of multi-d cube in magnitude unit\n')

#======================================================
# Set parameters
inpcat   = str(argv[1])
datatype = str(argv[2])
dim      = int(argv[3])
cube     = float(argv[4])
print('cube = ' + str(cube))

# J, K, IR1, IR2, IR3, IR4, MP1
flux_ID = [0, 3, 4, 5, 6, 7]
mag_ID  = [0, 3, 4, 5, 6, 7]

# Use Limit Stored in Hsieh_Functions
Jaxlim   = Hsieh_Jaxlim
Ksaxlim  = Hsieh_Ksaxlim
IR1axlim = Hsieh_IR1axlim
IR2axlim = Hsieh_IR2axlim
IR3axlim = Hsieh_IR3axlim
IR4axlim = Hsieh_IR4axlim
MP1axlim = Hsieh_MP1axlim

# For now, only 6 band
axlim_list = [Jaxlim, IR1axlim, IR2axlim, IR3axlim, IR4axlim, MP1axlim]

# Count shape of each dim
binsa = int(round((  Jaxlim[1] -   Jaxlim[0]) / cube)) + 1
binsb = int(round(( Ksaxlim[1] -  Ksaxlim[0]) / cube)) + 1
bins1 = int(round((IR1axlim[1] - IR1axlim[0]) / cube)) + 1
bins2 = int(round((IR2axlim[1] - IR2axlim[0]) / cube)) + 1
bins3 = int(round((IR3axlim[1] - IR3axlim[0]) / cube)) + 1
bins4 = int(round((IR4axlim[1] - IR4axlim[0]) / cube)) + 1
bins5 = int(round((MP1axlim[1] - MP1axlim[0]) / cube)) + 1
print(binsa, binsb, bins1, bins2, bins3, bins4, bins5)

#======================================================
# Check Directory
if path.isdir('GPV_' + str(dim) + 'Dposvec_bin' + str(cube)):
    exit('\nDirectory has been established ... \
        \nPass to next procedure ...\n')
else:
    system('mkdir GPV_' + str(dim) + 'Dposvec_bin' + str(cube))

#======================================================
# Load Galaxy Catalog
print("\ngalaxy position...")
with open(str(argv[1]), 'r') as catalogs:
    catalog = catalogs.readlines()

#======================================================
# Calculate Galaxy Position Vector
c_start = time.time()
bright, pos_vec = [], []
for i in range(len(catalog)):
    #======================================================
    # Percentage Indicator
    if i%100==0:
        print(str(float(i)/len(catalog)*100) + '%')
    #======================================================
    line = catalog[i]
    lines = line.split()
    if datatype == 'flux':
        mag_list = mJy_to_mag(lines, flux_ID=flux_ID, Qua=False, system="ukidss")
    elif datatype == 'mag':
        mag_list = mag_to_mag(lines, mag_ID=mag_ID, Qua=False, system="ukidss")
    else:
        print('Input type error')
    magJ, magIR1, magIR2, magIR3, magIR4, magMP1 = mag_list

    #======================================================
    # Remove AGB sources (NOT considered in SEIP catalog)
    #AGB = 0
    #if magIR2 != 'no' and magIR3 != 'no' and magMP1 != 'no':
    #    X23 = magIR2 - magIR3
    #    Y35 = magIR3 - magMP1
    #    if index_AGB(X23, Y35, [0,0,2,5], [-1,0,2,2]) < 0:
    #        AGB = 1
    #if AGB != 1:
    #    SEQ = [sort_up(mag_list[i], axlim_list[i], cube) for i in range(len(axlim_list))]
    #    pos_vec.append(SEQ)
    #======================================================

    SEQ = [sort_up_lack999(mag_list[i], axlim_list[i], cube) for i in range(len(axlim_list))]
    pos_vec.append(SEQ)
#======================================================
# Galaxy filter
bright, faint = [], []
new_pos_vec = dict()
for i, pos in enumerate(pos_vec):
    print(float(i)/len(pos_vec))
    # Filiter out Bright/Faint Sources
    if pos.count("Bright") > 0:
        bright.append(pos)
    elif pos.count("Faint") > 0:
        faint.append(pos)
    # Calculate the number of objects in same position
    else:
        if tuple(pos) in new_pos_vec.keys():
            new_pos_vec[tuple(pos)] += 1
        else:
            new_pos_vec[tuple(pos)] = 1
c_end   = time.time()
print("Calculating Galaxy Position took {:.3f} secs\n".format(c_end-c_start))
#======================================================
# Save Galaxy Position Vector, Bright, Faint
s_start = time.time()
chdir('GPV_' + str(dim) + 'Dposvec_bin' + str(cube))
np.save('Gal_Position_vectors', new_pos_vec)
np.save('Bright', bright)
np.save('Faint',  faint)
np.save('Shape',  np.array([binsa, bins1, bins2, bins3, bins4, bins5]))
chdir('../')
s_end   = time.time()
print("Saving Galaxy Position took {:.3f} secs\n".format(c_end-c_start))
