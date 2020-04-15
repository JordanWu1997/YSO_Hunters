# Sequence of executing programs
### Part 0 - Terminology

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
	- Make_Galaxy_Prob_Plot_Execution_All.py
	- Make_Galaxy_Prob_3D_Plot.py
	- Make_Galaxy_Prob_PCA_Cut_Plot.py
	- Make_Galaxy_Prob_3D_Plot_With_PCA.py
	
# Output File Structure
## In "Working Directory" (where all above programs should be excecuted)
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
	│     ├── L0_012345_PCA_E0.png                      #
	│     ├── L0_012345_WPCA_E0.png                     #
	│     ├── ...... (Different principle components)   
	│     ├── PCA_components_012345.npy                 #
	│     ├── PCA_premean_012345.npy                    #
	│     ├── PCA_variances_012345.npy                  #
	│     ├── PCA_var_ratios_012345.npy                 #
	│     ├── WPCA_components_012345.npy                #
	│     ├── WPCA_premean_012345.npy                   #
	│     ├── WPCA_variances_012345.npy                 #
	│     └── WPCA_var_ratios_012345.npy                #
	├── tomo_012/                                       #
	│     ├── 012_all_0_n5_i10.gif                      #
	│     ├── 012_all_0_n5_i10_WI_PCA_012345.gif        #
	│     ├── 012_all_0_n5_i10_WI_WPCA_012345.gif       #
	│     ├── 012axis_0.gif                             #
	│     ├── all_012_n5_i10/                           #
	│     ├── all_012_n5_i10_WI_PCA_012345/             #
	│     └─ all_012_n5_i10_WI_WPCA_012345/             #
	└── ...... (Different band combinations)
