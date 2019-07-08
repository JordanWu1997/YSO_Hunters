#! /bin/csh`
#:1,$s/to_be_replaced/to_replace/g

# This is for checking new galaxy probability which has different binsize and with UKIDSS data
new_dict_6D_method.py ../5D_test/Out_catalog SWIRE mag && \
python ../new_dict_6D_method_mask_J.py ./SWIRE_6D_GP_all_out_catalog.tbl SWIRE_WI_5D_MJ mag &&\
awk '($243!~/no_count/)&&($243<="1.0") {print $243}' SWIRE_6D_GP_all_out_catalog.tbl | wc -l
Get_Galaxy_Samples_MMD.py 6DUMJ_bin_02_GP_ls_1 6DMJ_bin_02_GP_ls_1


# This is for calculating object's gal prob with new algorithm which with UKIDSS data
new_dict_6D_method.py ../catalog-CHA_II_Gal_Prob_All.tbl CHA_II mag && \
Check_6D_Gal_Prob.py CHA_II_6D_GP_all_out_catalog.tbl CHA_II 

# This is for merging YSO.tbl and IC.tbl
cat ../CHA_II_YSO.tbl ../CHA_II_GP_to_image_check.tbl > ../OLD_ALL_YSO_WI_IC.tbl
cat CHA_II_6D_YSO.tbl CHA_II_6D_GP_to_image_check.tbl > NEW_ALL_YSO_WI_IC.tbl

# This is for comparing new result with old Hsieh's result
Comparator_SWIRE_format.py ../CHA_II_YSO.tbl CHA_II_6D_YSO.tbl OLD_ALGO_WO_IC NEW_ALGO_WO_IC 7 yes no && \
Comparator_SWIRE_format.py ../OLD_ALL_YSO_WI_IC.tbl NEW_ALL_YSO_WI_IC.tbl OLD_ALGO NEW_ALGO 7 yes no && \

new_dict_6D_method.py ../catalog-CHA_II_Gal_Prob_All.tbl CHA_II mag && \
Check_6D_Gal_Prob.py CHA_II_6D_GP_all_out_catalog.tbl CHA_II && \
cat CHA_II_6D_YSO.tbl CHA_II_6D_GP_to_image_check.tbl > NEW_ALL_YSO_WI_IC.tbl && \
Comparator_SWIRE_format.py ../CHA_II_YSO.tbl CHA_II_6D_YSO.tbl OLD_ALGO_WO_IC NEW_ALGO_WO_IC 7 yes no && \
Comparator_SWIRE_format.py ../OLD_ALL_YSO_WI_IC.tbl NEW_ALL_YSO_WI_IC.tbl OLD_ALGO NEW_ALGO 7 yes no

#Comparator_SWIRE_format.py CHA_II_6D_YSO.tbl ../../../../Table_to_Compare/Table_From_Hsieh/all_candidates.tbl 6D_YSO_WI_UK 5D_ALL 7 yes no && \
#Comparator_SWIRE_format.py CHA_II_6D_GP_to_image_check.tbl ../../../../Table_to_Compare/Table_From_Hsieh/all_candidates.tbl 6D_IC_WI_UK 5D_ALL 7 yes no

# Construct directories
mkdir '6D_bs=0.20' && \ 
mkdir '6D_bs=0.25' && \
mkdir '6D_bs=0.30' && \
mkdir '6D_bs=0.35' && \
mkdir '6D_bs=0.40'

# Combination (Pipeline)
echo Start calculating ...
new_dict_6D_method.py ../catalog-CHA_II_Gal_Prob_All.tbl CHA_II mag && \
Check_6D_Gal_Prob.py CHA_II_6D_GP_all_out_catalog.tbl CHA_II && \
Comparator_SWIRE_format.py CHA_II_6D_YSO.tbl ../CHA_II_YSO.tbl 6D_YSO_WI_UK 5D_YSO 7 yes no && \
Comparator_SWIRE_format.py CHA_II_6D_YSO.tbl ../../../../Table_to_Compare/Table_From_Hsieh/all_candidates.tbl 6D_YSO_WI_UK 5D_ALL 7 yes no && \
Comparator_SWIRE_format.py CHA_II_6D_GP_to_image_check.tbl ../../../../Table_to_Compare/Table_From_Hsieh/all_candidates.tbl 6D_IC_WI_UK 5D_ALL 7 yes no
