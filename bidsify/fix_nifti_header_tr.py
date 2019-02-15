#!/usr/bin/env python
import glob
import nibabel as nib
import os
try:
    data_loc = os.environ['DATA_LOC']
except KeyError:
    os.system('source /oak/stanford/groups/russpold/users/zenkavi/DevStudy_ServerScripts/setup/dev_study_env.sh')
    data_loc = os.environ['DATA_LOC']

# Raw data
raw_bold_files = glob.glob('%s/sub-*/func/sub-*_task-machinegame_run-*_bold.nii.gz'%(data_loc))
# Preprocessed data
bold_files = glob.glob("%s/derivatives/fmriprep_1.3.0/fmriprep/sub-*/func/sub-*_task-machinegame_run-*_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"%(data_loc))
bold_files = raw_bold_files + bold_files
bold_files.sort()

#bold_file_names = [os.path.basename(x) for x in bold_file_paths]

for cur_bold in bold_files:
    cur_img = nib.load(cur_bold)
    print('Loaded %s'%(cur_bold))
    if cur_img.header['pixdim'][4] != 1:
        print('Fixing TR for %s'%(cur_bold))
        cur_img.header['pixdim'][4] = 1
    try:
        nib.save(cur_img, cur_bold)
    except:
        print('Failed saving TR for %s'%(cur_bold))
