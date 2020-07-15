# Sequence of executing programs
### Part 0 - _Catalogs_
- (1) SEIP catalog (Used now)
    - ``` /mazu/users/jordan/YSO_Project/YSO_Hunters_Table/All_Converted_Catalog/SEIP_MODEL_II_GALAXY/SEIP_sed_exXUS_Galaxy.txt ```
    - Band: J, H, K, IR1, IR2, IR3, IR4, MP1 (unit: mJy)
    - Note: J, H, K have already transform from 2mass system to ukidss system
- (2) UKIDSS + c2d catalog (Not used now)
    - ``` /mazu/users/jordan/YSO_Project/YSO_Hunters_Table/All_Converted_Catalog/UKIDSS_DR10PLUS/ADD_UKIDSS/catalog-SWIRE_UKIDSS_ELAIS_N1_WI_2MASS_BR.tbl ```
    - Band: J, H, K, IR1, IR2, IR3, IR4, MP1 (unit: mJy)
    - Note:
        - For J, H, K bands, UKIDSS data is used to replace 2MASS data (which mag<11.5).
        - For J, H, K bands, 2MASS data also have been transformed to UKIDSS system.

### Part 1 - Count and project input galaxy catalog
- (1) Count_Gal_Pos_Vec_numba.py
- (2) Sort_Source_Lack999_Execution_All.py
	- Sort_Source_Lack999.py
	- Sort_Source_Lack999_Project.py
	- Sort_Source_Lack999_Cascade.py
	- Sort_Source_Lack999_Band.py

### Part2 - Do gaussian smooth
- (1) Do_Gaussian_Smooth_Construct_Bin.py
- (2) Do_Gaussian_Smooth_Execution_All.py
	- Do_Gaussian_Smooth_Slice.py
	- Do_Gaussian_Smooth_Slice_Index.py
	- Do_Gaussian_Smooth_Slice_Cascade.py

### Part3 - Visualize galaxy probability
- (1) Make_Galaxy_Prob_Plot_Execution_All.py
	- Make_Galaxy_Prob_3D_Plot.py
	- Make_Galaxy_Prob_PCA_Cut_Plot.py
	- Make_Galaxy_Prob_3D_Plot_With_PCA.py

### Part4 - Galaxy Probability
- Pick Method (1) or (2)
    - (1) Find GP Boundary (Along with Axis or PCA, Axis is recommended)
        - Find_Galaxy_Prob_6D_Boundary_Along_Band_Parallel.py
        - Find_Galaxy_Prob_6D_Boundary_Along_PCA_Parallel.py
    - (2) Construct GP Dictionary
        - Update_GP_Dict_Key_Tuple.py

### Part5 - Pipeline from Part1 to Part4
- Pipeline_Galaxy_Prob.csh
    - (1) Count_Gal_Pos_Vec_numba.py
    - (2) Sort_Source_Lack999_Execution_All.py
    - (3) Do_Gaussian_Smooth_Construct_Bin.py
    - (4) Do_Gaussian_Smooth_Execution_All.py
    - (5*) Update_GP_Dict_Key_Tuple.py (Only for GP Dictionary)

### APPENDIX -  Output File Structure
#### In "Working Directory" (where all above programs should be excecuted and input catalogs should be stored)
```
├── GPV_6Dposvec_bin0.2/                                    #
	├── Band_pos_num/                                   #
	├── Lack_pos_num/                                   #
	├── Bright.npy                                      #
	├── Faint.npy                                       #
	├── Gal_Position_numbers.npy                        #
	├── Gal_Position_vectors.npy                        #
	└── Shape.npy                                       #
├── GPV_smooth_sigma2_bond2_refD5/                          #
	├── 3d_beam_sigma2.npy                              #
	├── 4d_beam_sigma2.npy                              #
	├── 5d_beam_sigma2.npy                              #
	├── 6d_beam_sigma2.npy                              #
	└── ND_Beam_sigma2_refD5/                           #
    		└── Beam_in_diff_dim.png                    #
├── GPV_after_smooth_6D_bin0.2_sigma2_bond1_refD5/          #
	├── After_012345/                                   #
	├── After_Smooth_012345/                            #
	├── after_smooth_lack_0_012345_all_cas_num.npy      #
	├── after_smooth_lack_0_012345_all_cas_pos.npy      #
	└── ...... (Different band combinations)
├── GPV_after_smooth_6D_bin0.2_sigma2_bond1_refD5/          #
	├── pca_cut/                                        #
		├── L0_012345_PCA_E0.png                    #
		├── L0_012345_WPCA_E0.png                   #
	     	├── ...... (Different principle components)
		├── PCA_components_012345.npy               #
	     	├── PCA_premean_012345.npy                  #
	     	├── PCA_variances_012345.npy                #
	     	├── PCA_var_ratios_012345.npy               #
	     	├── WPCA_components_012345.npy              #
	     	├── WPCA_premean_012345.npy                 #
	     	├── WPCA_variances_012345.npy               #
	     	└── WPCA_var_ratios_012345.npy              #
	├── tomo_012/                                       #
	     	├── 012_all_0_n5_i10.gif                    #
	     	├── 012_all_0_n5_i10_WI_PCA_012345.gif      #
	     	├── 012_all_0_n5_i10_WI_WPCA_012345.gif     #
	     	├── 012axis_0.gif                           #
	     	├── all_012_n5_i10/                         #
	     	├── all_012_n5_i10_WI_PCA_012345/           #
	     	└─ all_012_n5_i10_WI_WPCA_012345/           #
	└── ...... (Different band combinations)
