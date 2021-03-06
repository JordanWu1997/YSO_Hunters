#!/usr/bin/ipython
import numpy as np
from os import system, chdir
from sys import argv

dim   = int(argv[1])       # Dimension of multi-D method
cube  = float(argv[2])     # Beamsize for each cube
sigma = int(argv[3])       # STD for Gaussian Smooth
ref   = int(argv[4])       # Reference Beam Dimension

posv_dir = 'GPV_' + str(dim) + 'Dposvec_bin' + str(cube) + '/'
beam_dir = 'GPV_smooth_sigma' + str(sigma) + '_refD' + str(ref) + '/'
out_dir  = 'GPV_grid_' + str(dim) + 'D_' + 'bin' + str(cube) + '_sigma' + str(sigma) + '_refD' + str(ref) + '/'

print("Loading ...")
Gal_pos  = np.load(posv_dir + "Gal_Position_vectors.npy")
six_beam = np.load(beam_dir + "6d_beam_sigma" + str(sigma) + ".npy")
fi_beam  = np.load(beam_dir + "5d_beam_sigma" + str(sigma) + ".npy")
fo_beam  = np.load(beam_dir + "4d_beam_sigma" + str(sigma) + ".npy")
th_beam  = np.load(beam_dir + "3d_beam_sigma" + str(sigma) + ".npy")
shape    = list(np.load(posv_dir + "Shape.npy"))

print("Start Calculation ...")
d6, d5, d4, d3 = {}, {}, {}, {}
for li in range(len(Gal_pos)):
    # Percentage Indicator
    if li % 100 == 0:
        print('Now: ' + str(float(li)/len(Gal_pos) * 100) + '%')

    gal = list(Gal_pos[li])

    #===================================================================================================================================
    # Find 6bands sources
    #===================================================================================================================================
    if gal.count("Lack") == 0 and gal.count("Faint") == 0:

        # Apply to six bands
        new_gal = list(gal)

        # Do 6band Gaussian Smooth
        i = int(new_gal[0]); j = int(new_gal[1]); k = int(new_gal[2]); l = int(new_gal[3]); m = int(new_gal[4]); n = int(new_gal[5])
        for v in range(len(six_beam)):
            vec = list(six_beam[v])
            vec[0] = int(vec[0]); vec[1] = int(vec[1]); vec[2] = int(vec[2]); vec[3] = int(vec[3]); vec[4] = int(vec[4]); vec[5] = int(vec[5])

            # Start from boundary and end till reaching the other side
            if 0 <= i+vec[0] < shape[0] and 0 <= j+vec[1] < shape[1] and 0 <= k+vec[2] < shape[2] and 0 <= l+vec[3] < shape[3] and 0 <= m+vec[4] < shape[4] and 0 <= n+vec[5] < shape[5]:
                key_tuple = tuple([int(i+vec[0]), int(j+vec[1]), int(k+vec[2]), int(l+vec[3]), int(m+vec[4]), int(n+vec[5])])
                if key_tuple in d6.keys():
                    d6[key_tuple] += vec[6] * int(new_gal[6])
                else:
                    d6.update({key_tuple: vec[6] * int(new_gal[6])})

        # Apply to five bands
        for dia in range(6):
            new_gal = list(gal)
            del new_gal[dia]
            new_shape = list(shape)
            del new_shape[dia]

            # Do 5band Gaussian Smooth
            i = int(new_gal[0]); j = int(new_gal[1]); k = int(new_gal[2]); l = int(new_gal[3]); m = int(new_gal[4])
            for v in range(len(fi_beam)):
                vec = list(fi_beam[v])
                vec[0] = int(vec[0]); vec[1] = int(vec[1]); vec[2] = int(vec[2]); vec[3] = int(vec[3]); vec[4] = int(vec[4])

                # Start from boundary and end till reaching the other side
                if 0 <= i+vec[0] < new_shape[0] and 0 <= j+vec[1] < new_shape[1] and 0 <= k+vec[2] < new_shape[2] and 0 <= l+vec[3] < new_shape[3] and 0 <= m+vec[4] < new_shape[4]:
                    key_l = [int(i+vec[0]), int(j+vec[1]), int(k+vec[2]), int(l+vec[3]), int(m+vec[4])]
                    key_n = tuple(key_l[0:dia] + ['Lack'] + key_l[dia:])
                    if key_n in d5.keys():
                        d5[key_n] += vec[5] * int(new_gal[5])
                    else:
                        d5.update({key_n: vec[5] * int(new_gal[5])})

        # Apply to four bands
        for A in range(6):
            for B in range(A):
                new_gal = list(gal)
                del new_gal[B], new_gal[A-1]
                new_shape = list(shape)
                del new_shape[B], new_shape[A-1]

                # Do 4band Gaussian Smooth
                i = int(new_gal[0]); j = int(new_gal[1]); k = int(new_gal[2]); l = int(new_gal[3])
                for v in range(len(fo_beam)):
                    vec = list(fo_beam[v])
                    vec[0] = int(vec[0]); vec[1] = int(vec[1]); vec[2] = int(vec[2]); vec[3] = int(vec[3])

                    # Start from boundary and end till reaching the other side
                    if 0 <= i+vec[0] < new_shape[0] and 0 <= j+vec[1] < new_shape[1] and 0 <= k+vec[2] < new_shape[2] and 0 <= l+vec[3] < new_shape[3]:
                        key_l = [int(i+vec[0]), int(j+vec[1]), int(k+vec[2]), int(l+vec[3])]
                        key_n = tuple(key_l[0:B] + ['Lack'] + key_l[B:A] + ['Lack'] + key_l[A:])
                        if key_n in d4.keys():
                            d4[key_n] += vec[4] * int(new_gal[4])
                        else:
                            d4.update({key_n: vec[4] * int(new_gal[4])})

        # Apply to three bands
        for A in range(6):
            for B in range(A):
                for C in range(B):
                    new_gal = list(gal)
                    del new_gal[C], new_gal[B-1], new_gal[A-2]
                    new_shape = list(shape)
                    del new_shape[C], new_shape[B-1], new_shape[A-2]

                    # Do 3band Gaussian Smooth
                    i = int(new_gal[0]); j = int(new_gal[1]); k = int(new_gal[2])
                    for v in range(len(th_beam)):
                        vec = list(th_beam[v])
                        vec[0] = int(vec[0]); vec[1] = int(vec[1]); vec[2] = int(vec[2])

                        # Start from boundary and end till reaching the other side
                        if 0 <= i+vec[0] < new_shape[0] and 0 <= j+vec[1] < new_shape[1] and 0 <= k+vec[2] < new_shape[2]:
                            key_l = [int(i+vec[0]), int(j+vec[1]), int(k+vec[2])]
                            key_n = tuple(key_l[0:C] + ['Lack'] + key_l[C:B] + ['Lack'] + key_l[B:A] + ['Lack'] + key_l[A:])
                            if key_n in d3.keys():
                                d3[key_n] += vec[3] * int(new_gal[3])
                            else:
                                d3.update({key_n: vec[3] * int(new_gal[3])})

    #===================================================================================================================================
    # Find 5bands sources
    #===================================================================================================================================
    elif gal.count("Lack") == 1 and gal.count("Faint") == 0:

        # Apply to five bands
        new_gal = list(gal)
        L1 = new_gal.index("Lack")
        del new_gal[L1]
        new_shape = list(shape)
        del new_shape[L1]

        # Do 5band Gaussian Smooth
        i = int(new_gal[0]); j = int(new_gal[1]); k = int(new_gal[2]); l = int(new_gal[3]); m = int(new_gal[4])
        for v in range(len(fi_beam)):
            vec = list(fi_beam[v])
            vec[0] = int(vec[0]); vec[1] = int(vec[1]); vec[2] = int(vec[2]); vec[3] = int(vec[3]); vec[4] = int(vec[4])

            # Start from boundary and end till reaching the other side
            if 0 <= i+vec[0] < new_shape[0] and 0 <= j+vec[1] < new_shape[1] and 0 <= k+vec[2] < new_shape[2] and 0 <= l+vec[3] < new_shape[3] and 0 <= m+vec[4] < new_shape[4]:
                key_l = [int(i+vec[0]), int(j+vec[1]), int(k+vec[2]), int(l+vec[3]), int(m+vec[4])]
                key_n = tuple(key_l[0:L1] + ['Lack'] + key_l[L1:])
                if key_n in d5.keys():
                    d5[key_n] += vec[5] * int(new_gal[5])
                else:
                    d5.update({key_n: vec[5] * int(new_gal[5])})

        # Apply to four bands
        for A in range(6):
            for B in range(A):
                if A == L1 or B == L1:
                    new_gal = list(gal)
                    del new_gal[B], new_gal[A-1]
                    new_shape = list(shape)
                    del new_shape[B], new_shape[A-1]

                    # Do 4band Gaussian Smooth
                    i = int(new_gal[0]); j = int(new_gal[1]); k = int(new_gal[2]); l = int(new_gal[3])
                    for v in range(len(fo_beam)):
                        vec = list(fo_beam[v])
                        vec[0] = int(vec[0]); vec[1] = int(vec[1]); vec[2] = int(vec[2]); vec[3] = int(vec[3])

                        # Start from boundary and end till reaching the other side
                        if 0 <= i+vec[0] < new_shape[0] and 0 <= j+vec[1] < new_shape[1] and 0 <= k+vec[2] < new_shape[2] and 0 <= l+vec[3] < new_shape[3]:
                            key_l = [int(i+vec[0]), int(j+vec[1]), int(k+vec[2]), int(l+vec[3])]
                            key_n = tuple(key_l[0:B] + ['Lack'] + key_l[B:A] + ['Lack'] + key_l[A:])
                            if key_n in d4.keys():
                                d4[key_n] += vec[4] * int(new_gal[4])
                            else:
                                d4.update({key_n: vec[4] * int(new_gal[4])})

        # Apply to three bands
        for A in range(6):
            for B in range(A):
                for C in range(B):
                    if A == L1 or B == L1 or C == L1:
                        new_gal = list(gal)
                        del new_gal[C], new_gal[B-1], new_gal[A-2]
                        new_shape = list(shape)
                        del new_shape[C], new_shape[B-1], new_shape[A-2]

                        # Do 3band Gaussian Smooth
                        i = int(new_gal[0]); j = int(new_gal[1]); k = int(new_gal[2])
                        for v in range(len(th_beam)):
                            vec = list(th_beam[v])
                            vec[0] = int(vec[0]); vec[1] = int(vec[1]); vec[2] = int(vec[2])

                            # Start from boundary and end till reaching the other side
                            if 0 <= i+vec[0] < new_shape[0] and 0 <= j+vec[1] < new_shape[1] and 0 <= k+vec[2] < new_shape[2]:
                                key_l = [int(i+vec[0]), int(j+vec[1]), int(k+vec[2])]
                                key_n = tuple(key_l[0:C] + ['Lack'] + key_l[C:B] + ['Lack'] + key_l[B:A] + ['Lack'] + key_l[A:])
                                if key_n in d3.keys():
                                    d3[key_n] += vec[3] * int(new_gal[3])
                                else:
                                    d3.update({key_n: vec[3] * int(new_gal[3])})

    #===================================================================================================================================
    # Find 4bands sources
    #===================================================================================================================================
    elif gal.count("Lack") == 2 and gal.count("Faint") == 0:

        # Apply to four bands
        new_gal = list(gal)
	L1 = new_gal.index("Lack")
	del new_gal[L1]
 	L2 = new_gal.index("Lack")
	del new_gal[L2]
	new_shape = list(shape)
	del new_shape[L1], new_shape[L2]
	L2 = L2 + 1

        # Do 4band Gaussian Smooth
	i = int(new_gal[0]); j = int(new_gal[1]); k = int(new_gal[2]); l = int(new_gal[3])
	for v in range(len(fo_beam)):
	    vec = fo_beam[v]
            vec[0] = int(vec[0]); vec[1] = int(vec[1]); vec[2] = int(vec[2]); vec[3] = int(vec[3])

            # Start from boundary and end till reaching the other side
	    if 0 <= i+vec[0] < new_shape[0] and 0 <= j+vec[1] < new_shape[1] and 0 <= k+vec[2] < new_shape[2] and 0 <= l+vec[3] < new_shape[3]:

                #==============================================================
                if vec[0] == 0 and vec[1] == 0 and vec[2] == 0 and vec[3] == 0:
                    print(new_gal)
                    print(i, j, k, l)
                #==============================================================

                key_l = [int(i+vec[0]), int(j+vec[1]), int(k+vec[2]), int(l+vec[3])]
                key_n = tuple(key_l[0:L1] + ['Lack'] + key_l[L1:L2] + ['Lack'] + key_l[L2:])
                if key_n in d4.keys():
                    d4[key_n] += vec[4] * int(new_gal[4])
                else:
                    d4.update({key_n: vec[4] * int(new_gal[4])})

        # Apply to three bands
        for A in range(6):
            for B in range(A):
                for C in range(B):
                    if (A == L1 and B == L2) or (A == L1 and C == L2) or (B == L1 and A == L2) or (B == L1 and C == L2) or (C==L1 and A==L2) or (C == L1 and B == L2):
                        new_gal = list(gal)
                        del new_gal[C], new_gal[B-1], new_gal[A-2]
                        new_shape = list(shape)
                        del new_shape[C], new_shape[B-1], new_shape[A-2]

                        # Do 3band Gaussian Smooth
                        i = int(new_gal[0]); j = int(new_gal[1]); k = int(new_gal[2])
                        for v in range(len(th_beam)):
                            vec = list(th_beam[v])
                            vec[0] = int(vec[0]); vec[1] = int(vec[1]); vec[2] = int(vec[2])

                            # Start from boundary and end till reaching the other side
                            if 0 <= i+vec[0] < new_shape[0] and 0 <= j+vec[1] < new_shape[1] and 0 <= k+vec[2] < new_shape[2]:
                                key_l = [int(i+vec[0]), int(j+vec[1]), int(k+vec[2])]
                                key_n = tuple(key_l[0:C] + ['Lack'] + key_l[C:B] + ['Lack'] + key_l[B:A] + ['Lack'] + key_l[A:])
                                if key_n in d3.keys():
                                    d3[key_n] += vec[3] * int(new_gal[3])
                                else:
                                    d3.update({key_n: vec[3] * int(new_gal[3])})

    #===================================================================================================================================
    # Find 3bands sources
    #===================================================================================================================================
    elif gal.count("Lack") == 3 and gal.count("Faint") == 0:

        # Apply to three bands
        new_gal = list(gal)
        L1 = new_gal.index("Lack")
        del new_gal[L1]
        L2 = new_gal.index("Lack")
        del new_gal[L2]
        L3 = new_gal.index("Lack")
        del new_gal[L3]
        new_shape = list(shape)
        del new_shape[L1], new_shape[L2], new_shape[L3]
        L2 = L2 + 1
        L3 = L3 + 2

        i = int(new_gal[0]); j = int(new_gal[1]); k = int(new_gal[2])
        for v in range(len(th_beam)):
            vec = th_beam[v]
            if 0 <= i+vec[0] < new_shape[0] and 0 <= j+vec[1] < new_shape[1] and 0 <= k+vec[2] < new_shape[2]:

                #==============================================================
                if vec[0] == 0 and vec[1] == 0 and vec[2] == 0 and vec[3] == 0:
                    print(new_gal)
                    print(i, j, k, l)
                #==============================================================


                key_l = [int(i+vec[0]), int(j+vec[1]), int(k+vec[2])]
                key_n = tuple(key_l[0:L1] + ['Lack'] + key_l[L1:L2] + ['Lack'] + key_l[L2:L3] + ['Lack'] + key_l[L3:])
                try:
                    d3[key_n] += vec[3] * int(new_gal[3])
                except KeyError:
                    d3.update({key_n: vec[3] * int(new_gal[3])})

# Save results
print("Save result ...")
system('mkdir ' + out_dir)
chdir(out_dir)
np.save("all_detect_grid_Full_6d", d6)
np.save("all_detect_grid_Full_5d", d5)
np.save("all_detect_grid_Full_4d", d4)
np.save("all_detect_grid_Full_3d", d3)
