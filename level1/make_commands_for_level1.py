#!/usr/bin/python
import os
import glob
import re

# Usage: python make_l1_commands.py > level1_task_list.sh

try:
    data_loc = os.environ['DATA_LOC']
except KeyError:
    os.system('source /oak/stanford/groups/russpold/users/zenkavi/DevStudy_ServerScripts/setup/dev_study_env.sh')
    data_loc = os.environ['DATA_LOC']

subdirs = glob.glob("%s/derivatives/fmriprep_1.3.0/fmriprep/sub-*/func/sub-*_task-machinegame_run-*_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"%(data_loc))

for dir in subdirs:

    subnum = int(re.findall('\d+', os.path.basename(dir))[0])
    runnum = int(re.findall('\d+', os.path.basename(dir))[1])

	command = 'feat $DATA_LOC/derivatives/level1_inputs/sub-%s/sub%s_run-%s_l1.fsf'%(subnum, subnum, runnum)
	print(command)

#Example command: feat $DATA_LOC/derivatives/level1_inputs/sub-100003/design_sub-100003_run-01.fsf
