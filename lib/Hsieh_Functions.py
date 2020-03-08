#!/usr/bin/python
'''----------------------------------------------------------------
This program is for packing all functions needed for calculating galaxy probability (P)

*Note:
    (1)6 bands are J, IR1, IR2, IR3, IR4, MP1
    (2)Catalog's format is SWIRE catalog

*New upload"
    (1)function that sets critierion on magnitude with flux_qua of different sources.
    (2)function that sets critierion on magnitude with imtype of different sources.
-------------------------------------------------------------------
latest update : 2019/02/20 Jordan Wu'''

import math as mh
import numpy as np

#==============================================================================
# Flux ID: J, IR1, IR2, IR3, IR4, MP1 (2MASS + Spitzer)
flux_ID = [33, 96, 117, 138, 159, 180]
# Mag ID:  J, IR1, IR2, IR3, IR4, MP1 (2MASS/UKIDSS + Spitzer)
mag_ID  = [35, 98, 119, 140, 161, 182]
# Qua ID:  J, IR1, IR2, IR3, IR4, MP1 (2MASS + Spitzer)
qua_ID  = [0, 100, 121, 142, 163, 184]
# PSF_ID:  J, IR1, IR2, IR3, IR4, MP1 (2MASS + Spitzer)
psf_ID  = [0, 102, 123, 144, 165, 186]
# F0 (mJy): J, IR1, IR2, IR3, IR4, MP1
f0_2MASS_Spitzer = [1594000, 280900, 179700, 115000, 64130, 7140]  # H: 1024000
f0_UKIDSS_Spitzer = [1530000, 280900, 179700, 115000, 64130, 7140] # H: 1019000
# Band name
band_name = ['J', 'IR1', 'IR2', 'IR3', 'IR4', 'MP1']
#==============================================================================

# HSIEH'S BOUNDARY
Hsieh_Jaxlim   = [4.0, 18.0]
Hsieh_Ksaxlim  = [8.0, 18.0]
Hsieh_IR1axlim = [8.0, 18.0]
Hsieh_IR2axlim = [7.0, 18.0]
Hsieh_IR3axlim = [5.0, 18.0]
Hsieh_IR4axlim = [5.0, 18.0]
Hsieh_MP1axlim = [3.5, 11.0]
# NEW BOUNDARY WI UKIDSS CATALOG
Jaxlim   = [3.5, 22.0]
Ksaxlim  = [8.0, 18.0]
IR1axlim = [8.0, 20.0]
IR2axlim = [7.0, 19.0]
IR3axlim = [5.0, 18.0]
IR4axlim = [5.0, 18.0]
MP1axlim = [3.5, 12.0]

#==============================================================================

def mJy_to_mag(x, flux_ID=flux_ID, qua_ID=qua_ID, Qua=True, Psf=False, system="twomass"):
    """
    This function is to change fluxes on the catalog to magnitudes
    This is for counting galaxy probability
    This function is to change fluxes on the catalog to magnitudes and select whose imagetype=1
    This is for counting Galaxy Probability P
    """
    if system == 'twomass':
        F0_list = f0_2MASS_Spitzer
    elif system == 'ukidss':
        F0_list = f0_UKIDSS_Spitzer

    if Qua:
        flux_Qua  = [x[ID] for ID in qua_ID]
    if Psf:
        PSF_list  = [x[ID] for ID in psf_ID]

    flux_list = [float(x[ID]) for ID in flux_ID]
    mag_list  = []
    if Qua:
        for i in range(len(flux_list)):
            # Ignore J band
            if i == 0:
                if flux_list[i] > 0.0:
                    mag_list.append(-2.5 * mh.log10(flux_list[i]/F0_list[i]))
                else:
                    mag_list.append('no')
            # PSF Check activated
            elif Psf and PSF_list[i] != "1" and flux_Qua[i] != "S":
                mag_list.append('no')
            # IR1,IR2,IR3,IR4,MP1 band
            elif flux_Qua[i] == "A" or  flux_Qua[i] == "B" or flux_Qua[i] == "C" or flux_Qua[i] == "D" or flux_Qua[i] == "K":
                if flux_list[i] > 0.0:
                    mag_list.append(-2.5 * mh.log10(flux_list[i]/F0_list[i]))
            # Qua labeled as 'S' (saturate candidate)
            elif flux_Qua[i] == "S":
                mag_list.append(-100.0)
            # Qua labeled as 'N' (not detected)
            elif flux_Qua[i] == "N":
                mag_list = ['no'] * len(flux_list)
                break
            # Qua labeled as 'U' (upper-limit)
            else:
                mag_list.append('no')
    else:
        for i in range(len(flux_list)):
            if flux_list[i] > 0.0:
                mag_list.append(-2.5 * mh.log10(flux_list[i]/F0_list[i]))
            else:
                mag_list.append('no')
    return mag_list

def mag_to_mag(x, mag_ID=mag_ID, qua_ID=qua_ID, Qua=True, Psf=False, system="twomass"):
    """
    This function is for classifying different band's magnitude by flux_Qua
    This is for new kind of catalog (with magnitudes of different bands)
    This function is to select those source with imagetype=1
    This is for counting Galaxy Probability P
    """
    if system == 'twomass':
        F0_list = f0_2MASS_Spitzer
    elif system == 'ukidss':
        F0_list = f0_UKIDSS_Spitzer

    if Qua:
        flux_Qua = [x[ID] for ID in qua_ID]
    if Psf:
        PSF_list  = [x[ID] for ID in psf_ID]
    mag_list = [float(x[ID]) for ID in mag_ID]
    select_mag_list = []
    if Qua:
        for i in range(len(mag_list)):
            # Ignore J band
            if i == 0:
                if mag_list[i] > 0.0:
                    select_mag_list.append(mag_list[i])
                else:
                    select_mag_list.append('no')
            # PSF Check activated
            elif Psf and PSF_list[i] != "1" and flux_Qua[i] != "S":
                select_mag_list.append('no')
            # IR1, IR2, IR3, IR4, MP1 band
            elif flux_Qua[i] == "A" or  flux_Qua[i] == "B" or flux_Qua[i] == "C" or flux_Qua[i] == "D" or flux_Qua[i] == "K":
                if mag_list[i] > 0.0:
                    select_mag_list.append(mag_list[i])
            # Qua labeled as 'S' (saturate candidate)
            elif flux_Qua[i] == "S":
                select_mag_list.append(-100.0)
            # Qua labeled as 'N' (not detected)
            elif flux_Qua[i] == "N":
                select_mag_list=['no'] * len(flux_list)
                break
            # Qua labeled as 'U' (upper-limit)
            else:
                select_mag_list.append('no')
    else:
        for i in range(len(mag_list)):
            if mag_list[i] > 0.0:
                select_mag_list.append(mag_list[i])
            else:
                select_mag_list.append('no')
    return select_mag_list

def index_AGB(X, Y, a=[0,0,2,5], b=[-1,0,2,2]):
    """
    This function is to determine if the object is an AGB or not
    a,b are transition point, X,Y are input color and mag (data)
    """
    if X < a[0]:
        result = -1
    elif X > a[len(a)-1]:
        result =  -1
    else:
        cutY = 0
        for i in range(len(a)-1):
            if a[i] < X <a[i+1]:
                cutY = b[i] + (b[i+1]-b[i]) / (a[i+1]-a[i]) * (X-a[i])
            else:
                pass
        result = Y - cutY
    return result

def sort_up(X, lim, cube=0.2):
    '''
    This function is to put criterions we set for multi-d spaces onto the object
    '''
    if X == 'no':
        reu = "Lack"
    elif float(X) < lim[0]:
        reu = "Bright"
    elif float(X) > lim[1]:
        reu = "Faint"
    else:
        #reu = int((float(X)-lim[0])/cube)
        reu = int(round((float(X)-lim[0])/cube))
    return reu

def sort_up_lack999(X, lim, cube=0.2):
    '''
    This function is to put criterions we set for multi-d spaces onto the object
    This one doesn't have 'lack' label but -999
    '''
    if X == 'no':
        #=================LACK
        reu = -999
        #=================
    elif float(X) < lim[0]:
        #=================BRIGHT
        reu = -9999
        #=================
    elif float(X) > lim[1]:
        #=================FAINT
        reu = 9999
        #=================
    else:
        #reu = int((float(X)-lim[0])/cube)
        reu = int(round((float(X)-lim[0])/cube))
    return reu
