#!/usr/bin/env python
'''
----------------------------------------------------------------

Example: [program] [method]
Input Variables:
    [method]:     method of calculating GP [BD/GD]
    [cloud name]: name of cloud of input catalog

----------------------------------------------------------------
Latest update: 2020/10/14 Jordan Wu'''

# Import Modules
#======================================================================================
from __future__ import print_function
from sys import argv, exit
import numpy as np
import time
from All_Variables import *
from Hsieh_Functions import *
from Useful_Functions import *
import SOP_Program_Path as spp

# Main Programs
#======================================================================================
if __name__ == '__main__':
    m_start = time.time()

    # Check inputs
    if len(argv) != 3:
        exit('\n\tError: Wrong Usage!\
              \n\tExample: [program] [cloud name] [method] \
              \n\t[cloud name]: name of cloud of input catalog \
              \n\t[method]: method of calculating GP [BD/GD/Diag]\n')
    else:
        print('\nStart merging ...')

    # Setup catalog prefix
    cloud_name = str(argv[1])
    method     = str(argv[2])

    if method == 'BD':
        prefix = 'BD_'
    elif method = 'Diag':
        prefix = 'Diag_'
    else:
        prefix = ''
    catalog_5D1_name = '{}_5D1_{}GP_out_catalog.tbl'.format(cloud_name, prefix)
    catalog_5D2_name = '{}_5D2_{}GP_out_catalog.tbl'.format(cloud_name, prefix)
    out_catalog_name = '{}_5D_tot_{}GP_out_catalog.tbl'.format(cloud_name, prefix)

    # Load catalog
    with open(catalog_5D1_name, 'r') as catalog:
        catalog_5D1 = catalog.readlines()
    with open(catalog_5D2_name, 'r') as catalog:
        catalog_5D2 = catalog.readlines()

    # Generate property indice to be merged
    ind_to_merge = [GP_OBJ_ID_5D2, \
                    GP_ID_5D2, \
                    GPP_OBJ_ID_5D2, \
                    GPP_ID_5D2, \
                    GP_KEY_ID_5D2]

    # Start merging
    result_5D_tot = []
    for i in range(len(catalog_5D1)):
        result_5D1 = catalog_5D1[i].split()
        result_5D2 = catalog_5D2[i].split()
        for ind in ind_to_merge:
            result_5D1[ind] = result_5D2[ind]
        result_5D_tot.append('\t'.join(result_5D1))

    # Save result
    with open(out_catalog_name, 'w') as out_catalog:
        out_catalog.write('\n'.join(result_5D_tot) + '\n')
    m_end   = time.time()
    print('\nWhole {} process took {:.3f} secs\n'.format(str(argv[0]), m_end-m_start))
