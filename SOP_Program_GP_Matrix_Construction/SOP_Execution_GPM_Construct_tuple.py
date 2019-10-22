#!/usr/bin/ipython
'''---------------------------------------------------------------------------------


------------------------------------------------------------------------------------
latest update : 2019/10/20 Jordan Wu'''

from sys import argv, exit
from os import system

if len(argv) != 6:
    exit('\n\tError: Wrong Arguments\
    \n\tExample: [program] [catalog] [dimension] [binsize] [sigma] [ref-D]\
    \n\t[catalog]: SWIRE format catalog (with calculated magnitude)\
    \n\t[dimension]: Dimension of multi-D method\
    \n\t[binsize]: length of each bin\
    \n\t[sigma]: STD for Gaussian smooth (unit: bin) usually as 2\
    \n\t[ref-D]: binsize reference dimension\n')

catalog = str(argv[1])
dim     = int(argv[2])
cube    = float(argv[3])
sigma   = int(argv[4])
ref     = int(argv[5])

system('counts_in_pos.py ' + catalog + ' ' + str(dim) + ' ' + str(cube))
system('gaussian_beam.py ' + str(sigma) + ' ' + str(ref))
system('new_sgm_Full_tuple.py '  + str(dim) + ' ' + str(cube) + ' ' + str(sigma) + ' ' + str(ref))
