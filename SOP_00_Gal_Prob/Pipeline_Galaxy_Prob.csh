#!/usr/bin/csh
# ====================================================================================================
# This program is a pipeline to construct galaxy probability
#
# Example: Pipeline_Galaxy_Prob.csh [input catalog] [datatype] [qualabel] [dimension] \
#                                   [sigma] [bond] [cube size] [refD] [slice] [one by one] [GP method]
# Input Variables:
#   [input catalog]: must include magnitudes if datatype is 'mag'"
#   [datatype]:      'mag' or 'flux' input data in magnitude or flux (mJy)"
#   [qualabel]:      if flux quality is considered in calculation"
#   [dimension]:     dimension of magnitude space (for now only '6')"
#   [sigma]:         standard deviation for gaussian dist. in magnitude"
#   [bond]:          bondary of gaussian smooth"
#   [cube size]:     length of multi-d cube in magnitude unit"
#   [refD]:          reference dimension which to modulus other dimension to"
#   [slice]:         the number of slice to gaussian smooth input catalog"
#   [one by one]:    load slice of smooth input one by one or not (True/False)"
#   [GP method]:     BD/GD (Boundary method/Galaxy Dictionary method)"
#
# Latest update JordanWu 2020/07/16
# ====================================================================================================

# Variables
# ======================================================
if ( ${#argv} != 11 ) then
    echo "\n\tError Usage"
    echo "\tExample: Pipeline_Galaxy_Prob.csh [input catalog] [datatype] [qualabel] \
                                            [dimension] [sigma] [bond] [cube size] [refD] [slice] [one by one] [GP method]"
    echo "\t[input catalog]: must include magnitudes if datatype is 'mag'"
    echo "\t[datatype]: 'mag' or 'flux' input data in magnitude or flux (mJy)"
    echo "\t[qualabel]: if flux quality is considered in calculation"
    echo "\t[dimension]: dimension of magnitude space (for now only '6')"
    echo "\t[sigma]: standard deviation for gaussian dist. in magnitude"
    echo "\t[bond]: bondary of gaussian smooth"
    echo "\t[cube size]: length of multi-d cube in magnitude unit"
    echo "\t[refD]: reference dimension which to modulus other dimension to"
    echo "\t[slice]: the number of slice to gaussian smooth input catalog"
    echo "\t[one by one]: load slice of smooth input one by one or not (yes/no)"
    echo "\t[GP method]: BD/GD (Boundary method/Galaxy Dictionary method)\n"
    exit
endif

# Command Line Argument
set inp_catalog=${1}
set cat_datatype=${2}
set qua_label=${3}
set dim=${4}
set sigma=${5}
set bond=${6}
set cube=${7}
set refD=${8}
set slice_num=${9}
set one_by_one=${10}
set GP_method=${11}
# Input Variables
set thread=10
set logfile='term.out'
set bin_dir=GPV_smooth_sigma${sigma}_bond${bond}_refD${refD}
set pos_slice_num=10
set inc=45

# Main Programs
# ======================================================

# Count Gal Position
echo 'Counting Galaxy Position ...'
Count_Gal_Pos_Vec_numba.py ${inp_catalog} ${cat_datatype} ${qua_label} ${dim} ${cube} | tee -a $logfile
Sort_Source_Lack999_Execution_All.py ${dim} ${cube} | tee -a $logfile

# Do Gaussian Smooth
echo 'Gaussian Smoothing ...'
if (! -d ${bin_dir} ) Do_Gaussian_Smooth_Construct_Bin.py ${sigma} ${bond} ${refD} | tee -a $logfile
Do_Gaussian_Smooth_Execution_All.py ${dim} ${cube} ${sigma} ${bond} ${refD} ${slice_num} ${one_by_one} | tee -a $logfile

# GP Method for calculation
echo 'Constructing Galaxy Probability ...'
if ( ${GP_method} == GD ) then
    Update_GP_Dict_Key_Tuple.py ${dim} ${cube} ${sigma} ${bond} ${refD} | tee -a $logfile
else if ( ${GP_method} == BD ) then
    Find_Galaxy_Prob_6D_Boundary_Along_Band_Parallel.py ${dim} ${cube} ${sigma} ${bond} ${refD} 012345 0 default default ${thread} | tee -a $logfile
else
    echo 'Wrong GP_method ...' && exit
endif

# Plot for Galaxy Probability (2D tomography & 3D)
if ( ${plot} == yes ) then
    Make_Galaxy_Prob_Plot_Execution_All.py ${dim} ${cube} ${sigma} ${bond} ${refD} ${pos_slice_num} ${inc} | tee -a $logfile
else
    echo 'No Galaxy Probability Plots ...'
endif

# Save logfile
mv $logfile GPV_after_smooth_${dim}D_bin${cube}_sigma${sigma}_bond${bond}_refD${refD}/
