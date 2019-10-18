#!/usr/bin/csh

#==============
# Mean Av value
#==============
# CHA_II : 3.15
# LUP_I  : 2.33
# LUP_III: 2.49
# LUP_IV : 3.60
# PER    : 4.56
# SER    : 7.45
# OPH    : 4.98
# All    : 4.39


# Initialization
mkdir CHA_II
mkdir LUP_I
mkdir LUP_III
mkdir LUP_IV
mkdir SER
mkdir PER
mkdir OPH

#==================================================================================================================
# Catalog Dir And Naming Style - Without UKIDSS Observation
#==================================================================================================================
# ../../All_Converted_Catalog/2MASS_TO_UKIDSS/
# e.g. catalog-CHA_II_2MASS_to_UKIDSS_HREL.tbl

cd CHA_II
SOP_Execution_Preset.py ../../All_Converted_Catalog/2MASS_TO_UKIDSS/catalog-CHA_II_2MASS_to_UKIDSS_HREL.tbl CHA_II New
SOP_Execution_5D_method.py Default CHA_II
SOP_Execution_6D_method.py CHA_II mag True Default 0.4
cd CHA_II_6D_BS_0.4
SOP_Execution_Extinction_check.py CHA_II 0.2 3.15
cd ../../

cd LUP_I
SOP_Execution_Preset.py ../../All_Converted_Catalog/2MASS_TO_UKIDSS/catalog-LUP_I_2MASS_to_UKIDSS_HREL.tbl LUP_I New
SOP_Execution_5D_method.py Default LUP_I
SOP_Execution_6D_method.py LUP_I mag True Default 0.4
cd LUP_I_6D_BS_0.4
SOP_Execution_Extinction_check.py LUP_I 0.2 2.33
cd ../../

cd LUP_III
SOP_Execution_Preset.py ../../All_Converted_Catalog/2MASS_TO_UKIDSS/catalog-LUP_III_2MASS_to_UKIDSS_HREL.tbl LUP_III New
SOP_Execution_5D_method.py Default LUP_III
SOP_Execution_6D_method.py LUP_III mag True Default 0.4
cd LUP_III_6D_BS_0.4
SOP_Execution_Extinction_check.py LUP_III 0.2 1.93
cd ../../

cd LUP_IV
SOP_Execution_Preset.py ../../All_Converted_Catalog/2MASS_TO_UKIDSS/catalog-LUP_IV_2MASS_to_UKIDSS_HREL.tbl LUP_IV New
SOP_Execution_5D_method.py Default LUP_IV
SOP_Execution_6D_method.py LUP_IV mag True Default 0.4
cd LUP_IV_6D_BS_0.4
SOP_Execution_Extinction_check.py LUP_IV 0.2 3.60
cd ../../

#==================================================================================================================
# Catalog Dir And Naming Style - With UKIDSS Observation
#==================================================================================================================
# ../../All_Converted_Catalog/UKIDSS_DR11PLUS_WI_2MASS_BR/ADD_UKIDSS/
# e.g. catalog-SER_C2D_UKIDSS_WI_2MASS_BR.tbl

cd OPH
SOP_Execution_Preset.py ../../All_Converted_Catalog/UKIDSS_DR11PLUS_WI_2MASS_BR/ADD_UKIDSS/catalog-OPH_C2D_UKIDSS_WI_2MASS_BR.tbl OPH New
SOP_Execution_5D_method.py Default OPH
SOP_Execution_6D_method.py OPH mag True Default 0.4
cd OPH_6D_BS_0.4
SOP_Execution_Extinction_check.py OPH 0.2 4.56
cd ../../

cd SER
SOP_Execution_Preset.py ../../All_Converted_Catalog/UKIDSS_DR11PLUS_WI_2MASS_BR/ADD_UKIDSS/catalog-SER_C2D_UKIDSS_WI_2MASS_BR.tbl SER New
SOP_Execution_5D_method.py Default SER
SOP_Execution_6D_method.py SER mag True Default 0.4
cd SER_6D_BS_0.4
SOP_Execution_Extinction_check.py SER 0.2 7.45
cd ../../

cd PER
SOP_Execution_Preset.py ../../All_Converted_Catalog/UKIDSS_DR11PLUS_WI_2MASS_BR/ADD_UKIDSS/catalog-PER_C2D_UKIDSS_WI_2MASS_BR.tbl PER New
SOP_Execution_5D_method.py Default PER
SOP_Execution_6D_method.py PER mag True Default 0.4
cd PER_6D_BS_0.4
SOP_Execution_Extinction_check.py PER 0.2 4.56
cd ../../
