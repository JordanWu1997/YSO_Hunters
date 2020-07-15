#!/usr/bin/csh

# This is for no UKIDSS detection
cp /mazu/users/jordan/YSO_Project/YSO_Hunters_Table/All_Converted_Catalog/SPITZER/catalog-CHA_II-HREL.tbl Catalog-CHA_II-HREL.tbl > term.out
Add_Mag_To_C2D_Full.py Catalog-CHA_II-HREL.tbl Catalog-CHA_II-HREL-Add_Mag.tbl >> term.out
TF_From_2MASS_To_UKIDSS_System.py Catalog-CHA_II-HREL-Add_Mag.tbl Catalog-CHA_II-HREL-Add_Mag-TF_UKIDSS.tbl >> term.out
Add_Mag_Qua_JHK_UKIDSS.py Catalog-CHA_II-HREL-Add_Mag-TF_UKIDSS.tbl default N A_fake >> term.out
Add_Mag_Qua_JHK_UKIDSS.py Catalog-CHA_II-HREL-Add_Mag-TF_UKIDSS-Add_JHK_Qua.tbl default U A_fake >> term.out
SOP_Execution_Preset.py Catalog-CHA_II-HREL-Add_Mag-TF_UKIDSS-Add_JHK_Qua-Add_JHK_Qua.tbl CHA_II Self_made >> term.out
Calculate_GP_WI_6D_Bound_Array.py CHA_II_saturate_correct_file.tbl CHA_II mag /mazu/users/jordan/YSO_Project/SEIP_catalog_GP_WO_AGB/GPV_after_smooth_6D_bin1.0_sigma2_bond0_refD5/after_smooth_6D_lower_bounds_AlB0.npy /mazu/users/jordan/YSO_Project/SEIP_catalog_GP_WO_AGB/GPV_after_smooth_6D_bin1.0_sigma2_bond0_refD5/after_smooth_6D_upper_bounds_AlB0.npy 012345 1.0 2 0 5 >> term.out
Classify_WI_6D_Galaxy_Prob.py CHA_II_6D_BD_GP_out_catalog.tbl CHA_II >> term.out
Check_Coord.py CHA_II_6D_YSO.tbl default CHA_II_YSO default 7 False >> term.out
Check_Coord.py CHA_II_6D_Galaxy.tbl default CHA_II_Galaxy default 7 False >> term.out
Check_Coord.py CHA_II_6D_GP_to_image_check.tbl default CHA_II_6D_GP_IC default 7 False >> term.out
Check_Coord.py CHA_II_6D_GP_others.tbl default CHA_II_6D_OTHERS default 7 False >> term.out

# This is for UKIDSS detection
cp /mazu/users/jordan/YSO_Project/YSO_Hunters_Table/All_Converted_Catalog/SPITZER/catalog-OPH-HREL.tbl Catalog-OPH-HREL.tbl >> term.out
# OPH
Add_Mag_JHK_UKIDSS_C2D_Combined.py Catalog-OPH-HREL.tbl /mazu/users/jordan/YSO_Project/YSO_Hunters_Table/All_UKIDSS_Catalog/UKIDSS_OBSERVATION/DR11PLUS/UKIDSS_GCS/UKIDSS_GCS_OPH.csv 13 Catalog-OPH-HREL-Add_Mag-Add_UKIDSS_JHK_2MASSBR.tbl 2MASSBR >> term.out
# SER
Add_Mag_JHK_UKIDSS_C2D_Combined.py Catalog-SER-HREL.tbl /mazu/users/jordan/YSO_Project/YSO_Hunters_Table/All_UKIDSS_Catalog/UKIDSS_OBSERVATION/DR11PLUS/UKIDSS_GPS/UKIDSS_GPS_SER.csv 13 Catalog-SER-HREL-Add_Mag-Add_UKIDSS_JHK_2MASSBR.tbl 2MASSBR >> term.out
# PER
Add_Mag_JHK_UKIDSS_C2D_Combined.py Catalog-PER-HREL.tbl /mazu/users/jordan/YSO_Project/YSO_Hunters_Table/All_UKIDSS_Catalog/UKIDSS_OBSERVATION/DR11PLUS/Survey_Merging/UKIDSS_COMBINED_PER.tbl 0 Catalog-PER-HREL-Add_Mag-Add_UKIDSS_JHK_2MASSBR.tbl 2MASSBR >> term.out
# ROW 28
Add_Mag_Qua_JHK_UKIDSS.py Catalog-OPH-HREL-Add_Mag-Add_UKIDSS_JHK_2MASSBR.tbl default N A_fake >> term.out
Add_Mag_Qua_JHK_UKIDSS.py Catalog-OPH-HREL-Add_Mag-TF_UKIDSS-Add_JHK_Qua.tbl default U A_fake >> term.out
SOP_Execution_Preset.py Catalog-OPH-HREL-Add_Mag-Add_UKIDSS_JHK_2MASSBR-Add_JHK_Qua.tbl OPH Self_made >> term.out
Calculate_GP_WI_6D_Bound_Array.py OPH_saturate_correct_file.tbl OPH mag /mazu/users/jordan/YSO_Project/SEIP_catalog_GP_WO_AGB/GPV_after_smooth_6D_bin1.0_sigma2_bond0_refD5/after_smooth_6D_lower_bounds_AlB0.npy /mazu/users/jordan/YSO_Project/SEIP_catalog_GP_WO_AGB/GPV_after_smooth_6D_bin1.0_sigma2_bond0_refD5/after_smooth_6D_upper_bounds_AlB0.npy 012345 1.0 2 0 5 >> term.out
Classify_WI_6D_Galaxy_Prob.py OPH_6D_BD_GP_out_catalog.tbl OPH >> term.out
Check_Coord.py OPH_6D_YSO.tbl default OPH_YSO default 7 False >> term.out
Check_Coord.py OPH_6D_Galaxy.tbl default OPH_Galaxy default 7 False >> term.out
Check_Coord.py OPH_6D_GP_to_image_check.tbl default OPH_6D_GP_IC default 7 False >> term.out
Check_Coord.py OPH_6D_GP_others.tbl default OPH_6D_GP_OTHERS default 7 False >> term.out
