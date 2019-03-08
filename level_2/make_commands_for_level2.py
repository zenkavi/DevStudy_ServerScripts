#!/usr/bin/python
import os
import glob
import re

# Usage: python make_commands_for_level2.py > level2_task_list.sh

try:
    data_loc = os.environ['DATA_LOC']
except KeyError:
    os.system('source /oak/stanford/groups/russpold/users/zenkavi/DevStudy_ServerScripts/setup/dev_study_env.sh')
    data_loc = os.environ['DATA_LOC']

subdirs = glob.glob("%s/derivatives/fmriprep_1.3.0/fmriprep/sub-*/func/sub-*_task-machinegame_run-*_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"%(data_loc))

subdirs=glob.glob("%s/derivatives/level_1/sub-*/"%(data_loc))
subdirs.sort()

for dir in subdirs:
    subnum = re.findall('\d+', os.path.dirname(dir))[5]
    command = 'feat $DATA_LOC/derivatives/level_2/sub-%s/model/sub-%s_l2.fsf'%(subnum, subnum)
    print(command)
#Example command: feat $DATA_LOC/derivatives/level12/sub-100003/model/sub-100003_l2.fsf
