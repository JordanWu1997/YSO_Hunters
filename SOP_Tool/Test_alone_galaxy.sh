#!/bin/csh

cat SWIRE_6D_GP_to_image_check.tbl SWIRE_6D_YSO.tbl > Candidates_to_check_GP.tbl
awk '$243!~/no_count/ {print $243}' Candidates_to_check_GP.tbl | wc
awk '$243!~/no_count/ && $243=="1e-05"{print $243}' Candidates_to_check_GP.tbl | wc
awk '$243!~/no_count/ && $243=="1e-05"' Candidates_to_check_GP.tbl > Alone_Galaxy.tbl
awk '{print $36, $99, $120, $141, $162, $183, $243, $244, $245}' Alone_Galaxy.tbl | more
