#!/usr/bin/csh
# ======================================================
# This program is a pipeline for merge YSO catalog

# Latest update JordanWu 2020/08/07
# ======================================================

# Variables
# ======================================================
# Help for input arguments

# cloud indice and ukidss observation indicator
set clouds=(CHA_II LUP_I LUP_III LUP_IV OPH SER PER)

# Main Program
# ======================================================
set out_dir='All_YSO'
set out_int_hsieh='all_YSO_and_Hsieh.tbl'
set out_not_hsieh='all_YSO_not_Hsieh.tbl'
set out_all_new='all_GP_Diag_new_YSO.tbl'
set out_all_galaxy='all_GP_Diag_new_Galaxy.tbl'

# Initialization
if ( -d ${out_dir} ) then
    rm -fr ${out_dir} && mkdir ${out_dir}
else
    mkdir ${out_dir}
endif
cd ${out_dir}

# Merge All Clouds
foreach cloud (${clouds})
    cat ../${cloud}/AND_${cloud}_YSO_all_Hsieh_YSOc.tbl >> ${out_int_hsieh}
    cat ../${cloud}/DIFF_${cloud}_YSO.tbl >> ${out_not_hsieh}
end
cat ${out_int_hsieh} ${out_not_hsieh} >> ${out_all_new}

# For Diag BD method
awk '$272~"BYSO"' ${out_all_new} > all_GP_Diag_new_BYSO.tbl
awk '$272~"IYSO"' ${out_all_new} > all_GP_Diag_new_IYSO.tbl
awk '$272!~"IYSO" && $272!~"BYSO"' ${out_all_new} > all_GP_Diag_new_NIBYSO.tbl

# Galaxy
# Merge All Clouds
foreach cloud (${clouds})
    cat ../${cloud}/${cloud}_6D_Galaxy.tbl >> ${out_all_galaxy}
end
