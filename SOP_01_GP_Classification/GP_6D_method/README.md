# Sequence of executing programs
- For now, 6D means J, IR1, IR2, IR3, IR4, MP1 6 bands
- There are two methods to calculate galaxy probability
    - (1) Use upper/lower bound to classify input object and assign GP
    - (2) Use pos/num in galaxy probability dictionary to calculate input object's GP
### Part 0 - TODO before running programs below
- *galaxy bound array* or *galaxy probability dictionary* must be created before executing programs below
### Part 1 - Calculate 6D Galaxy Probability
- Option 1 (Recommended):
    - Calculate_GP_WI_6D_Bound_Array.py
        - Use Upper/Lower Bound stored in "array"
- Option 2 (Not Recommended):
    - Calculate_GP_WI_6D_Dict_Key_Str.py (Not used now)
        - Use Galaxy Probability Dictionary with Key stored in "string"
    - Calculate_GP_WI_6D_Dict_Key_Tuple.py
        - Use Galaxy Probability Dictionary with Key stored in "tuple"
### Part 2 - Classify YSO/Galaxy/Image_Check with calculated galaxy probabitliy
- (1) Classify_WI_6D_Galaxy_Prob.py

### TODO:
- (1) Finish the files path in above programs

### Galaxy Probability Assignment Policy For Boundary Method
- Galaxy position vector: -999 component-> lack of detection
- Galaxy Probability (type: value)
    - "not_count" : LESS3BD
    - "not_count" : AGB
    - 1e-5        : MP1_Sat
    - 1e-4        : Bright
    - 1e-3        : YSO
    - 1e4         : Faint
    - 1e3         : Galaxy
