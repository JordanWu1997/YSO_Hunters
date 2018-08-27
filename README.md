# **YSO Hunters**
## **I.Introduction**
- Distinguishing Galaxies and Young Stellar Objects (YSOs) from a database solely containing magnitudes has been
proved to be a difficult task, since the physical composition of both types of objects are similar but with different
amount (Harvey et al. 2006). Hsieh & Lai (2013) found that YSOs can stand out from Galaxies in Multi-dimensional
Magnitude Space, and thus can be separated straightforwardly. Unfortunately, the computer memory required by
the Multi-dimensional Magnitude Space method is too much for a database with 8 photometric bands, so Hsieh & Lai
(2013) used two 5-dimensional arrays instead. Here we attempt to reduce the memory requirement by choosing the
proper magnitude range (mag1, mag2),so that mag<mag1 are (almost) certainly to be YSOs and mag>mag2 are all
Galaxies. Thus, the grid point required by the Multi-dimensional Magnitude Space will be greatly reduced. Our results
will test whether the two 5-dimensional arrays chosen in Hsieh & Lai (2013) are adequate.

## **II.Goal**
- 重現 Hsieh & Lai (2013) 之結果
- 使用新的邊界劃分(on multi-d MMD)節省計算multi-dimensional Magnitude Space之記憶體
- 將5-dimensional Magnitude Space延伸至更高維度(6,7,...)

## **III.Step**
![alt text](https://github.com/ShihPingLai/YSO_Hunters/blob/master/Steps.png)
## **IV.Star Removal**
![alt text](https://github.com/ShihPingLai/YSO_Hunters/blob/master/Star_removal.PNG)

## **VI.Problem**
- Inchone's YSO_table(Flux in all_candidatas.tbl) differ from our data source(Glue_7_Clouds.tbl)
  - Because we did not consider the extinction
## **VII.Work log**
- 7/19
  - Find the possible cause about problem 1 : We did not de-redden the whole c2d catalog
- 7/24
  - To realize the knowledge about extinction
- 7/25
  - Learn to use astropy to read the data from ds9
- 7/26
  - Discussion with Inchone Hsieh :
    - How to remove the Av from c2d sources
    - What are 'Image check '(step6) and 'IR1 image check'(step7)
- 8/06
  - check CHA_II catalog after extinction correction :
    - HREL is different from Hsieh's catalog (He may use Full table)
    - One candidate is missing in HREL table (Check Hsieh's table, that one is not in HREL table) 
- 8/07
  - Check data_type from Inchone's Chamaleon_RemoveStar_catalog (can_iden.tbl)
  - Remove star form every cloud catalog
- 8/14
  - Uncertainties Package (python's package to calculate uncertainties)
    - Maybe go wrong with log (since it uses Gaussian to fit, the upper and the lower are symmetric )
    - It can't use numpy or math (Use Uncertianties its own log etc.)
- 8/27
  - To write the each part of program about SOP
## **VIII.Data Sources**
- **Catalog from c2d & SWIRE :**
  - Molecular Clouds HREL catalog :
    - /data/public/spitzer/c2d/data.spitzer.caltech.edu/popular/c2d/20071101_enhanced_v1
  - Extinction Map (Av table) :
    - /cosmo/users/inchone/Remove_Av_sources_in_whole_clouds/Old/New_version/Backup_Av_table
  - Mosaic for Saturate Check
    - from Hsieh:
      - /data/users/inchone/Perseus/oldold/mosaic
    - from spitzer database:
      - /data/public/spitzer/c2d/data.spitzer.caltech.edu/popular/c2d/20071101_enhanced_v1/CHA_II/MOSAICS

- **Programs from Inchone Hsieh :**
  - Galaxy Probability:
    - /cosmo/users/inchone/Remove_Av_sources_in_whole_clouds/SWI_c2d_PSD_new_process2_multi-dim_version/J_MP1_plus_IR1_MP1_methed
  - Galaxy Probability (p):
    - /cosmo/users/inchone/Remove_Av_sources_in_whole_clouds/SWI_c2d_PSD_new_process2_multi-dim_version/J_MP1_plus_IR1_MP1_methed/Chamaeleon/YSO_Selection
  - Remove Av:
    - /cosmo/users/inchone/Remove_Av_sources_in_whole_clouds/Old/New_version/
  - Saturate Check:
    - /cosmo/users/inchone/Remove_Av_sources_in_whole_clouds/SWI_c2d_PSD_new_process2_multi-dim_version/J_MP1_plus_IR1_MP1_methed/Perseus
  - Get IR Image:  
    - /cosmo/users/inchone/Remove_Av_sources_in_whole_clouds/Old/multi-dim_version/Saturate_and_Band_fill_correct/Chamaleon/Saturate_no_count/getfits.py
  - Image Check:
    - /cosmo/users/inchone/Remove_Av_sources_in_whole_clouds/SWI_c2d_PSD_new_process2_multi-dim_version/J_MP1_plus_IR1_MP1_methed/Perseus/YSO_Selection/notPSF1_check
## **X.Improve**
- Make all procession be automatic
- Reduce the errors about extinction correction
- Use marginal curved surface instead of the marginal plane
## **IX.Reference**
**Hsieh and Lai's Result vs Evan's Result :**
![alt_text](https://github.com/ShihPingLai/YSO_Hunters/blob/master/Hsieh's_Result.png)
**Hsieh and Lai's missing YSOs :**
![alt text](https://github.com/ShihPingLai/YSO_Hunters/blob/master/Hsieh's_missing_YSO.png)
**Catalog Classification from c2d legacy project :**
![alt text](https://github.com/ShihPingLai/YSO_Hunters/blob/master/c2d_obtype.png)
