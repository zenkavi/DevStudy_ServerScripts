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
    np.savetxt(r'%s%s/sub-%s_task-machinegame_run-%s_cond3.txt'%(out_path,subnum,subnum,runnum), cond3.values, fmt='%1.3f')
    np.savetxt(r'%s%s/sub-%s_task-machinegame_run-%s_cond4.txt'%(out_path,subnum,subnum,runnum), cond4.values, fmt='%1.3f')

    post_choice_df = df.query('trial_type == "response"')
    cond5 = post_choice_df.query('(stimulus == 1 & response == 2) | (stimulus == 2 & response == 1) | (stimulus == 3 & response == 1) | (stimulus == 4 & response == 2)')
    cond6 = pd.concat([post_choice_df, cond5]).drop_duplicates(keep=False)

    cond5 = cond5[['onset', 'duration']]
    cond5['correct'] = 1
    cond6 = cond6[['onset', 'duration']]
    cond6['incorrect'] = 1

    np.savetxt(r'%s%s/sub-%s_task-machinegame_run-%s_cond5.txt'%(out_path,subnum,subnum,runnum), cond5.values, fmt='%1.3f')
    np.savetxt(r'%s%s/sub-%s_task-machinegame_run-%s_cond6.txt'%(out_path,subnum,subnum,runnum), cond6.values, fmt='%1.3f')

    #Merge EV regressor to events df
    ev_df = pd.read_csv(os.path.join(data_loc, 'sub-%s_task-machinegame_run-%s_ev.csv'%(subnum, runnum)))
    pd.merge(post_choice_df, ev_df, on='')
    np.savetxt(r'%s%s/sub-%s_task-machinegame_run-%s_cond6.txt'%(out_path,subnum,subnum,runnum), cond7.values, fmt='%1.3f')

    print('Done saving condition files for sub-%s run-%s'%(subnum, runnum))


#cond1.txt = gain outcome (parametric)
#cond2.txt = loss outcome (parametric)
#cond3.txt = pre correct choice (stim-presentation)
    #trial_type == 'stim-presentation'
        #stimulus == 1 & response == 2
        #stimulus == 2 & response == 1
        #stimulus == 3 & response == 1
        #stimulus == 4 & response == 2
#cond4.txt = pre incorrect choice (stim-presentation)
    #trial_type == 'stim-presentation'
        #stimulus == 1 & response == 1
        #stimulus == 2 & response == 2
        #stimulus == 3 & response == 2
        #stimulus == 4 & response == 1
#cond5.txt = post correct choice (response)
    #trial_type == 'response'
        #stimulus == 1 & response == 2
        #stimulus == 2 & response == 1
        #stimulus == 3 & response == 1
        #stimulus == 4 & response == 2
#cond6.txt = post incorrect choice (response)
    #trial_type == 'response'
        #stimulus == 1 & response == 1
        #stimulus == 2 & response == 2
        #stimulus == 3 & response == 2
        #stimulus == 4 & response == 1
#cond7.txt = EV?

#contrasts:
#cond1 - baseline
#cond2 - baseline
#cond2 - cond1
#cond1 - cond2
#cond3 - baseline
#cond4 - baseline
#cond4 - cond3
#cond3 - cond4
#cond5 - baseline
#cond6 - baseline
#cond6 - cond5
#cond5 - cond6
