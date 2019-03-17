#!/usr/bin/python
import os
import glob
import re
from argparse import ArgumentParser

#Usage: python make_l2_fsfs.py -m 1

parser = ArgumentParser()
parser.add_argument("-m", "--model_number", default = "1", help="model number")
args = parser.parse_args()

model_num = args.model_number

try:
    data_loc = os.environ['DATA_LOC']
    server_scripts = os.environ['SERVER_SCRIPTS']
except KeyError:
    os.system('source /oak/stanford/groups/russpold/users/zenkavi/DevStudy_ServerScripts/setup/dev_study_env.sh')
    data_loc = os.environ['DATA_LOC']
    server_scripts = os.environ['SERVER_SCRIPTS']

l2dir="%s/derivatives/level_2"%(data_loc)
l1dir="%s/derivatives/level_1"%(data_loc)
subdirs=glob.glob("%s/derivatives/level_1/sub-*/"%(data_loc))
subdirs.sort()

all_featdirs = glob.glob('%s/*/model%s/run*'%(l1dir, model_num))

for dir in subdirs:
  subnum = re.findall('\d+', os.path.dirname(dir))[5]
  outdir = '"%s/sub-%s/model%s/%s"'%(l2dir, subnum, model_num,subnum)
  if not os.path.exists('%s/sub-%s/model%s/'%(l2dir, subnum,model_num)):
      os.makedirs('%s/sub-%s/model%s/'%(l2dir, subnum,model_num))
  featdirs = [i for i in all_featdirs if subnum in i]
  featdirs.sort()
  ntpts = len(featdirs)
  print("Making l2 fsf for sub-%s"(%subnum))
  if ntpts == 6:
      replacements = {"OUTDIR": outdir, "NTPTS": str(ntpts), "FEATDIR1": '"%s"'%(featdirs[0]), "FEATDIR2": '"%s"'%(featdirs[1]), "FEATDIR3":'"%s"'%(featdirs[2]), "FEATDIR4": '"%s"'%(featdirs[3]), "FEATDIR5": '"%s"'%(featdirs[4]), "FEATDIR6": '"%s"'%(featdirs[5])}
      with open("%s/level_2/template_l2.fsf"%(server_scripts)) as infile:
          with open("%s/sub-%s/model%s/sub-%s_l2.fsf"%(l2dir, subnum, model_num, subnum), 'w') as outfile:
              for line in infile:
                  for src, target in replacements.items():
                      line = line.replace(src, target)
                  outfile.write(line)
  elif ntpts == 5:
      replacements = {"OUTDIR": outdir, "NTPTS": str(ntpts), "FEATDIR1": '"%s"'%(featdirs[0]), "FEATDIR2": '"%s"'%(featdirs[1]), "FEATDIR3":'"%s"'%(featdirs[2]), "FEATDIR4": '"%s"'%(featdirs[3]), "FEATDIR5": '"%s"'%(featdirs[4])}
      with open("%s/level_2/template_l2_r5.fsf"%(server_scripts)) as infile:
          with open("%s/sub-%s/model%s/sub-%s_l2.fsf"%(l2dir, subnum, model_num, subnum), 'w') as outfile:
              for line in infile:
                  for src, target in replacements.items():
                      line = line.replace(src, target)
                  outfile.write(line)
  elif ntpts == 4:
      replacements = {"OUTDIR": outdir, "NTPTS": str(ntpts), "FEATDIR1": '"%s"'%(featdirs[0]), "FEATDIR2": '"%s"'%(featdirs[1]), "FEATDIR3":'"%s"'%(featdirs[2]), "FEATDIR4": '"%s"'%(featdirs[3])}
      with open("%s/level_2/template_l2_r4.fsf"%(server_scripts)) as infile:
          with open("%s/sub-%s/model%s/sub-%s_l2.fsf"%(l2dir, subnum, model_num, subnum), 'w') as outfile:
              for line in infile:
                  for src, target in replacements.items():
                      line = line.replace(src, target)
                  outfile.write(line)
  elif ntpts == 3:
      replacements = {"OUTDIR": outdir, "NTPTS": str(ntpts), "FEATDIR1": '"%s"'%(featdirs[0]), "FEATDIR2": '"%s"'%(featdirs[1]), "FEATDIR3":'"%s"'%(featdirs[2])}
      with open("%s/level_2/template_l2_r3.fsf"%(server_scripts)) as infile:
          with open("%s/sub-%s/model%s/sub-%s_l2.fsf"%(l2dir, subnum, model_num, subnum), 'w') as outfile:
              for line in infile:
                  for src, target in replacements.items():
                      line = line.replace(src, target)
                  outfile.write(line)
  elif ntpts == 2:
      replacements = {"OUTDIR": outdir, "NTPTS": str(ntpts), "FEATDIR1": '"%s"'%(featdirs[0]), "FEATDIR2": '"%s"'%(featdirs[1])}
      with open("%s/level_2/template_l2_r2.fsf"%(server_scripts)) as infile:
          with open("%s/sub-%s/model%s/sub-%s_l2.fsf"%(l2dir, subnum, model_num, subnum), 'w') as outfile:
              for line in infile:
                  for src, target in replacements.items():
                      line = line.replace(src, target)
                      outfile.write(line)
  elif ntpts == 1:
      replacements = {"OUTDIR": outdir, "NTPTS": str(ntpts), "FEATDIR1": '"%s"'%(featdirs[0])}
      with open("%s/level_2/template_l2_r1.fsf"%(server_scripts)) as infile:
          with open("%s/sub-%s/model%s/sub-%s_l2.fsf"%(l2dir, subnum, model_num, subnum), 'w') as outfile:
              for line in infile:
                  for src, target in replacements.items():
                      line = line.replace(src, target)
                      outfile.write(line)
