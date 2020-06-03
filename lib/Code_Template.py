#!/usr/bin/python
'''
--------------------------------------------------------
Abstract:
    This is a program for ...

Example:
    [program] [] [] ...

    Input variables:
        []:
        []:

Editor:
    Jordan Wu
Email:
    jordankhwu@gmail.com
Note:
    (1)
    (2)
TODO:
    (1)
    (2)

Update log:
    - YYYY/MM/DD First created

####################################
#   Python2                        #
#   This code is made in python2   #
####################################
-------------------------------------------------------
'''

# Load Modules
#======================================================
from __future__ import print_function
from All_Variables import *
from Hsieh_Functions import *
from Useful_Functions import *
from sys import argv, exit
import numpy as np
import time

# Global Variables
#======================================================

# Functions
#======================================================

# Main Program
#======================================================
if __name__ == '__main__':
    t_start = time.time()

    # Check inputs
    if len(argv) != 1:
        exit('\n\t')

    # Input variables

    # Check directory/files

    # Print out input information
    t_end   = time.time()
    print("{} took {:.3f} secs\n".format(str(argv[0]), t_end-t_start))
