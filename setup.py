#!/usr/bin/python

from glob import glob
from os import system
from sys import argv, exit

print('\nFiles to change head line')
exec_file_list = []
for dirs in glob('./*'):
    for files in glob('{}/*'.format(dirs)):
        if '.py' in files:
            exec_file_list.append(files)
            print(files)

headline = str(argv[1])
for files in exec_file_list:
    system("sed -i \'1s/.*/{}/\' {}".format(headline, files))
print('\nDefault HL: #!/usr/bin/python\
       \nNew HL    : #!{}'.format(headline))
