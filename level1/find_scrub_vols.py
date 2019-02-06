#!/usr/bin/env python
import glob
import numpy as np
import os
import pandas as pd
import re
import sys

#Usage: find_scrub_vols.py fd_thresh
#Acceptable fd_thresh = 0.5
#Stringent fd_thresh = 0.2

fd_thresh = float(sys.argv[1])

try:
    data_loc = os.environ['DATA_LOC']
except KeyError:
    os.system('source /oak/stanford/groups/russpold/users/zenkavi/DevStudy_ServerScripts/setup/dev_study_env.sh')
    data_loc = os.environ['DATA_LOC']

#load fmriprep_counfounds file
fmriprep_counfounds_files = glob.glob('%s/derivatives/fmriprep_1.2.5/fmriprep/sub-*/func/sub-*_task-machinegame_run-*_desc-confounds_regressors.tsv'%(data_loc))
fmriprep_counfounds_files.sort()

scrub_report = pd.DataFrame(columns=['sub_id', 'run', 'pct_scrubbed'])

#get index of vols where fd>0.9
for cur_confounds in fmriprep_counfounds_files:
    cur_df = pd.read_csv(cur_confounds, sep='\t')
    scrub_vols = np.where(cur_df.framewise_displacement>fd_thresh,1,0)
    out_file_name = os.path.basename(cur_confounds)
    out_file_name = re.sub("desc-confounds_regressors.tsv", "scrub_vols.txt", out_file_name)
    nums = re.findall('\d+', out_file_name)
    subnum = int(nums[0])
    runnum = int(nums[1])
    out_path = os.path.join(data_loc, 'derivative/level_1/sub-%s'%(str(subnum)))
    np.savetxt(os.path.join(out_path, out_file_name), scrub_vols.astype(int), fmt='%i', delimiter='\n')
    scrub_report = scrub_report.append({'sub_id': subnum, 'run': runnum, 'pct_scrubbed': sum(scrub_vols)/len(scrub_vols)*100}, ignore_index=True)

#output report on how many/what percent of volumes per run are scrubbed
scrub_report.to_csv('/oak/stanford/groups/russpold/data/ds000054/0.0.2/derivatives/level_1/scrub_fd_%s_report.csv'%(str(fd_thresh)))
