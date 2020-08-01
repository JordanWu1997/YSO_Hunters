#!/usr/bin/python
'''
-------------------------------------------------------
Example [program] [catalog] [content] [index]
Input Variables:
    [catalog]: input catalog
    [content]: "default" or specific content name
    [Index]  : "all" or a specific range e.g "1~10"\

-------------------------------------------------------
Latest update: 2020/05/27 Jordan Wu'''

# Load Modules
#======================================================
from __future__ import print_function
from argparse import ArgumentParser
import inspect
import time
from All_Variables import *
from Hsieh_Functions import *
from Useful_Functions import *

# Global Variables
#======================================================
GP_OBJ_ID,  GP_VAL_ID   = 241, 242
GPP_OBJ_ID, GPP_VAL_ID  = 243, 244
GP_ID  = [241, 242]
GPP_ID = [243, 244]
KEY_ID = [245]
VAR_list = [var for var in dir() if 'ID' in var]
ID_list  = ['flux_ID', 'mag_ID', 'qua_ID', 'psf_ID', 'Av_ID', 'c2d_lab_ID', 'GP_ID', 'GPP_ID', 'KEY_ID']

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
            except IndexError:
                output = 'NOT FOUND'
            except ValueError:
                try:
                    output = '\t'.join(['{:10}'.format(str(line[ID])) for ID in eval(IDs)])
                except IndexError:
                    output = 'NOT FOUND'
            print('#{}\t{}\t{}'.format('{:<10d}'.format(index), '{:10}'.format(IDs.strip('_ID')), output))
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

    # Parser arguments
    parser = ArgumentParser(description="Print out catalog information",\
                            epilog="Available content:{}".format('\t'.join([name for name in dir()\
                            if ('ID' in name) and ('f0' not in name) and ('UKIDSS' not in name) and (name != 'ID_list')])))
    parser.add_argument("inp_cat", type=str, help="Input catalog to print")
    parser.add_argument("content", default="default", type=str, help="Content to print or 'default'")
    parser.add_argument("-is", "--index_start", default=0, dest="index_s", type=int, help="Assign content start index")
    parser.add_argument("-ie", "--index_end", default=-1, dest="index_e", type=int, help="Assign content end index")
    args = parser.parse_args()
    inp_cat = args.inp_cat
    content = args.content
    index_s = args.index_s
    index_e = args.index_e

    # Set up printing regions
    with open(inp_cat, 'r') as inp:
        catalog = inp.readlines()
    catalog = catalog[index_s:index_e]

    # Start printing
    if content == 'default':
        print(' ')
        for i in range(len(catalog)):
            line = catalog[i].split()
            print_out_one_line_default(line, index=i)
    else:
        if content in dir():
            print('\n{:10}\n'.format(content))
            for i in range(len(catalog)):
                line = catalog[i].split()
                print_out_one_line_content(line, content, index=i)
        else:
            print('\nContent not found ...')
    print('\n{}'.format(inp_cat))

    # Print out input information
    t_end   = time.time()
    print("\n{} took {:.3f} secs\n".format(parser.prog, t_end-t_start))
