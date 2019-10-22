# SWIRE-format catalog dictionary
## Introduction
This file is for storing all information about index in SWIRE-format catalog.
## Index list
*note: all index start from 0*
- ### All about Source:
	- #### RA DEC:
		- 0, 2
	- #### RA DEC error:
		- 1, 3
	- #### Evan's Galaxy Probability:
		- 11
	- #### Evan's object type:
		- 16
- ### All about Flux:
	- #### flux value:
		- J, H, K, IR1, IR2, IR3, IR4, MP1, MP2
		- 33, 54, 75, 96, 117, 138, 159, 180, 201
 	- #### flux error:
		- J, H, K, IR1, IR2, IR3, IR4, MP1, MP2
		- 34, 55, 76, 97, 118, 139, 160, 181, 202
	- #### flux quality:
		- J, H, K, IR1, IR2, IR3, IR4, MP1, MP2
		- 37, 58, 79, 100, 121, 142, 163, 184, 205
	- #### flux imagetype (only for IRAC, MIPS):
		- IR1, IR2, IR3, IR4, MP1, MP2
		- 102, 123, 144, 165, 186, 207
	- #### zero-point flux value (flux for magnitude=0)
		- J, H, K, IR1, IR2, IR3, IR4, MP1
		- 1594000, 1024000, 666700, 280900, 179700, 115000, 64130, 7140
		- Note:
			- (1) These are actual values, not index on catalog
			- (2) Unit: mili-Jansky
- ### All about Magnitude:
	- #### magnitude value (IRAC, MIPS):
		- IR1, IR2, IR3, IR4, MP1
		- 98, 119, 140, 161, 182
	- #### magnitude error (IRAC, MIPS):
		- IR1, IR2, IR3, IR4, MP1
		- 99, 120, 141, 162, 183
	- #### magnitude value (UKIDSS J, H, K):
		- J, H, K
		- 35, 56, 77
	- #### magnitude error (UKIDSS J, H, K):
		- J, H, K
		- 36, 57, 78  
- ### All about Galaxy Probability (GP)
	- #### galaxy probability object type:
		- 5D GP1, 5D GP2, 6D GP
		- 233, 235, 241
	- #### galaxy probability value:
		- 5D GP1, 5D GP2, 6D GP
		- 234, 236, 242
- ### All about Galaxy Probability P (GPP)
	- #### galaxy probability object type:
		- 5D GP1, 5D GP2, 6D GP
		- 237, 239, 243
	- #### galaxy probability value:
		- 5D GP1, 5D GP2, 6D GP
		- 238, 240, 244

## Program to convert catalogs in different format
- #### Transform from c2d format to SWIRE format
	- /home/ken/C2D-SWIRE_20180710/SOP_Tool_20181117/to_c2d_format.py
- #### (1)Transform SWIRE flux into magnitude (2)Write UKIDSS JHK magnitude to SWIRE format catalog
	- /home/ken/C2D-SWIRE_20180710/SOP_Tool_20181117/JHK_UKIDSS_SWIRE_mag.py
