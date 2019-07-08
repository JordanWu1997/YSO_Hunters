#!/usr/bin/ipython
'''----------------------------------------------------------------
This program is for calculating 6-d galaxy probability (P)

Input : catalog with 
        (1)5-d galaxy probablity
        (2)galaxy probability P

Output: catalog with 
        (1)6-d galaxy probability
        (2)6-d galaxy probability P
*Note: 
    (1)6 bands are J, IR1, IR2, IR3, IR4, MP1
    (2)Some function are imported from Hsieh_Functions.py
    #================================================================
    (3)Gal_Prob=0 is now assigned to Gal_Prob =1e-9 (Originally, 1e-3)
    #================================================================

**New add function: computing with different binsizes
-------------------------------------------------------------------
latest update : 2019/02/26 Jordan Wu'''

#======================================================================================
# Setup initial environment; Check input arguments
#======================================================================================
import time
import numpy as np
from os import system
from sys import argv, exit
from Hsieh_Functions import *

if len(argv) == 5 or len(argv) == 7:
    print('Start 6D Galaxy Prob calculating ...')
else:
    exit('Error: Wrong Usage!\n \
          Exmaple: python [program] [catalog] [cloud\'s name] [data_type] [model]\n \
          data_type: flux or mag (default=flux)\n\
          model_set: old/new/latest: full/conditional/conditional_wi_new_limit UKIDSS catalog')

#======================================================================================
# Start loading Galaxy probabilty dictionary
#======================================================================================
tStart = time.time()

if str(argv[-1]) == 'argv':
    Binsize = str(argv[-2])
else:
    Binsize = str(input('binsize = '))
print('Loading arrays ...')

if str(argv[4]) == 'old':
    path = '/home/ken/new_mg/GPV_SOP_Program/result' + Binsize + '/'
elif str(argv[4]) == 'new':
    path = '/home/ken/new_mg/GPV_SOP_Program/result_condition_' + Binsize + '/'
elif str(argv[4]) == 'latest':
    path = '/home/ken/new_mg/GPV_SOP_Program/' ###################### TO BE CONTINUED ...
else:
    exit('Wrong model selection ...')
print('Array path: ' + path)

# New type galaxy position in dictionary 
Fu_Dict = np.load(path + 'all_detect_grid_Full_6d.npy').item()
L1_Dict = np.load(path + 'all_detect_grid_Full_5d.npy').item()
L2_Dict = np.load(path + 'all_detect_grid_Full_4d.npy').item()
L3_Dict = np.load(path + 'all_detect_grid_Full_3d.npy').item()

tEnd = time.time()
print("Loading arrays took %f sec" % (tEnd - tStart))
time.sleep(2)

#======================================================================================
# Set up parameters
#======================================================================================
print('Loading catalog ...')
table = open(str(argv[1]), 'r')
catalog = table.readlines()
table.close()

Cloud = str(argv[2])
data_type = str(argv[3])

#parameter
cube = float(Binsize)
if str(argv[4]) == 'latest':
    Jaxlim =   [4.0, 18.0]
    IR1axlim = [8.0, 18.0]
    IR2axlim = [7.0, 18.0]
    IR3axlim = [5.0, 18.0]
    IR4axlim = [5.0, 18.0]
    MP1axlim = [3.5, 11.0]
else:
    # NEW BOUNDARY WI UKIDSS CATALOG
    Jaxlim =   [3.5, 22.0]
    IR1axlim = [8.0, 20.0]
    IR2axlim = [7.0, 19.0]
    IR3axlim = [5.0, 18.0]
    IR4axlim = [5.0, 18.0]
    MP1axlim = [3.5, 12.0]

band_name = ['J','IR1','IR2','IR3','IR4','MP1']

#======================================================================================
# Start calculating 6-D Galaxy probabilty
#======================================================================================
tStart = time.time()
print('Start Calculating ...')
out = []
for i in range(len(catalog)):

    # Percentage Indicator
    if i % 100 == 1:
        print('%.6f' % (float(i)/float(len(catalog))*100) + '%')
    # Set up initial condition
    line = catalog[i].split()
    
    #===============================================
    if data_type == 'flux':
        mag_list = magnitudelist(line)

    # Command below is for UKIDSS-SWIRE type catalog  
    elif data_type == 'mag':
        mag_list = mag_magnitudelist(line)

    # Default: flux type
    else:
        mag_list = magnitudelist(line)
    #===============================================
    
    magJ = mag_list[0]; magIR1 = mag_list[1]; magIR2 = mag_list[2]; magIR3 = mag_list[3]; magIR4 = mag_list[4]; magMP1 = mag_list[5]
    PSF_list = [line[39], line[102], line[123], line[144], line[165], line[186]]
    SEQ = [seq(magJ,Jaxlim,cube), seq(magIR1,IR1axlim,cube), seq(magIR2,IR2axlim,cube), seq(magIR3, IR3axlim,cube), seq(magIR4,IR4axlim,cube), seq(magMP1,MP1axlim,cube)]
    num = 6 - SEQ.count('Lack')
    ob_type = str(num) + "bands_"
    count = 'no_count'
    KEY = '_'
    
    # Remove AGB
    de="unknown"
    if magIR2 != 'no' and magIR3 != 'no' and magMP1 != 'no':
        X23 = magIR2 - magIR3; Y35 = magIR3 - magMP1
        if index(X23,Y35,[0,0,2,5],[-1,0,2,2]) < 0:
            de = "AGB"
            ob_type += "AGB_"
            count = "no_count"

    # Sort with detected band num
    if num >= 3 and de != "AGB":
        
        # Set up parameters for searching lack bands
        KEY = str([seq(magJ,Jaxlim,cube), seq(magIR1,IR1axlim,cube), seq(magIR2,IR2axlim,cube), seq(magIR3, IR3axlim,cube), seq(magIR4,IR4axlim,cube), seq(magMP1,MP1axlim,cube)])
        KEY = KEY.strip('[')
        KEY = KEY.strip(']')
        key_array = np.array([seq(magJ,Jaxlim,cube), seq(magIR1,IR1axlim,cube), seq(magIR2,IR2axlim,cube), seq(magIR3, IR3axlim,cube), seq(magIR4,IR4axlim,cube), seq(magMP1,MP1axlim,cube)])    
        index_array = np.argwhere(key_array=='Lack')
        
        if SEQ.count('Faint') > 0:
            count = 99999
            ob_type += 'Faint'
        elif SEQ.count('Bright') > 0:
            count = 1e-4
            ob_type += 'Bright'
        
        elif num == 6:
            try:
                count = Fu_Dict[KEY]
                ob_type += "Lack_no_"
            except KeyError:
                count = 1e-5
                ob_type += "Lack_no_"
                ob_type += '_6D_NOGALAXY_'

        elif num == 5:
            try:
                count = L1_Dict[KEY]
                ob_type += "Lack_" + band_name[int(index_array[0])]
            except KeyError:
                count = 1e-5
                ob_type += "Lack_" + band_name[int(index_array[0])]
                ob_type += '_5D_NOGALAXY_'
            
        elif num == 4:
            try:
                count = L2_Dict[KEY]
                ob_type += "Lack_" + band_name[int(index_array[0])] + band_name[int(index_array[1])]
            except KeyError:
                count = 1e-5
                ob_type += "Lack_" + band_name[int(index_array[0])] + band_name[int(index_array[1])]
                ob_type += '_4D_NOGALAXY_'

        elif num == 3:
            try:
                count = L3_Dict[KEY]
                ob_type += "Lack_" + band_name[int(index_array[0])] + band_name[int(index_array[1])] + band_name[int(index_array[2])]
            except KeyError:
                count = 1e-5
                ob_type += "Lack_" + band_name[int(index_array[0])] + band_name[int(index_array[1])] + band_name[int(index_array[2])]
                ob_type += '_3D_NOGALAXY_'
 
        if count == 0.0:
            count = 10**-9

    if line[184] == "S":
        count = 10**-4

    ob_type += "bandfill=" + str(PSF_list.count("-2"))
    
    #Just to create some empty columns
    if len(line) < 246:
        while len(line) <= 246:
            line.append('z')
        line[241] = ob_type
        line[242] = str(count)
    else:
        line[241] = ob_type
        line[242] = str(count)
    
    out.append("\t".join(line))

tEnd = time.time()
print("Calculating 6D_Gal_Prob took %f sec" % (tEnd - tStart))

#======================================================================================
# END of calculating 6D GALAXY PROB; Save the result
#======================================================================================
system('rm ./' + Cloud + "_6D_GP_out_catalog")
out = "\n".join(out) + '\n'
out_ca = open(Cloud + "_6D_GP_out_catalog","w")
out_ca.write(out)
out_ca.close()

#======================================================================================
# START of calculating 6D GALAXY PROB P
#======================================================================================
print('Loading catalog ...')
table = open(Cloud + "_6D_GP_out_catalog","r")
catalog = table.readlines()
table.close()
tStart = time.time()
print('Start Calculating ...')

out = []
for i in range(len(catalog)):
    
    # Percentage Indicator
    if i % 100 == 1:
        print('%.6f' % (float(i)/float(len(catalog))*100) + '%')
    
    # Set up initial condition
    line = catalog[i].split()
    
    #===============================================
    if data_type == 'flux':
        mag_list = PSF_magnitudelist(line)
   
    # Command below is for UKIDSS-SWIRE type catalog  
    elif data_type == 'mag':
        mag_list = mag_PSF_magnitudelist(line)
    
    # Default: flux type
    else:
        mag_list = PSF_magnitudelist(line)
    #===============================================
    
    magJ = mag_list[0]; magIR1 = mag_list[1]; magIR2 = mag_list[2]; magIR3 = mag_list[3]; magIR4 = mag_list[4]; magMP1 = mag_list[5]
    PSF_list = [line[39], line[102], line[123], line[144], line[165], line[186]]
    SEQ = [seq(magJ,Jaxlim,cube), seq(magIR1,IR1axlim,cube), seq(magIR2,IR2axlim,cube), seq(magIR3,IR3axlim,cube), seq(magIR4,IR4axlim,cube), seq(magMP1,MP1axlim,cube)]
    num = 6 - SEQ.count('Lack')
    ob_type = str(num) + "bands_"
    count = 'no_count'
    KEY = '_'

    # Remove AGB
    de="unknown"
    if magIR2 != 'no' and magIR3 != 'no' and magMP1 != 'no':
        X23 = magIR2 - magIR3; Y35 = magIR3 - magMP1
        if index(X23,Y35,[0,0,2,5],[-1,0,2,2]) < 0:
            de = "AGB"
            ob_type += "AGB_"
            count = "no_count"
    
    # Sort with detected band num
    if num >= 3 and de != "AGB":

        # Set up parameters for searching lack bands                                                                                            
        KEY = str([seq(magJ,Jaxlim,cube), seq(magIR1,IR1axlim,cube),seq(magIR2,IR2axlim,cube), seq(magIR3, IR3axlim,cube), seq(magIR4,IR4axlim,cube), seq(magMP1,MP1axlim,cube)])
        KEY = KEY.strip('[')
        KEY = KEY.strip(']')
        key_array = np.array([seq(magJ,Jaxlim,cube), seq(magIR1,IR1axlim,cube), seq(magIR2,IR2axlim,cube), seq(magIR3, IR3axlim,cube), seq(magIR4,IR4axlim,cube), seq(magMP1,MP1axlim,cube)])
        index_array = np.argwhere(key_array=='Lack')

        if SEQ.count('Faint') > 0:
            count = 99999
            ob_type += 'Faint'

        elif SEQ.count('Bright') > 0:
            count = 1e-4
            ob_type += 'Bright'

        elif num == 6:
            try:
                count = Fu_Dict[KEY]
                ob_type += "Lack_no_"
            except KeyError:
                count = 1e-5
                ob_type += "Lack_no_"
                ob_type += '_6D_NOGALAXY_'

        elif num == 5:
            try:
                count = L1_Dict[KEY]
                ob_type += "Lack_" + band_name[int(index_array[0])]
            except KeyError:
                count = 1e-5
                ob_type += "Lack_" + band_name[int(index_array[0])]
                ob_type += '_5D_NOGALAXY_'

        elif num == 4:
            try:
                count = L2_Dict[KEY]
                ob_type += "Lack_" + band_name[int(index_array[0])] + band_name[int(index_array[1])]
            except KeyError:
                count = 1e-5
                ob_type += "Lack_" + band_name[int(index_array[0])] + band_name[int(index_array[1])]
                ob_type += '_4D_NOGALAXY_'

        elif num == 3:
            try:
                count = L3_Dict[KEY]
                ob_type += "Lack_" + band_name[int(index_array[0])] + band_name[int(index_array[1])] + band_name[int(index_array[2])]
            except KeyError:
                count = 1e-5
                ob_type += "Lack_" + band_name[int(index_array[0])] + band_name[int(index_array[1])] + band_name[int(index_array[2])]
                ob_type += '_3D_NOGALAXY_'

        if count == 0.0:
            count = 10**-9

    if line[184] == "S":
        count = 10**-4

    ob_type += "bandfill=" + str(PSF_list.count("-2"))
    line[243] = ob_type
    line[244] = str(count)
    out.append("\t".join(line))

tEnd = time.time()
print("Calculating 6D Gal_Prob_P took %f sec" % (tEnd - tStart))

#======================================================================================
# END of calculating 6D GALAXY PROB P; Clean old results and Save the new results     
#======================================================================================
system('rm ' + Cloud + "_6D_GP_all_out_catalog.tbl")
out = "\n".join(out) + '\n'
out_ca = open(Cloud + "_6D_GP_all_out_catalog.tbl","w")
out_ca.write(out)
out_ca.close()

print('6D Gal Prob calculation ends ...')
system('rm ' + Cloud + "_6D_GP_out_catalog")
