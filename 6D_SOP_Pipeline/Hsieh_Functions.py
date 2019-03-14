#!/usr/bin/ipython
'''----------------------------------------------------------------
This program is for packing all functions needed for calculating galaxy probability (P)

*Note: 
    (1)6 bands are J, IR1, IR2, IR3, IR4, MP1
    (2)Catalog's format is SWIRE catalog
-------------------------------------------------------------------
latest update : 2019/02/20 Jordan Wu'''

#--------------------------------------------------------------------------------------------------------------
import numpy as np

cube=0.2
Jaxlim=[4.0,18.0]
Ksaxlim=[4.0,18.0]
IR1axlim=[8.0,18]
IR2axlim=[7.0,18.0]
IR3axlim=[5.0,17]
IR4axlim=[5.0,18.0]
MP1axlim=[3.5,11.0]

#--------------------------------------------------------------------------------------------------------------

def magnitudelist(x):
    '''
    This function is to change fluxes on the catalog to magnitudes
    This is for counting galaxy probability
    '''
    flux_list=[float(x[33]),float(x[96]),float(x[117]),float(x[138]),float(x[159]),float(x[180])]
    F0_list=[1594000,280900,179700,115000,64130,7140]
    flux_Qua=[x[37],x[100],x[121],x[142],x[163],x[184]]
    mag_list=[]
    for i in range(len(F0_list)):    
        # J band
        if i==0:
            if flux_list[i]>0:
                mag_list.append(-2.5*np.log10(float(flux_list[i])/F0_list[i]))
            else:
                mag_list.append('no')
        # IR1,IR2,IR3,IR4,MP1 band     
        elif flux_Qua[i]=="A" or  flux_Qua[i]=="B" or flux_Qua[i]=="C" or flux_Qua[i]=="D" or flux_Qua[i]=="K":
            mag_list.append(-2.5*np.log10(float(flux_list[i])/F0_list[i]))
        
        # Qua labeled as 'S' (saturate candidate)
        elif flux_Qua[i]=="S":
            mag_list.append(-100)
        
        # Qua labeled as 'N' (not detected)
        elif flux_Qua[i]=="N":
            mag_list=['no','no','no','no','no','no']
            break

        # Qua labeled as 'U' (upper-limit)
        else:
            mag_list.append('no')

    return mag_list
#--------------------------------------------------------------------------------------------------------------
def PSF_magnitudelist(x):
    '''
    This function is to change fluxes on the catalog to magnitudes and select whose imagetype=1
    This is for counting Galaxy Probability P
    '''
    flux_list=[float(x[33]),float(x[96]),float(x[117]),float(x[138]),float(x[159]),float(x[180])]
    F0_list=[1594000,280900,179700,115000,64130,7140]
    flux_Qua=[x[37],x[100],x[121],x[142],x[163],x[184]]
    PSF_list=[x[39],x[102],x[123],x[144],x[165],x[186]]
    mag_list=[]
    for i in range(len(F0_list)):
        if i==0:
            if flux_list[i]>0:
                mag_list.append(-2.5*np.log10(float(flux_list[i])/F0_list[i]))
            else:
                mag_list.append('no')
        elif PSF_list[i]!="1" and flux_Qua[i]!="S":
            mag_list.append('no')
        elif flux_Qua[i]=="A" or  flux_Qua[i]=="B" or flux_Qua[i]=="C" or flux_Qua[i]=="D" or flux_Qua[i]=="K":
            mag_list.append(-2.5*np.log10(float(flux_list[i])/F0_list[i]))
        elif flux_Qua[i]=="S":
            mag_list.append(-100)
        elif flux_Qua[i]=="N":
            mag_list=['no','no','no','no','no','no','no']
            break
        else:
            mag_list.append('no')
    return mag_list
#--------------------------------------------------------------------------------------------------------------
def index(X,Y,a,b): #a,b are transition point, X,Y are input color and mag (data)
    '''
    This function is to determine if the object is an AGB or not
    '''
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
#--------------------------------------------------------------------------------------------------------------
def seq(X,lim):
    '''
    This function is to put criterions we set for multi-d spaces onto the object 
    '''
    if X=='no':
        reu="Lack"
    elif X<lim[0]:
        reu="Bright"
    elif X>lim[1]:
        reu="Faint"
    else:
        reu=int((X-lim[0])/cube)
    return reu
#--------------------------------------------------------------------------------------------------------------
