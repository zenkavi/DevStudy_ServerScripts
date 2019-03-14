Notes on exclusions for ds000054
==========================================================

- Missing files
  Missing behavioral data for all runs of sub-100060 **[MOVED TO SOURCEDATA]**  
  Missing behavioral data for all runs of sub-200027 **[MOVED TO SOURCEDATA]**  
  Missing behavioral data for all runs of sub-200081 **[MOVED TO SOURCEDATA]**  
  Missing behavioral data for all runs of sub-304228 **[MOVED TO SOURCEDATA]**  
  Missing behavioral data for all runs of sub-308023 **[MOVED TO SOURCEDATA]**  
  Missing behavioral data for all runs of sub-406989 **[MOVED TO SOURCEDATA]**  
  Missing behavioral data for all runs of sub-411236 **[MOVED TO SOURCEDATA]**  
  Missing behavioral data for run 6 for sub-100110 **[MOVED TO SOURCEDATA]**
  Missing images for runs 3-6 of sub-100109 **[MOVED TO SOURCEDATA]**
  Missing images for runs 2-6 of sub-100215 **[MOVED TO SOURCEDATA]**
  Missing images for runs 4-6 of sub-100169
  Missing images for runs 6 of sub-200025 **[first volume corrupt]**
  Missing images for runs 6 of sub-408511 **[last volume corrupt]**

- BOLD volumes with volumes !=216:  
  sub-100103/func/sub-100103_task-machinegame_run-03_bold.nii.gz,42 **[MOVED TO SOURCEDATA]**
  sub-100110/func/sub-100110_task-machinegame_run-06_bold.nii.gz,161 **[MOVED TO SOURCEDATA]**
  sub-100188/func/sub-100188_task-machinegame_run-04_bold.nii.gz,153 **[MOVED TO SOURCEDATA]**
  sub-100241/func/sub-100241_task-machinegame_run-04_bold.nii.gz,11 **[MOVED TO SOURCEDATA]**
  *sub-306065/func/sub-306065_task-machinegame_run-01_bold.nii.gz,148* *[noted in Subject_fMRI_analysis_tracking]*   
  sub-406989/func/sub-406989_task-machinegame_run-01_bold.nii.gz,131 **[MOVED TO SOURCEDATA]**  

- Fmap volumes != 96,96,56 (voxels):
  sub-406989/fmap/sub-406989_magnitude1.nii.gz, This file has the dimensions: 92,96,56 (voxels). **[MOVED TO SOURCEDATA]**  
  sub-406989/fmap/sub-406989_magnitude2.nii.gz, This file has the dimensions: 92,96,56 (voxels). **[MOVED TO SOURCEDATA]**  
  sub-406989/fmap/sub-406989_phasediff.nii.gz, This file has the dimensions: 92,96,56 (voxels). **[MOVED TO SOURCEDATA]**

- Anatomical != 0.80mm x 0.80mm x 0.80mm  
  sub-406989/anat/sub-406989_T1w.nii.gz, This file has the resolution: 0.80mm x 0.85mm x 0.85mm. **[MOVED TO SOURCEDATA]**

- Behavioral variability
  /sub-408988/sub-408988_task-machinegame_run-005_cond1.txt - no behavioral variability, subject asleep? **[currently excluded]**

- No confounds file for sub-100051 run 1 **[currently excluded]**

Excluded subjects:
sub-100060
sub-200027
sub-200081
sub-304228
sub-308023
sub-406989
sub-411236
sub-100109
sub-100215

Excluded runs for missing data:
sub-100110 run 6
sub-100169 run 4,5,6
sub-100103 run 3
sub-100188 run 4
sub-100241 run 4
sub-100051 run 1
sub-200025 run 6
sub-408511 run 6
sub-306065 run 1
sub-408988 run 5

Excluded runs for scrub volumes:
   sub_id run pct_scrubbed
1  100003   5     32.40741
2  100003   4     26.38889
3  100003   6     26.38889
4  100003   3     23.14815
5  100051   6     54.16667
6  100051   5     44.44444
7  100051   4     33.33333
8  100051   2     30.55556
9  100059   6     22.22222
10 100062   3     32.87037
11 100062   2     29.62963
12 100062   1     21.75926
13 100063   6     37.96296
14 100063   5     31.48148
15 100063   4     27.31481
16 100063   2     20.37037
17 100103   4     48.14815
18 100103   5     39.81481
19 100103   2     35.18519
20 100103   6     20.37037
21 100104   6     42.59259
22 100104   3     26.38889
23 100104   5     26.38889
24 100105   2     46.29630
25 100105   6     39.35185
26 100105   3     38.42593
27 100105   4     30.09259
28 100105   5     26.38889
29 100110   6     29.81366
30 100241   3     37.96296
31 100241   6     33.79630
32 100241   5     32.87037
33 100243   6     30.09259
34 100243   5     22.22222
35 100243   1     21.75926
36 100244   5     22.68519
37 200088   5     36.11111
38 200088   3     29.16667
39 200088   6     26.38889
40 200088   4     21.75926
41 200168   6     30.09259
42 200168   5     29.62963
43 411477   5     43.05556
44 411477   3     22.22222
