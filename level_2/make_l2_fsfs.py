#!/usr/bin/python
import os
import glob
import re

try:
    data_loc = os.environ['DATA_LOC']
    server_scripts = os.environ['SERVER_SCRIPTS']
except KeyError:
    os.system('source /oak/stanford/groups/russpold/users/zenkavi/DevStudy_ServerScripts/setup/dev_study_env.sh')
    data_loc = os.environ['DATA_LOC']
    server_scripts = os.environ['SERVER_SCRIPTS']

fsfdir="%s/derivatives/level_2"%(data_loc)
subdirs=glob.glob("%s/derivatives/level_1/sub-*/"%(data_loc))
subdirs.sort()

for dir in subdirs:
  subnum = re.findall('\d+', os.path.dirname(dir))[5]

  outdir = '"%s/sub-%s/model/"'%(fsfdir, subnum)
  if not os.path.exists('%s/sub-%s/model/'%(fsfdir, subnum)):
      os.makedirs('%s/sub-%s/model/'%(fsfdir, subnum))

  ntpts = ...


  #OUTDIR: "/oak/stanford/groups/russpold/data/ds000054/0.0.4/derivatives/level_2"
  #FEATDIR1: "/oak/stanford/groups/russpold/data/ds000054/0.0.4/derivatives/level_1/sub-100003/model/run-001.feat"

  if ntpts == 6:
      replacements = {"OUTDIR": outdir, "NTPTS": ntpts, "FEATDIR1": feadirs[0], "FEATDIR2": feadirs[1], "FEATDIR3": feadirs[2], "FEATDIR4": feadirs[3], "FEATDIR5": feadirs[4], "FEATDIR6": feadirs[5]}
      with open("%s/level_2/template_l2.fsf"%(server_scripts)) as infile:
  elif ntpts == 5:
      with open("%s/level_2/template_l2_r5.fsf"%(server_scripts)) as infile:
  elif ntpts == 3:
      with open("%s/level_2/template_l2_r3.fsf"%(server_scripts)) as infile:
          with open("%s/sub-%s/model/sub-%s_l2.fsf"%(fsfdir, subnum, subnum), 'w') as outfile:
              for line in infile:
                  for src, target in replacements.items():
                      line = line.replace(src, target)
                  outfile.write(line)
