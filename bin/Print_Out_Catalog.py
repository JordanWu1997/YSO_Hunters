#!/usr/bin/python
'''
-------------------------------------------------------
Example [program] [catalog] [content]
Input Variables:
    [catalog]: input catalog
    [content]: "default" or specific content name
-------------------------------------------------------
Latest update: 2020/05/27 Jordan Wu'''

# Load Modules
#======================================================
from __future__ import print_function
from sys import argv, exit
from Hsieh_Functions import *
from Useful_Functions import *
import inspect
import time

# Global Variables
#======================================================
GP_OBJ_ID,  GP_VAL_ID   = 241, 242
GPP_OBJ_ID, GPP_VAL_ID  = 243, 244
GP_GPP_ID = [241, 242, 243, 244, 245]
VAR_list = [var for var in dir() if 'ID' in var]
ID_list  = ['flux_ID', 'mag_ID', 'qua_ID', 'psf_ID', 'Av_ID', 'c2d_lab_ID', 'GP_GPP_ID']

# Functions
#======================================================
def retrieve_name(var):
    '''
    This is to get variables name in "STRING"
    '''
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]

def print_out_one_line_default(line, index=0, ID_list=ID_list, VAR_list=VAR_list):
    '''
    This is to print well-formatted list for input line
    '''
    # Print Coordinate (RA, DEC) and Band Name
    print('\n{:120}'.format(''.join(['='] * 120)))
    print('#{}\t{}\t{}'.format('{:<10d}'.format(index), '{:10}'.format('RA DEC'),\
                               '\t'.join(['{:.7f}'.format(float(line[ID])) for ID in coor_ID])))
    print('#{}\t{}\t{}'.format('{:<10d}'.format(index), '{:10}'.format('BAND'),\
                                '\t'.join(['{:10}'.format(name) for name in band_name])))
    # Print out different IDs
    for IDs in ID_list:
        if IDs in VAR_list:
            try:
                output = '\t'.join(['{:.7f}'.format(float(line[ID])) for ID in eval(IDs)])
                print('#{}\t{}\t{}'.format('{:<10d}'.format(index), '{:10}'.format(IDs.strip('_ID')), output))
            except ValueError:
                output = '\t'.join(['{:10}'.format(str(line[ID])) for ID in eval(IDs)])
                print('#{}\t{}\t{}'.format('{:<10d}'.format(index), '{:10}'.format(IDs.strip('_ID')), output))
            except IndexError:
                output = 'NOT FOUND'
                print('#{}\t{}\t{}'.format('{:10}'.format(index), '{:10}'.format(IDs.strip('_ID')), output))
    print('{:120}'.format(''.join(['='] * 120)))

def print_out_one_line_content(line, content, index=0, coor_ID=coor_ID):
    '''
    This is to print out specific content in input line
    '''
    print('#{}\t{}\t{}'.format('{:<10d}'.format(index),\
                               '\t'.join(['{:.7f}'.format(float(line[ID])) for ID in coor_ID]),\
                               '\t'.join(['{:10}'.format(line[ID]) for ID in eval(content)])))

# Main Program
#======================================================
if __name__ == '__main__':
    t_start = time.time()

    # Check inputs
    if len(argv) != 4:
        exit('\n\tWrong Usage\
              \n\tExample [program] [catalog] [content]\
              \n\t[catalog]: input catalog\
              \n\t[content]: "default" or specific content name\
              \n\t[Index]  : "all" or a specific range e.g "1~10"\
              \n\n\t***available content***\
              \n\t\t{}\
              \n\t***********************\n'.format(
              '\n\t\t'.join([name for name in dir() if ('ID' in name) and ('f0' not in name)])))

    # Input variables
    catalogs = str(argv[1])
    content  = str(argv[2])
    index_op = str(argv[3])

    # Set up printing regions
    with open(catalogs, 'r') as inp:
        catalog = inp.readlines()
    if index_op != 'all':
        line_index = index_op.split('~')
        if len(line_index) != 1:
            indice = range(int(line_index[0]), int(line_index[1])+1)
        else:
            indice = range(int(line_index[0]), int(line_index[0])+1)
    else:
        indice = range(len(catalog))

    # Start printing
    if content == 'default':
        print(' ')
        for i in indice:
            line = catalog[i].split()
            print(len(line))
            print_out_one_line_default(line, index=i)
    else:
        if content in dir():
            print('\n{:10}\n'.format(content))
            for i in indice:
                line = catalog[i].split()
                print_out_one_line_content(line, content, index=i)
        else:
            print('\nContent not found ...')
    print('\n{}'.format(catalogs))

    # Print out input information
    t_end   = time.time()
    print("\n{} took {:.3f} secs\n".format(str(argv[0]), t_end-t_start))
