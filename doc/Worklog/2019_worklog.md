## **V.Problem**
- Inchone's YSO_table(Flux in all_candidatas.tbl) differ from our data source(Glue_7_Clouds.tbl)
  - Because we did not consider the extinction

## **VI.Work log**
- 07/19
	- Find the possible cause about problem 1 : We did not de-redden the whole c2d catalog
- 07/24
	- To realize the knowledge about extinction
- 07/25
	- Learn to use astropy to read the data from ds9
- 07/26
	- Discussion with Inchone Hsieh :
		- How to remove the Av from c2d sources
		- What are 'Image check '(step6) and 'IR1 image check'(step7)
- 08/06
	- check CHA_II catalog after extinction correction :
		- HREL is different from Hsieh's catalog (He may use Full table)
		- One candidate is missing in HREL table (Check Hsieh's table, that one is not in HREL table)
- 08/07
	- Check data_type from Inchone's Chamaleon_RemoveStar_catalog (can_iden.tbl)
	- Remove star form every cloud catalog
- 08/14
    - Uncertainties Package (python's package to calculate uncertainties)
    - Maybe go wrong with log (since it uses Gaussian to fit, the upper and the lower are symmetric )
    - It can't use numpy or math (Use Uncertianties its own log etc.)
- 08/27
	- To write the each part of program about SOP
- 09/02
	- SOP program for
		- (1)Star_Removal complete
		- (2)Extinction_Correction complete
		- (3)Gal_Prob calulate and sort complete (but still improving)
	- Program of producing image check for saturate sources is still missing.(maybe write a new one)
- 09/04
	- SOP program for Gal_Prob calculate and sort complete and improved
- 09/06
	- SOP program for MP1_Saturate(Step 4) is almost complete but with some questions
		- mosaics of OPH has different file name compared to CHA_II, LUP ...
		- what's difference  between file name with an A and BCD ?
	- SOP program for Image_Check(Step 7) confronts same questions as MP1_saturate does.
- 09/18
	- SOP programs for individual steps are OK.
	- program to run all SOP program is OK with step1~step6 (but Saturate_Check, Image_Check are still trying.)
- 09/19
	- program to run all SOP program is OK with step1~step (including Image_Check)
	- still working on distinguish Saturate source after Gal_Prob check
- 10/07
	- SER's Yso candidates have some problems
		- Hsieh's Yso candidates are not fully included in our solid yso result(before image check)
		- not Hsieh's but ours, not ours but Hsieh both are not zero.
	- plot SER's Yso candidates onto MP1 image, IR1 image
- 10/09
	- SER's problems are found
		- Extinction correction didn't work due to the wrong extinction map.
		- trying to fix
    - Use PNICER to create a new extinction map.
