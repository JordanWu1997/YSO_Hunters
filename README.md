# **YSO Hunters**
## **I.Introduction**
Distinguishing Galaxies and Young Stellar Objects (YSOs) from a database solely containing magnitudes has been proved to be a difficult task, since the physical composition of both types of objects are similar but with different amount (Harvey et al. 2006). Hsieh & Lai (2013) found that YSOs can stand out from Galaxies in Multi-dimensional Magnitude Space, and thus can be separated straightforwardly. Unfortunately, the computer memory required by the Multi-dimensional Magnitude Space method is too much for a database with 8 photometric bands, so Hsieh & Lai (2013) used two 5-dimensional arrays instead. Here we provide two new methods to distinguish galaxies and YSOs. The first method is based on Hsieh ^ Lai (2013) but use 6-dimensional array instead. The second method is to find the boundary to separate galaxies and YSOs in 6-dimensional magnitude space. We will test whether the method in Hsieh & Lai (2013) is adequate or new method can provide more confidence in distinguishing galaxies and YSOs.

## **II.Goal**
- [x] Repeat the procession of Hsieh & Lai (2013) and get the same result
- [ ] Use marginal plane on multi-dimensional space to save RAM
- [ ] Make the program construct more dimension space at same time

## **III.Improvement**
- [ ] ~~Reduce the errors about extinction correction~~
- [ ] ~~Use marginal curved surface instead of the marginal plane (position support vector)~~
- [x] Make all processions be automatic (SOP Program)
- [x] Add 1 more band to multi-D galaxy probability
- [ ] Add new extinction test (application for selecting reliable YSO candidates)
- [x] Make all programs more flexiable (catalog column indice independence)

## **IV. How To Use SOP Programs**
#### 0. Catalog on zeus (Optional)
- All used catalog stored under:
    - ``` /mazu/users/jordan/YSO_Project/YSO_Hunters_Table/All_Converted_Catalog ```
    1.  Purpose: Construct galaxy probabilties and find boundaries
        - SEIP_MODEL_II_GALAXY: galaxy catalog (from SEIP catalog classified by SCAO model II) to construct galaxy probabilities and find boundaries
        - UKIDSS_DR10PLUS: c2d catalog for ELAIS N1 region
    2.  Purpose: Try to find out new YSO in molecular cloud regions
        - 2MASS_TO_UKIDSS: For region where no UKIDSS observation, just transform c2d catalog to UKIDSS system (MC: CHA_II, LUP_I, LUP_III, LUP_IV)
        - UKIDSS_DR11PLUS_WI_2MASS_BR: For J, H, K band, Replace 2MASS observation (which MAG<11.5) with UKIDSS observation and transform 2MASS data to UKIDSS system (MC: OPH, PER, SER)
    3.  Purpose: Backup c2d catalogs
        - SPITZER: The c2d catalog from spitzer catalog (ELAIS_N1, CHA_II, LUP_I, LUP_III, LUP_IV, SER, PER, OPH)

#### 1. Add Directories started with SOP to current working environments
- e.g. In .cshrc file:
```
#====================================================================
# Set Storage Path (Directory where you store YSO_Hunter)
set Storage = "/home/jordan/YSO_Project/"

# Setup Working Environments For YSO Hunter Programs
setenv PATH ${PATH}:$Storage/YSO_Hunters/bin
setenv PATH ${PATH}:$Storage/YSO_Hunters/lib
setenv PATH ${PATH}:$Storage/YSO_Hunters/SOP_00_Gal_Prob_Model
setenv PATH ${PATH}:$Storage/YSO_Hunters/SOP_01_GP_Classification/GP_5D_method
setenv PATH ${PATH}:$Storage/YSO_Hunters/SOP_01_GP_Classification/Classification_Preset
setenv PATH ${PATH}:$Storage/YSO_Hunters/SOP_01_GP_Classification/GP_5D_method_from_Hsieh
setenv PATH ${PATH}:$Storage/YSO_Hunters/SOP_01_GP_Classification/GP_6D_method
setenv PATH ${PATH}:$Storage/YSO_Hunters/SOP_01_GP_Classification/GP_nD_method
setenv PATH ${PATH}:$Storage/YSO_Hunters/SOP_02_Further_Check/Candidate_Av_Check
setenv PATH ${PATH}:$Storage/YSO_Hunters/SOP_02_Further_Check/Candidate_Image_Check

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
export PATH=${PATH}:$Storage/YSO_Hunters/bin
export PATH=${PATH}:$Storage/YSO_Hunters/lib
export PATH=${PATH}:$Storage/YSO_Hunters/SOP_00_Gal_Prob_Model
export PATH=${PATH}:$Storage/YSO_Hunters/SOP_01_GP_Classification/Classification_Preset
export PATH=${PATH}:$Storage/YSO_Hunters/SOP_01_GP_Classification/GP_5D_method
export PATH=${PATH}:$Storage/YSO_Hunters/SOP_01_GP_Classification/GP_5D_method_from_Hsieh
export PATH=${PATH}:$Storage/YSO_Hunters/SOP_01_GP_Classification/GP_6D_method
export PATH=${PATH}:$Storage/YSO_Hunters/SOP_01_GP_Classification/GP_nD_method
export PATH=${PATH}:$Storage/YSO_Hunters/SOP_02_Further_Check/Candidate_Av_Check
export PATH=${PATH}:$Storage/YSO_Hunters/SOP_02_Further_Check/Candidate_Image_Check

# Setup Python Module Environments For YSO Hunter Programs
export PYTHONPATH="$Storage/YSO_Hunters/lib:$PYTHONPATH"
export PYTHONPYCACHEPREFIX="$HOME/.cache/cpython/"
#====================================================================
```

#### 2. Execute ```python setup.py [path_to_python]```
- Use ```which python``` to find currently working python
- Setup python working path. If not, the default is **/usr/bin/python**

#### 3. Revise Locations of Some Programs/Files if ```Error: No such file``` occurs.
- First, check YSO_HUNTER/SOP_Program_Path/SOP_Program_Path.py if **all paths/files** exist
- Then , change some path or file that may be needed to revised
	- e.g. location where multi-D galaxy probability dictionary stored
- For all __variables__, please run ```All_Variables.py``` in terminal and check
- For all __paths__, please run ```SOP_Program_Path.py``` in terminal and check

#### 4. Standard Sequence for Execution:
- **Note: This Command Must Execute Under Specific Binsize Directory**
- **Note: If you have any problem please check README.md in specific directories**
    -  Pipeline_Galaxy_Prob.csh (SOP_00_Gal_Prob)
    -  SOP_Execution_Preset.py (SOP_01_Preset)
    -  SOP_Execution_5D_method.py (SOP_02_5D_method)
    -  Pipeline_Classification.csh (bin)
    -  ~SOP_Execution_Extinction_check.py~ (NOT COMPLETED YET ...)
