#!/usr/bin/csh

if ( $# != 1 ) then
  echo "example [./i.sh] [Binsize] "
  exit
endif

set Binsize = $argv[1]
echo "Binsize = $Binsize"

set Mean_Av_array = (3.15 2.33 2.49 3.60 4.56 7.45 4.98 4.39)
set Cloud_array   = (CHA_II LUP_I  LUP_III  LUP_IV SER PER OPH)
set WO_UkidssPath = '/home/jordan/YSO_Project/C2D-SWIRE_20180710/All_Converted_Catalog/2MASS_TO_UKIDSS/'
set WI_UkidssPath = '/home/jordan/YSO_Project/C2D-SWIRE_20180710/All_Converted_Catalog/UKIDSS_DR11PLUS_WI_2MASS_BR/ADD_UKIDSS/'

foreach i ( `seq 1 1 {$#Cloud_array}` )

	# Initialization
	echo $Cloud_array[$i]
	if ( -d "$Cloud_array[$i]" ) then
		echo 'Overwrite existed directory ...'
    	 rm -fr $Cloud_array[$i]
	endif
     mkdir $Cloud_array[$i]

	# Set up input catalog
	if ( $i <= 4 ) then
		set inp_catalog = {$WO_UkidssPath}catalog-{$Cloud_array[$i]}_2MASS_to_UKIDSS_HREL.tbl
	else
		set inp_catalog = {$WI_UkidssPath}catalog-$Cloud_array[$i]_C2D_UKIDSS_WI_2MASS_BR.tbl
	endif

	# Start computation
	cd $Cloud_array[$i]
	SOP_Execution_Preset.py $inp_catalog $Cloud_array[$i] New
	SOP_Execution_5D_method.py Default $Cloud_array[$i]
	SOP_Execution_6D_method.py $Cloud_array[$i] mag True Default $Binsize
	cd $Cloud_array[$i]_6D_BS_{$Binsize}
	SOP_Execution_Extinction_check.py $Cloud_array[$i] $Binsize $Mean_Av_array[$i]
	cd ../../

end
