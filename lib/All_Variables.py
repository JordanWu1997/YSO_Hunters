#!/usr/bin/python
'''----------------------------------------------------------------
Abstract:
    This program is for packing all variables for YSO Hunters

-------------------------------------------------------------------
latest update : 2020/06/04 Jordan Wu'''

# Variables
#==============================================================================

# Add on (Not in Hsieh_Functions Modules)
c2d_lab_ID = [16]

# Flux ID: J, IR1, IR2, IR3, IR4, MP1 (2MASS + Spitzer)
flux_ID     = [33, 96, 117, 138, 159, 180]
flux_err_ID = [34, 97, 118, 139, 160, 181]

# Flux ID: J, IR1, IR2, IR3, IR4, MP1 (ONLY Spitzer)
flux_ID_Spitzer     = [96, 117, 138, 159, 180]
flux_err_ID_Spitzer = [97, 118, 139, 160, 181]

# Flux ID: J, H, K (ONLY 2MASS)
flux_ID_2Mass     = [33, 54, 75]
flux_err_ID_2Mass = [34, 55, 76]

# Mag ID:  J, IR1, IR2, IR3, IR4, MP1 (2MASS/UKIDSS + Spitzer)
mag_ID             = [35, 98, 119, 140, 161, 182]
mag_ID_2Mass       = [35, 56, 77]
mag_err_ID_2Mass   = [36, 57, 78]
mag_ID_Spitzer     = [98, 119, 140, 161, 182]
mag_err_ID_Spitzer = [99, 120, 141, 162, 183]

# Qua ID:  J, IR1, IR2, IR3, IR4, MP1 (2MASS + Spitzer)
qua_ID         = [37, 100, 121, 142, 163, 184]
qua_ID_2Mass   = [37, 58, 79]
qua_ID_Spitzer = [100, 121, 142, 163, 184]

# PSF_ID:  J, IR1, IR2, IR3, IR4, MP1 (2MASS + Spitzer)
psf_ID         = [38, 102, 123, 144, 165, 186]
psf_ID_Spitzer = [102, 123, 144, 165, 186]

# F0 (mJy): J, IR1, IR2, IR3, IR4, MP1
f0_full_C2D       = [1594000, 1024000, 666700, 280900, 179700, 115000, 64130, 7140, 778]
f0_2MASS_Spitzer  = [1594000, 280900, 179700, 115000, 64130, 7140]  # H: 1024000, K: 666700
f0_UKIDSS_Spitzer = [1530000, 280900, 179700, 115000, 64130, 7140] # H: 1019000
f0_Spitzer        = [280900, 179700, 115000, 64130, 7140]
f0_2MASS          = [1594000, 1024000, 666700]
f0_UKIDSS         = [1530000, 1019000, 631000]

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
band_name      = ['J', 'IR1', 'IR2', 'IR3', 'IR4', 'MP1']
full_band_name = ['J', 'H', 'Ks', 'IR1', 'IR2', 'IR3', 'IR4', 'MP1', 'MP2']

# Band wavelength
full_band_wavelength_2MASS_SPITZER  = [1.235,   1.662,  2.159, 3.6, 4.5, 5.8, 8.0, 24.0, 70.0]
full_band_wavelength_UKIDSS_SPITZER = [1.2483, 1.6313, 2.2010, 3.6, 4.5, 5.8, 8.0, 24.0, 70.0]

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

# Main Programs
#==============================================================================
if __name__ == '__main__':
    print('\nPrint All Variables')
    print('#===================================\n')
    for name in dir():
        if name[:2] != '__':
            print('{:30}:{:100}'.format(name, str(eval(name))))
    print('\n#===================================\n')
