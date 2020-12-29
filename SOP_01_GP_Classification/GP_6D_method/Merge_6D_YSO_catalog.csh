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
set out_all_new='all_new_YSO.tbl'

if ( ! -d ${out_dir} ) mkdir ${out_dir} && cd ${out_dir}
foreach cloud (${clouds})
    cat ../${cloud}/AND_${cloud}_YSO_all_Hsieh_YSOc.tbl >> ${out_int_hsieh}
    cat ../${cloud}/DIFF_${cloud}_YSO.tbl >> ${out_not_hsieh}
end
cat ${out_int_hsieh} ${out_not_hsieh} >> ${out_all_new}

# For normal BD method
#awk '$242~"UYSO"' ${out_all_new} > all_new_UYSO.tbl
#awk '$242~"LYSO"' ${out_all_new} > all_new_LYSO.tbl
#awk '$242!~"UYSO" && $242!~"LYSO"' ${out_all_new} > all_new_NULYSO.tbl

# For Diag BD method
awk '$272~"LYSO"' ${out_all_new} > all_new_LYSO.tbl
awk '$272!~"UYSO" && $272!~"LYSO"' ${out_all_new} > all_new_NULYSO.tbl
