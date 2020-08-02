# Executable Programs for YSO Hunters

### Part 0 - About Pipelines
- #### Pipeline_Classification.csh
  - Pipeline for galaxy probability classification
### Part 1 - About Catalogs
- #### TF_To_C2D_Format_Catalog.py
  - Transform to unified catalog for usage in YSO Hunters
- #### TF_From_2MASS_To_UKIDSS_System.py
  -  Transform photometry system from 2MASS to UKIDSS
- #### Merge_UKIDSS_Survey.py
  - Merge different surveys of UKIDSS data (e.g. PER)
- #### Add_Mag_JHK_UKIDSS_C2D_Combined.py
  - Add magnitudes of J,H,K band to input catalog
    - For bright sources (J > 11.5 mag), transform system from 2MASS to UKIDSS
    - For faint sources (Not bright one), replace catalog data with data on input UKIDSS survey catalog 
  - Add magnitudes of IR1, IR2, IR3, IR4, MP1 band to input catalog
- #### Add_Mag_Qua_JHK_UKIDSS.py
  - Make artificial flux/mag quality labels for UKIDSS data since there are no quality labels on UKIDSS survey
- #### Add_Mag_To_C2D_Full.py
  - Add magnitudes from J to MP1 (8 bands) to input catalog (which should already have flux data)

### Part 2 - About Images
- #### WCS_To_Fits.py
  - Directly get fits image with input RA DEC (in deg)

### Part 3 - About Extinction
- #### Calculate_Extinction.py
  - Use NICER to calculate extinction and export extinction map and extinction table (This program is from Jacob)
- #### Make_Extinction_Table.py
  - Make extinction table from extinction map
- #### Hist_Av.py
  - Plot histograms of the extinction maps of seven different molecular clouds

### Part 4 - Others
- #### Make_GIF.sh
  - Make png images to gif animations
- #### Check_Coord.py
  - Check same sources of two input catalogs
- #### Make_SED_Plot.py
  - Make SED for sources of input catalog
- #### Print_Out_Catalog.py
  - Print out contents of input catalog in specific order
  
