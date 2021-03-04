#!/usr/bin/env python
'''
--------------------------------------------------------------------------------

Generate Confusion Matrix Program

--------------------------------------------------------------------------------
latest update : 2021/03/05 Jordan Wu'''


# Import Modules
import os
import time
import numpy as np
from All_Variables import *


# Assign parameters
feats  = ['1.0', '0.5']
labels = ['new_BYSO', 'new_IYSO', 'new_Galaxy']
common_med = 'all_GP_Diag'
common_end = 'tbl'


def timeit(method):
    '''
    Measure time consumption
    '''
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('\n%r  took %2.2f ms' % \
                  (method.__name__, (te - ts) * 1000))
        return result
    return timed


def Generate_input_table(**kwarg):
    '''
    Generate table, table_names to plot cf matrix
    '''
    tables, table_names = [], []
    for feat in feats:
        table, table_name = [], []
        for label in labels:
            table.append('{}_{}_{}.{}'.format(feat, common_med, label, common_end))
            table_name.append('{}_{}'.format(feat, label))
        tables.append(table)
        table_names.append(table_name)
    return tables, table_names


def Generate_cf_matrix(tables, table_names):
    '''
    Calculate cf matrix element
    Done by sort and uniq (terminal tools)
    '''
    cf_matrix = np.empty((len(tables[0]), len(tables[1])))
    for i, cat1 in enumerate(tables[0]):
        for j, cat2 in enumerate(tables[1]):
            print_string = 'print ${:d}, ${:d}'.format(coor_ID[0]+1, coor_ID[1]+1)
            os.system("rm -f temp.coor temp.coor.uniq")
            os.system("awk \'{" + print_string + "}\' " + cat1 + "  > temp.coor")
            os.system("awk \'{" + print_string + "}\' " + cat2 + " >> temp.coor")
            os.system("sort temp.coor | uniq -d > temp.coor.uniq")
            with open('{}/temp.coor.uniq'.format(os.getcwd())) as f:
                cf_matrix[i][j] = len(f.readlines())
    os.system("rm -f temp.coor temp.coor.uniq")
    return cf_matrix


def Print_cf_matrix(cf_matrix, tables, table_names):
    '''
    Print out cf matrix
    '''
    print()
    print('H-axis:', tables[1])
    print('V-axis:', tables[0])
    print()
    print(cf_matrix)


@timeit
def main():
    '''
    Main program
    '''
    tables, table_names = Generate_input_table()
    cf_matrix = Generate_cf_matrix(tables, table_names)
    Print_cf_matrix(cf_matrix, tables, table_names)


# Main Program
if __name__ == '__main__':
    main()
