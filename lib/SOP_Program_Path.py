#!/usr/bin/python
'''
---------------------------------------------------------------------
Abstract:
    This is to store all paths of programs/catalogs
---------------------------------------------------------------------
Latest update : 2019/05/27 Jordan Wu
'''

# All_Table_Prefix
#====================================================================
Hsieh_Table_Prefix  = "/brick/pangu/cosmo/users/inchone/"
SPITZER_Prefix      = "/brick/pangu/data/public/spitzer/"
New_Table_Prefix    = "/mazu/users/jordan/YSO_Project/YSO_Hunters_Table/"

# PATH FOR
#   - SOP_Program_Preset/SOP_Execution_Preset.py
#====================================================================
Hsieh_Av_Table_path    = "{}All_Extinction_Table/Tables_From_Hsieh/".format(New_Table_Prefix)
Selfmade_Av_Table_path = "{}All_Extinction_Table/Tables_Self_Made/".format(New_Table_Prefix)

# PATH FOR
#   - SOP_Program_Preset/Find_Saturate.py
#   - SOP_Program_5D_method/getfits.py
#====================================================================
Mosaic_path = "{}c2d/data.spitzer.caltech.edu/popular/c2d/20071101_enhanced_v1/".format(SPITZER_Prefix)

# PATH FOR
#   - SOP_Program_5D_method/multi-d_Prob_J_MP1.py
#   - SOP_Program_5D_method/PSF1_detection_multi-d_Prob_J_MP1.py
#====================================================================
Hsieh_5D_GP1_Array_path = "{}Remove_Av_sources_in_whole_clouds/SWI_c2d_PSD_new_process2_multi-dim_version/J_MP1_plus_IR1_MP1_methed/c2d_SWIRE_J-MP1/".format(Hsieh_Table_Prefix)

# PATH FOR
#   - SOP_Program_5D_method/multi-d_Prob_IR1_MP1.py
#   - SOP_Program_5D_method/PSF1_detection_multi-d_Prob_IR1_MP1.py
#====================================================================
Hsieh_5D_GP2_Array_path = "{}Remove_Av_sources_in_whole_clouds/SWI_c2d_PSD_new_process2_multi-dim_version/J_MP1_plus_IR1_MP1_methed/c2d_SWIRE_IR1-MP1/".format(Hsieh_Table_Prefix)

# PATH FOR
#   - SOP_Program_6D_method/new_dict_6D_method.py
#====================================================================
Selfmade_6D_GP_Dict_path = "{}All_6D_GP_Dict/6D_BS0.4_REFD5_tuple/Small_test/GPV_grid_6D_bin0.4_sigma2_refD5/".format(New_Table_Prefix)

# PATH FOR
#   - SOP_Program_6D_method/new_dict_6D_method.py
Selfmade_6D_GP_BD_Path = "{}".format(New_Table_Prefix)

# PATH FOR
#   - SOP_Program_6D_method/SOP_Execution_6D_method.py
Hsieh_YSO_List_path = '{}All_Table_To_Compare/Table_From_Hsieh/'.format(New_Table_Prefix)
#====================================================================

# PATH FOR Tables
# Hsieh's YSO cancidates table (Only RA, DEC)
#====================================================================
Hsieh_YSO_Coor_path = '{}All_Table_To_Compare/HL_YSOs_2013/'.format(New_Table_Prefix)

# SEIP catalog from Jacob
# J, Ks, H, IR1, IR2, IR3, IR4, MP1
#====================================================================
SEIP_Catalog_path = '{}All_Converted_Catalog/SEIP_pred_catalog/'.format(New_Table_Prefix)

# SPITZER HREL catalog in SWIRE format (CHA_II, LUP_I, LUP_III, LUP_IV, OPH, SER, PER)
HREL_Catalog_path = '{}All_Converted_Catalog/SPITZER/'.format(New_Table_Prefix)

# SPITZER + UKIDSS DR10 WITH BRIGHT 2MASS
SPITZER_UKIDSS_SWIRE_N1_path = '{}All_Converted_Catalog/UKIDSS_DR10PLUS/ADD_UKIDSS'.format(New_Table_Prefix)

# SPITZER HREL catalog + UKIDSS and BRIGHT 2MASS
SPITZER_UKIDSS_2MASS_BR_path = '{}All_Converted_Catalog/UKIDSS_DR11PLUS_WI_2MASS_BR/ADD_UKIDSS'.format(New_Table_Prefix)

# SPITZER HREL catalog + 2MASS transformed to UKIDSS system
SPITER_2MASS_To_UKIDSS_path  = '{}All_Converted_Catalog/2MASS_TO_UKIDSS'.format(New_Table_Prefix)

# Main Programs
#====================================================================
if __name__ == '__main__':
    print('\nPrint All Stored Paths And Prefixs')
    print('#===================================\n')
    for name in dir():
        if name[:2] != '__':
            print('{:30}:{:100}'.format(name, str(eval(name))))
    print('\n#===================================\n')
