#!/usr/bin/python
import os
import glob
import nibabel as nib
import re

try:
    data_loc = os.environ['DATA_LOC']
    server_scripts = os.environ['SERVER_SCRIPTS']
except KeyError:
    os.system('source /oak/stanford/groups/russpold/users/zenkavi/DevStudy_ServerScripts/setup/dev_study_env.sh')
    data_loc = os.environ['DATA_LOC']
    server_scripts = os.environ['SERVER_SCRIPTS']

fsfdir="%s/derivatives/level_1"%(data_loc)
subdirs=glob.glob("%s/derivatives/fmriprep_1.3.0/fmriprep/sub-*/func/sub-*_task-machinegame_run-*_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"%(data_loc))
subdirs.sort()

for dir in subdirs:
  subnum = re.findall('\d+', os.path.basename(dir))[0]
  runnum = re.findall('\d+', os.path.basename(dir))[1]

  outdir = '"%s/sub-%s/model/run-%s"'%(fsfdir, subnum, runnum)
  cur_img = nib.load(dir)
  ntpts = str(int(cur_img.header['dim'][4]))
  featdir = '"%s/derivatives/fmriprep_1.3.0/fmriprep/sub-%s/func/sub-%s_task-machinegame_run-%s_space-MNI152NLin2009cAsym_desc-preproc_bold"'%(data_loc, subnum, subnum, runnum)
  scrubvols = "%s/sub-%s/sub-%s_task-machinegame_run-%s_scrub_vols.txt"%(fsfdir, subnum, subnum, runnum)
  anat = '"%s/derivatives/fmriprep_1.3.0/fmriprep/sub-%s/anat/sub-%s_space-MNI152NLin2009cAsym_desc-preproc_T1w"'%(data_loc, subnum, subnum)
  cev1 = '"%s/sub-%s/sub-%s_task-machinegame_run-%s_cond1.txt"'%(fsfdir, subnum, subnum, runnum)
  cev2 = '"%s/sub-%s/sub-%s_task-machinegame_run-%s_cond2.txt"'%(fsfdir, subnum, subnum, runnum)
  cev3 = '"%s/sub-%s/sub-%s_task-machinegame_run-%s_cond3.txt"'%(fsfdir, subnum, subnum, runnum)
  cev4 = '"%s/sub-%s/sub-%s_task-machinegame_run-%s_cond4.txt"'%(fsfdir, subnum, subnum, runnum)
  cev5 = '"%s/sub-%s/sub-%s_task-machinegame_run-%s_cond5.txt"'%(fsfdir, subnum, subnum, runnum)
  cev6 = '"%s/sub-%s/sub-%s_task-machinegame_run-%s_cond6.txt"'%(fsfdir, subnum, subnum, runnum)
  cev7 = '"%s/sub-%s/sub-%s_task-machinegame_run-%s_cond7.txt"'%(fsfdir, subnum, subnum, runnum)
  cev8 = '"%s/sub-%s/sub-%s_task-machinegame_run-%s_cond8   .txt"'%(fsfdir, subnum, subnum, runnum)

  replacements = {"OUTDIR": outdir, "NTPTS": ntpts, "FEATDIR": featdir, "SCRUBVOLS": scrubvols, "ANAT": anat, "CEV1": cev1, "CEV2": cev2, "CEV3": cev3, "CEV4": cev4, "CEV5": cev5, "CEV6": cev6, "CEV7": cev7, "CEV8": cev8}

  with open("%s/level1/template_l1.fsf"%(server_scripts)) as infile:
    with open("%s/sub-%s/model/sub-%s_run-%s_l1.fsf"%(fsfdir, subnum, subnum, runnum), 'w') as outfile:
        for line in infile:
          for src, target in replacements.items():
            line = line.replace(src, target)
          outfile.write(line)
