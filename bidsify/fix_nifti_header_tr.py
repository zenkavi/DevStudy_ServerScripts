#!/usr/bin/env python
import os
import glob
import subprocess

try:
    data_loc = os.environ['DATA_LOC']
except KeyError:
    os.system('source /oak/stanford/groups/russpold/users/zenkavi/DevStudy_ServerScripts/setup/dev_study_env.sh')
    data_loc = os.environ['DATA_LOC']

bold_files = glob.glob('%s/sub-*/func/sub-*_task-machinegame_run-*_bold.nii.gz'%(data_loc))

for cur_bold in bold_files:
    out = subprocess.check_output('fslinfo %s | grep "pixdim"'%(cur_bold), shell=True, stderr=subprocess.STDOUT).decode("utf-8")
    out_split = out.split('\n')
    try:
        out_split.remove('')
    out_split = [o.replace('        ', ':') for o in out_split]
    out_dict = {k:v for k,v in (x.split(':') for x in out_split)}
    pixdim1 = out_dict.get('pixdim1')
    pixdim2 = out_dict.get('pixdim2')
    pixdim3 = out_dict.get('pixdim3')
    pixdim4 = out_dict.get('pixdim4')
    if(pixdim4 != '2.000000'):
        pixdim4 = '2.000000'
