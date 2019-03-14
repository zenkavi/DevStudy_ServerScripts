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

for cur_ef in events_files:
    df = pd.read_csv(cur_ef, sep = '\t')
    nums = re.findall('\d+', os.path.basename(cur_ef))
    subnum = nums[0]
    runnum = nums[1]
    print("Making condition files for sub-%s run-%s"%(subnum, runnum))
    cond1 = df.query('points_earned>0')[['onset', 'duration', 'points_earned']]
    np.savetxt(r'%s%s/sub-%s_task-machinegame_run-%s_cond1.txt'%(out_path,subnum,subnum,runnum), cond1.values, fmt='%1.3f')
    cond2 = df.query('points_earned<0')[['onset', 'duration', 'points_earned']]
    np.savetxt(r'%s%s/sub-%s_task-machinegame_run-%s_cond2.txt'%(out_path,subnum,subnum,runnum), cond2.values, fmt='%1.3f')
    pre_choice_df = df.copy()
    pre_choice_df.response = pre_choice_df.response.shift(-1)
    pre_choice_df = pre_choice_df.query('trial_type == "stim_presentation"')
    cond3 = pre_choice_df.query('(stimulus == 1 & response == 2) | (stimulus == 2 & response == 1) | (stimulus == 3 & response == 1) | (stimulus == 4 & response == 2)')
    cond4 = pd.concat([pre_choice_df, cond3]).drop_duplicates(keep=False)
    cond3 = cond3[['onset', 'duration']]
    cond3['correct'] = 1
    cond4 = cond4[['onset', 'duration']]
    cond4['incorrect'] = 1
    if len(cond4) == 0:
        cond4 = pd.DataFrame(data={'onset': [0], 'duration': [0], 'incorrect': [1]})
        cols = ['onset', 'duration', 'incorrect']
        cond4 = cond4[cols]
    np.savetxt(r'%s%s/sub-%s_task-machinegame_run-%s_cond3.txt'%(out_path,subnum,subnum,runnum), cond3.values, fmt='%1.3f')
    np.savetxt(r'%s%s/sub-%s_task-machinegame_run-%s_cond4.txt'%(out_path,subnum,subnum,runnum), cond4.values, fmt='%1.3f')
    post_choice_df = df.query('trial_type == "response"')
    cond5 = post_choice_df.query('(stimulus == 1 & response == 2) | (stimulus == 2 & response == 1) | (stimulus == 3 & response == 1) | (stimulus == 4 & response == 2)')
    cond6 = pd.concat([post_choice_df, cond5]).drop_duplicates(keep=False)
    cond5 = cond5[['onset', 'duration']]
    cond5['correct'] = 1
    cond6 = cond6[['onset', 'duration']]
    cond6['incorrect'] = 1
    if len(cond6) == 0:
        cond6 = pd.DataFrame(data={'onset': [0], 'duration': [0], 'incorrect': [1]})
        cols = ['onset', 'duration', 'incorrect']
        cond6 = cond6[cols]
    np.savetxt(r'%s%s/sub-%s_task-machinegame_run-%s_cond5.txt'%(out_path,subnum,subnum,runnum), cond5.values, fmt='%1.3f')
    np.savetxt(r'%s%s/sub-%s_task-machinegame_run-%s_cond6.txt'%(out_path,subnum,subnum,runnum), cond6.values, fmt='%1.3f')
    ev_rpe_df = pd.read_csv(os.path.join(data_loc, 'derivatives/level_1/sub-%s/sub-%s_task-machinegame_run-%s_ev_rpe.csv'%(subnum, subnum, runnum)))
    pre_choice_df = pd.concat([pre_choice_df.reset_index(drop=True), ev_rpe_df.EV], axis=1)
    cond7 = pre_choice_df[['onset', 'duration', 'EV']]
    post_choice_df = pd.concat([post_choice_df.reset_index(drop=True), ev_rpe_df.PE], axis=1)
    post_choice_df = post_choice_df[np.isfinite(post_choice_df['PE'])]
    cond8 = post_choice_df[['onset', 'duration', 'PE']]
    np.savetxt(r'%s%s/sub-%s_task-machinegame_run-%s_cond7.txt'%(out_path,subnum,subnum,runnum), cond7.values, fmt='%1.3f')
    np.savetxt(r'%s%s/sub-%s_task-machinegame_run-%s_cond8.txt'%(out_path,subnum,subnum,runnum), cond8.values, fmt='%1.3f')
    print('Done saving condition files for sub-%s run-%s'%(subnum, runnum))


#MEAN OF ALL = 0
#cond 1 = stim 1
#cond 2 = stim 2
#cond 3 = stim 3
#cond 4 = stim 4
#cond 5 = RT
#cond 6 = junk
#24 motion parameters
#scrub volumes
