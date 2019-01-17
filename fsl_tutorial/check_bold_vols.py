#!/usr/bin/env python

import glob
import pandas as pd
import subprocess

path = '/oak/stanford/groups/russpold/data/ds000054/0.0.1/'

boldfiles = glob.glob('%s/sub-[0-9][0-9][0-9][0-9][0-9][0-9]/func/sub-[0-9][0-9][0-9][0-9][0-9][0-9]_task-machinegame_run-0[0-9]_bold.nii.gz'%(path))

out_df = pd.DataFrame()

for file in boldfiles:
    cmd = ['fslnvols', '%s'%(file)]
    vols = int(subprocess.check_output(cmd).strip())
    cur_row = pd.DataFrame({"file": [file], "vols": [vols]})
    out_df = out_df.append(cur_row)

out_df = out_df.sort_values(by=['vols'])
out_df.to_csv('/oak/stanford/groups/russpold/users/zenkavi/DevStudy_ServerScripts/fsl_tutorial/check_bold_vols.csv')

if len(out_df.vols.unique())>1:
    print('Different volume numbers found!')
else:
    print('All volume numbers are the same.')
