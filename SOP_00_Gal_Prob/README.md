# Execute Program Sequence
## All Program Must Run Under *Demo* Directory

Part 1 - Count and project input galaxy catalog
- (1) Count_Gal_Pos_Vec_numba.py
- (2) Sort_Source_Lack999.py
- (3) Sort_Source_Lack999_Project.py
- (4) Sort_Source_Lack999_Cascade.py
- (5) Sort_Source_Lack999_Band.py

Part2 - Do gaussian smooth
- (1) Do_Gaussian_Smooth_Construct_Bin.py
- (2) Do_Gaussian_Smooth_Execution_All.py
	- Do_Gaussian_Smooth_Slice.py
	- Do_Gaussian_Smooth_Slice_Index.py
	- Do_Gaussian_Smooth_Slice_Cascade.py

# Output File Structure
```
GPV_6Dposvec_bin0.2/
├── Band_pos_num
├── Bright.npy
├── Faint.npy
├── Gal_Position_numbers.npy
├── Gal_Position_vectors.npy
├── Lack_pos_num
└── Shape.npy

GPV_after_smooth_6D_bin0.2_sigma2_bond1_refD5/
├── After_012345
├── After_345
├── After_Smooth_012
├── After_Smooth_0123
├── After_Smooth_01234
├── After_Smooth_012345
├── After_Smooth_01235
├── After_Smooth_0124
├── After_Smooth_01245
├── After_Smooth_0125
├── After_Smooth_013
├── After_Smooth_0134
├── After_Smooth_01345
├── After_Smooth_0135
├── After_Smooth_014
├── After_Smooth_0145
├── After_Smooth_015
├── After_Smooth_023
├── After_Smooth_0234
├── After_Smooth_02345
├── After_Smooth_0235
├── After_Smooth_024
├── After_Smooth_0245
├── After_Smooth_025
├── After_Smooth_034
├── After_Smooth_0345
├── After_Smooth_035
├── After_Smooth_045
├── After_Smooth_123
├── After_Smooth_1234
├── After_Smooth_12345
├── After_Smooth_1235
├── After_Smooth_124
├── After_Smooth_1245
├── After_Smooth_125
├── After_Smooth_134
├── After_Smooth_1345
├── After_Smooth_135
├── After_Smooth_145
├── After_Smooth_234
├── After_Smooth_2345
├── After_Smooth_235
├── After_Smooth_245
├── After_Smooth_345
├── after_smooth_lack_0_012345_all_cas_num.npy
├── after_smooth_lack_0_012345_all_cas_pos.npy
├── after_smooth_lack_1_01234_all_cas_num.npy
├── after_smooth_lack_1_01234_all_cas_pos.npy
├── after_smooth_lack_1_01235_all_cas_num.npy
├── after_smooth_lack_1_01235_all_cas_pos.npy
├── after_smooth_lack_1_01245_all_cas_num.npy
├── after_smooth_lack_1_01245_all_cas_pos.npy
├── after_smooth_lack_1_01345_all_cas_num.npy
├── after_smooth_lack_1_01345_all_cas_pos.npy
├── after_smooth_lack_1_02345_all_cas_num.npy
├── after_smooth_lack_1_02345_all_cas_pos.npy
├── after_smooth_lack_1_12345_all_cas_num.npy
├── after_smooth_lack_1_12345_all_cas_pos.npy
├── after_smooth_lack_2_0123_all_cas_num.npy
├── after_smooth_lack_2_0123_all_cas_pos.npy
├── after_smooth_lack_2_0124_all_cas_num.npy
├── after_smooth_lack_2_0124_all_cas_pos.npy
├── after_smooth_lack_2_0125_all_cas_num.npy
├── after_smooth_lack_2_0125_all_cas_pos.npy
├── after_smooth_lack_2_0134_all_cas_num.npy
├── after_smooth_lack_2_0134_all_cas_pos.npy
├── after_smooth_lack_2_0135_all_cas_num.npy
├── after_smooth_lack_2_0135_all_cas_pos.npy
├── after_smooth_lack_2_0145_all_cas_num.npy
├── after_smooth_lack_2_0145_all_cas_pos.npy
├── after_smooth_lack_2_0234_all_cas_num.npy
├── after_smooth_lack_2_0234_all_cas_pos.npy
├── after_smooth_lack_2_0235_all_cas_num.npy
├── after_smooth_lack_2_0235_all_cas_pos.npy
├── after_smooth_lack_2_0245_all_cas_num.npy
├── after_smooth_lack_2_0245_all_cas_pos.npy
├── after_smooth_lack_2_0345_all_cas_num.npy
├── after_smooth_lack_2_0345_all_cas_pos.npy
├── after_smooth_lack_2_1234_all_cas_num.npy
├── after_smooth_lack_2_1234_all_cas_pos.npy
├── after_smooth_lack_2_1235_all_cas_num.npy
├── after_smooth_lack_2_1235_all_cas_pos.npy
├── after_smooth_lack_2_1245_all_cas_num.npy
├── after_smooth_lack_2_1245_all_cas_pos.npy
├── after_smooth_lack_2_1345_all_cas_num.npy
├── after_smooth_lack_2_1345_all_cas_pos.npy
├── after_smooth_lack_2_2345_all_cas_num.npy
├── after_smooth_lack_2_2345_all_cas_pos.npy
├── after_smooth_lack_3_012_all_cas_num.npy
├── after_smooth_lack_3_012_all_cas_pos.npy
├── after_smooth_lack_3_013_all_cas_num.npy
├── after_smooth_lack_3_013_all_cas_pos.npy
├── after_smooth_lack_3_014_all_cas_num.npy
├── after_smooth_lack_3_014_all_cas_pos.npy
├── after_smooth_lack_3_015_all_cas_num.npy
├── after_smooth_lack_3_015_all_cas_pos.npy
├── after_smooth_lack_3_023_all_cas_num.npy
├── after_smooth_lack_3_023_all_cas_pos.npy
├── after_smooth_lack_3_024_all_cas_num.npy
├── after_smooth_lack_3_024_all_cas_pos.npy
├── after_smooth_lack_3_025_all_cas_num.npy
├── after_smooth_lack_3_025_all_cas_pos.npy
├── after_smooth_lack_3_034_all_cas_num.npy
├── after_smooth_lack_3_034_all_cas_pos.npy
├── after_smooth_lack_3_035_all_cas_num.npy
├── after_smooth_lack_3_035_all_cas_pos.npy
├── after_smooth_lack_3_045_all_cas_num.npy
├── after_smooth_lack_3_045_all_cas_pos.npy
├── after_smooth_lack_3_123_all_cas_num.npy
├── after_smooth_lack_3_123_all_cas_pos.npy
├── after_smooth_lack_3_124_all_cas_num.npy
├── after_smooth_lack_3_124_all_cas_pos.npy
├── after_smooth_lack_3_125_all_cas_num.npy
├── after_smooth_lack_3_125_all_cas_pos.npy
├── after_smooth_lack_3_134_all_cas_num.npy
├── after_smooth_lack_3_134_all_cas_pos.npy
├── after_smooth_lack_3_135_all_cas_num.npy
├── after_smooth_lack_3_135_all_cas_pos.npy
├── after_smooth_lack_3_145_all_cas_num.npy
├── after_smooth_lack_3_145_all_cas_pos.npy
├── after_smooth_lack_3_234_all_cas_num.npy
├── after_smooth_lack_3_234_all_cas_pos.npy
├── after_smooth_lack_3_235_all_cas_num.npy
├── after_smooth_lack_3_235_all_cas_pos.npy
├── after_smooth_lack_3_245_all_cas_num.npy
├── after_smooth_lack_3_245_all_cas_pos.npy
├── after_smooth_lack_3_345_all_cas_num.npy
├── after_smooth_lack_3_345_all_cas_pos.npy
├── Lack_0_012345_all_cas_num.npy
├── Lack_0_012345_all_cas_pos.npy
├── Lack_3_345_all_cas_num.npy
└── Lack_3_345_all_cas_pos.npy
```
