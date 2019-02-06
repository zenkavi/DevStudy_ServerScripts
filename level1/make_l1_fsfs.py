#!/usr/bin/python

import os
import glob
import re

data_loc = os.envrion['DATA_LOC']

# Set this to the directory where you'll dump all the fsf files
# May want to make it a separate directory, because you can delete them all o
#   once Feat runs
fsfdir="%s/derivatives/level1_inputs/"%(data_loc)

# Get all the paths!  Note, this won't do anything special to omit bad subjects
subdirs=glob.glob("%s/derivatives/fmriprep_1.2.5/fmriprep/sub-*/func/sub-*_task-machinegame_run-*_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"%(data_loc))

for dir in list(subdirs):
  subnum = int(re.findall('\d+', os.path.basename(dir))[0])
  runnum = int(re.findall('\d+', os.path.basename(dir))[1])

  ntime = os.popen('fslnvols %s/bold.nii.gz'%(dir)).read().rstrip()
  replacements = {'SUBNUM':subnum, 'NTPTS':ntime, 'RUNNUM':runnum}
  with open("%s/template_l1.fsf"%(fsfdir)) as infile:
    with open("%s/lev1/design_sub%s_run%s.fsf"%(fsfdir, subnum, runnum), 'w') as outfile:
        for line in infile:
          for src, target in replacements.items():
            line = line.replace(src, target)
          outfile.write(line)
