# **YSO Hunters**
## **I.Introduction**
Distinguishing Galaxies and Young Stellar Objects (YSOs) from a database solely containing magnitudes has been proved to be a difficult task, since the physical composition of both types of objects are similar but with different amount (Harvey et al. 2006). Hsieh & Lai (2013) found that YSOs can stand out from Galaxies in Multi-dimensional Magnitude Space, and thus can be separated straightforwardly. Unfortunately, the computer memory required by the Multi-dimensional Magnitude Space method is too much for a database with 8 photometric bands, so Hsieh & Lai (2013) used two 5-dimensional arrays instead. Here we attempt to reduce the memory requirement by choosing the proper magnitude range (mag1, mag2),so that mag\<mag1 are (almost) certainly to be YSOs and mag\>mag2 are all Galaxies. Thus, the grid point required by the Multi-dimensional Magnitude Space will be greatly reduced. Our results will test whether the two 5-dimensional arrays chosen in Hsieh & Lai (2013) are adequate.

## **II.Goal**
- Repeat the procession of Hsieh & Lai (2013) and get the same result
- Use marginal plane on multi-dimensional space to save RAM
- Make the program construct mroe dimension space at same time

## **III.Improvement**
- Make all processions be automatic (SOP Program)
- ~~Reduce the errors about extinction correction~~
- ~~Use marginal curved surface instead of the marginal plane (position support vector)~~
- Add 1 more band to multi-D galaxy probability
- Add new extinction test (application for selecting reliable YSO candidates)

## **IV. How To Use SOP Programs**
1. Add Directories started with SOP to current working environments
  - e.g. In .cshrc file:
    ```
	set Storage = **where_you_store_YSO_Hunter**

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
	setenv PYTHONPATH ${PYTHONPATH}:$Storage/YSO_Hunters/SOP_Program_Path
    ```
2. Revise Locations of Some Programs if **No such file** error happens.
  - First, check YSO_HUNTER/SOP_Program_Path/SOP_Program_Path.py if all path exist
  - Then , change some path or file that may be needed to revised
    - e.g. location where multi-D galaxy probability array stored

3. Standard Sequence for Execution:
	1. SOP_Execution_GPM_Construct.py (Still working ...)
    2. SOP_Execution_Preset.py
    3. SOP_Execution_5D_method.py
    4. SOP_Execution_6D_method.py
    5. SOP_Execution_Extinction_check.py
        - **Note This Command Must Execute inside Specific Binsize Directory**
