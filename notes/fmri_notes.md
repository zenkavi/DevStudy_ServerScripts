Notes on `FSL for task fMRI` series from mumfordbrainstats
==========================================================

- **[DONE]** Convert DICOM to NIfTI

- QA
  - Check if all files exist (Notes from BIDS report)
    - Missing behavioral data for all runs of sub-100060 **[MOVED TO SOURCEDATA]**
    - Missing behavioral data for all runs of sub-200027 **[MOVED TO SOURCEDATA]**
    - Missing behavioral data for all runs of sub-200081 **[MOVED TO SOURCEDATA]**
    - Missing behavioral data for all runs of sub-304228 **[MOVED TO SOURCEDATA]**
    - Missing behavioral data for all runs of sub-308023 **[MOVED TO SOURCEDATA]**
    - Missing behavioral data for all runs of sub-406989 **[MOVED TO SOURCEDATA]**
    - Missing behavioral data for all runs of sub-411236 **[MOVED TO SOURCEDATA]**
    - Missing behavioral data for run 6 for sub-100110
  - Check BOLD volumes
    - Images with volumes !=216:
    /oak/stanford/groups/russpold/data/ds000054/0.0.1/sub-100241/func/sub-100241_task-machinegame_run-04_bold.nii.gz,11
    /oak/stanford/groups/russpold/data/ds000054/0.0.1/sub-100103/func/sub-100103_task-machinegame_run-03_bold.nii.gz,42
    /oak/stanford/groups/russpold/data/ds000054/0.0.1/sub-406989/func/sub-406989_task-machinegame_run-01_bold.nii.gz,131
    /oak/stanford/groups/russpold/data/ds000054/0.0.1/sub-100215/func/sub-100215_task-machinegame_run-01_bold.nii.gz,141
    /oak/stanford/groups/russpold/data/ds000054/0.0.1/sub-306065/func/sub-306065_task-machinegame_run-01_bold.nii.gz,148
    /oak/stanford/groups/russpold/data/ds000054/0.0.1/sub-100188/func/sub-100188_task-machinegame_run-04_bold.nii.gz,153
    /oak/stanford/groups/russpold/data/ds000054/0.0.1/sub-100110/func/sub-100110_task-machinegame_run-06_bold.nii.gz,161

- Skull script structural images
- QA
- Functionals preprocessing
  - Trim volumes from beginning
  - Fix orientation issues
  - Assess motion
- QA
- Level 1 analyses
- QA
- Level 2 analyses
- QA
- Group level analyses
- QA
