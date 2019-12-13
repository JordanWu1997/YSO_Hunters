# Execute Program Sequence
0. ## All Program Must Run Under *Demo* Directory
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
Demo/
├── GPV_6Dposvec_bin1.0
│   ├── Bright.npy
│   ├── Faint.npy
│   ├── Gal_Position_vectors.npy
│   ├── Lack_0band_sources.npy
│   ├── Lack_1band_sources.npy
│   ├── Lack_2band_sources.npy
│   ├── Lack_3band_sources.npy
│   └── Shape.npy
├── GPV_after_smooth_6D_bin1.0_sigma2_bond0_refD5
│   ├── 3d_after_smooth.npy
│   ├── 4d_after_smooth.npy
│   ├── 5d_after_smooth.npy
│   ├── 6d_after_smooth.npy
│   ├── tmp_L0
│   │   ├── 000_6d_after_smooth.npy
│   │   ├── 000_tmp_cat.npy
│   │   ├── 001_6d_after_smooth.npy
│   │   ├── 001_tmp_cat.npy
│   │   ├── 002_6d_after_smooth.npy
│   │   ├── 002_tmp_cat.npy
│   │   ├── 003_6d_after_smooth.npy
│   │   ├── 003_tmp_cat.npy
│   │   ├── 004_6d_after_smooth.npy
│   │   ├── 004_tmp_cat.npy
│   │   ├── 005_6d_after_smooth.npy
│   │   ├── 005_tmp_cat.npy
│   │   ├── 006_6d_after_smooth.npy
│   │   ├── 006_tmp_cat.npy
│   │   ├── 007_6d_after_smooth.npy
│   │   ├── 007_tmp_cat.npy
│   │   ├── 008_6d_after_smooth.npy
│   │   ├── 008_tmp_cat.npy
│   │   ├── 009_6d_after_smooth.npy
│   │   └── 009_tmp_cat.npy
│   ├── tmp_L1
│   │   ├── 000_5d_after_smooth.npy
│   │   ├── 000_tmp_cat.npy
│   │   ├── 001_5d_after_smooth.npy
│   │   ├── 001_tmp_cat.npy
│   │   ├── 002_5d_after_smooth.npy
│   │   ├── 002_tmp_cat.npy
│   │   ├── 003_5d_after_smooth.npy
│   │   ├── 003_tmp_cat.npy
│   │   ├── 004_5d_after_smooth.npy
│   │   ├── 004_tmp_cat.npy
│   │   ├── 005_5d_after_smooth.npy
│   │   ├── 005_tmp_cat.npy
│   │   ├── 006_5d_after_smooth.npy
│   │   ├── 006_tmp_cat.npy
│   │   ├── 007_5d_after_smooth.npy
│   │   ├── 007_tmp_cat.npy
│   │   ├── 008_5d_after_smooth.npy
│   │   ├── 008_tmp_cat.npy
│   │   ├── 009_5d_after_smooth.npy
│   │   └── 009_tmp_cat.npy
│   ├── tmp_L2
│   │   ├── 000_4d_after_smooth.npy
│   │   ├── 000_tmp_cat.npy
│   │   ├── 001_4d_after_smooth.npy
│   │   ├── 001_tmp_cat.npy
│   │   ├── 002_4d_after_smooth.npy
│   │   ├── 002_tmp_cat.npy
│   │   ├── 003_4d_after_smooth.npy
│   │   ├── 003_tmp_cat.npy
│   │   ├── 004_4d_after_smooth.npy
│   │   ├── 004_tmp_cat.npy
│   │   ├── 005_4d_after_smooth.npy
│   │   ├── 005_tmp_cat.npy
│   │   ├── 006_4d_after_smooth.npy
│   │   ├── 006_tmp_cat.npy
│   │   ├── 007_4d_after_smooth.npy
│   │   ├── 007_tmp_cat.npy
│   │   ├── 008_4d_after_smooth.npy
│   │   ├── 008_tmp_cat.npy
│   │   ├── 009_4d_after_smooth.npy
│   │   └── 009_tmp_cat.npy
│   └── tmp_L3
│       ├── 000_3d_after_smooth.npy
│       ├── 000_tmp_cat.npy
│       ├── 001_3d_after_smooth.npy
│       ├── 001_tmp_cat.npy
│       ├── 002_3d_after_smooth.npy
│       ├── 002_tmp_cat.npy
│       ├── 003_3d_after_smooth.npy
│       ├── 003_tmp_cat.npy
│       ├── 004_3d_after_smooth.npy
│       ├── 004_tmp_cat.npy
│       ├── 005_3d_after_smooth.npy
│       ├── 005_tmp_cat.npy
│       ├── 006_3d_after_smooth.npy
│       ├── 006_tmp_cat.npy
│       ├── 007_3d_after_smooth.npy
│       ├── 007_tmp_cat.npy
│       ├── 008_3d_after_smooth.npy
│       ├── 008_tmp_cat.npy
│       ├── 009_3d_after_smooth.npy
│       └── 009_tmp_cat.npy
└── GPV_smooth_sigma2_bond0_refD5
    ├── 3d_beam_sigma2.npy
    ├── 4d_beam_sigma2.npy
    ├── 5d_beam_sigma2.npy
    ├── 6d_beam_sigma2.npy
    └── ND_Beam_sigma2_refD5
        └── Beam_in_diff_dim.png

```
