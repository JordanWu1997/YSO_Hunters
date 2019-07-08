#!/usr/bin/ipython

'''
-------------------------------------------------------------------
This program is for excuting programs that calculates GP and checks GP

Input : c2d catalog with star_removal, extinctioin_correction

Output : (1)Program that calculates GP
            catalog with Gal_Prob, Gal_Prob_p
         
         (2)Program that checks GP
            catalog with GP N pass and fail
            catalog with GP P pass, fail, and candidates to Image Check

#Gal_Prob_N: normal galaxy probability
#Gal_Prob_P: galaxy probability with source passing PSF test

-------------------------------------------------------------------

latest update : 2018/11/18
'''

import os
from sys import argv
from sys import exit

if len(argv) != 3:
    print('Error: Wrong Usage')
    print('Exmaple: ipython Gal_Prob_Execution.py [catalog] [MC cloud]')
    exit()

path = '/home/ken/C2D-SWIRE_20180710/SOP_Program_5D_method/'

catalog = argv[1]; cloud = argv[2]

#Step1 : multi-d J-MP1 Gal_Prob
print('multi-Prob_J_MP1 ...')
os.system('ipython ' + path + 'multi-d_Prob_J_MP1.py' + ' ' + catalog)

#Step2 : multi-d IR1-MP1 Gal_Prob
print('multi-Prob_IR1_MP1 ...')
os.system('ipython ' + path + 'multi-d_Prob_IR1_MP1.py')

#Step3 : multi-d J-MP1 Gal_Prob
print('multi-Prob_P_J_MP1 ...')
os.system('ipython ' + path + 'PSF1_detection_multi-d_Prob_J_MP1.py' + ' ' + 'Out_catalog')
os.system('rm Out_catalog')

#Step4 : multi-d IR1-MP1 Gal_Prob
print('multi-Prob_P_IR1_MP1 ...')
os.system('ipython ' + path + 'PSF1_detection_multi-d_Prob_IR1_MP1.py')

#Step5 : Collect data
os.system('mv ' + 'Out_catalog' + ' ' + 'catalog-' + str(cloud)+ '_Gal_Prob_All.tbl' )
os.system('rm step')

#Step6 : Check Galaxy Prob
os.system('ipython ' + path + 'Check_Prob.py ' + 'catalog-' + str(cloud) + '_Gal_Prob_All.tbl' + ' ' + str(cloud))

