#! /bin/csh

# This is for checking new galaxy probability which has different binsize and with UKIDSS data
#new_dict_6D_method.py ../5D_test/Out_catalog SWIRE mag && \
#awk '($243!~/no_count/)&&($243<="1.0") {print $243}' SWIRE_6D_GP_all_out_catalog.tbl | wc

# This is for calculating object's gal prob with new algorithm which with UKIDSS data
#new_dict_6D_method.py ../catalog-CHA_II_Gal_Prob_All.tbl CHA_II mag && \
#Check_6D_Gal_Prob.py CHA_II_6D_GP_all_out_catalog.tbl CHA_II 

# This is for comparing new result with old Hsieh's result
#Comparator_SWIRE_format.py CHA_II_6D_YSO.tbl ../CHA_II_YSO.tbl 6D_YSO_WI_UK 5D_YSO 7 yes no && \
#Comparator_SWIRE_format.py CHA_II_6D_YSO.tbl ../../../../Table_to_Compare/Table_From_Hsieh/all_candidates.tbl 6D_YSO_WI_UK 5D_ALL 7 yes no && \
#Comparator_SWIRE_format.py CHA_II_6D_GP_to_image_check.tbl ../../../../Table_to_Compare/Table_From_Hsieh/all_candidates.tbl 6D_IC_WI_UK 5D_ALL 7 yes no

echo Start calculating ...
# Combination (Pipeline)
new_dict_6D_method.py ../catalog-CHA_II_Gal_Prob_All.tbl CHA_II mag && \
Check_6D_Gal_Prob.py CHA_II_6D_GP_all_out_catalog.tbl CHA_II &&\
Comparator_SWIRE_format.py CHA_II_6D_YSO.tbl ../CHA_II_YSO.tbl 6D_YSO_WI_UK 5D_YSO 7 yes no && \
Comparator_SWIRE_format.py CHA_II_6D_YSO.tbl ../../../../Table_to_Compare/Table_From_Hsieh/all_candidates.tbl 6D_YSO_WI_UK 5D_ALL 7 yes no && \
Comparator_SWIRE_format.py CHA_II_6D_GP_to_image_check.tbl ../../../../Table_to_Compare/Table_From_Hsieh/all_candidates.tbl 6D_IC_WI_UK 5D_ALL 7 yes no
