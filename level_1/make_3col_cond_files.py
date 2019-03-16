import glob
import numpy as np
import os
import pandas as pd
import re

try:
    data_loc = os.environ['DATA_LOC']
except KeyError:
    os.system('source /oak/stanford/groups/russpold/users/zenkavi/DevStudy_ServerScripts/setup/dev_study_env.sh')
    data_loc = os.environ['DATA_LOC']

events_files = glob.glob('%s/sub-*/func/sub-*_task-machinegame_run-*_events.tsv'%(data_loc))
events_files.sort()

out_path = "%s/derivatives/level_1/sub-"%(data_loc)

all_events = pd.DataFrame()

for cur_ef in events_files:
    df = pd.read_csv(cur_ef, sep = '\t')
    all_events = all_events.append(df, ignore_index= True)

all_events = all_events[all_events['response_time'].notnull()]

mean_rt = all_events.response_time.mean()

for cur_ef in events_files:
    df = pd.read_csv(cur_ef, sep = '\t')
    nums = re.findall('\d+', os.path.basename(cur_ef))
    subnum = nums[0]
    runnum = nums[1]
    print("Making condition files for sub-%s run-%s"%(subnum, runnum))

    cond_m1 = df.query('trial_type == "stimulus_presentation" & stimulus == 1')[['onset']]
    cond_m1['duration'] = mean_rt
    cond_m1['machine1'] = 1
    np.savetxt(r'%s%s/sub-%s_task-machinegame_run-%s_cond_m1.txt'%(out_path,subnum,subnum,runnum), cond_m1.values, fmt='%1.3f')

    cond_m2 = df.query('trial_type == "stimulus_presentation" & stimulus == 2')[['onset', 'duration']]
    cond_m2['duration'] = mean_rt
    cond_m2['machine2'] = 1
    np.savetxt(r'%s%s/sub-%s_task-machinegame_run-%s_cond_m2.txt'%(out_path,subnum,subnum,runnum), cond_m2.values, fmt='%1.3f')

    cond_m3 = df.query('trial_type == "stimulus_presentation" & stimulus == 3')[['onset', 'duration']]
    cond_m3['duration'] = mean_rt
    cond_m3['machine3'] = 1
    np.savetxt(r'%s%s/sub-%s_task-machinegame_run-%s_cond_m3.txt'%(out_path,subnum,subnum,runnum), cond_m3.values, fmt='%1.3f')

    cond_m4 = df.query('trial_type == "stimulus_presentation" & stimulus == 4')[['onset', 'duration']]
    cond_m4['duration'] = mean_rt
    cond_m4['machine4'] = 1
    np.savetxt(r'%s%s/sub-%s_task-machinegame_run-%s_cond_m4.txt'%(out_path,subnum,subnum,runnum), cond_m4.values, fmt='%1.3f')

    df.rt_shift = df.response_time.shift(-1)

    cond_m1_rt = df.query('trial_type == "stimulus_presentation" & stimulus == 1')[['onset']]
    cond_m1_rt['duration'] = mean_rt
    cond_m1_rt['demaned_rt'] = df.rt_shift - mean_rt

    cond_m2_rt = df.query('trial_type == "stimulus_presentation" & stimulus == 2')[['onset']]
    cond_m2_rt['duration'] = mean_rt
    cond_m2_rt['demaned_rt'] = df.rt_shift - mean_rt

    cond_m3_rt = df.query('trial_type == "stimulus_presentation" & stimulus == 3')[['onset']]
    cond_m3_rt['duration'] = mean_rt
    cond_m3_rt['demaned_rt'] = df.rt_shift - mean_rt

    cond_m4_rt = df.query('trial_type == "stimulus_presentation" & stimulus == 4')[['onset']]
    cond_m4_rt['duration'] = mean_rt
    cond_m4_rt['demaned_rt'] = df.rt_shift - mean_rt

    post_choice_df = df.query('trial_type == "response"')

    ev_rpe_df = pd.read_csv(os.path.join(data_loc, 'derivatives/level_1/sub-%s/sub-%s_task-machinegame_run-%s_ev_rpe.csv'%(subnum, subnum, runnum)))

    post_choice_df = pd.concat([post_choice_df.reset_index(drop=True), ev_rpe_df.PE], axis=1)
    post_choice_df = post_choice_df[np.isfinite(post_choice_df['PE'])]
    cond_pe = post_choice_df[['onset', 'duration', 'PE']]
    np.savetxt(r'%s%s/sub-%s_task-machinegame_run-%s_pe.txt'%(out_path,subnum,subnum,runnum), cond_pe.values, fmt='%1.3f')


    cond_junk = df.query('response == 0')[['onset', 'duration']]
    cond_junk['junk'] = 1
    np.savetxt(r'%s%s/sub-%s_task-machinegame_run-%s_cond_junk.txt'%(out_path,subnum,subnum,runnum), cond_junk.values, fmt='%1.3f')

    print('Done saving condition files for sub-%s run-%s'%(subnum, runnum))

#PLUS:
#Temporal derivatives
#24 motion parameters
#scrub volumes
