#!/usr/bin/python
'''
----------------------------------------------------------------
This stores useful functions in YSO Hunter project
----------------------------------------------------------------
Latest update : Jordan Wu'''

from __future__ import print_function
import math as mh
import numpy as np
from numba import jit
import sys

def drawProgressBar(percent, barLen = 50):
    '''
    draw progress bar
    '''
    # percent float from 0 to 1.
    sys.stdout.write("\r")
    sys.stdout.write("[{:<{}}] {:.3f}%".format("=" * int(barLen * percent), barLen, (percent * 100)))
    sys.stdout.flush()

@jit(nopython=True)
def cal_smooth_beam(pos_array, num_array, no_lack_ind, beam):
    '''
    Calculate and smooth every point within a gaussian beam
    '''
    after_beam_smooth_pos = []
    after_beam_smooth_num = []
    for i in range(len(beam)):
        #=========================================================
        # Make New Key from Relative Position
        pos = beam[i]
        rel_pos = pos[:-1]
        new_pos = -999 * np.ones(dim)
        for j in range(len(no_lack_ind)):
            new_pos[no_lack_ind[j]] = pos_array[no_lack_ind[j]] + rel_pos[j]
        #=========================================================
        # Check if New Position Vector within multi-D space
        # Note: upper is from shape which is total num of cube in each dim (index+1)
        pos_check = np.zeros(dim)
        for k in range(len(new_pos)):
            if new_pos[k] != -999.:
                pos_check[k] = new_pos[k]
        if np.all(np.less(pos_check, upper)) and np.all(np.greater_equal(pos_check, lower)):
            weight = float(pos[-1])
            after_beam_smooth_pos.append(new_pos)
            after_beam_smooth_num.append(float(num_array) * weight)
    return after_beam_smooth_pos, after_beam_smooth_num

def sort_up_array_element(input_array):
    '''
    Use this to sort up array (MUST DO before cascade array)
    '''
    input_array_t  = np.transpose(input_array)
    sort_ind_array = np.lexsort(tuple(input_array_t))
    sort_up_array  = input_array[sort_ind_array]
    return sort_ind_array, sort_up_array

@jit(nopython=True)
def cascade_array(sort_pos, sort_num):
    '''
    Use this to find out sources locate in same position and cascade them
    Note: No tuple() support in numba, No format() support in numba
    '''
    #================================================
    # Input
    after_cascade_pos = []
    after_cascade_num = []
    start = 0
    end   = 0
    for i in range(len(sort_num)-1):
        #================================================
        # Indicator
        #if i % 1000 == 0 and i>999:
        #    print(float(i+1)/len(sort_value))
        #================================================
        # Get reference and target
        tar, ref = sort_pos[i], sort_pos[i+1]
        end += 1
        #================================================
        # Determine repeated or not
        if not np.all(np.equal(tar, ref)):
            after_cascade_pos.append(sort_pos[start])
            after_cascade_num.append(np.sum(sort_num[start:end]))
            start = end
    #================================================
    # Include the last term
    after_cascade_pos.append(sort_pos[start])
    after_cascade_num.append(np.sum(sort_num[start:]))
    return after_cascade_pos, after_cascade_num

def cascade_array_same_pos(sort_pos):
    '''
    Use this to find out sources locate in same position and cascade them
    '''
    after_cascade_pos = []
    start = 0
    end   = 0
    for i in range(len(sort_pos)-1):
        tar, ref = sort_pos[i], sort_pos[i+1]
        end += 1
        if not np.all(np.equal(tar, ref)):
            after_cascade_pos.append(sort_pos[start])
            start = end
    after_cascade_pos.append(sort_pos[start])
    return after_cascade_pos

@jit(nopython=True)
def find_pos_id_in_gal_pos(gal_pos, target):
    '''
    This is to find if target in galaxy position array
    '''
    id_list = []
    for i in range(len(gal_pos)):
        if np.all(np.equal(gal_pos[i], target)):
            id_list.append(i)
    id_array = np.array(id_list)
    return id_array

# Main Programs
if __name__ == '__main__':

    from inspect import isfunction

    print('\nPrint All Functions')
    print('#===================================\n')
    for name in dir():
        if isfunction(eval(name)):
            print('{:30}:{:100}'.format(name, str(eval(name))))
    print('\n#===================================\n')
