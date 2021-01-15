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

# Initialization
if ( -d ${out_dir} ) then
    rm ${out_dir} && mkdir ${out_dir}
else
    mkdir ${out_dir}
cd ${out_dir}

cat ${out_int_hsieh} ${out_not_hsieh} >> ${out_all_new}

awk '$242~"FYSO"' ${out_all_new} > all_new_FYSO.tbl
awk '$242~"BYSO"' ${out_all_new} > all_new_BYSO.tbl
awk '$242!~"FYSO" && $242!~"BYSO"' ${out_all_new} > all_new_NFBYSO.tbl
