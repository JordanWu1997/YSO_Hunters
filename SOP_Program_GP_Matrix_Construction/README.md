# Execute Program Sequence
1. ## Construct_Gaussian_Bin.py
	- [program] [sigma] [bond] [ref-D]
2. ## Count_Gal_Pos_Vec.py
	- [program] [input catalog] [mag/flux] [dimension] [cube size]
3. ## Sort_and_Project_Lack_Source.py
	- [program] [dim] [cube size]
4. ## Multi_Thead_Gaussian_Smooth.py
	- [program] [dim] [cube size] [sigma] [bond] [ref-D] [num_TH] [lack_inp]
	- This has already combined:
		1. ### Slice_Sort_Lack_Source.py
			- [program] [dim] [cube size] [sigma] [bond] [ref-D] [num_TH] [lack_inp]
		2. ### Do_Gaussian_Smooth_Index.py
			- [program] [dim] [cube size] [sigma] [bond] [ref-D] [lack] [index]
5. ## Cascade_Multi_Thread_Gaussian_Smooth.py
	- [program] [dim] [cube size] [sigma] [bond] [ref-D] [lack_inp]

# Output File Structure
```bash
GPV_after_smooth_6D_bin1.0_sigma2_bond0_refD5/
\u251c\u2500\u2500 3d_after_smooth.npy
\u251c\u2500\u2500 4d_after_smooth.npy
\u251c\u2500\u2500 5d_after_smooth.npy
\u251c\u2500\u2500 6d_after_smooth.npy
\u251c\u2500\u2500 tmp_L0
\u2502\u00a0\u00a0 \u251c\u2500\u2500 000_6d_after_smooth.npy
\u2502\u00a0\u00a0 \u251c\u2500\u2500 000_tmp_cat.npy
\u2502\u00a0\u00a0 \u251c\u2500\u2500 001_6d_after_smooth.npy
\u2502\u00a0\u00a0 \u251c\u2500\u2500 001_tmp_cat.npy
\u2502\u00a0\u00a0 \u251c\u2500\u2500 002_6d_after_smooth.npy
\u2502\u00a0\u00a0 \u251c\u2500\u2500 002_tmp_cat.npy
\u2502\u00a0\u00a0 \u251c\u2500\u2500 003_6d_after_smooth.npy
\u2502\u00a0\u00a0 \u251c\u2500\u2500 003_tmp_cat.npy
\u2502\u00a0\u00a0 \u251c\u2500\u2500 004_6d_after_smooth.npy
\u2502\u00a0\u00a0 \u251c\u2500\u2500 004_tmp_cat.npy
\u2502\u00a0\u00a0 \u251c\u2500\u2500 005_6d_after_smooth.npy
\u2502\u00a0\u00a0 \u251c\u2500\u2500 005_tmp_cat.npy
\u2502\u00a0\u00a0 \u251c\u2500\u2500 006_6d_after_smooth.npy
\u2502\u00a0\u00a0 \u251c\u2500\u2500 006_tmp_cat.npy
\u2502\u00a0\u00a0 \u251c\u2500\u2500 007_6d_after_smooth.npy
\u2502\u00a0\u00a0 \u251c\u2500\u2500 007_tmp_cat.npy
\u2502\u00a0\u00a0 \u251c\u2500\u2500 008_6d_after_smooth.npy
\u2502\u00a0\u00a0 \u251c\u2500\u2500 008_tmp_cat.npy
\u2502\u00a0\u00a0 \u251c\u2500\u2500 009_6d_after_smooth.npy
\u2502\u00a0\u00a0 \u2514\u2500\u2500 009_tmp_cat.npy
```
