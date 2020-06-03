# Executable Programs for YSO Hunters

### Part 1 - About Catalogs
- Merge_UKIDSS_Survey.py
  - Merge different surveys of UKIDSS data (e.g. PER)
- TF_From_2MASS_To_UKIDSS_System.py
  -  Transform photometry system from 2MASS to UKIDSS
- TF_To_C2D_Format_Catalog.py
  - Transform to unified catalog for usage in YSO Hunters
- Add_Mag_JHK_UKIDSS_C2D_Combined.py
  - Add magnitudes of J,H,K band to input catalog
    - For bright sources (J > 11.5 mag), transform system from 2MASS to UKIDSS
    - For faint sources (Not bright one), replace catalog data with data on input UKIDSS survey catalog 
  - Add magnitudes of IR1, IR2, IR3, IR4, MP1 band to input catalog *(must already be transformed)*
- Add_Mag_Qua_JHK_UKIDSS.py
  - Make artificial flux/mag quality labels for UKIDSS data since there's no quality labels on UKIDSS survey
- Add_Mag_To_C2D_Full.py
  - Add magnitudes from J to MP1 (8 bands) to input catalog (which should already have flux data)

### Part 2 - About Images
- Deg_To_WCS.py
- Get_Fits.py
- WCS_To_Fits.py

### Part 3 - About Extinction
- Calculate_Extinction.py
- Get_Av_table.py
- Make_Extinction_Table.py
- Hist_Av.py

### Part 4 - Others
- Make_GIF.sh
- Check_Coord.py
- Make_SED_Plot.py
- Print_Out_Catalog.py
