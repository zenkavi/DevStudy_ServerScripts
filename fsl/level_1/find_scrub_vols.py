#!/usr/bin/env python
import glob
import numpy as np
import os
import pandas as pd
import re
import sys
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-fd", "--fd_thresh", default=0.5, help="FD threshold to scrub")
parser.add_argument("-ep", "--exclude_percent", default=20 , help="Threshold of percentage of scrubbed volumes for excluding a run")
args = parser.parse_args()

fd_thresh = args.fd_thresh
exclude_percent = args.exclude_percent

try:
    data_loc = os.environ['DATA_LOC']
except KeyError:
    os.system('source /oak/stanford/groups/russpold/users/zenkavi/DevStudy_ServerScripts/setup/dev_study_env.sh')
    data_loc = os.environ['DATA_LOC']

#load fmriprep_confounds file
fmriprep_confounds_files = glob.glob('%s/derivatives/fmriprep_1.3.0/fmriprep/sub-*/func/sub-*_task-machinegame_run-*_desc-confounds_regressors.tsv'%(data_loc))
fmriprep_confounds_files.sort()

scrub_report = pd.DataFrame(columns=['sub_id', 'run', 'pct_scrubbed'])

#get index of vols where fd>0.9
for cur_confounds in fmriprep_confounds_files:
    cur_df = pd.read_csv(cur_confounds, sep='\t')
    scrub_vols = np.where(cur_df.framewise_displacement>fd_thresh,1,0)
    out_file_name = os.path.basename(cur_confounds)
    out_file_name = re.sub("desc-confounds_regressors.tsv", "scrub_vols.txt", out_file_name)
    nums = re.findall('\d+', out_file_name)
    subnum = int(nums[0])
    runnum = int(nums[1])
    out_path = os.path.join(data_loc, 'derivatives/level_1/sub-%s'%(subnum))
    os.makedirs(out_path, exist_ok=True)
    np.savetxt(os.path.join(out_path, out_file_name), scrub_vols.astype(int), fmt='%i', delimiter='\n')
    pct_scrubbed = sum(scrub_vols)/len(scrub_vols)*100
    scrub_report = scrub_report.append({'sub_id': subnum, 'run': runnum, 'pct_scrubbed': pct_scrubbed}, ignore_index=True)

    #remove that run from derivatives/fmriprep so it is not used for further processing if pct_scrubbed>20%
    if pct_scrubbed > exclude_percent:
        mv_path = '%s/sourcedata/derivatives/fmriprep/sub-%s/'%(data_loc,str(subnum))
        os.makedirs(mv_path, exist_ok=True)
        mv_files = glob.glob('%s/derivatives/fmriprep_1.3.0/fmriprep/sub-%s/func/*sub-%s*run-00%s*'%(data_loc,str(subnum),str(subnum),str(runnum)))
        for i in mv_files:
            os.rename(i, os.path.join(mv_path, os.path.basename(i)))

#output report on how many/what percent of volumes per run are scrubbed
scrub_report.to_csv('%s/derivatives/level_1/scrub_fd_%s_report.csv'%(data_loc, str(fd_thresh)))
