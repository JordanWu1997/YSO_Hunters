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
	- Sort_Source_Lack999_Slice.py
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
```
