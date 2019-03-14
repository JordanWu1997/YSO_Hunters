#!/usr/bin/ipython
'''
------------------------------------------------------------------------------
This program is for image check process to check if the candidates on the list
is the same as Hsieh's all candidate's catalog and find the index of image:

Input: catalog to find index

Output: (1)catalog NEW and HSIEH
        (2)catalog of remaining objects
        (3)catalog NEW and HSIEH's index of image_check's file
------------------------------------------------------------------------------
latest update : 2018/11/22
'''

from sys import argv
from sys import exit
from os import system

if len(argv) != 4:
    print('ERROR! Wrong Usage!')
    print('Example: python [program] [catalog] [round_to] [option]')
    print('Ture/False: to save common/incommon catalog or not')
    exit()

catalog = open(argv[1],'r')
catalog_full = open('/home/ken/C2D-SWIRE_20180710/all_candidates.tbl', 'r')
round_to = int(argv[2])
option = str(argv[3])

candidates , all_candidates = catalog.readlines(), catalog_full.readlines()

Consistent = []; Inconsistent = []; C_index_list = []

for candidate in candidates:
    can = candidate.split()
    for all_candidate in all_candidates:
        all_can = all_candidate.split()
        if round(float(can[0]),round_to) == round(float(all_can[0]),round_to) and round(float(can[2]),round_to) == round(float(all_can[2]),round_to):
            index_num = candidates.index(candidate)
            print('This one (index) on all candidate catalog: %i' % (index_num+1))
            Consistent.append(candidate)
            C_index_list.append(index_num+1)

    if candidate not in Consistent:
        Inconsistent.append(candidate)

if option == 'True':
    
    system('rm On_all_cans_catalog')
    system('rm Not_on_all_cans_catalog')
    system('rm On_all_index_catalog')

    Out1 = open('On_all_cans_catalog', 'w')
    Out2 = open('Not_on_all_cans_catalog', 'w')
    Out3 = open('On_all_index_catalog', 'w')

    for Row in Consistent:
        Out1.write(str(Row))
    for Row in Inconsistent:
        Out2.write(str(Row))
    for Row in C_index_list:
        Out3.write(str(Row)+'\n')
