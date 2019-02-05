#!/usr/bin/env python
import glob
import numpy as np
import os
import pandas as pd
import re

np.set_printoptions(precision=1, suppress=True)

try:
    data_loc = os.environ['DATA_LOC']
except KeyError:
    os.system('source /oak/stanford/groups/russpold/users/zenkavi/DevStudy_ServerScripts/setup/dev_study_env.sh')
    data_loc = os.environ['DATA_LOC']

#load fmriprep_counfounds file
fmriprep_counfounds_files = glob.glob('%s/derivatives/fmriprep_1.2.5/fmriprep/sub-*/func/sub-*_task-machinegame_run-*_desc-confounds_regressors.tsv'%(data_loc))
fmriprep_counfounds_files.sort()

scrub_report = pd.DataFrame()

#get index of vols where fd>0.9
for cur_confounds in fmriprep_counfounds_files:
    cur_df = pd.read_csv(cur_confounds, sep='\t')
    scrub_vols = np.where(cur_df.framewise_displacement>0.9,1,0)
    out_path = os.path.dirname(cur_confounds)
    out_file_name = os.path.basename(cur_confounds)
    out_file_name = re.sub("desc-confounds_regressors.tsv", "scrub_vols.txt", out_file_name)
    np.savetxt(os.path.join(out_path, out_file_name), scrub_vols.astype(int), fmt='%i', delimiter='\n')

#create one output report on how many/what percent of volumes per run are scrubbed
