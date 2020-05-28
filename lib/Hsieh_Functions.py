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

from __future__ import print_function
import math as mh
import numpy as np

#==============================================================================
# Add on (Not in Hsieh_Functions Modules)
c2d_lab_ID = [16]

# Flux ID: J, IR1, IR2, IR3, IR4, MP1 (2MASS + Spitzer)
flux_ID = [33, 96, 117, 138, 159, 180]
flux_err_ID = [34, 97, 118, 139, 160, 181]
# Flux ID: J, IR1, IR2, IR3, IR4, MP1 (ONLY Spitzer)
flux_ID_Spitzer = [96, 117, 138, 159, 180]
flux_err_ID_Spitzer = [97, 118, 139, 160, 181]
# Flux ID: J, H, K (ONLY 2MASS)
flux_ID_2Mass = [33, 54, 75]
flux_err_ID_2Mass = [34, 55, 76]

# Mag ID:  J, IR1, IR2, IR3, IR4, MP1 (2MASS/UKIDSS + Spitzer)
mag_ID  = [35, 98, 119, 140, 161, 182]
mag_ID_2Mass = [35, 56, 77]
mag_err_ID_2Mass = [36, 57, 78]
mag_ID_Spitzer = [98, 119, 140, 161, 182]
mag_err_ID_Spitzer = [99, 120, 141, 162, 183]

# Qua ID:  J, IR1, IR2, IR3, IR4, MP1 (2MASS + Spitzer)
qua_ID  = [37, 100, 121, 142, 163, 184]
qua_ID_2Mass = [37, 58, 79]
qua_ID_Spitzer = [100, 121, 142, 163, 184]

# PSF_ID:  J, IR1, IR2, IR3, IR4, MP1 (2MASS + Spitzer)
psf_ID  = [38, 102, 123, 144, 165, 186]
psf_ID_Spitzer = [102, 123, 144, 165, 186]

# F0 (mJy): J, IR1, IR2, IR3, IR4, MP1
f0_full_C2D = [1594000, 1024000, 666700, 280900, 179700, 115000, 64130, 7140, 778]
f0_2MASS_Spitzer = [1594000, 280900, 179700, 115000, 64130, 7140]  # H: 1024000, K: 666700
f0_UKIDSS_Spitzer = [1530000, 280900, 179700, 115000, 64130, 7140] # H: 1019000
f0_Spitzer = [280900, 179700, 115000, 64130, 7140]

# parameters [band, flux index, mag index, C_av(Exctintion_coef)]
C_av_list = [['J',  0.2741],
            ['H',   0.1622],
            ['K',   0.1119],
            ['IR1', 0.0671],
            ['IR2', 0.0543],
            ['IR3', 0.0444],
            ['IR4', 0.0463],
            ['MP1', 0.0259],
            ['MP2', 0]]

# Extinction Correction Parameters
Av_coor_ID       = [0, 1]  # RA, Dec on extinction table
Av_ID            = [17]
Av_tbl_col_ID    = [2, 6]  # [6] for Hsieh's old Av table
coor_ID          = [0, 2]  # RA, Dec on input table
full_flux_ID     = [33, 54, 75, 96, 117, 138, 159, 180, 201]
full_mag_ID      = [35, 56, 77, 98, 119, 140, 161, 182, 203]
full_flux_err_ID = [34, 55, 76, 97, 118, 139, 160, 181, 202]
full_mag_err_ID  = [36, 57, 78, 99, 120, 141, 162, 183, 204]

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
    # Different f0 values for different systems
    if system == 'twomass':
        F0_list = f0_2MASS_Spitzer
    elif system == 'ukidss':
        F0_list = f0_UKIDSS_Spitzer
    # Assign Qua, PSF index
    if Qua: flux_Qua  = [x[ID] for ID in qua_ID]
    if Psf: PSF_list  = [x[ID] for ID in psf_ID]
    # Start calculating magnitude
    flux_list = [float(x[ID]) for ID in flux_ID]
    if Qua:
        if "N" in flux_Qua:
            mag_list = [0] * len(flux_list)
        else:
            mag_list = []
            for i in range(len(flux_list)):
                # PSF Check activated
                if Psf and PSF_list[i] != "1" and flux_Qua[i] != "S":
                    mag_list.append('no')
                # IR1, IR2, IR3, IR4, MP1 band ("A_fake", "U_fake" for J,H,K)
                elif flux_Qua[i] in ["A_fake", "U_fake", "A", "B", "C", "D", "K"]:
                    if flux_list[i] > 0.0:
                        mag_list.append(-2.5 * mh.log10(flux_list[i]/F0_list[i]))
                    else:
                        mag_list.append('no')
                # Qua labeled as 'S' (saturate candidate)
                elif flux_Qua[i] == "S":
                    mag_list.append(-100.0)
                # Qua labeled as 'U' (upper-limit)
                else:
                    mag_list.append('no')
    else:
        mag_list = []
        for i in range(len(flux_list)):
            if flux_list[i] > 0.0:
                mag_list.append(-2.5 * mh.log10(flux_list[i]/F0_list[i]))
            else:
                mag_list.append('no')
    return mag_list

def mJy_to_mag_ONLY_Spitzer(x):
    '''
    This function is to change fluxes on the catalog to magnitudes
    IR1, IR2, IR3, IR4, MP1 (SPITZER)
    '''
    flux_list = [float(x[ID]) for ID in flux_ID_Spitzer]
    flux_Qua  = [x[ID] for ID in qua_ID_Spitzer]
    F0_list   = f0_Spitzer
    mag_list  = []
    for i in range(len(F0_list)):
        if float(flux_list[i]) > 0.0:
            mag_list.append(-2.5 * mh.log10(float(flux_list[i])/F0_list[i]))
        else:
            mag_list.append(0.0)
    return mag_list

def flux_error_to_mag_ONLY_Spitzer(x):
    '''
    This function is to change flux error on the catalog to magnitudes error
    IR1, IR2, IR3, IR4, MP1 (SPITZER)
    '''
    df_list = [float(x[ID]) for ID in flux_err_ID_Spitzer]
    F0_list = f0_Spitzer
    dm_list = []
    for i in range(len(F0_list)):
        if df_list[i] > 0.0:
            dm = float(df_list[i])/F0_list[i] * 2.5 * mh.log10(mh.e)
        else :
            dm = 0.0
        dm_list.append(dm)
    return dm_list

def mJy_to_mag_FULL_C2D(x):
    '''
    This function is to change fluxes on the catalog to magnitudes
    J, H, Ks, IR1, IR2, IR3, IR4, MP1 (2MASS + SPITZER)
    '''
    flux_list = [float(x[ID]) for ID in full_flux_ID]
    F0_list   = f0_full_C2D
    mag_list  = []
    for i in range(len(F0_list)):
        if float(flux_list[i]) > 0.0:
            mag_list.append(-2.5 * mh.log10(float(flux_list[i])/F0_list[i]))
        else:
            mag_list.append(0.0)
    return mag_list

def mag_error_to_mag_FULL_C2D(x):
    '''
    This function is to change flux error on the catalog to magnitudes error
    J, H, Ks, IR1, IR2, IR3, IR4, MP1 (2MASS + SPITZER)
    '''
    df_list = [float(x[ID]) for ID in full_flux_ID]
    F0_list = f0_full_C2D
    dm_list = []
    for i in range(len(F0_list)):
        if df_list[i] > 0.0:
            dm_list.append(float(df_list[i])/F0_list[i] * 2.5 * mh.log10(mh.e))
        else:
            dm_list.append(0.0)
    return dm_list

#==============================================================================
def mag_to_mag(x, mag_ID=mag_ID, qua_ID=qua_ID, Qua=True, Psf=False, system="twomass"):
    """
    This function is for classifying different band's magnitude by flux_Qua
    This is for new kind of catalog (with magnitudes of different bands)
    This function is to select those source with imagetype=1
    This is for counting Galaxy Probability P
    """
    # Different f0 values for different systems
    if system == 'twomass':
        F0_list = f0_2MASS_Spitzer
    elif system == 'ukidss':
        F0_list = f0_UKIDSS_Spitzer
    # Assign Qua, PSF index
    if Qua: flux_Qua = [x[ID] for ID in qua_ID]
    if Psf: PSF_list = [x[ID] for ID in psf_ID]
    # Start calculating magnitude
    mag_list = [float(x[ID]) for ID in mag_ID]
    if Qua:
        # Qua labeled as 'N' (not detected)
        if "N" in flux_Qua:
            select_mag_list = ['no'] * len(mag_list)
        else:
            select_mag_list = []
            for i in range(len(mag_list)):
                # PSF Check activated
                if Psf and PSF_list[i] != "1" and flux_Qua[i] != "S":
                    select_mag_list.append('no')
                # IR1, IR2, IR3, IR4, MP1 band ("A_fake for J,H,K)
                elif flux_Qua[i] in ["A_fake", "A", "B", "C", "D", "K"]:
                    if mag_list[i] > 0.0:
                        select_mag_list.append(mag_list[i])
                    else:
                        select_mag_list.append('no')
                # Qua labeled as 'S' (saturate candidate)
                elif flux_Qua[i] == "S":
                    select_mag_list.append(-100.0)
                # Qua labeled as 'U' (upper-limit)
                else:
                    select_mag_list.append('no')
    else:
        select_mag_list = []
        for i in range(len(mag_list)):
            if mag_list[i] > 0.0:
                select_mag_list.append(mag_list[i])
            else:
                select_mag_list.append('no')
    return select_mag_list

#==============================================================================
def JHK_flux_to_mag(J_flux, H_flux, K_flux, to_UKIDSS=True):
    '''
    This function is to (1)change fluxes on the catalog to magnitudes
                        (2)transform magnitudes from 2MASS to UKIDSS
    '''
    if float(J_flux) > 0.0 and float(H_flux) > 0.0 and float(K_flux) > 0.0:
        F0_list = [1594000, 1024000, 666700]
        mag_J = -2.5 * np.log10(float(J_flux)/F0_list[0])
        mag_H = -2.5 * np.log10(float(H_flux)/F0_list[1])
        mag_K = -2.5 * np.log10(float(K_flux)/F0_list[2])
    else:
        mag_J, mag_H, mag_K = 0.0, 0.0, 0.0

    if to_UKIDSS:
        if mag_J > 0.0 and mag_H > 0.0:
            mag_J = mag_J - 0.065 * (mag_J - mag_H)
            mag_H = mag_H + 0.07  * (mag_J - mag_H)
        if mag_J > 0.0 and mag_K > 0.0:
            mag_K = mag_K + 0.01  * (mag_J - mag_K)
    return mag_J, mag_H, mag_K

#==============================================================================
def index_AGB(X, Y, a=[0,0,2,5], b=[-1,0,2,2]):
    """
    This function is to determine if the object is an AGB or not
    a,b are transition point, X,Y are input color and mag (data)
    X is IR2-IR3, Y is IR3-MP1
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

#==============================================================================
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

def bin_to_mag(X, lim, cube=0.2):
    '''
    This function is to transform from binned data to original magnitude
    It will return center of the bin
    '''
    mag = lim[0] + (X-0.5) * cube
    return mag
