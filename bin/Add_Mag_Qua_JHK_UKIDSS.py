#!/usr/bin/python
'''
--------------------------------------------------------
Abstract:
    This program is to replace qua label in catalogs

Example:
    [program] [input table] [output file name] [old_label] [new_label]

Input Variables
    [output file name]: filename or "default"\
    [old label]: Qua label on input catalog\
    [new label]: Qua label to replace old one\n')

--------------------------------------------------------
Latest update 2020/05/28 Jordan Wu'''

# Import Modules
#=======================================================
from __future__ import print_function
from sys import argv, exit
from os import system
import time
from All_Variables import *
from Hsieh_Functions import *
from Useful_Functions import *

# Main Programs
#=======================================================
if __name__ == '__main__':

    # Check inputs
    if len(argv) != 5:
        exit('\n\tWrong Input Argument!\
              \n\tExample: [program] [input table] [output file name] [old_label] [new_label]\
              \n\t[output file name]: filename or "default"\
              \n\t[old label]: Qua label on input catalog\
              \n\t[new label]: Qua label to replace old one\n')

    # For now it's J, H, K
    qua_list    = qua_ID_2Mass
    catalog     = str(argv[1])
    output_name = str(argv[2])
    old_label   = str(argv[3])
    new_label   = str(argv[4])
    if output_name == 'default':
        output_name = '{}-Add_JHK_Qua.tbl'.format(catalog.strip('.tbl'))

    print('\nChange JHK Qua from {} to {}'.format(old_label, new_label))
    print('\nInput: ')
    system('wc -l {}'.format(catalog))
    with open(catalog, 'r') as cat:
        data = cat.readlines()

    out_catalog = []
    for i in range(len(data)):
        row = data[i].split()
        for qua_id in qua_list:
            if row[qua_id] == old_label:
                row[qua_id] = new_label
        out_catalog.append('\t'.join(row))
        drawProgressBar(float(i+1)/len(data))

    print('\nOutput: ')
    with open(output_name, 'w') as out:
        for row in out_catalog:
            out.write('{}\n'.format(row))
    system('echo "\n" && wc -l {}'.format(output_name))
    print(' ')
