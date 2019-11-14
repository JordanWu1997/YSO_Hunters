#!/usr/bin/ipython

import numpy as np
from sys import argv, exit
from os import chdir, system, path
from Hsieh_Functions import *

# Set parameters
dim  = int(argv[2])
cube = float(argv[3])

print('cube = ' + str(cube))

# Use Limit Stored in Hsieh_Functions
Jaxlim   = Hsieh_Jaxlim
Ksaxlim  = Hsieh_Ksaxlim
IR1axlim = Hsieh_IR1axlim
IR2axlim = Hsieh_IR2axlim
IR3axlim = Hsieh_IR3axlim
IR4axlim = Hsieh_IR4axlim
MP1axlim = Hsieh_MP1axlim

#Jaxlim   = Jaxlim
#Ksaxlim  = Ksaxlim
#IR1axlim = IR1axlim
#IR2axlim = IR2axlim
#IR3axlim = IR3axlim
#IR4axlim = IR4axlim
#MP1axlim = MP1axlim

# Count shape of each dim
binsa = int((  Jaxlim[1] -   Jaxlim[0]) / cube) + 1
binsb = int(( Ksaxlim[1] -  Ksaxlim[0]) / cube) + 1
bins1 = int((IR1axlim[1] - IR1axlim[0]) / cube) + 1
bins2 = int((IR2axlim[1] - IR2axlim[0]) / cube) + 1
bins3 = int((IR3axlim[1] - IR3axlim[0]) / cube) + 1
bins4 = int((IR4axlim[1] - IR4axlim[0]) / cube) + 1
bins5 = int((MP1axlim[1] - MP1axlim[0]) / cube) + 1
print(binsa, binsb, bins1, bins2, bins3, bins4, bins5)

# Directory Check
if path.isdir('GPV_' + str(dim) + 'Dposvec_bin' + str(cube)):
    exit('\n\tDirectory has been established ... \
        \n\tPass to next procedure ...\n')
else:
    system('mkdir GPV_' + str(dim) + 'Dposvec_bin' + str(cube))

#=======================================================================================================================
# Functions
#========================================================================================================================
def magnitudelist(x):
    '''
    # flux_list_origin = [float(x[33]),float(x[75]),float(x[96]),float(x[117]),float(x[138]),float(x[159]),float(x[180])]
    # F0_list = [1594000,666700,280900,179700,115000,64130,7140]
    '''
    x = x.split()
    mag = [float(x[35]),float(x[77]),float(x[98]),float(x[119]),float(x[140]),float(x[161]),float(x[182])]
    mag_list = []
    for i in range(len(mag)):
        if float(mag[i]) > 0.0:
            mag_list.append(float(mag[i]))
        elif float(mag[i]) <= 0.0:
            mag_list.append('no')
    return mag_list

def index(X,Y,a,b):
    '''
    # a,b are transition point, X,Y are input color and mag (data)
    '''
    if X < a[0]:
        cutY = b[0]
    elif X > a[len(a)-1]:
        cutY = b[len(a)-1]
    for i in range(len(a)-1):
        if a[i] < X < a[i+1]:
            cutY = b[i] + (b[i+1]-b[i])/(a[i+1]-a[i])*(X-a[i])
    value = Y-cutY
    return value

def seq(X,lim):
    if X == 'no':
        reu = "Lack"
    elif X < lim[0]:
        reu = "Bright"
    elif X > lim[1]:
        reu = "Faint"
    else:
        reu = int((X-lim[0])/cube)
    return reu
#=======================================================================================================================

with open(str(argv[1]), 'r') as catalogs:
    catalog = catalogs.readlines()

print("\ngalaxy position...")
bright, pos_vec = [], []
for i in range(len(catalog)):
    # Percentage Indicator
    if i%100==0:
        print(str(float(i)/len(catalog)*100) + '%')

    line = catalog[i]
    lines = line.split()
    mag_list = magnitudelist(line)
    magJ, magKs, magIR1, magIR2, magIR3, magIR4, magMP1 = mag_list

    flux_list_origin = [lines[33],lines[75],lines[96],lines[117],lines[138],lines[159],lines[180]]
    mag_list_origin  = [lines[35],lines[77],lines[98],lines[119],lines[140],lines[161],lines[182]]

    # Remove AGB sources
    AGB = 0
    if magIR2 != 'no' and magIR3 != 'no' and magMP1 != 'no':
        X23 = magIR2-magIR3
        Y35 = magIR3-magMP1
        if index(X23,Y35,[0,0,2,5],[-1,0,2,2])<0:
            AGB = 1

    # Make grids
    if AGB != 1:
        seqa = seq(magJ,Jaxlim)
        seq1 = seq(magIR1,IR1axlim)
        seq2 = seq(magIR2,IR2axlim)
        seq3 = seq(magIR3,IR3axlim)
        seq4 = seq(magIR4,IR4axlim)
        seq5 = seq(magMP1,MP1axlim)

        if dim == 6:
            SEQ = [seqa,seq1,seq2,seq3,seq4,seq5] #For six bands
        elif dim == 5:
            SEQ=[seq1,seq2,seq3,seq4,seq5] #For five bands
        pos_vec.append(SEQ)

    # Find Bright Objects
    if SEQ.count("Bright")>0:
        print(SEQ)
        bright.append([mag_list_origin, flux_list_origin, i])

new_pos_vec, faint= [], []
while True:
    if len(pos_vec) == 0:
        break

    # Filiter out Bright/Faint Sources
    first = list(pos_vec[0])
    if first.count("Bright") > 0:
        print(first)
        bright.append(first)
    elif first.count("Faint") > 0:
       faint.append(first)

    # Calculate the number of objects in same position
    number = 0
    print(len(pos_vec))
    for n in pos_vec:
        if n == first:
            number += 1
            pos_vec.remove(n)

    first.append(number)
    new_pos_vec.append(first)

# Save Galaxy Position Vector, Bright, Faint
chdir('GPV_' + str(dim) + 'Dposvec_bin' + str(cube))
np.save('Gal_Position_vectors', new_pos_vec)
np.save('Bright', bright)
np.save('Faint', faint)
if dim == 6:
    np.save('Shape', np.array([binsa, bins1, bins2, bins3, bins4, bins5]))
elif dim == 5:
    np.save('Shape', np.array([bins1, bins2, bins3, bins4, bins5]))
chdir('../')
