#!/usr/bin/python
'''
----------------------------------------------------------------------
This program is for step1 (star_removal)

Input : c2d HREL catalog

Output : catalog with star, zero, 2mass, one, two, red1, red2 removal
----------------------------------------------------------------------
latest update: 2019/01/02 Jordan Wu'''

# Import Modules
#====================================
from __future__ import print_function
from os import system, path
from sys import argv, exit

# Global Variables
#====================================
objecttype_ID = 17

# Main Programs
#====================================
if __name__ == '__main__':

    # Check inputs
    if len(argv) != 4:
        exit('\n\tError: Wrong Usage\
            \n\tExample: python Star_Removal.py [catalog] [cloud\'s name] [data-Option]\
            \n\t[data-Option]: True/False to delete all data except all_removal catalog\n')

    # Input variables
    table  = str(argv[1])
    cloud  = str(argv[2])
    delete = bool(argv[3] == True)
    print('\nCloud name: {}\nCatalog: {}\nObject type ID: {:d}'.format(cloud, table, objecttype_ID))

    # Check temporary directories
    if path.isdir('tables'):
        system('rm -r tables')
    system('mkdir tables')

    # Generate table's name
    remove_seq_list   = ['star', 'zero', '2mass', 'one', 'two', 'red1', 'red2']
    remove_label_list = ['{}_'.format('_'.join(remove_seq_list[:i+1])) for i in range(len(remove_seq_list)+1)]
    table_name_list   = ['tables/catalog-{}-HREL_{}removal.tbl'.format(cloud, remove_label) for remove_label in remove_label_list]
    star_table_name   = '{}_star.tbl'.format(cloud)
    final_table_name  = 'catalog-{}-HREL_all_star_removal.tbl'.format(cloud)
    all_table_list    = table_name_list + [final_table_name] + [star_table_name]

    # Extract table's data to output table by AWK
    for i in range(len(table_name_list)):
        if i == 0:
            system('awk \'${:d}==\"{}\"\' {} > {}'.format(objecttype_ID, remove_seq_list[i], table, star_table_name))
            system('awk \'${:d}!=\"{}\"\' {} > {}'.format(objecttype_ID, remove_seq_list[i], table, table_name_list[i]))
        elif i == len(remove_seq_list):
            system('cp {} {}'.format(table_name_list[-1], final_table_name))
        else:
            system('awk \'${:d}!=\"{}\"\' {} > {}'.format(objecttype_ID, remove_seq_list[i], table_name_list[i-1], table_name_list[i]))

    # Print out results and deal with temporary files
    print('\n# of lines in tables:')
    for table in all_table_list:
        system('wc -l {}'.format(table))
    if delete: system('rm -rf tables')
