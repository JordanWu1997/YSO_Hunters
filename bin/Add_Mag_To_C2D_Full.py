#!/usr/bin/env python
'''----------------------------------------------------------------
This program is for packing all functions needed for calculating galaxy probability (P)

Example [program] [input name] [output name]

Input Variables
    [input name]:  input catalog name
    [output name]: output catalog name

*Note:
    (1) 6 bands are J, IR1, IR2, IR3, IR4, MP1
    (2) Catalog's format is SWIRE catalog

*New upload"
    (1) function that sets critierion on magnitude with flux_qua of different sources.
    (2) function that sets critierion on magnitude with imtype of different sources.
-------------------------------------------------------------------
latest update : 2020/05/26 Jordan Wu'''

# Load Modules
#======================================================
from __future__ import print_function
from All_Variables import *
from Hsieh_Functions import *
from Useful_Functions import *
from sys import argv, exit
import time
import os

# Global Variables
#======================================================
full_flux_ID     = full_flux_ID
full_flux_err_ID = full_flux_err_ID
full_mag_ID      = full_mag_ID
full_mag_err_ID  = full_mag_err_ID

# Main Programs
#======================================================
if __name__ == '__main__':
    t_start = time.time()

    # Check inputs
    if len(argv) != 3:
        exit('\n\tWrong Usage\
              \n\tExample [program] [input name] [output name]\n')

    # Input variables
    input_name  = str(argv[1])
    output_name = str(argv[2])
    print('\nInput  file: {}\
           \nOutput file: {}'.format(input_name, output_name))

    # Load input catalog
    with open(input_name, 'r') as inp_cat:
        input_cat = inp_cat.readlines()

    # Add magnitudes
    output = []
    for i in range(len(input_cat)):
        # Percentage Indicator
        drawProgressBar(float(i+1)/len(input_cat))
        line = input_cat[i].split()
        mag_list = mJy_to_mag_FULL_C2D(line)
        err_list = mag_error_to_mag_FULL_C2D(line)
        for j in range(len(mag_list)):
            line[full_mag_ID[j]]     = str(mag_list[j])
            line[full_mag_err_ID[j]] = str(err_list[j])
        output.append('\t'.join(line))

    # Save output result
    out_cat = open(str(argv[2]), 'w')
    with open(output_name, 'w') as out_cat:
        for out in output:
            out_cat.write('{}\n'.format(out))
    # Print output info
    os.system('echo "\n" && wc -l {}'.format(output_name))
    t_end   = time.time()
    print('# on input catalog:  {:d}'.format(len(input_cat)))
    print('# on output catalog: {:d}'.format(len(output)))
    print('\nWhole {} process took {:.3f} secs\n'.format(str(argv[0]), t_end-t_start))
