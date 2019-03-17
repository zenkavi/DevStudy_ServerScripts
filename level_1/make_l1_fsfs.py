#!/usr/bin/python
import os
import glob
import nibabel as nib
import re
from argparse import ArgumentParser

#Usage: python make_l1_fsfs.py -m 1 -ev1 m1 -ev2 m2 -ev3 m3 -ev4 m4 -ev5 m1_rt -ev6 m2_rt -ev7 m3_rt -ev8 m4_rt -ev9 pe_lv -ev10 pe_hv -ev11 junk

parser = ArgumentParser()
parser.add_argument("-m", "--model_number", help="model number")
parser.add_argument('-e','--evs', nargs='+', help='EVs', default = ['m1', 'm2', 'm3', 'm4', 'm1_rt', 'm2_rt', 'm3_rt', 'm4_rt', 'pe_lv', 'pe_hv', 'junk'])
args = parser.parse_args()

model_num = args.model_number
evs = args.evs

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
  print("Making design files for sub-%s run-%s"%(subnum, runnum))
  outdir = '"%s/sub-%s/model%s/run-%s"'%(fsfdir, subnum, model_num,runnum)
  cur_img = nib.load(dir)
  ntpts = str(int(cur_img.header['dim'][4]))
  featdir = '"%s/derivatives/fmriprep_1.3.0/fmriprep/sub-%s/func/sub-%s_task-machinegame_run-%s_space-MNI152NLin2009cAsym_desc-preproc_bold"'%(data_loc, subnum, subnum, runnum)
  scrubvols = '"%s/sub-%s/sub-%s_task-machinegame_run-%s_scrub_vols.txt"'%(fsfdir, subnum, subnum, runnum)
  anat = '"%s/derivatives/fmriprep_1.3.0/fmriprep/sub-%s/anat/sub-%s_space-MNI152NLin2009cAsym_desc-preproc_T1w"'%(data_loc, subnum, subnum)
  cur_evs = ['"%s/sub-%s/sub-%s_task-machinegame_run-%s_cond_%s.txt"'%(fsfdir, subnum, subnum, runnum, x) for x in evs ]
  replacements = {"OUTDIR": outdir, "NTPTS": ntpts, "FEATDIR": featdir, "SCRUBVOLS": scrubvols, "ANAT": anat, "CEV1": cur_evs[0], "CEV2": cur_evs[1], "CEV3": cur_evs[2], "CEV4": cur_evs[3], "CEV5": cur_evs[4], "CEV6": cur_evs[5], "CEV7": cur_evs[6], "CEV8": cur_evs[7], "CEV9": cur_evs[8], "CEV10": cur_evs[9], "CEV11": cur_evs[10]}
  if not os.path.exists("%s/sub-%s/model%s/"%(fsfdir, subnum, model_num)):
      os.makedirs(os.path.join("%s/sub-%s/model%s/"%(fsfdir, subnum, model_num)))
  with open("%s/level_1/template_l1_scrub.fsf"%(server_scripts)) as infile:
    with open("%s/sub-%s/model%s/sub-%s_run-%s_l1.fsf"%(fsfdir, subnum, model_num, subnum, runnum), 'w') as outfile:
        for line in infile:
          for src, target in replacements.items():
            line = line.replace(src, target)
          outfile.write(line)
