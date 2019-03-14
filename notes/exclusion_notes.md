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
sub-200025 run 6
sub-408511 run 6
sub-100103 run 3
sub-100188 run 4
sub-100241 run 4
sub-306065 run 1
sub-408988 run 5
sub-100051 run 1

Excluded runs for scrub volumes:
