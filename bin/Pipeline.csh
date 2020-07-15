#!/usr/bin/csh
# ======================================================
# This program is a pipeline for cloud catalog
# MCCloud: CHA_II, LUP_I, LUP_III, LUP_IV, OPH, SER, PER
#
# Pipeline.csh [dim] [cube size] [sigma] [bond] [refD] [GP method]
#
# [dim]: dim of magnitude space (for now only '6')
# [cube size]: length of multi-d cube in magnitude unit
# [sigma]: standard deviation for gaussian dist. in magnitude
# [refD]: reference dimension which to modulus other dimension to
# [GP method]: BD/GD (Boundary method / Galaxy Dictionary method)
#
# Latest update JordanWu 2020/07/15
# ======================================================

# Variables
# ======================================================
# Help for input arguments
if ($#argv != 6) then
    echo "\n\tExample: Pipeline.csh [dimension] [cube size] [sigma] [bond] [refD] [GP method]"
    echo "\t[dimension]: dimension of magnitude space (for now only '6')"
    echo "\t[cube size]: length of multi-d cube in magnitude unit"
    echo "\t[sigma]: standard deviation for gaussian dist. in magnitude"
    echo "\t[refD]: reference dimension which to modulus other dimension to"
    echo "\t[GP method]: BD/GD (Boundary method/Galaxy Dictionary method)\n"
    exit
endif

# table, directory, and logfile
set YSO_table='/mazu/users/jordan/YSO_Project/YSO_Hunters_Table'
set SEIP_dir='/mazu/users/jordan/YSO_Project/SEIP_GP_Bound'
set logfile='term.out'
# command line argument
set dim=$1
set cube=$2
set sigma=$3
set bond=$4
set refD=$5
set method=$6
# cloud indice and ukidss observation indicator
set indice=(1 2 3 4 5 6 7)
set clouds=(CHA_II LUP_I LUP_III LUP_IV OPH SER PER)
set ukidss_obs=(0 0 0 0 1 1 1 )

# Main Program
# ======================================================
foreach i ($indice)
    # Initialization
    # --------------------------------------------------------------------------------------------------------
    set cloud=$clouds[$i]
    echo "\nInitializing $cloud ..."
    # Add artificial quality label and Start Preset Procedure
    # --------------------------------------------------------------------------------------------------------
    if (! -d $cloud ) mkdir $cloud && cd $cloud
    if ( -f $logfile ) rm $logfile
    /usr/bin/cp -f $YSO_table/All_Converted_Catalog/SPITZER/catalog-$cloud-HREL.tbl catalog-$cloud-HREL.tbl >> $logfile
    # WO/WI UKIDSS observation
    # --------------------------------------------------------------------------------------------------------
    echo "Adding magnitudes ..."
    if ( $ukidss_obs[$i] == 0 ) then
        Add_Mag_To_C2D_Full.py catalog-$cloud-HREL.tbl catalog-$cloud-HREL-Add_Mag.tbl >> $logfile
        TF_From_2MASS_To_UKIDSS_System.py catalog-$cloud-HREL-Add_Mag.tbl catalog-$cloud-HREL-Add_Mag-TF_UKIDSS.tbl >> $logfile
        echo "Adding artificial quality labels ..."
        Add_Mag_Qua_JHK_UKIDSS.py catalog-$cloud-HREL-Add_Mag-TF_UKIDSS.tbl default N A_fake >> $logfile
        Add_Mag_Qua_JHK_UKIDSS.py catalog-$cloud-HREL-Add_Mag-TF_UKIDSS-Add_JHK_Qua.tbl default U A_fake >> $logfile
        echo "Start setting neeed presets ..."
        SOP_Execution_Preset.py catalog-$cloud-HREL-Add_Mag-TF_UKIDSS-Add_JHK_Qua-Add_JHK_Qua.tbl $cloud Self_made >> $logfile
    else if ( $ukidss_obs[$i] == 1 ) then
        # Different UKIDSS observation programs
        # --------------------------------------------------------------------------------------------------------
        if ( $cloud == OPH ) then
            set ukidss_catalog="$YSO_table/All_UKIDSS_Catalog/UKIDSS_OBSERVATION/DR11PLUS/UKIDSS_GCS/UKIDSS_GCS_$cloud.csv"
            set header=13
        else if ( $cloud == SER ) then
            set ukidss_catalog="$YSO_table/All_UKIDSS_Catalog/UKIDSS_OBSERVATION/DR11PLUS/UKIDSS_GPS/UKIDSS_GPS_$cloud.csv"
            set header=13
       else if ( $cloud == PER ) then
            set ukidss_catalog="$YSO_table/All_UKIDSS_Catalog/UKIDSS_OBSERVATION/DR11PLUS/Survey_Merging/UKIDSS_COMBINED_$cloud.tbl"
            set header=0
        endif
        Add_Mag_JHK_UKIDSS_C2D_Combined.py catalog-$cloud-HREL.tbl $ukidss_catalog $header \
                                           catalog-$cloud-HREL-Add_Mag-Add_UKIDSS_JHK_2MASSBR.tbl 2MASSBR >> $logfile
        echo "Adding artificial quality labels ..."
        Add_Mag_Qua_JHK_UKIDSS.py catalog-$cloud-HREL-Add_Mag-Add_UKIDSS_JHK_2MASSBR.tbl N A_fake >> $logfile
        Add_Mag_Qua_JHK_UKIDSS.py catalog-$cloud-HREL-Add_Mag-Add_UKIDSS_JHK_2MASSBR-Add_JHK_Qua.tbl default U A_fake >> $logfile
        echo "Start setting neeed presets ..."
        SOP_Execution_Preset.py catalog-$cloud-HREL-Add_Mag-Add_UKIDSS_JHK_2MASSBR-Add_JHK_Qua.tbl $cloud Self_made >> $logfile
    else
        echo "Please check UKIDSS observation data ..."
    endif
    # Method to calculate galaxy probability (BD or GP)
    # --------------------------------------------------------------------------------------------------------
    echo "Calculating GP by $method method ..."
    if ( $method == BD ) then
        Calculate_GP_WI_6D_Bound_Array.py $cloud\_saturate_correct_file.tbl \
        $cloud mag $SEIP_dir/GPV_after_smooth_$dim\D_bin$cube\_sigma$sigma\_bond$bond\_refD$refD/after_smooth_$dim\D_lower_bounds_AlB0.npy \
        $SEIP_dir/GPV_after_smooth_$dim\D_bin$cube\_sigma$sigma\_bond$bond\_refD$refD/after_smooth_$dim\D_upper_bounds_AlB0.npy \
        012345 $cube $sigma $bond $refD >> $logfile
        set GP_out=$cloud\_6D_BD_GP_out_catalog.tbl
    else if ( $method == GD ) then
        Calculate_GP_WI_6D_Dict_Key_Tuple.py $dim $cube \
        $SEIP_dir/GPV_after_smooth_$dim\D_bin$cube\_sigma$sigma\_bond$bond\_refD$refD/ \
        $cloud\_saturate_correct_file.tbl $cloud mag True >> $logfile
        set GP_out=$cloud\_6D_GP_all_out_catalog.tbl
    else
        echo "No assigned method ..."
    endif
    # Classfy objects by galaxy probability and compare with Hsieh's 1310 YSO candidates
    echo "Classifying and compare with Hsieh's YSOc ..."
    # --------------------------------------------------------------------------------------------------------
    Classify_WI_6D_Galaxy_Prob.py $GP_out $cloud >> $logfile
    Check_Coord.py $cloud\_6D_YSO.tbl default $cloud\_YSO default 7 False >> $logfile
    Check_Coord.py $cloud\_6D_Galaxy.tbl default $cloud\_Galaxy default 7 False >> term.out
    Check_Coord.py $cloud\_6D_GP_to_image_check.tbl default $cloud\_6D_GP_IC default 7 False >> term.out
    Check_Coord.py $cloud\_6D_GP_others.tbl default $cloud\_6D_OTHERS default 7 False >> term.out
    # Single cloud ends and change directory to next one
    # --------------------------------------------------------------------------------------------------------
    echo "$cloud completes ...\n"
    cd .. && pwd
end
