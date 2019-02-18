#!/usr/bin/python
import os
import glob
import re

try:
    data_loc = os.environ['DATA_LOC']
except KeyError:
    os.system('source /oak/stanford/groups/russpold/users/zenkavi/DevStudy_ServerScripts/setup/dev_study_env.sh')
    data_loc = os.environ['DATA_LOC']

fsfdir="%s/derivatives/level_1/"%(data_loc)

#DOUBLE CHECK WHAT THIS WAS IN THE ORIGINAL SCRIPT
subdirs=glob.glob("%s/derivatives/fmriprep_1.3.0/fmriprep/sub-*/func/sub-*_task-machinegame_run-*_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"%(data_loc))

for dir in list(subdirs):
  subnum = int(re.findall('\d+', os.path.basename(dir))[0])
  runnum = int(re.findall('\d+', os.path.basename(dir))[1])

  ntime = os.popen('fslnvols %s'%(dir)).read().rstrip()
  outdir = '%s/sub-%s/'%(fsfdir, subnum)

  replacements = {'SUBNUM':subnum, 'NTPTS':ntime, 'RUNNUM':runnum, 'OUTDIR': outdir}

  with open("%s/template_l1.fsf"%(fsfdir)) as infile:
    with open("%s/sub-%s/l1_design_sub-%s_run-%s.fsf"%(fsfdir, subnum, subnum, runnum), 'w') as outfile:
        for line in infile:
          for src, target in replacements.items():
            line = line.replace(src, target)
          outfile.write(line)

OUTDIR
# Output directory
set fmri(outputdir) "/oak/stanford/groups/russpold/data/ds000054/0.0.2/derivatives/level_1/sub-100003/model/run-01"

NTPTS
# Total volumes
set fmri(npts) 216

FEATDIR
# 4D AVW data or FEAT directory (1)
set feat_files(1) "/oak/stanford/groups/russpold/data/ds000054/0.0.2/derivatives/fmriprep_1.3.0/fmriprep/sub-100003/func/sub-100003_task-machinegame_run-01_space-MNI152NLin2009cAsym_desc-preproc_bold"

SCRUBVOLS
# Confound EVs text file for analysis 1
set confoundev_files(1) "/oak/stanford/groups/russpold/data/ds000054/0.0.2/derivatives/level_1/sub-100003/sub-100003_task-machinegame_run-01_scrub_vols.txt"

ANAT
# Subject's structural image for analysis 1
set highres_files(1) "/oak/stanford/groups/russpold/data/ds000054/0.0.2/derivatives/fmriprep_1.3.0/fmriprep/sub-100003/anat/sub-100003_space-MNI152NLin2009cAsym_desc-preproc_T1w"

CEV1 - CEV8
# Custom EV file (EV 1)
set fmri(custom1) "/oak/stanford/groups/russpold/data/ds000054/0.0.2/derivatives/level_1/sub-100003/sub-100003_task-machinegame_run-01_cond1.txt"
