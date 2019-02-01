#!/usr/bin/env python
import os
import glob
import nibabel as nib
try:
    data_loc = os.environ['DATA_LOC']
except KeyError:
    os.system('source /oak/stanford/groups/russpold/users/zenkavi/DevStudy_ServerScripts/setup/dev_study_env.sh')
    data_loc = os.environ['DATA_LOC']

bold_files = glob.glob('%s/sub-*/func/sub-*_task-machinegame_run-*_bold.nii.gz'%(data_loc))

for cur_bold in bold_files:
    cur_img = nib.load(cur_bold)
    print('Loaded %s'%(cur_bold))
    if cur_img.header['pixdim'][4] != 2:
        print('Fixing TR for %s'%(cur_bold))
        cur_img.header['pixdim'][4] = 2
    try:
        nib.save(cur_img, cur_bold)
    except:
        print('Failed saving TR for %s'%(cur_bold))
