#!/usr/bin/python
'''
Executing following programs
# Sort_Source_Lack999.py [program] [sigma] [bond] [ref-D]
# Sort_Source_Lack999_Project.py [program] [dim] [cube size]
# Sort_Source_Lack999_Cascade.py [program] [dim] [cube size]
# Sort_Source_Lack999_Band.py [program] [dim] [cube size]
'''
from __future__ import print_function
import time
from os import system

if len(argv) != 3:
    exit('\n\tError: Wrong Arguments\
    \n\tExample: [program] [dim] [cube size]\
    \n\t[dim]: dim of magnitude space (for now only "6")\
    \n\t[cube size]: length of multi-d cube in magnitude unit\n')

# Input Variables
#=======================================================
dim      = int(argv[1])       # Dimension of multi-D method
cube     = float(argv[2])     # Beamsize for each cube

# Main Program
#=======================================================
if __name__ == '__main__':
    all_start = time.time()
    # Sort_Source_Lack999.py
    system('{} {:d} {:.1f}'.format('Sort_Source_Lack999.py', dim, cube))
    # Sort_Source_Lack999_Project.py
    system('{} {:d} {:.1f}'.format('Sort_Source_Lack999_Project.py', dim, cube))
    # Sort_Source_Lack999_Cascade.py
    system('{} {:d} {:.1f}'.format('Sort_Source_Lack999_Cascade.py', dim, cube))
    # Sort_Source_Lack999_Band.py
    system('{} {:d} {:.1f}'.format('Sort_Source_Lack999_Band.py', dim, cube))
    all_end   = time.time()
    print('\n{} took {:.3f} secs\n'.format(argv[0], all_end-all_start))
