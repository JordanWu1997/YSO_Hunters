#!/usr/bin/ipython

'''
#----------------------------------------------------------------------------------------
This program is used to compare two catalogs if there are common source in both catalogs.
RA and DEC is used to determine whether two sources are the same .
Because it's quick search, no data will be storage, just simply print out!

print: (1)Common Sources 
       (2)Source in catalog1 not in catalog2 
       (3)Source in catalog2 not in catalog1 
#---------------------------------------------------------------------------------------
latest update: 20181023'''

import numpy as np
from sys import argv
from sys import exit

if len(argv) != 3:
    print('Error Usage')
    print('Example: python [program] [catalog1] [catalog2]')
    exit()

catalog1 = open(argv[1], 'r')
catalog2 = open(argv[2], 'r')

RA_cat1 = []; DEC_cat1 = []; All_cat1 = []
for row in catalog1.readlines():
    All_cat1.append(row)
    row = row.split()
    RA_cat1.append(row[0])
    DEC_cat1.append(row[2])

RA_cat2 = []; DEC_cat2 = []; All_cat2 =[]
for row in catalog2.readlines():
    All_cat2.append(row)
    row = row.split()
    RA_cat2.append(row[0])
    DEC_cat2.append(row[2])

coord1 = set(list(zip(RA_cat1, DEC_cat1)))
coord2 = set(list(zip(RA_cat2, DEC_cat2)))

if len(zip(*list(coord1 & coord2))) != 0:
    Common = zip(*list(coord1 & coord2))[0]
else: Common = []

if len(zip(*list(coord1 - coord2))) != 0:
    Complement_1_not_2 = zip(*list(coord1 - coord2))[0]
else: Complement_1_not_2 =[]

if len(zip(*list(coord2 - coord1))) != 0:
    Complement_2_not_1 = zip(*list(coord2 - coord1))[0]
else: Complement_2_not_1 =[]

print('1: ' + str(argv[1]) + ' ; ' + '2: ' + str(argv[2]))
print('Common = ' + str(len(Common)))
print('1_not_2 = ' + str(len(Complement_1_not_2)))
print('2_not_1 = ' + str(len(Complement_2_not_1)))
