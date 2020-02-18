#!/usr/bin/python
import numpy as np
from os import system, chdir
from sys import argv, exit
from itertools import combinations

if len(argv) != 3:
    exit('\n\tError: Wrong Arguments\
    \n\tExample: [program] [dim] [cube size]\
    \n\t[dim]: dim of magnitude space (for now only "6")\
    \n\t[cube size]: length of multi-d cube in magnitude unit\n')

print("Loading ...")
dim      = int(argv[1])       # Dimension of multi-D method
cube     = float(argv[2])     # Beamsize for each cube
posv_dir = 'GPV_' + str(dim) + 'Dposvec_bin' + str(cube) + '/'
Gal_pos  = np.load(posv_dir + "Gal_Position_vectors.npy").item()
shape    = list(np.load(posv_dir + "Shape.npy"))

#=======================================================
def find_Lack(lst):
    index_list = [i for i, x in enumerate(lst) if x == "Lack"]
    return index_list

def update_dict(old_key, new_key, inp_dict, out_dict):
    number = inp_dict[tuple(old_key)]
    if new_key not in out_dict.keys():
        out_dict.update({tuple(new_key): number})
    else:
        out_dict[tuple(input_key)] += number
#=======================================================

print("Start Calculation ...")
M0 = dict()
M1 = dict()
M2 = dict()
M3 = dict()
for i, key in enumerate(Gal_pos.keys()):
    # Percentage Indicator
    if i % 100 == 0:
        print('Now: ' + str(float(i)/len(Gal_pos.keys()) * 100) + '%')
    gal = list(key)
    #===================================================================================================================================
    # Find Full-band (6bands) sources
    #===================================================================================================================================
    if gal.count("Lack") == 0:
        new_gal = list(gal)
        update_dict(gal, new_gal, Gal_pos, M0)
        left_bd = [i for i in range(len(shape))]
        for comb in combinations(left_bd, 1):
            new_gal = list(gal)
            new_gal[comb[0]] = "Lack"
            update_dict(gal, new_gal, Gal_pos, M1)
        for comb in combinations(left_bd, 2):
            new_gal = list(gal)
            new_gal[comb[0]] = "Lack"
            new_gal[comb[1]] = "Lack"
            update_dict(gal, new_gal, Gal_pos, M2)
        for comb in combinations(left_bd, 3):
            new_gal = list(gal)
            new_gal[comb[0]] = "Lack"
            new_gal[comb[1]] = "Lack"
            new_gal[comb[2]] = "Lack"
            update_dict(gal, new_gal, Gal_pos, M3)
    #===================================================================================================================================
    # Find Lack 1 band (5bands) sources
    #===================================================================================================================================
    elif gal.count("Lack") == 1:
        new_gal = list(gal)
        L1 = find_Lack(new_gal)[0]
        update_dict(gal, new_gal, Gal_pos, M1)
        left_bd = [i for i in range(0, L1)] + [j for j in range(L1+1, len(shape))]
        for comb in combinations(left_bd, 1):
            new_gal = list(gal)
            new_gal[comb[0]] = "Lack"
            update_dict(gal, new_gal, Gal_pos, M2)
        for comb in combinations(left_bd, 2):
            new_gal = list(gal)
            new_gal[comb[0]] = "Lack"
            new_gal[comb[1]] = "Lack"
            update_dict(gal, new_gal, Gal_pos, M3)
    #===================================================================================================================================
    # Find Lack 2 band (4bands) sources
    #===================================================================================================================================
    elif gal.count("Lack") == 2:
        new_gal = list(gal)
        L1, L2 = find_Lack(new_gal)[0], find_Lack(new_gal)[1]
        update_dict(gal, new_gal, Gal_pos, M2)
        left_bd = [i for i in range(0, L1)] + [j for j in range(L1+1, L2)] + [k for k in range(L2+1, len(shape))]
        for comb in combinations(left_bd, 1):
            new_gal = list(gal)
            new_gal[comb[0]] = "Lack"
            update_dict(gal, new_gal, Gal_pos, M3)
    #===================================================================================================================================
    # Find Lack 3 band (3bands) sources
    #===================================================================================================================================
    elif gal.count("Lack") == 3:
        # Apply to three bands
        new_gal = list(gal)
        update_dict(gal, new_gal, Gal_pos, M3)

# Save results
print("Save result ...")
chdir(posv_dir)
np.save("Lack_0band_sources", M0)
np.save("Lack_1band_sources", M1)
np.save("Lack_2band_sources", M2)
np.save("Lack_3band_sources", M3)
