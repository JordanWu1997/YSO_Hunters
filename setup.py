#!/usr/bin/python
'''
----------------------------------------------------------------------
Abstract:
    This is to change python working path for all YSO Hunters programs

Example: [program] [python path]

Input Variables:
    [python path]: python working path
----------------------------------------------------------------------
Latest updated: 2020/06/04 Jordan Wu'''

from glob import glob
from os import system
from sys import argv, exit

if __name__ == '__main__':

    # Check inputs
    if len(argv) != 2:
        exit('\n\tExample: [program] [python path]\
              \n\t[python path]: python working path\n')

    # Get file list
    print('\nFiles to change head line')
    exec_file_list = []
    for dirs in glob('./*'):
        for files in glob('{}/*'.format(dirs)):
            if '.py' in files:
                exec_file_list.append(files)
                print(files)

    # Change headline
    headline = '#!{}'.format(str(argv[1]))
    if headline == 'default':
        headline = '#!/usr/bin/python'
    for files in exec_file_list:
        system("sed -i '1s/.*/{}/' {}".format(headline, files))
    print('\nDefault HL: #!/usr/bin/python\
           \nNew HL    : {}'.format(headline))
