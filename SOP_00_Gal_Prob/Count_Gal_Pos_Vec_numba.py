#!/usr/bin/python
from __future__ import print_function
import time
import numpy as np
from numba import jit
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
print('\ncube = ' + str(cube))

# J, K, IR1, IR2, IR3, IR4, MP1
print('flux_ID')
print(flux_ID)
print('mag_ID')
print(mag_ID)
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
print('Shape')
print(binsa, binsb, bins1, bins2, bins3, bins4, bins5)

# Check Directory
if path.isdir('GPV_' + str(dim) + 'Dposvec_bin' + str(cube)):
    #exit('\nDirectory has been established ... \
    #    \nPass to next procedure ...\n')
    system('rm -fr GPV_' + str(dim) + 'Dposvec_bin' + str(cube))
    system('mkdir GPV_' + str(dim) + 'Dposvec_bin' + str(cube))
else:
    system('mkdir GPV_' + str(dim) + 'Dposvec_bin' + str(cube))

#======================================================
# Main Functions
@jit(nopython=True)
def filter_bright_faint(pos_vec_array):
    '''
    This is to filter out bright, faint and sources we want
    '''
    bright = []
    faint  = []
    source = []
    for i in range(len(pos_vec_array)):
        #print(float(i)/len(pos_vec_array))
        pos_vec_array_sub = pos_vec_array[i]
    #================================================
    # Filiter out Bright/Faint Sources
        if np.any(np.where(pos_vec_array_sub == -9999)):
            bright.append(pos_vec_array_sub)
        elif np.any(np.where(pos_vec_array_sub == -99999)):
            faint.append(pos_vec_array_sub)
        else:
            source.append(pos_vec_array_sub)
    return bright, faint, source

@jit(nopython=True)
def cascade_array(sort_position):
    '''
    Use this to find out sources locate in same position and cascade them
    Note: No tuple() support in numba, No format() support in numba
    '''
    #================================================
    # Input
    after_cascade_pos = []
    after_cascade_value = []
    start = 0
    end   = 0
    for i in range(len(sort_position)-1):
        #================================================
        # Indicator
        if i % 1000 == 0 and i>999:
            print(float(i+1)/len(sort_position))
        #================================================
        # Get reference and target
        tar, ref = sort_position[i], sort_position[i+1]
        end += 1
        #================================================
        # Determine repeated or not
        if not np.all(np.equal(tar, ref)):
            after_cascade_pos.append(sort_position[start])
            after_cascade_value.append(end-start)
            start = end
    #================================================
    # Include the last term
    after_cascade_pos.append(sort_position[start])
    after_cascade_value.append(len(sort_position)-start)
    return after_cascade_pos, after_cascade_value

def update_dict(pos, value):
    '''
    This is to update dictionary with key [position] and its value
    '''
    #================================================
    # Input
    out_dict = dict()
    for i in range(len(value)):
        #================================================
        # Indicator
        if i % 1000 == 0 and i>999:
            print('{:.6f} %'.format(float(i+1) / len(_value) * 100))
        #================================================
        # Update dictionary
        key = tuple(pos[i])
        out_dict[key] = float(value[i])
    return out_dict

#======================================================
# Load Galaxy Catalog
l_start = time.time()
print("\nLoading input catalog ...")
with open(str(argv[1]), 'r') as catalogs:
    catalog = catalogs.readlines()
l_end   = time.time()
print("\nLoading catalog took {:.3f} secs\n".format(l_end-l_start))

#======================================================
# Calculate Galaxy Position Vector
c_start = time.time()
pos_vec = []
for i in range(len(catalog)):
    #======================================================
    # Percentage Indicator
    if i%100==0:
        print(str(float(i)/len(catalog)*100) + '%')
    #======================================================
    # Unit transformation
    line = catalog[i]
    lines = line.split()
    if datatype == 'flux':
        mag_list = mJy_to_mag(lines, flux_ID=flux_ID, Qua=False, system="ukidss")
    elif datatype == 'mag':
        mag_list = mag_to_mag(lines, mag_ID=mag_ID, Qua=False, system="ukidss")
    else:
        print('Input type error')
    magJ, magIR1, magIR2, magIR3, magIR4, magMP1 = mag_list
    SEQ = [sort_up_lack999(mag_list[i], axlim_list[i], cube) for i in range(len(axlim_list))]
    pos_vec.append(SEQ)

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

c_end   = time.time()
print("\nCalculate all sources position in n-dim space took {:.3f} secs\n".format(c_end-c_start))

#======================================================
# Galaxy filter
f_start = time.time()
pos_vec_array = np.array(pos_vec)
bright, faint, source = filter_bright_faint(pos_vec_array)
source_array = np.array(source)
f_end   = time.time()
print("Filter out bright and faint sources took {:.3f} secs\n".format(f_end-f_start))

#================================================
# Sort Input Galaxy Position/Probability array
u_start = time.time()
position_t = np.transpose(source_array)
sort_ind = np.lexsort(tuple(position_t))
sort_position = np.array(source_array[sort_ind], dtype=int)
uni_pos, uni_num = cascade_array(sort_position)
new_pos_vec_dict = update_dict(uni_pos, uni_num)
u_end   = time.time()
print("Sort and write to dictionary took {:.3f} secs\n".format(c_end-c_start))

#======================================================
# Save Galaxy Position Vector, Bright, Faint
s_start = time.time()
chdir('GPV_' + str(dim) + 'Dposvec_bin' + str(cube))
np.save('Gal_Position_vectors', new_pos_vec_dict)
np.save('Bright', bright)
np.save('Faint',  faint)
np.save('Shape',  np.array([binsa, bins1, bins2, bins3, bins4, bins5]))
chdir('../')
s_end   = time.time()
print("Saving Galaxy Position took {:.3f} secs\n".format(c_end-c_start))
