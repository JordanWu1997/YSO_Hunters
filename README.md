# **YSO Hunters**
## **I.Introduction**
Distinguishing Galaxies and Young Stellar Objects (YSOs) from a database solely containing magnitudes has been proved to be a difficult task, since the physical composition of both types of objects are similar but with different amount (Harvey et al. 2006). Hsieh & Lai (2013) found that YSOs can stand out from Galaxies in Multi-dimensional Magnitude Space, and thus can be separated straightforwardly. Unfortunately, the computer memory required by the Multi-dimensional Magnitude Space method is too much for a database with 8 photometric bands, so Hsieh & Lai (2013) used two 5-dimensional arrays instead. Here we attempt to reduce the memory requirement by choosing the proper magnitude range (mag1, mag2),so that mag\<mag1 are (almost) certainly to be YSOs and mag\>mag2 are all Galaxies. Thus, the grid point required by the Multi-dimensional Magnitude Space will be greatly reduced. Our results will test whether the two 5-dimensional arrays chosen in Hsieh & Lai (2013) are adequate.

## **II.Goal**
- Repeat the procession of Hsieh & Lai (2013) and get the same result
- Use marginal plane on multi-dimensional space to save RAM
- Make the program construct mroe dimension space at same time

## **III.Improvement**
- ~~Reduce the errors about extinction correction~~
- ~~Use marginal curved surface instead of the marginal plane (position support vector)~~
- Make all processions be automatic (SOP Program)
- Add 1 more band to multi-D galaxy probability
- Add new extinction test (application for selecting reliable YSO candidates)
- **TODO**
	- Try to make all programs more flexiable (catalog column indice independence)

## **IV. How To Use SOP Programs**
#### 0. Catalog on zeus (Optional)
- All used catalog stored under:
    - ``` /home/jordan/YSO_Project/C2D-SWIRE_20180710/All_Converted_Catalog ```
    1.  Purpose: Construct galaxy probabilties and find boundaries
        - SEIP_pred_catalog: SEIP catalog to construct galaxy probabilities and find boundaries
        - UKIDSS_DR10PLUS: c2d catalog for ELAIS N1 region
    2.  Purpose: Try to find out new YSO in molecular cloud regions
        - 2MASS_TO_UKIDSS: For region where no UKIDSS observation, just transform old c2d catalog to UKIDSS system (CHA_II, LUP_I, LUP_III, LUP_IV)
        - UKIDSS_DR11PLUS_WI_2MASS_BR: For J, H, K band, Replace 2MASS observation (which MAG<11.5) with UKIDSS observation and transform 2MASS data to UKIDSS system.
    3.  Purpose: Backup c2d catalogs
        - SPITZER: The c2d catalog from spitzer catalog

#### 1. Add Directories started with SOP to current working environments
- e.g. In .cshrc file:
```
#====================================================================
# Set Storage Path (Directory where you store YSO_Hunter)
set Storage = "/home/jordan/YSO_Project/"

# Setup Working Environments For YSO Hunter Programs
setenv PATH ${PATH}:$Storage/YSO_Hunters/bin
setenv PATH ${PATH}:$Storage/YSO_Hunters/lib
setenv PATH ${PATH}:$Storage/YSO_Hunters/SOP_00_Gal_Prob
setenv PATH ${PATH}:$Storage/YSO_Hunters/SOP_01_Preset
setenv PATH ${PATH}:$Storage/YSO_Hunters/SOP_02_5D_method
setenv PATH ${PATH}:$Storage/YSO_Hunters/SOP_03_6D_method
setenv PATH ${PATH}:$Storage/YSO_Hunters/SOP_04_Av_Check
setenv PATH ${PATH}:$Storage/YSO_Hunters/SOP_05_Image_Check

# Setup Python Module Environments For YSO Hunter Programs
setenv PYTHONPATH ${PYTHONPATH}:$Storage/YSO_Hunters/lib
setenv PYTHONPYCACHEPREFIX $HOME/.cache/cpython
#====================================================================
```
- e.g. In .bashrc file:
```
#====================================================================
# Set Storage Path (Directory where you store YSO_Hunter)
export Storage="/home/jordan/YSO_Project/"

# Setup Working Environments For YSO Hunter Programs
export PATH="$Storage/YSO_Hunters/bin:$PATH"
export PATH="$Storage/YSO_Hunters/lib:$PATH"
export PATH="$Storage/YSO_Hunters/SOP_00_Gal_Prob:$PATH"
export PATH="$Storage/YSO_Hunters/SOP_01_Preset:$PATH"
export PATH="$Storage/YSO_Hunters/SOP_02_5D_method:$PATH"
export PATH="$Storage/YSO_Hunters/SOP_03_6D_method:$PATH"
export PATH="$Storage/YSO_Hunters/SOP_04_Av_Check:$PATH"
export PATH="$Storage/YSO_Hunters/SOP_05_Image_Check:$PATH"

# Setup Python Module Environments For YSO Hunter Programs
export PYTHONPATH="$Storage/YSO_Hunters/lib:$PYTHONPATH"
export PYTHONPYCACHEPREFIX="$HOME/.cache/cpython/"
#====================================================================
```

#### 2. Revise Locations of Some Programs if **No such file** error happens.
	- First, check YSO_HUNTER/SOP_Program_Path/SOP_Program_Path.py if all path exist
	- Then , change some path or file that may be needed to revised
		- e.g. location where multi-D galaxy probability array stored

#### 3. Standard Sequence for Execution:
	1. SOP_Execution_GPM_Construct.py (Still working ...)
	2. SOP_Execution_Preset.py
	3. SOP_Execution_5D_method.py
	4. SOP_Execution_6D_method.py
	5. SOP_Execution_Extinction_check.py
		- **Note This Command Must Execute Under Specific Binsize Directory**
