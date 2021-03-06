#!/usr/bin/env python
'''----------------------------------------------------------------
Abstract:
    This program is for packing all variables for YSO Hunters

-------------------------------------------------------------------
latest update : 2020/09/29 Jordan Wu'''

# Functions
# ==============================================================================
def get_max_column_num(var_names):
    '''
    This is to get maximum column num
    But the result need to +1 since it starts from 0
    '''
    max_column_num = 0
    for name in var_names:
        if name[:2] != '__':
            ID = eval(name)
            if type(ID) == int:
                num = int(ID)
                if num > max_column_num:
                    max_column_num = num
            elif (type(ID) == list) and (type(ID[0]) == int):
                num = max(ID)
                if (type(num) != str) and (num > max_column_num):
                    max_column_num = num
            else:
                pass
    max_column_num = max_column_num + 1
    return max_column_num

def print_all_variables(variable_dir):
    '''
    This is to print out all stored variables
    '''
    for name in variable_dir:
        if name[:2] != '__':
            print('{:30}:{:100}'.format(name, str(eval(name))))


def set_common_variables(band_ID, band_name, axlim_list, \
                         flux_ID, flux_err_ID, f0_list, mag_ID, mag_err_ID, qua_ID, psf_ID, \
                         GP_OBJ_ID, GP_ID, GPP_OBJ_ID, GPP_ID, GP_KEY_ID):
    '''
    This is to set important and common variables
    '''
    return band_ID, band_name, axlim_list, \
           flux_ID, flux_err_ID, f0_list, mag_ID, mag_err_ID, qua_ID, psf_ID, \
           GP_OBJ_ID, GP_ID, GPP_OBJ_ID, GPP_ID, GP_KEY_ID

# Variables
# ==============================================================================
# Add on (Not in Hsieh_Functions Modules)
c2d_lab_ID = [16]

# Flux IDs
full_flux_ID = [33, 54, 75, 96, 117, 138, 159, 180]
# Flux ID: J, H, IR2, IR4, MP1 (2MASS + Spitzer)
flux_ID_5D1     = [33, 75, 117, 159, 180]
flux_err_ID_5D1 = [34, 76, 118, 160, 181]
# Flux ID: IR1, IR2, IR3, IR4, MP1 (ONLYSpitzer)
flux_ID_5D2     = [96, 117, 138, 159, 180]
flux_err_ID_5D2 = [97, 118, 139, 160, 181]
# Flux ID: J, IR1, IR2, IR3, IR4, MP1 (2MASS + Spitzer)
flux_ID_6D     = [33, 96, 117, 138, 159, 180]
flux_err_ID_6D = [34, 97, 118, 139, 160, 181]
# Flux ID: IR1, IR2, IR3, IR4, MP1 (ONLY Spitzer)
flux_ID_Spitzer     = [96, 117, 138, 159, 180]
flux_err_ID_Spitzer = [97, 118, 139, 160, 181]
# Flux ID: J, H, K (ONLY 2MASS)
flux_ID_2Mass     = [33, 54, 75]
flux_err_ID_2Mass = [34, 55, 76]

# Magnitude IDs
full_mag_ID  = [35, 56, 77, 99, 120, 141, 162, 183]
mag_ID_5D1     = [35, 77, 119, 161, 182]
mag_err_ID_5D1 = [36, 78, 120, 162, 183]
# Flux ID: IR1, IR2, IR3, IR4, MP1 (ONLYSpitzer)
mag_ID_5D2     = [98, 119, 140, 161, 182]
mag_err_ID_5D2 = [99, 120, 141, 162, 183]
# Mag ID:  J, IR1, IR2, IR3, IR4, MP1 (2MASS/UKIDSS + Spitzer)
mag_ID_6D          = [35, 98, 119, 140, 161, 182]
mag_err_ID_6D      = [36, 99, 120, 141, 162, 183]
mag_ID_2Mass       = [35, 56, 77]
mag_err_ID_2Mass   = [36, 57, 78]
mag_ID_Spitzer     = [98, 119, 140, 161, 182]
mag_err_ID_Spitzer = [99, 120, 141, 162, 183]

# Quality IDs
# Qua ID:  J, IR1, IR2, IR3, IR4, MP1 (2MASS + Spitzer)
full_qua_ID    = [37, 58, 79, 100, 121, 142, 163, 184, 205]
qua_ID_5D1     = [37, 79, 121, 163, 184]
qua_ID_5D2     = [100, 121, 142, 163, 184]
qua_ID_6D      = [37, 100, 121, 142, 163, 184]
qua_ID_2Mass   = [37, 58, 79]
qua_ID_Spitzer = [100, 121, 142, 163, 184]

# PSF IDs
# PSF_ID:  J, IR1, IR2, IR3, IR4, MP1 (2MASS + Spitzer)
full_psf_ID    = [39, 60, 81, 102, 123, 144, 165, 186]
psf_ID_5D1     = [39, 81, 123, 165, 186]
psf_ID_5D2     = [102, 123, 144, 165, 186]
psf_ID_6D      = [39, 102, 123, 144, 165, 186]
psf_ID_Spitzer = [102, 123, 144, 165, 186]

# F0 (mJy): J, IR1, IR2, IR3, IR4, MP1
f0_full_C2D       = [1594000., 1024000., 666700., 280900., 179700., 115000., 64130., 7140., 778.]
f0_2MASS_Spitzer  = [1594000., 280900., 179700., 115000., 64130., 7140.]  # H: 1024000., K: 666700.
f0_UKIDSS_Spitzer = [1530000., 280900., 179700., 115000., 64130., 7140.] # H: 1019000.
f0_Spitzer        = [280900., 179700., 115000., 64130., 7140.]
f0_2MASS          = [1594000., 1024000., 666700.]
f0_UKIDSS         = [1530000., 1019000., 631000.]
f0_list_6D        = [1530000., 280900., 179700., 115000., 64130., 7140.]
f0_list_5D1       = [1530000., 631000., 179700., 64130., 7140.]
f0_list_5D2       = [280900., 179700., 115000., 64130., 7140.]

# Parameters [band, flux index, mag index, C_av(Exctintion_coef)]
C_av_list = [['J',  0.2741],
            ['H',   0.1622],
            ['K',   0.1119],
            ['IR1', 0.0671],
            ['IR2', 0.0543],
            ['IR3', 0.0444],
            ['IR4', 0.0463],
            ['MP1', 0.0259],
            ['MP2', 0.]]

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
band_name         = ['J', 'IR1', 'IR2', 'IR3', 'IR4', 'MP1']
Spitzer_band_name = ['IR1', 'IR2', 'IR3', 'IR4', 'MP1']
full_band_name    = ['J', 'H', 'Ks', 'IR1', 'IR2', 'IR3', 'IR4', 'MP1', 'MP2']
band_name_6D      = ['J', 'IR1', 'IR2', 'IR3', 'IR4', 'MP1']
band_name_5D1     = ['J', 'Ks', 'IR2', 'IR4', 'MP1']
band_name_5D2     = ['IR1', 'IR2', 'IR3', 'IR4', 'MP1']

# Band wavelength
full_band_wavelength_2MASS_SPITZER  = [1.235,   1.662,  2.159, 3.6, 4.5, 5.8, 8.0, 24.0, 70.0]
full_band_wavelength_UKIDSS_SPITZER = [1.2483, 1.6313, 2.2010, 3.6, 4.5, 5.8, 8.0, 24.0, 70.0]

# Axe limit in multi-D space
# HSIEH'S BOUNDARY
Hsieh_Jaxlim   = [4.0, 18.0]
Hsieh_Ksaxlim  = [8.0, 18.0]
Hsieh_Haxlim   = [0.0,  0.0]
Hsieh_IR1axlim = [8.0, 18.0]
Hsieh_IR2axlim = [7.0, 18.0]
Hsieh_IR3axlim = [5.0, 18.0]
Hsieh_IR4axlim = [5.0, 18.0]
Hsieh_MP1axlim = [3.5, 11.0]
# NEW BOUNDARY WI UKIDSS CATALOG
Jaxlim   = [3.5, 22.0]
Haxlim   = [0.0,  0.0]
Ksaxlim  = [8.0, 18.0]
IR1axlim = [8.0, 20.0]
IR2axlim = [7.0, 19.0]
IR3axlim = [5.0, 18.0]
IR4axlim = [5.0, 18.0]
MP1axlim = [3.5, 12.0]
# Axe limit list
axlim_list_5D1 = [Jaxlim, Ksaxlim, IR2axlim, IR4axlim, MP1axlim]
axlim_list_5D2 = [IR1axlim, IR2axlim, IR3axlim, IR4axlim, MP1axlim]
axlim_list_6D  = [Jaxlim, IR1axlim, IR2axlim, IR3axlim, IR4axlim, MP1axlim]
full_axlim_list = [Jaxlim, Haxlim, Ksaxlim, IR1axlim, IR2axlim, IR3axlim, IR4axlim, MP1axlim]

# GP/GPP Index
GP_OBJ_ID_5D1, GP_ID_5D1 = 233, 234
GP_OBJ_ID_5D2, GP_ID_5D2 = 235, 236
GP_OBJ_ID_6D, GP_ID_6D = 241, 242

GPP_OBJ_ID_5D1, GPP_ID_5D1 = 237, 238
GPP_OBJ_ID_5D2, GPP_ID_5D2 = 239, 240
GPP_OBJ_ID_6D, GPP_ID_6D = 243, 244

GP_KEY_ID_5D1, GP_KEY_ID_5D2 = 245, 246
GP_KEY_ID_6D = 247

GP_OBJ_ID_6D_0, GP_ID_6D_0   = 241, 242
GPP_OBJ_ID_6D_0, GPP_ID_6D_0 = 243, 244
GP_OBJ_ID_6D_1, GP_ID_6D_1   = 245, 246
GPP_OBJ_ID_6D_1, GPP_ID_6D_1 = 247, 248
GP_OBJ_ID_6D_2, GP_ID_6D_2   = 249, 250
GPP_OBJ_ID_6D_2, GPP_ID_6D_2 = 251, 252
GP_OBJ_ID_6D_3, GP_ID_6D_3   = 253, 254
GPP_OBJ_ID_6D_3, GPP_ID_6D_3 = 255, 256
GP_OBJ_ID_6D_4, GP_ID_6D_4   = 257, 258
GPP_OBJ_ID_6D_4, GPP_ID_6D_4 = 259, 260
GP_OBJ_ID_6D_5, GP_ID_6D_5   = 261, 262
GPP_OBJ_ID_6D_5, GPP_ID_6D_5 = 263, 264

GP_KEY_ID_6D_0 = 265
GP_KEY_ID_6D_1 = 266
GP_KEY_ID_6D_2 = 267
GP_KEY_ID_6D_3 = 268
GP_KEY_ID_6D_4 = 269
GP_KEY_ID_6D_5 = 270

# GP/GPP Diag Index
GP_OBJ_ID_6D_Diag, GP_ID_6D_Diag = 271, 272
GPP_OBJ_ID_6D_Diag, GPP_ID_6D_Diag = 273, 274
GP_KEY_ID_6D_Diag = 275

# GP/GPP Diag Index
GP_OBJ_ID_5D1_Diag, GP_ID_5D1_Diag = 276, 277
GPP_OBJ_ID_5D1_Diag, GPP_ID_5D1_Diag = 278, 279

GP_OBJ_ID_5D2_Diag, GP_ID_5D2_Diag = 280, 281
GPP_OBJ_ID_5D2_Diag, GPP_ID_5D2_Diag = 282, 283

GP_KEY_ID_5D1_Diag = 284
GP_KEY_ID_5D2_Diag = 285

# Set variables
# ==============================================================================
# Var Set 1: For 6D GP (J, IR1, IR2, IR3, IR4, MP1)
def set_common_variables(band_ID, band_name, axlim_list, \
                         flux_ID, flux_err_ID, f0_list, mag_ID, mag_err_ID, qua_ID, psf_ID, \
                         GP_OBJ_ID, GP_ID, GPP_OBJ_ID, GPP_ID, GP_KEY_ID):
    '''
    This is to set important and common variables
    '''
    return band_ID, band_name, axlim_list, \
           flux_ID, flux_err_ID, f0_list, mag_ID, mag_err_ID, qua_ID, psf_ID, \
           GP_OBJ_ID, GP_ID, GPP_OBJ_ID, GPP_ID, GP_KEY_ID

band_ID, band_name, axlim_list, \
flux_ID, flux_err_ID, f0_list, mag_ID, mag_err_ID, qua_ID, psf_ID, \
GP_OBJ_ID, GP_ID, GPP_OBJ_ID, GPP_ID, GP_KEY_ID = \
set_common_variables(band_ID=[0, 3, 4, 5, 6, 7], band_name=band_name_6D, axlim_list=axlim_list_6D, \
                     flux_ID=flux_ID_6D, flux_err_ID=flux_err_ID_6D, f0_list=f0_list_6D, \
                     mag_ID=mag_ID_6D, mag_err_ID=mag_err_ID_6D, qua_ID=qua_ID_6D, psf_ID=psf_ID_6D, \
                     GP_OBJ_ID=GP_OBJ_ID_6D, GP_ID=GP_ID_6D, GPP_OBJ_ID=GPP_OBJ_ID_6D, GPP_ID=GPP_ID_6D, GP_KEY_ID=GP_KEY_ID_6D)

# # Var Set 2: For 5D GP1 (J, Ks, IR2, IR4, MP1)
# band_ID, band_name, axlim_list, \
# flux_ID, flux_err_ID, f0_list, mag_ID, mag_err_ID, qua_ID, psf_ID, \
# GP_OBJ_ID, GP_ID, GPP_OBJ_ID, GPP_ID, GP_KEY_ID = \
# set_common_variables(band_ID=[0, 2, 4, 6, 7], band_name=band_name_5D1, axlim_list=axlim_list_5D1, \
                     # flux_ID=flux_ID_5D1, flux_err_ID=flux_err_ID_5D1, f0_list=f0_list_5D1, \
                     # mag_ID=mag_ID_5D1, mag_err_ID=mag_err_ID_5D1, qua_ID=qua_ID_5D1, psf_ID=psf_ID_5D1, \
                     # GP_OBJ_ID=GP_OBJ_ID_5D1, GP_ID=GP_ID_5D1, GPP_OBJ_ID=GPP_OBJ_ID_5D1, GPP_ID=GPP_ID_5D1, GP_KEY_ID=GP_KEY_ID_5D1)

# # Var Set 3: For 5D GP2 (IR1, IR2, IR3, IR4, MP1)
# band_ID, band_name, axlim_list, \
# flux_ID, flux_err_ID, f0_list, mag_ID, mag_err_ID, qua_ID, psf_ID, \
# GP_OBJ_ID, GP_ID, GPP_OBJ_ID, GPP_ID, GP_KEY_ID = \
# set_common_variables(band_ID=[3, 4, 5, 6, 7], band_name=band_name_5D2, \
                     # flux_ID=flux_ID_5D2, flux_err_ID=flux_err_ID_5D2, f0_list=f0_list_5D2, axlim_list=axlim_list_5D2, \
                     # mag_ID=mag_ID_5D2, mag_err_ID=mag_err_ID_5D2, qua_ID=qua_ID_5D2, psf_ID=psf_ID_5D2, \
                     # GP_OBJ_ID=GP_OBJ_ID_5D2, GP_ID=GP_ID_5D2, GPP_OBJ_ID=GPP_OBJ_ID_5D2, GPP_ID=GPP_ID_5D2, GP_KEY_ID=GP_KEY_ID_5D2)

# Variables which used in all following programs can be modified here
# ==============================================================================
max_column_num = get_max_column_num(dir())

# Main Programs
# ==============================================================================
if __name__ == '__main__':
    print('\nPrint All Variables')
    print('#====================================================\n')
    print_all_variables(dir())
    print('\n#==================================================\n')
