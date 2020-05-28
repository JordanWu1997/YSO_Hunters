#!/usr/bin/python
'''
------------------------------------------------------------------------------
Abstract:
    This program is for comparing two different catalogs.
    One can check if the object on two different catalogs is a same source,
    or One can check if even some same sources have different property (e.g. flux)
    This program can also provide (1)Interaction of two catalogs
                                  (2)different catalogs' Complement

Example: [program] [input catalog] [reference] [input_name] [ref_name] [round_to] [only_coor]

Input Variables:
    [input catalog]: input catalog
    [reference]:     catalog as reference (default Hsieh all YSO catalog (1310))
    [input_name]:    assign name to input catalog (default "A")
    [ref_name]:      assign name to reference catalog (default "B")
    [round_to]:      decimal digits round to
    [only_coor]:     print out catalog only with coordinates RA, DEC [True/False]\n')

------------------------------------------------------------------------------
Latest update: 2020/05/27 Jordan Wu
'''

# Import Modules
#======================================================
from __future__ import print_function
from sys import argv, exit
import SOP_Program_Path as spp
from Useful_Functions import *
import time

# Global Variables
#======================================================
inp_coor_ID = [0, 2]
ref_coor_ID = [0, 2]
round_to    = 7

# Functions
#======================================================
def check_if_same_source(inp_list, ref_list, round_to=round_to, inp_coor_ID=inp_coor_ID, ref_coor_ID=ref_coor_ID):
    '''
    This is to check RA, DEC on catalogs if both inputs are identical source
    '''
    inp_RA, inp_DEC = inp_list[inp_coor_ID[0]], inp_list[inp_coor_ID[1]]
    ref_RA, ref_DEC = ref_list[ref_coor_ID[0]], ref_list[ref_coor_ID[1]]
    label = 'NOT_SAME'
    if (round(float(inp_RA), round_to) == round(float(ref_RA), round_to)) and \
       (round(float(inp_DEC), round_to) == round(float(ref_DEC), round_to)):
        label = 'SAME'
    return label

def find_input_same(inp_lines, ref_lines):
    '''
    This is to find same (INP^REF)
    '''
    SAME_num, SAME_list = 0, []
    for i, inp_line in enumerate(inp_lines):
        drawProgressBar(float(i+1)/len(inp_lines))
        inp = inp_line.split()
        for ref_line in ref_lines:
            ref = ref_line.split()
            if check_if_same_source(inp, ref) == 'SAME':
                SAME_list.append(inp)
                SAME_num += 1
                break
    return SAME_num, SAME_list

def find_input_diff(inp_lines, same_lines):
    '''
    This is to find diff (INP-SAME)
    '''
    DIFF_num, DIFF_list = 0, []
    for i, inp_line in enumerate(inp_lines):
        drawProgressBar(float(i+1)/len(inp_lines))
        inp = inp_line.split()
        flag = 'DIFF'
        for same_line in same_lines:
            if check_if_same_source(inp, same_line) == 'SAME':
                flag = 'SAME'
        if flag == 'DIFF':
            DIFF_list.append(inp)
            DIFF_num += 1
    return DIFF_num, DIFF_list

# Main Programs
#======================================================
if __name__ == '__main__':
    t_start = time.time()

    # Check inputs
    if len(argv) != 7:
        exit('\n\tERROR! Wrong Arguments!\
              \n\tExample: [Program] [input catalog] [reference] [input_name] [ref_name] [round_to] [only_coor]\
              \n\t[input catalog]: input catalog\
              \n\t[reference]: catalog as reference (default Hsieh all YSO catalog (1310))\
              \n\t[input_name]: assign name to input catalog (default "A")\
              \n\t[ref_name]: assign name to reference catalog (default "B")\
              \n\t[round_to]: decimal digits round to\
              \n\t[only_coor]: print out catalog only with coordinates RA, DEC [True/False]\n')

    # Input variables
    inp_catalog = str(argv[1])
    ref_catalog = str(argv[2])
    inp_name    = str(argv[3]) #default A
    ref_name    = str(argv[4]) #default B
    round_to    = int(argv[5])
    only_coor   = bool(argv[6] == 'True')
    if inp_name == 'default':
        inp_name = 'A'
    if ref_name == 'default':
        ref_name = 'B'
    if ref_catalog == 'default':
        ref_catalog = '{}all_candidates.tbl'.format(spp.Hsieh_YSO_List_path)
        ref_name    = 'all_Hsieh_YSOc'

   # Print info
    print('\nRunning {}'.format(str(argv[0])))
    print('\nInput        : {:20} ({:10})\
           \nRefer        : {:20} ({:10})\
           \nInp_Coord_ID : {:20}\
           \nRef_Coord_ID : {:20}\
           \nRound digit  : {:d}'\
           .format(inp_catalog, inp_name, ref_catalog, ref_name, str(inp_coor_ID), str(ref_coor_ID), round_to))

    # Load catalogs ...
    with open(inp_catalog, 'r') as inp:
        inp_lines = inp.readlines()
    with open(ref_catalog, 'r') as ref:
        ref_lines = ref.readlines()

    # Start find intersection and minus ...
    INP_num, REF_num = len(inp_lines), len(ref_lines)
    print('\nIntersection {} ^ {}...'.format(inp_name, ref_name))
    SAME_num, SAME_list = find_input_same(inp_lines, ref_lines)
    print('\nMinus {} ...'.format(inp_name))
    INP_DIFF_num, INP_DIFF_list = find_input_diff(inp_lines, SAME_list)
    print('\nMinus {} ...'.format(ref_name))
    REF_DIFF_num, REF_DIFF_list = find_input_diff(ref_lines, SAME_list)

    # Print statistics ...
    print('\n\n{:30}: {:<10d}\
           \n{:30}: {:<10d}\
           \n{:30}: {:<10d}\
           \n{:30}: {:<10d}\
           \n{:30}: {:<10d}\n'\
           .format(\
           '#INP', INP_num,\
           '#REF', REF_num,\
           '#SAME (INP^REF)', SAME_num,\
           '#DIFF ({} - SAME)'.format(inp_name), INP_DIFF_num,\
           '#DIFF ({} - SAME)'.format(ref_name), REF_DIFF_num))

    # Save results ...
    with open('AND_{}_{}.tbl'.format(inp_name, ref_name), 'w') as output:
        for i in range(len(SAME_list)):
            if only_coor:
                output.write('{}\n'.format('\t'.join([SAME_list[i][inp_coor_ID[0]], SAME_list[i][inp_coor_ID[1]]])))
            else:
                output.write('{}\n'.format('\t'.join(SAME_list[i])))
    with open('DIFF_{}.tbl'.format(inp_name), 'w') as output:
        for i in range(len(INP_DIFF_list)):
            if only_coor:
                output.write('{}\n'.format('\t'.join([INP_DIFF_list[i][inp_coor_ID[0]], INP_DIFF_list[i][inp_coor_ID[1]]])))
            else:
                output.write('{}\n'.format('\t'.join(INP_DIFF_list[i])))
    with open('DIFF_{}.tbl'.format(ref_name), 'w') as output:
        for i in range(len(REF_DIFF_list)):
            if only_coor:
                output.write('{}\n'.format('\t'.join([REF_DIFF_list[i][inp_coor_ID[0]], REF_DIFF_list[i][inp_coor_ID[1]]])))
            else:
                output.write('{}\n'.format('\t'.join(REF_DIFF_list[i])))

    # Print time consumption ...
    t_end   = time.time()
    print('Whole {} process took {:.3f} secs\n'.format(str(argv[0]), t_end-t_start))
