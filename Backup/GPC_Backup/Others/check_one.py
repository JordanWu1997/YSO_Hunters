import numpy as np
from sys import argv

GPS = np.load(argv[-1]).item()
one = 0
for i in GPS.values() :
    if float(i) >= 1:
        one += 1

print(str(one) + '/' + str(len(GPS.values())))
