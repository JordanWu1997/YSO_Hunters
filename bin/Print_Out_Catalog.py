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
import time

# Global Variables
#======================================================

# Functions
#======================================================
def print_out_one_line_default(line, index=0):
    '''
    This is to print well-formatted list for input line
    '''

    print('\n#{}\t{}\t{}'.format('{:<10d}'.format(index),\
                               '{:10}'.format('RA DEC'),\
                               '\t'.join(['{:.7f}'.format(float(line[ID])) for ID in coor_ID])))

    print('#{}\t{}\t{}'.format('{:<10d}'.format(index),\
                                '{:10}'.format('BAND'),\
                                '\t'.join(['{:10}'.format(name) for name in band_name])))

    print('#{}\t{}\t{}'.format('{:<10d}'.format(index),\
                                '{:10}'.format('FLUX'),\
                                '\t'.join(['{:.7f}'.format(float(line[ID])) for ID in flux_ID])))

    print('#{}\t{}\t{}'.format('{:<10d}'.format(index),\
                                '{:10}'.format('MAG'),\
                                '\t'.join(['{:.7f}'.format(float(line[ID])) for ID in mag_ID])))

    print('#{}\t{}\t{}'.format('{:<10d}'.format(index),\
                                '{:10}'.format('QUA'),\
                                '\t'.join(['{:10}'.format(line[ID]) for ID in qua_ID])))

    print('#{}\t{}\t{}'.format('{:<10d}'.format(index),\
                                '{:10}'.format('PSF'),\
                                '\t'.join(['{:10}'.format(line[ID]) for ID in psf_ID])))

    print('#{}\t{}\t{}'.format('{:<10d}'.format(index),\
                                '{:10}'.format('Av MAG'),\
                                '\t'.join(['{:.7f}'.format(float(line[ID])) for ID in Av_ID])))

    print('#{}\t{}\t{}'.format('{:<10d}'.format(index),\
                                '{:10}'.format('C2D label'),\
                                '\t'.join(['{}'.format(line[ID]) for ID in c2d_lab_ID])))

def print_out_one_line_content(line, content, index=0):
    '''
    This is to print out specific content in input line
    '''
    print('#{}\t{}\t{}'.format('{:<10d}'.format(index),\
                               '\t'.join(['{:.7f}'.format(float(line[ID])) for ID in coor_ID]),\
                               '\t'.join(['{}'.format(line[ID]) for ID in eval(content)])))

# Main Program
#======================================================
if __name__ == '__main__':
    t_start = time.time()

    # Check inputs
    if len(argv) != 3:
        exit('\n\tWrong Usage\
              \n\tExample [program] [catalog] [content]\
              \n\t[catalog]: input catalog\
              \n\t[content]: "default" or specific content name\
              \n\n\t***available content***\
              \n\t\t{}\
              \n\t***********************\n'.format(
              '\n\t\t'.join([name for name in dir() if ('ID' in name) and ('f0' not in name)])))

    # Input variables
    catalogs = str(argv[1])
    content  = str(argv[2])
    with open(catalogs, 'r') as inp:
        catalog = inp.readlines()

    # Start printing
    if content == 'default':
        for i in range(len(catalog)):
            line = catalog[i].split()
            print_out_one_line_default(line, index=i+1)
    else:
        if content in dir():
            print('{}\t'.format(content))
            for i in range(len(catalog)):
                line = catalog[i].split()
                print_out_one_line_content(line, content, index=i+1)
        else:
            print('\nContent not found ...')
    print('\n{}'.format(catalogs))

    # Print out input information
    t_end   = time.time()
    print("\n{} took {:.3f} secs\n".format(str(argv[0]), t_end-t_start))
