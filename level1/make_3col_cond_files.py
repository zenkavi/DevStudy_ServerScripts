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
    np.savetxt(r'%s%s/sub-%s_task-machinegame_run-%s_cond2.txt'%(out_path,subnum,subnum,runnum), cond1.values, fmt='%1.3f')
    cond3
    cond4
    cond5
    cond6


#cond1.txt = gain (parametric)
#cond2.txt = loss (parametric)
#cond3.txt = pre correct choice (stim-presentation)
#cond4.txt = pre incorrect choice (stim-presentation)
#cond5.txt = post correct choice (response)
#cond6.txt = post incorrect choice (response)

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
