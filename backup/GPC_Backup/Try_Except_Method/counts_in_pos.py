#! bin/python/ -f

from pylab import *
from numpy import *
from sys import argv
from os import chdir, system
#prameter setting
if argv[-1] == '':
    cube = 0.2
else:
    cube = float(argv[-1])

print('cube =' + str(cube) +  '( Default = 0.2)')
Jaxlim=[3.5,22]
Ksaxlim=[4,18]
IR1axlim=[8.0,20]
IR2axlim=[7.0,19]
IR3axlim=[5.0,18]
IR4axlim=[5.0,18]
MP1axlim=[3.5,12]


#End
###Change 5D or 6D => line 107 and 145

binsa=int((Jaxlim[1]-Jaxlim[0])/cube)+1
binsb=int((Ksaxlim[1]-Ksaxlim[0])/cube)+1

bins1=int((IR1axlim[1]-IR1axlim[0])/cube)+1
bins2=int((IR2axlim[1]-IR2axlim[0])/cube)+1
bins3=int((IR3axlim[1]-IR3axlim[0])/cube)+1
bins4=int((IR4axlim[1]-IR4axlim[0])/cube)+1
bins5=int((MP1axlim[1]-MP1axlim[0])/cube)+1
print(binsa,binsb,bins2,bins4,bins5)

from numpy import *
catalog=open('/home/ken/C2D-SWIRE_20180710/Converted_catalog/catalog-SWIRE_UKIDSS_ELAIS_N1_WI_CONDITION.tbl','r')
#catalog = open(argv[-1], 'r')
catalog=catalog.readlines()


def magnitudelist(x):
    x=x.split()
    #flux_list_origin = [float(x[33]),float(x[75]),float(x[96]),float(x[117]),float(x[138]),float(x[159]),float(x[180])]
    flux_list = [float(x[35]),float(x[77]),float(x[98]),float(x[119]),float(x[140]),float(x[161]),float(x[182])]
    #F0_list=[1594000,666700,280900,179700,115000,64130,7140]
    mag_list = []
    for i in range(len(flux_list)):
        if float(flux_list[i])>0:
            mag_list.append(float(flux_list[i]))
        if float(flux_list[i])<=0:
            mag_list.append('no')
    return mag_list

def index(X,Y,a,b): #a,b are transition point, X,Y are input color and mag (data)
    if X<a[0]:
        cutY=b[0]
    elif X>a[len(a)-1]:
        cutY=b[len(a)-1]
    for i in range(len(a)-1):
        if a[i]<X<a[i+1]:
            cutY=b[i]+(b[i+1]-b[i])/(a[i+1]-a[i])*(X-a[i])
        else:
            pass
    value=Y-cutY
    return value

def seq(X,lim):
    if X=='no':
        reu="Lack"
    elif X<lim[0]:
        reu="Bright"
    elif X>lim[1]:
        reu="Faint"
    else:
        reu=int((X-lim[0])/cube)
    return reu
bright = []
pos_vec=[]
print("galaxy position...")
for i in range(len(catalog)):
    if i%100==0:
        print(float(i)/len(catalog))
    line=catalog[i]
    lines = line.split()
    mag_list=magnitudelist(line)
    magJ=mag_list[0];magKs=mag_list[1];magIR1=mag_list[2];magIR2=mag_list[3];magIR3=mag_list[4];magIR4=mag_list[5];magMP1=mag_list[6]


    flux_list_origin = [lines[33],lines[75],lines[96],lines[117],lines[138],lines[159],lines[180]]
    mag_list_origin = [lines[35],lines[77],lines[98],lines[119],lines[140],lines[161],lines[182]]
# remove AGB sources
    AGB = 0
    if magIR2!='no' and magIR3!='no' and magMP1!='no':
        X23=magIR2-magIR3;Y35=magIR3-magMP1
        if index(X23,Y35,[0,0,2,5],[-1,0,2,2])<0:
            AGB = 1
# make grid
    if AGB!=1:
        seqa=seq(magJ,Jaxlim)
        seq1=seq(magIR1,IR1axlim)
        seq2=seq(magIR2,IR2axlim)
        seq3=seq(magIR3,IR3axlim)
        seq4=seq(magIR4,IR4axlim)
        seq5=seq(magMP1,MP1axlim)
        SEQ=[seqa,seq1,seq2,seq3,seq4,seq5] #For six bands
        #SEQ=[seq1,seq2,seq3,seq4,seq5] #For five bands
        pos_vec.append(SEQ)
    if SEQ.count("Bright")>0:
        print(SEQ)
        #bright.append([[magJ, magIR1, magIR2, magIR3, magIR4, magMP1], flux_list_origin, i])
        bright.append([mag_list_origin, flux_list_origin, i])
    if i==262:
        aaa=SEQ

new_pos_vec=[]
faint = []
while True:
    if len(pos_vec)==0:
        break
    first=list(pos_vec[0])
    if first.count("Bright")>0:
        print(first)
        bright.append(first)
    if first.count("Faint")>0:
       faint.append(first) 
    number=0
    print(len(pos_vec))
    for n in pos_vec:
        if n == first:
            number += 1
            pos_vec.remove(n)
    if first==aaa:
        print("NNNNNNNNNNNNnn=",number,first)
    first.append(number)
    new_pos_vec.append(first)
chdir('../')
system('mkdir GPV_6bands_Condition_newlim_bin' + str(cube))
chdir('GPV_6bands_Condition_newlim_bin' + str(cube))
save('Gal_Position_vectors',new_pos_vec)
save('Bright', bright)
save('Faint', faint)
#save('Shape',array([bins1,bins2,bins3,bins4,bins5]))  #For five bands
#save('Shape',array([binsa,binsb,bins2,bins4,bins5]))
save('Shape',array([binsa,bins1,bins2,bins3,bins4,bins5]))  #For six bands
