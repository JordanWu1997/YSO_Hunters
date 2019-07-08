#!/bin/csh

rm -Ir '6D_BS=0.2_WI_CONDITION'
rm -Ir '6D_BS=0.4_WI_CONDITION'

mkdir '6D_BS=0.2_WI_CONDITION'
mkdir '6D_BS=0.4_WI_CONDITION'
cat LUP_IV_YSO.tbl LUP_IV_GP_to_image_check.tbl > LUP_IV_OLD_ALGO.tbl

cd '6D_BS=0.2_WI_CONDITION'
new_dict_6D_method.py  ../catalog-LUP_IV_Gal_Prob_All.tbl LUP_IV mag new 0.2 argv
Check_6D_Gal_Prob.py LUP_IV_6D_GP_all_out_catalog.tbl LUP_IV
cat LUP_IV_6D_YSO.tbl LUP_IV_6D_GP_to_image_check.tbl > LUP_IV_NEW_ALGO.tbl

mkdir 'NEW_OLD_COMPARISON'
cd 'NEW_OLD_COMPARISON'
Comparator_SWIRE_format.py ../LUP_IV_NEW_ALGO.tbl ../../LUP_IV_OLD_ALGO.tbl NEW_ALGO OLD_ALGO 7 yes no
Get_Galaxy_Samples_MMD_wo_annotate.py NEW_ALGO_and_OLD_ALGO.tbl not_NEW_ALGO_but_OLD_ALGO.tbl not_OLD_ALGO_but_NEW_ALGO.tbl True new &
awk '{print "fk5;point(", $1, ",", $3 ")#point=cross color=green"}' NEW_ALGO_and_OLD_ALGO.tbl > BOTH_OLD_NEW_ALGO.reg
awk '{print "fk5;point(", $1, ",", $3 ")#point=cross color=blue"}' not_NEW_ALGO_but_OLD_ALGO.tbl > ONLY_OLD_ALGO.reg
awk '{print "fk5;point(", $1, ",", $3 ")#point=cross color=red"}' not_OLD_ALGO_but_NEW_ALGO.tbl > ONLY_NEW_ALGO.reg

mkdir 'HIGH_AV'
mkdir 'LOW_AV'
cd 'HIGH_AV'
awk '$18>5.0{print "fk5;point(", $1, ",", $3 ")#point=cross color=yello"}' ../NEW_ALGO_and_OLD_ALGO.tbl > BOTH_OLD_NEW_ALGO.reg
awk '$18>5.0{print "fk5;point(", $1, ",", $3 ")#point=cross color=cyan"}' ../not_NEW_ALGO_but_OLD_ALGO.tbl > ONLY_OLD_ALGO.reg
awk '$18>5.0{print "fk5;point(", $1, ",", $3 ")#point=cross color=violet"}' ../not_OLD_ALGO_but_NEW_ALGO.tbl > ONLY_NEW_ALGO.reg
awk '$18>5.0' ../NEW_ALGO_and_OLD_ALGO.tbl > BOTH_OLD_NEW_ALGO.tbl
awk '$18>5.0' ../not_NEW_ALGO_but_OLD_ALGO.tbl > ONLY_OLD_ALGO.tbl
awk '$18>5.0' ../not_OLD_ALGO_but_NEW_ALGO.tbl > ONLY_NEW_ALGO.tbl
mkdir 'BOTH_OLD_NEW_ALGO_SED'
mkdir 'ONLY_OLD_ALGO_SED'
mkdir 'ONLY_NEW_ALGO_SED'
cd 'BOTH_OLD_NEW_ALGO_SED'
#Make_SED_Plot.py ../BOTH_OLD_NEW_ALGO.tbl 10
cd ../'ONLY_OLD_ALGO_SED'
#Make_SED_Plot.py ../ONLY_OLD_ALGO.tbl 10
cd ../'ONLY_NEW_ALGO_SED'
#Make_SED_Plot.py ../ONLY_NEW_ALGO.tbl 10

cd ../../'LOW_AV'
awk '$18<=5.0{print "fk5;point(", $1, ",", $3 ")#point=cross color=green"}' ../NEW_ALGO_and_OLD_ALGO.tbl > BOTH_OLD_NEW_ALGO.reg
awk '$18<=5.0{print "fk5;point(", $1, ",", $3 ")#point=cross color=blue"}' ../not_NEW_ALGO_but_OLD_ALGO.tbl > ONLY_OLD_ALGO.reg
awk '$18<=5.0{print "fk5;point(", $1, ",", $3 ")#point=cross color=red"}' ../not_OLD_ALGO_but_NEW_ALGO.tbl > ONLY_NEW_ALGO.reg
awk '$18<=5.0' ../NEW_ALGO_and_OLD_ALGO.tbl > BOTH_OLD_NEW_ALGO.tbl
awk '$18<=5.0' ../not_NEW_ALGO_but_OLD_ALGO.tbl > ONLY_OLD_ALGO.tbl
awk '$18<=5.0' ../not_OLD_ALGO_but_NEW_ALGO.tbl > ONLY_NEW_ALGO.tbl
mkdir 'BOTH_OLD_NEW_ALGO_SED'
mkdir 'ONLY_OLD_ALGO_SED'
mkdir 'ONLY_NEW_ALGO_SED'
cd 'BOTH_OLD_NEW_ALGO_SED'
#Make_SED_Plot.py ../BOTH_OLD_NEW_ALGO.tbl 10
cd ../'ONLY_OLD_ALGO_SED'
#Make_SED_Plot.py ../ONLY_OLD_ALGO.tbl 10
cd ../'ONLY_NEW_ALGO_SED'
#Make_SED_Plot.py ../ONLY_NEW_ALGO.tbl 10

cd ../../../../'6D_BS=0.4_WI_CONDITION'
new_dict_6D_method.py  ../catalog-LUP_IV_Gal_Prob_All.tbl LUP_IV mag new 0.4 argv
Check_6D_Gal_Prob.py LUP_IV_6D_GP_all_out_catalog.tbl LUP_IV
cat LUP_IV_6D_YSO.tbl LUP_IV_6D_GP_to_image_check.tbl > LUP_IV_NEW_ALGO.tbl

mkdir 'NEW_OLD_COMPARISON'
cd 'NEW_OLD_COMPARISON'
Comparator_SWIRE_format.py ../LUP_IV_NEW_ALGO.tbl ../../LUP_IV_OLD_ALGO.tbl NEW_ALGO OLD_ALGO 7 yes no
Get_Galaxy_Samples_MMD_wo_annotate.py NEW_ALGO_and_OLD_ALGO.tbl not_NEW_ALGO_but_OLD_ALGO.tbl not_OLD_ALGO_but_NEW_ALGO.tbl True new &
awk '{print "fk5;point(", $1, ",", $3 ")#point=cross color=green"}' NEW_ALGO_and_OLD_ALGO.tbl > BOTH_OLD_NEW_ALGO.reg
awk '{print "fk5;point(", $1, ",", $3 ")#point=cross color=blue"}' not_NEW_ALGO_but_OLD_ALGO.tbl > ONLY_OLD_ALGO.reg
awk '{print "fk5;point(", $1, ",", $3 ")#point=cross color=red"}' not_OLD_ALGO_but_NEW_ALGO.tbl > ONLY_NEW_ALGO.reg

#==============================================================================================================================================
mkdir 'Extinction_Check_Av_bound=5.0'
cd 'Extinction_Check_Av_bound=5.0'
awk '($101!="E" && $101 != "U" && $99 > 15.0) && ($122!="E" && $122 != "U" && $120 > 15.0) && ($185!="E" && $185 != "U" && $183 > 9.0)' ../../LUP_IV_NEW_ALGO.tbl > LUP_IV_NEW_ALGO_Extinction_check.tbl
awk '($101!="E" && $101 != "U" && $99 <= 15.0) && ($122!="E" && $122 != "U" && $120 <= 15.0) && ($185!="E" && $185 != "U" && $183 <= 9.0)' ../../LUP_IV_NEW_ALGO.tbl > LUP_IV_NEW_ALGO_No_Extinction_check.tbl
awk '$18>5.0' LUP_IV_NEW_ALGO_Extinction_check.tbl > LUP_IV_NEW_ALGO_HIGH_AV.tbl
awk '$18<=5.0' LUP_IV_NEW_ALGO_Extinction_check.tbl > LUP_IV_NEW_ALGO_LOW_AV.tbl
awk '$18>5.0{print "fk5;point(", $1, ",", $3 ")#point=cross color=red"}' LUP_IV_NEW_ALGO_Extinction_check.tbl > LUP_IV_NEW_ALGO_HIGH_AV.reg
awk '$18<=5.0{print "fk5;point(", $1, ",", $3 ")#point=cross color=green"}' LUP_IV_NEW_ALGO_Extinction_check.tbl > LUP_IV_NEW_ALGO_LOW_AV.reg
mkdir 'HIGH_AV'
mkdir 'LOW_AV'
cd 'HIGH_AV'
Make_SED_Plot.py ../LUP_IV_NEW_ALGO_HIGH_AV.tbl 10
cd ../'LOW_AV'
Make_SED_Plot.py ../LUP_IV_NEW_ALGO_LOW_AV.tbl 10
cd ../../

mkdir 'Extinction_Check_Av_bound=mean'
cd 'Extinction_Check_Av_bound=mean'
awk '($101!="E" && $101 != "U" && $99 > 15.0) && ($122!="E" && $122 != "U" && $120 > 15.0) && ($185!="E" && $185 != "U" && $183 > 9.0)' ../../LUP_IV_NEW_ALGO.tbl > LUP_IV_NEW_ALGO_Extinction_check.tbl
awk '($101!="E" && $101 != "U" && $99 <= 15.0) && ($122!="E" && $122 != "U" && $120 <= 15.0) && ($185!="E" && $185 != "U" && $183 <= 9.0)' ../../LUP_IV_NEW_ALGO.tbl > LUP_IV_NEW_ALGO_No_Extinction_check.tbl
awk '$18>3.8' LUP_IV_NEW_ALGO_Extinction_check.tbl > LUP_IV_NEW_ALGO_HIGH_AV.tbl
awk '$18<=3.8' LUP_IV_NEW_ALGO_Extinction_check.tbl > LUP_IV_NEW_ALGO_LOW_AV.tbl
awk '$18>3.8{print "fk5;point(", $1, ",", $3 ")#point=cross color=red"}' LUP_IV_NEW_ALGO_Extinction_check.tbl > LUP_IV_NEW_ALGO_HIGH_AV.reg
awk '$18<=3.8{print "fk5;point(", $1, ",", $3 ")#point=cross color=green"}' LUP_IV_NEW_ALGO_Extinction_check.tbl > LUP_IV_NEW_ALGO_LOW_AV.reg
mkdir 'HIGH_AV'
mkdir 'LOW_AV'
cd 'HIGH_AV'
Make_SED_Plot.py ../LUP_IV_NEW_ALGO_HIGH_AV.tbl 10
cd ../'LOW_AV'
Make_SED_Plot.py ../LUP_IV_NEW_ALGO_LOW_AV.tbl 10
cd ../../
#==============================================================================================================================================

mkdir 'HIGH_AV'
mkdir 'LOW_AV'
cd 'HIGH_AV'
awk '$18>5.0{print "fk5;point(", $1, ",", $3 ")#point=cross color=yellow"}' ../NEW_ALGO_and_OLD_ALGO.tbl > BOTH_OLD_NEW_ALGO.reg
awk '$18>5.0{print "fk5;point(", $1, ",", $3 ")#point=cross color=cyan"}' ../not_NEW_ALGO_but_OLD_ALGO.tbl > ONLY_OLD_ALGO.reg
awk '$18>5.0{print "fk5;point(", $1, ",", $3 ")#point=cross color=violet"}' ../not_OLD_ALGO_but_NEW_ALGO.tbl > ONLY_NEW_ALGO.reg
awk '$18>5.0' ../NEW_ALGO_and_OLD_ALGO.tbl > BOTH_OLD_NEW_ALGO.tbl
awk '$18>5.0' ../not_NEW_ALGO_but_OLD_ALGO.tbl > ONLY_OLD_ALGO.tbl
awk '$18>5.0' ../not_OLD_ALGO_but_NEW_ALGO.tbl > ONLY_NEW_ALGO.tbl
mkdir 'BOTH_OLD_NEW_ALGO_SED'
mkdir 'ONLY_OLD_ALGO_SED'
mkdir 'ONLY_NEW_ALGO_SED'
cd 'BOTH_OLD_NEW_ALGO_SED'
Make_SED_Plot.py ../BOTH_OLD_NEW_ALGO.tbl 10
cd ../'ONLY_OLD_ALGO_SED'
Make_SED_Plot.py ../ONLY_OLD_ALGO.tbl 10
cd ../'ONLY_NEW_ALGO_SED'
Make_SED_Plot.py ../ONLY_NEW_ALGO.tbl 10

cd ../../'LOW_AV'
awk '$18<=5.0{print "fk5;point(", $1, ",", $3 ")#point=cross color=green"}' ../NEW_ALGO_and_OLD_ALGO.tbl > BOTH_OLD_NEW_ALGO.reg
awk '$18<=5.0{print "fk5;point(", $1, ",", $3 ")#point=cross color=blue"}' ../not_NEW_ALGO_but_OLD_ALGO.tbl > ONLY_OLD_ALGO.reg
awk '$18<=5.0{print "fk5;point(", $1, ",", $3 ")#point=cross color=red"}' ../not_OLD_ALGO_but_NEW_ALGO.tbl > ONLY_NEW_ALGO.reg
awk '$18<=5.0' ../NEW_ALGO_and_OLD_ALGO.tbl > BOTH_OLD_NEW_ALGO.tbl
awk '$18<=5.0' ../not_NEW_ALGO_but_OLD_ALGO.tbl > ONLY_OLD_ALGO.tbl
awk '$18<=5.0' ../not_OLD_ALGO_but_NEW_ALGO.tbl > ONLY_NEW_ALGO.tbl
mkdir 'BOTH_OLD_NEW_ALGO_SED'
mkdir 'ONLY_OLD_ALGO_SED'
mkdir 'ONLY_NEW_ALGO_SED'
cd 'BOTH_OLD_NEW_ALGO_SED'
Make_SED_Plot.py ../BOTH_OLD_NEW_ALGO.tbl 10
cd ../'ONLY_OLD_ALGO_SED'
Make_SED_Plot.py ../ONLY_OLD_ALGO.tbl 10
cd ../'ONLY_NEW_ALGO_SED'
Make_SED_Plot.py ../ONLY_NEW_ALGO.tbl 10
