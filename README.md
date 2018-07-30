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
- 使用新的邊界劃分節省計算multi-dimensional Magnitude Space之記憶體
- 將5-dimensional Magnitude Space延伸至更高維度(6,7,...)

## **III.Step**
![alt text](https://github.com/ShihPingLai/YSO_Hunters/blob/master/Steps.png)
- [ ] step 1
- [ ] step 2
- [X] step 3
- [ ] step 4
- [X] step 5
- [ ] step 6
- [ ] step 7
- [ ] step 8
## **IV.Extinction**
## **V.Result**
![alt text](https://github.com/ShihPingLai/YSO_Hunters/blob/master/inchone_vs_YSOHunters_7.19.png)
## **VI.Problem**
- Inchone's YSO_table(Flux in all_candidatas.tbl) differ from our data source(Glue_7_Clouds.tbl)
- Our YSO table(Glue_7_Clouds_yso_candidates) does not entirely containe lInchone's YSO table(all_candidatas.tb)
## **VII.Work log**
- 7/19
  - Find the possible cause about problem 1 : We did not de-redden the whole c2d catalog
- 7/24
  - To realize the knowledge about extinction
- 7/25
  - Learn to use astropy to read the data from ds9
- 7/26
  - To handle problems with Ichone :
    - How to remove the Av from c2d sources
    - What are 'Image check '(step6) and 'IR1 image check'(step7)
    - 
## **VIII.Data Sources**
- Molecular Clouds HREL catalog :
  - /data/public/spitzer/c2d/data.spitzer.caltech.edu/popular/c2d/20071101_enhanced_v1
- Programs from Inchone Hsieh :
  - Galaxy Probability:
    - /cosmo/users/inchone/Remove_Av_sources_in_whole_clouds/SWI_c2d_PSD_new_process2_multi-dim_version/J_MP1_plus_IR1_MP1_methed
  - Remove Av:
    - /cosmo/users/inchone/Remove_Av_sources_in_whole_clouds/Old/New_version/
  - Saturate Check:
    - /cosmo/users/inchone/Remove_Av_sources_in_whole_clouds/SWI_c2d_PSD_new_process2_multi-dim_version/J_MP1_plus_IR1_MP1_methed/Perseus
  - Image Check:
    - /cosmo/users/inchone/Remove_Av_sources_in_whole_clouds/SWI_c2d_PSD_new_process2_multi-dim_version/J_MP1_plus_IR1_MP1_methed/Perseus/YSO_Selection/notPSF1_check
## **IX.Reference**
