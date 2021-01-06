#!/usr/bin/env python
'''
#-----------------------------------------------------------
Lastest Change: (1) Unify indents of all code lines
                (2) Change value of Gal_Prob for case (GP=0)
                    It will be assigned as GP=1e-9

20190227 Jordan Wu
#-----------------------------------------------------------
'''

from numpy import *
from sys import argv
import SOP_Program_Path as spp

#path="/cosmo/users/inchone/Remove_Av_sources_in_whole_clouds/SWI_c2d_PSD_new_process2_multi-dim_version/J_MP1_plus_IR1_MP1_methed/c2d_SWIRE_IR1-MP1/"

path = spp.Hsieh_5D_GP2_Array_path
print "Loading array"
fid_smooth_array=load(path+"All_grid/all_detect_grid.npy")
array_matrix=[[0 for i in range(5)] for i in range(5)]
for A in range(5):
    for B in range(A+1):
	arr=load(path+"All_grid/Lack_band_"+str(B+1)+str(A+1)+"_grid.npy")
	array_matrix[B][A]=arr

print "Loading catalog"
#catalog=open(argv[-1])
catalog=open("step")
catalog=catalog.readlines()

#parameter
cube=0.2
IR1axlim=[8.0,18.0]
IR2axlim=[7.0,18.0]
IR3axlim=[5.0,18.0]
IR4axlim=[5.0,18.0]
MP1axlim=[3.5,11.0]

band_name=['IR1','IR2','IR3','IR4','MP1']
def magnitudelist(x):
    flux_list=[float(x[96]),float(x[117]),float(x[138]),float(x[159]),float(x[180])]
    flux_Qua=[x[100],x[121],x[142],x[163],x[184]]
    F0_list=[280900,179700,115000,64130,7140]
    mag_list=[]
    for i in range(len(F0_list)):
        if flux_Qua[i]=="A" or  flux_Qua[i]=="B" or flux_Qua[i]=="C" or flux_Qua[i]=="D" or flux_Qua[i]=="K":
            mag_list.append(-2.5*log10(float(flux_list[i])/F0_list[i]))
	elif flux_Qua[i]=="S":
	    mag_list.append(-100)
	elif flux_Qua[i]=="N":
	    mag_list=['no','no','no','no','no','no','no']
	    break
        else:
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

out=[]; YSO_PSF_bad=[]; YSO_PSFcheck=[]; YSO_bandfill01=[]
for i in range(len(catalog)):
    if i%100==0:
	print float(i)/len(catalog)
    line=catalog[i].split()
    mag_list=magnitudelist(line)
    magIR1=mag_list[0];magIR2=mag_list[1];magIR3=mag_list[2];magIR4=mag_list[3];magMP1=mag_list[4]
    PSF_list=[line[102],line[123],line[144],line[165],line[186]]
#calculate
    SEQ=[seq(magIR1,IR1axlim),seq(magIR2,IR2axlim),seq(magIR3,IR3axlim),seq(magIR4,IR4axlim),seq(magMP1,MP1axlim)]
#number of detected bands
    num=5-SEQ.count("Lack")
    type=str(num)+"bands_"
    count="no_count"
#Remove AGB
    de="unknown"
    if magIR2!='no' and magIR3!='no' and magMP1!='no':
        X23=magIR2-magIR3;Y35=magIR3-magMP1
        if index(X23,Y35,[0,0,2,5],[-1,0,2,2])<0:
	    de="AGB"
            type += "AGB_"
	    count="no_count"
#count calculate i.e fall in grid
    if num>=3 and de!="AGB":
        if SEQ.count("Faint")>0:
            type += "Faint"
            count=99999
        elif SEQ.count("Bright")>0:
            type += "Bright"
            count=10**-4
	elif num==5:
	    count=fid_smooth_array[SEQ[0]][SEQ[1]][SEQ[2]][SEQ[3]][SEQ[4]]
	elif num==4:
	    L1=SEQ.index("Lack")
	    del SEQ[L1]
	    count=array_matrix[L1][L1][SEQ[0]][SEQ[1]][SEQ[2]][SEQ[3]]
	    type += "Lack_" + band_name[L1]
	elif num==3:
	    L1=SEQ.index("Lack")
	    del SEQ[L1]
	    L2=SEQ.index("Lack")
	    del SEQ[L2]
	    L2 += 1
	    type += "Lack_" + band_name[L1] + band_name[L2]
	    count=array_matrix[L1][L2][SEQ[0]][SEQ[1]][SEQ[2]]
#==========================================
        if count==0.0:
            count=10**-9 #original: 1e-3
#=========================================
    if line[184]=="S":
        count==10**-4
    type += "bandfill="+str(PSF_list.count("-2"))
    line.append('Z')
    line.append('Z')
    line[235]=type
    line[236]=str(count)
    out.append("\t".join(line))
out="\n".join(out) + "\n"
out_ca=open("Out_catalog","w")
out_ca.write(out)
