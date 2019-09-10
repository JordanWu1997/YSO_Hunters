import numpy as np
from sys import argv
print('old + new + output')
old = open(argv[-1], 'r')
new = open(argv[-2], 'r')
output = open(argv[-3], 'w')
#outputf = open(argv[-3]+'f', 'w')
n = new.readlines()
o = old.readlines()
print(len(n), len(o))
print('loading')

def delta(dm, F, band):
    if dm >= -100:
        df = (dm/(2.5*np.log10(np.e))) * F
        return df
    else :
        return dm


def flux(mag, band):
    global F0
    if band == 'J':
        F0 = 1530000
    elif band == 'K':
        F0 = 631000
    elif band == 'H':
        F0 == 1019000
    if mag >= -100:
        y = (10**(mag/(-2.5)))*F0
        return y
    else :
        return mag

result = []
fr = []
for line1 in n:
    ra_n = line1.split()[1]
    dec_n = line1.split()[2]
    J = line1.split()[3].replace('E', 'e')
    J = flux(float(J), 'J')
    #J = flux(J, 'J')
    dJ = line1.split()[4].replace('E', 'e')
    dJ = delta(float(dJ), J, 'J')
    #dJ = flux(dJ, 'J')
    H = line1.split()[5].replace('E', 'e')
    H = flux(float(H), 'H')
    #H = flux(H, 'H')
    dH = line1.split()[6].replace('E', 'e')
    dH = delta(float(dH), H, 'H')
    #dH = flux(dH, 'H')
    K = line1.split()[7].replace('E', 'e')
    K = flux(float(K), 'K')
    #K = flux(K, 'K')
    dK = line1.split()[8].replace('E', 'e')
    dK = delta(float(dK), K, 'K')
    #dK = flux(dK, 'K')
    print('new = ' + ra_n + ' ' + dec_n)
    for line in o:
        ra=line.split()[0]
        dec=line.split()[2]
        #print(ra, dec)
        if float(ra) == float(ra_n) and float(dec) == float(dec_n) :
            print(J, dJ, H, dH, K, dK)
            exchanged = line.split()[:33] + [J] + [dJ] + line.split()[35:54] + [H] + [dH] + line.split()[56:75] + [K] + [dK] + line.split()[77:]
            #fr.append(exchanged)
            print(exchanged[33], exchanged[34], exchanged[54], exchanged[55], exchanged[75], exchanged[76])
            se = "\t".join([str(e) for e in exchanged])
            result.append(se)
            break


#print(len(old))
print(len(result))
re = "\n".join([e for e in result])
#print(len(re))
output.write(re)
#output.write(fr)
