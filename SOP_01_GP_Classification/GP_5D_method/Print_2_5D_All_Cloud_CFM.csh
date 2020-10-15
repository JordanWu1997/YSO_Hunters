#!/usr/bin/csh
# ======================================================
# This program is to collect information of each cloud
# and then print out as confusion matrix
#
# Latest update JordanWu 2020/07/27
# ======================================================

set indice=(1 2 3 4 5 6 7)
set clouds=(CHA_II LUP_I LUP_III LUP_IV OPH SER PER)

foreach i (${indice})
    cd ${clouds[${i}]}
    Print_2_5D_GPs_Confusion_Matrix.py ${clouds[${i}]}
    cd ../
end
