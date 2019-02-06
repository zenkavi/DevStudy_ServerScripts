#!/usr/bin/python
import os
import glob
import re

try:
    data_loc = os.environ['DATA_LOC']
except KeyError:
    os.system('source /oak/stanford/groups/russpold/users/zenkavi/DevStudy_ServerScripts/setup/dev_study_env.sh')
    data_loc = os.environ['DATA_LOC']

fsfdir="%s/derivatives/level1_inputs/"%(data_loc)

#DOUBLE CHECK WHAT THIS WAS IN THE ORIGINAL SCRIPT
subdirs=glob.glob("%s/derivatives/fmriprep_1.2.5/fmriprep/sub-*/func/sub-*_task-machinegame_run-*_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"%(data_loc))

for dir in list(subdirs):
  subnum = int(re.findall('\d+', os.path.basename(dir))[0])
  runnum = int(re.findall('\d+', os.path.basename(dir))[1])

  ntime = os.popen('fslnvols %s'%(dir)).read().rstrip()

  replacements = {'SUBNUM':subnum, 'NTPTS':ntime, 'RUNNUM':runnum}

  with open("%s/template_l1.fsf"%(fsfdir)) as infile:
    with open("%s/sub-%s/l1_design_sub-%s_run-%s.fsf"%(fsfdir, subnum, subnum, runnum), 'w') as outfile:
        for line in infile:
          for src, target in replacements.items():
            line = line.replace(src, target)
          outfile.write(line)
