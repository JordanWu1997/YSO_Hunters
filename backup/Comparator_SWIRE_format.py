#!/usr/bin/ipython
'''
------------------------------------------------------------------------------
This program is for comparing two different catalogs.

One can check if the object on two different catalogs is a same source,

or One can check if even some same sources have different property (e.g. flux)

This program can also provide (1)Interaction of two catalogs
                              (2)different catalogs' Complement
------------------------------------------------------------------------------
latest update : 2019/03/02
'''

from sys import argv
from sys import exit
import numpy as np

if len(argv) != 8:
    exit('\n\tERROR! Wrong Arguments!\
        \n\tInput Example:Comparator_SWIRE_format.py [catalog_1] [catalog_2] [name_1] [name_2] [round_to] [option] [C_check]\
        \n\toption: yes/no (yes: save A_and_B, ~A_and_B, A_and_~B catalogs ; no: nothing\
        \n\tC_check: yes/no (Consistency_Check to check same source\'s flux (IR1~MP1))\n')

catalog1 = open(argv[1],'r')
catalog2 = open(argv[2],'r')
name1 = str(argv[3])
name2 = str(argv[4])
round_to = int(argv[5])
option = str(argv[6])
Consistency_Check = str(argv[7])

print('\ncatalog: '+str(argv[1])+ ', '+str(argv[2]))

candidate1 = catalog1.readlines()
candidate2 = catalog2.readlines()
catalog1.close()
catalog2.close()

num1, num2 = np.shape(candidate1), np.shape(candidate2)
print('num: '+str(num1)+' ,'+str(num2))

SameSource = 0
DifferentSource = 0
Inconsistence = 0
Consistence = 0

n_A_B = 0
n_not_A_but_B = 0
n_not_B_but_A = 0

A_and_B = []
not_A_but_B =[]
not_B_but_A =[]

for Row in candidate1:
    cat1 = Row.split()
    for row in candidate2:
        cat2 = row.split()

        if round(float(cat1[0]),round_to) == round(float(cat2[0]),round_to) and round(float(cat1[2]),round_to) == round(float(cat2[2]),round_to):
        #if round(float(cat1[0]),round_to) == round(float(cat2[0]),round_to) and round(float(cat1[2]),round_to) == round(float(cat2[1]),round_to):
            SameSource += 1
            n_A_B += 1
            A_and_B.append(Row)

            if Consistency_Check == 'yes':
                
                if round(float(cat1[96]),round_to) != round(float(cat2[96]),round_to) or round(float(cat1[117]),round_to) != round(float(cat2[117]), round_to) or round(float(cat1[138]), round_to) != round(float(cat2[138]), round_to) or round(float(cat1[159]), round_to) != round(float(cat2[159]), round_to) or round(float(cat1[180]), round_to) != round(float(cat2[180]), round_to):

                    Inconsistence +=1                
                    print(cat1[0], cat1[2],cat2[0], cat2[2], 'Inconsistent')
                    print(round(float(cat1[96]), 4), round(float(cat2[96]), 4))
                    print(round(float(cat1[117]), 4), round(float(cat2[117]), 4))
                    print(round(float(cat1[138]), 4), round(float(cat2[138]), 4))
                    print(round(float(cat1[159]), 4), round(float(cat2[159]), 4))
                    print(round(float(cat1[180]), 4), round(float(cat2[180]), 4))
                
                else:
                    Consistence +=1

print('SameSource '+'round_to '+str(round_to)+' : '+str(SameSource))
print('Inconsistence :'+str(Inconsistence))
print('Consistence :'+str(Consistence))

if option == 'yes':
    for Row in candidate1:
        count = 0
        cat1 = Row.split()
        for row in A_and_B:
            cat2 = row.split()            
            if round(float(cat1[0]),round_to) != round(float(cat2[0]),round_to) and round(float(cat1[2]),round_to) != round(float(cat2[2]),round_to):
                count += 1

        if count == len(A_and_B):
            n_not_B_but_A += 1
            not_B_but_A.append(Row)

    for Row in candidate2:
        count = 0
        cat1 = Row.split()
        for row in A_and_B:
            cat2 = row.split()
            if round(float(cat1[0]),round_to) != round(float(cat2[0]),round_to) and round(float(cat1[2]),round_to) != round(float(cat2[2]),round_to):
                count += 1

        if count == len(A_and_B):        
            n_not_A_but_B += 1
            not_A_but_B.append(Row)  
    
    out_cat_A_and_B = open(name1 + '_and_' + name2 + '.tbl', 'w')
    out_cat_not_A_but_B = open('not_' + name1 + '_but_' + name2 + '.tbl', 'w')
    out_cat_not_B_but_A = open('not_' + name2 + '_but_' + name1 + '.tbl', 'w')

    for Row in A_and_B:
        out_cat_A_and_B.write(str(Row))
    
    for Row in not_A_but_B:
        out_cat_not_A_but_B.write(str(Row))
    
    for Row in not_B_but_A:
        out_cat_not_B_but_A.write(str(Row))
    
    out_cat_A_and_B.close()
    out_cat_not_A_but_B.close()
    out_cat_not_B_but_A.close()
    
    print(name1 + '_and_' + name2 + ': ' + str(n_A_B))  
    print('not_' + name1 + '_but_' + name2 + ': ' + str(n_not_A_but_B))
    print('not_' + name2 + '_but_' + name1 + ': ' + str(n_not_B_but_A))
