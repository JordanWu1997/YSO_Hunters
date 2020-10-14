#!/usr/bin/python
'''
----------------------------------------------------------------------
Abstract:
    This is to change python working path for all YSO Hunters programs

Example: [program] [python path]

Input Variables:
    [python path]: python working path or "default"
    [default]    : /usr/bin/python
----------------------------------------------------------------------
Latest updated: 2020/08/01 Jordan Wu'''

from __future__ import print_function
from glob import glob
from os import system
from argparse import ArgumentParser

if __name__ == '__main__':

    # Default argument and parser
    de_path = '/usr/bin/python'
    parser = ArgumentParser(description='Setup python working paths for YSO Hunters.',
                            epilog='Default working path: /usr/bin/python')
    parser.add_argument("-p", dest="py_path", default=de_path, type=str, help="python working path to be set", required=True)
    parser.add_argument("-v", dest="verbose", action='store_true', help="print info verbosely",)
    args = parser.parse_args()
    py_path = args.py_path
    verbose = args.verbose

    # Get file list
    if verbose: print('\nFiles to change head line ...')
    exec_file_list = []
    for dirs in glob('./*'):
        if 'backup' not in dirs.lower():
            for files in glob('{}/*'.format(dirs)):
                if ('.py' in files) and ('.pyc' not in files):
                    exec_file_list.append(files)
                    if verbose: print(files)
    for dirs in glob('./*/'):
        if 'backup' not in dirs.lower():
            for files in glob('{}/*'.format(dirs)):
                if ('.py' in files) and ('.pyc' not in files):
                    exec_file_list.append(files)
                    if verbose: print(files)
    for dirs in glob('./*/*'):
        if 'backup' not in dirs.lower():
            for files in glob('{}/*'.format(dirs)):
                if ('.py' in files) and ('.pyc' not in files):
                    exec_file_list.append(files)
                    if verbose: print(files)

    # Change headline
    headline = '#!{}'.format(py_path)
    if verbose: print('\n{:12}: {}'.format('Default HL', de_path))
    if verbose: print(  '{:12}: {}'.format('New HL', py_path))
    headline = '\/'.join(headline.split('/'))
    # for files in exec_file_list:
        # system("sed -i \'1 s/.*/{}/\' {}".format(headline, files))
