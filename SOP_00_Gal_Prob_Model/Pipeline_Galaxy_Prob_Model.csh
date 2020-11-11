#!/usr/bin/csh
# ====================================================================================================
# This program is a pipeline to construct galaxy probability
#
# Example: Pipeline_Galaxy_Prob.csh [input catalog] [datatype] [qualabel] [dimension] \
#                                   [sigma] [bond] [cube size] [refD] \
#                                   [smooth] [slice] [one by one] [GP method] [Plot]
# Input Variables:
#   [input catalog]: must include magnitudes if datatype is 'mag'"
#   [datatype]:      'mag' or 'flux' input data in magnitude or flux (mJy)"
#   [qualabel]:      if flux quality is considered in calculation"
#   [dimension]:     dimension of magnitude space (for now only '6')"
#   [cube size]:     length of multi-d cube in magnitude unit"
#   [sigma]:         standard deviation for gaussian dist. in magnitude"
#   [bond]:          bondary of gaussian smooth"
#   [refD]:          reference dimension which to modulus other dimension to"
#   [smooth]:        gaussian smooth or use existed gaussian smooth result if there is one (yes/no)
#   [slice]:         the number of slice to gaussian smooth input catalog"
#   [one by one]:    load slice of smooth input one by one or not (True/False)"
#   [GP method]:     BD/GD (Boundary method/Galaxy Dictionary method)"
#   [plot]: plot     galaxy probability 2D & 3D scatter (yes/no)\n"
#
# Latest update JordanWu 2020/09/19
# ====================================================================================================

# Variables
# ======================================================
if ( ${#argv} != 14 ) then
    echo "\n\tError Usage"
    echo "\tExample: Pipeline_Galaxy_Prob.csh\
                     [input catalog] [catalog format] [datatype] [qualabel]\
                     [dimension] [cube size] [sigma] [bond] [refD] \
                     [smooth] [slice] [one by one]\
                     [GP method] [plot]\n"
    echo "\t[input catalog]: must include magnitudes if datatype is 'mag'"
    echo "\t[catalog format]: format of catalog (SEIP_JACOB/C2D_HSIEH)"
    echo "\t[datatype]: input data in type of magnitude or flux (in mJy) ('mag' or 'flux')"
    echo "\t[qualabel]: if flux quality is considered in calculation (yes/no)"
    echo "\t[dimension]: dimension of magnitude space (for now only '6')"
    echo "\t[cube size]: length of multi-d cube in magnitude unit (must in float)"
    echo "\t[sigma]: standard deviation for gaussian dist. in magnitude (must in integer)"
    echo "\t[bond]: bondary of gaussian smooth (must in integer)"
    echo "\t[refD]: reference dimension which to modulus other dimension to (must in integer)"
    echo "\t[smooth]: gaussian smooth or use existed gaussian smooth result if there is one (yes/no)"
    echo "\t[slice]: the number of slice to gaussian smooth input catalog (must in integer)"
    echo "\t[one by one]: load slice of smooth input one by one or not (yes/no)"
    echo "\t[GP method]: Boundary method/Galaxy Dictionary method (BD/GD/BOTH)"
    echo "\t[plot]: plot galaxy probability 2D & 3D scatter (yes/no)\n"
    echo "\t*** If gal_pos has already been calculated, just use 'SKIP' as input to 'input catalog', 'catalog format', 'datatype', 'qualabel'"
    echo "\t*** If 'smooth' option is 'no', then just use 'SKIP' as input to 'slice', 'one bye one'\n"
    exit
endif

# Command Line Argument
set inp_catalog=${1}
set cat_format=${2}
set cat_datatype=${3}
set dim=${5}
set cube=${6}
set sigma=${7}
set bond=${8}
set refD=${9}
set smooth_option=${10}
set slice_num=${11}
set one_by_one=${12}
set GP_method=${13}
set plot=${14}

if ( $4 == yes ) then
    set qua_label = True
else
    set qua_label = False
endif

# Generate Full Inp bands
set i = 0
set full_inp = ""
while ($i < $dim)
   set full_inp = "${full_inp}${i}"
   @ i++
end

# Assign BD method along axis
set BD_axis = 0

# Input Variables
set thread=10
set logfile='term.out'
set bin_dir=GPV_smooth_sigma${sigma}_bond${bond}_refD${refD}
set pos_slice_num=10
set inc=45

# Main Programs
# ======================================================

# Count Gal Position
if ( ${inp_catalog} != SKIP) then
    echo 'Counting Galaxy Position ...'
    Count_Gal_Pos_Vec_numba.py ${inp_catalog} ${cat_format} ${cat_datatype} ${qua_label} ${dim} ${cube} | tee -a $logfile
    Sort_Source_Lack999_Execution_All.py ${dim} ${cube} | tee -a $logfile
else
    echo 'Galaxy Position has been counted ... [SKIP]'
endif

# Do Gaussian Smooth
if ( ${smooth_option} == yes ) then
    echo 'Gaussian Smoothing ...'
    if (! -d ${bin_dir} ) Do_Gaussian_Smooth_Construct_Bin.py ${sigma} ${bond} ${refD} | tee -a $logfile
    Do_Gaussian_Smooth_Execution_All.py ${dim} ${cube} ${sigma} ${bond} ${refD} ${slice_num} ${one_by_one} | tee -a $logfile
else
    echo 'Gaussian Smooth has been done ... [SKIP]'
endif

# GP Method for Calculation
if ( ${GP_method} == GD ) then
    echo 'Constructing Galaxy Probability ... [GD method]'
    Update_GP_Dict_Key_Tuple.py ${dim} ${cube} ${sigma} ${bond} ${refD} | tee -a $logfile
else if ( ${GP_method} == BD ) then
    echo 'Constructing Galaxy Probability ... [BD method]'
    Find_Galaxy_Prob_Bounary_Along_Basis.py ${dim} ${cube} ${sigma} ${bond} ${refD} ${full_inp} ${BD_axis} -n_th ${thread} | tee -a $logfile
else if ( ${GP_method} == BOTH) then
    echo 'Constructing Galaxy Probability ... [GD method]'
    Update_GP_Dict_Key_Tuple.py ${dim} ${cube} ${sigma} ${bond} ${refD} | tee -a $logfile
    echo 'Constructing Galaxy Probability ... [BD method]'
    Find_Galaxy_Prob_Bounary_Along_Basis.py ${dim} ${cube} ${sigma} ${bond} ${refD} ${full_inp} ${BD_axis} -n_th ${thread} | tee -a $logfile
else
    echo 'Wrong GP_method ...' && exit
endif

# Plot for Galaxy Probability (2D tomography & 3D)
if ( ${plot} == yes ) then
    Make_Galaxy_Prob_Plot_Execution_All.py ${dim} ${cube} ${sigma} ${bond} ${refD} ${pos_slice_num} ${inc} | tee -a $logfile
else
    echo 'No Galaxy Probability Plots ... [SKIP]'
endif

# Save logfile
mv $logfile GPV_after_smooth_${dim}D_bin${cube}_sigma${sigma}_bond${bond}_refD${refD}/
