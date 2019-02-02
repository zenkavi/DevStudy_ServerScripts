#!/usr/bin/env python
import glob
import nibabel as nib
import os
from shutil import copyfile
try:
    data_loc = os.environ['DATA_LOC']
except KeyError:
    os.system('source /oak/stanford/groups/russpold/users/zenkavi/DevStudy_ServerScripts/setup/dev_study_env.sh')
    data_loc = os.environ['DATA_LOC']

bold_file_paths = glob.glob('%s/sub-*/func/sub-*_task-machinegame_run-*_bold.nii.gz'%(data_loc))
bold_file_paths.sort()

bold_file_names = [os.path.basename(x) for x in bold_file_paths]

for cur_bold in bold_file_paths:
    cur_img = nib.load(cur_bold)
    print('Loaded %s'%(cur_bold))
    if cur_img.header['pixdim'][4] != 2:
        print('Fixing TR for %s'%(cur_bold))
        cur_img.header['pixdim'][4] = 2
    try:
        nib.save(cur_img, cur_bold)
    except:
        print('Failed saving TR for %s'%(cur_bold))

#Will I have to copy back and forth if I can't figure out permissions??
