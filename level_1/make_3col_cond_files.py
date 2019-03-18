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

mean_rt = all_events.response_time.mean()/1000

del all_events

for cur_ef in events_files:
    df = pd.read_csv(cur_ef, sep = '\t')
    nums = re.findall('\d+', os.path.basename(cur_ef))
    subnum = nums[0]
    runnum = nums[1]
    print("Making condition files for sub-%s run-%s"%(subnum, runnum))

    cond_m1 = df.query('trial_type == "stim_presentation" & stimulus == 1')[['onset']]
    cond_m1['duration'] = mean_rt
    cond_m1['machine1'] = 1
    if len(cond_m1)<1:
        cond_m1 = pd.DataFrame(data={'onset': [0], 'duration': [0], 'machine1': [1]})[['onset', 'duration', 'machine1']]
    np.savetxt(r'%s%s/sub-%s_task-machinegame_run-%s_cond_m1.txt'%(out_path,subnum,subnum,runnum), cond_m1.values, fmt='%1.3f')

    cond_m2 = df.query('trial_type == "stim_presentation" & stimulus == 2')[['onset', 'duration']]
    cond_m2['duration'] = mean_rt
    cond_m2['machine2'] = 1
    if len(cond_m2)<1:
        cond_m2 = pd.DataFrame(data={'onset': [0], 'duration': [0], 'machine2': [1]})[['onset', 'duration', 'machine2']]
    np.savetxt(r'%s%s/sub-%s_task-machinegame_run-%s_cond_m2.txt'%(out_path,subnum,subnum,runnum), cond_m2.values, fmt='%1.3f')

    cond_m3 = df.query('trial_type == "stim_presentation" & stimulus == 3')[['onset', 'duration']]
    cond_m3['duration'] = mean_rt
    cond_m3['machine3'] = 1
    if len(cond_m3)<1:
        cond_m3 = pd.DataFrame(data={'onset': [0], 'duration': [0], 'machine3': [1]})[['onset', 'duration', 'machine3']]
    np.savetxt(r'%s%s/sub-%s_task-machinegame_run-%s_cond_m3.txt'%(out_path,subnum,subnum,runnum), cond_m3.values, fmt='%1.3f')

    cond_m4 = df.query('trial_type == "stim_presentation" & stimulus == 4')[['onset', 'duration']]
    cond_m4['duration'] = mean_rt
    cond_m4['machine4'] = 1
    if len(cond_m4)<1:
        cond_m4 = pd.DataFrame(data={'onset': [0], 'duration': [0], 'machine4': [1]})[['onset', 'duration', 'machine4']]
    np.savetxt(r'%s%s/sub-%s_task-machinegame_run-%s_cond_m4.txt'%(out_path,subnum,subnum,runnum), cond_m4.values, fmt='%1.3f')

    df['rt_shift'] = df.response_time.shift(-1)

    cond_m1_rt = df.query('trial_type == "stim_presentation" & stimulus == 1')[['onset']]
    cond_m1_rt['duration'] = mean_rt
    cond_m1_rt['demaned_rt'] = df.rt_shift - mean_rt
    if len(cond_m1_rt)<1:
        cond_m1_rt = pd.DataFrame(data={'onset': [0], 'duration': [0], 'demaned_rt': [0]})[['onset', 'duration', 'demaned_rt']]
    np.savetxt(r'%s%s/sub-%s_task-machinegame_run-%s_cond_m1_rt.txt'%(out_path,subnum,subnum,runnum), cond_m1_rt.values, fmt='%1.3f')

    cond_m2_rt = df.query('trial_type == "stim_presentation" & stimulus == 2')[['onset']]
    cond_m2_rt['duration'] = mean_rt
    cond_m2_rt['demaned_rt'] = df.rt_shift - mean_rt
    if len(cond_m2_rt)<1:
        cond_m2_rt = pd.DataFrame(data={'onset': [0], 'duration': [0], 'demaned_rt': [0]})[['onset', 'duration', 'demaned_rt']]
    np.savetxt(r'%s%s/sub-%s_task-machinegame_run-%s_cond_m2_rt.txt'%(out_path,subnum,subnum,runnum), cond_m2_rt.values, fmt='%1.3f')

    cond_m3_rt = df.query('trial_type == "stim_presentation" & stimulus == 3')[['onset']]
    cond_m3_rt['duration'] = mean_rt
    cond_m3_rt['demaned_rt'] = df.rt_shift - mean_rt
    if len(cond_m3_rt)<1:
        cond_m3_rt = pd.DataFrame(data={'onset': [0], 'duration': [0], 'demaned_rt': [0]})[['onset', 'duration', 'demaned_rt']]
    np.savetxt(r'%s%s/sub-%s_task-machinegame_run-%s_cond_m3_rt.txt'%(out_path,subnum,subnum,runnum), cond_m3_rt.values, fmt='%1.3f')

    cond_m4_rt = df.query('trial_type == "stim_presentation" & stimulus == 4')[['onset']]
    cond_m4_rt['duration'] = mean_rt
    cond_m4_rt['demaned_rt'] = df.rt_shift - mean_rt
    if len(cond_m4_rt)<1:
        cond_m4_rt = pd.DataFrame(data={'onset': [0], 'duration': [0], 'demaned_rt': [0]})[['onset', 'duration', 'demaned_rt']]
    np.savetxt(r'%s%s/sub-%s_task-machinegame_run-%s_cond_m4_rt.txt'%(out_path,subnum,subnum,runnum), cond_m4_rt.values, fmt='%1.3f')

    post_choice_df = df.query('trial_type == "response"')

    ev_rpe_df = pd.read_csv(os.path.join(data_loc, 'derivatives/level_1/sub-%s/sub-%s_task-machinegame_run-%s_ev_rpe.csv'%(subnum, subnum, runnum)))

    post_choice_df = pd.concat([post_choice_df.reset_index(drop=True), ev_rpe_df.PE], axis=1)
    post_choice_df = post_choice_df[np.isfinite(post_choice_df['PE'])]

    cond_pe_lv = post_choice_df.query("stimulus == 1 | stimulus == 3")[['onset', 'duration', 'PE']]
    cond_pe_lv.PE = cond_pe_lv.PE - cond_pe_lv.PE.mean()
    if len(cond_pe_lv)<1:
        cond_pe_lv = pd.DataFrame(data={'onset': [0], 'duration': [0], 'PE': [0]})[['onset', 'duration', 'PE']]
    np.savetxt(r'%s%s/sub-%s_task-machinegame_run-%s_cond_pe_lv.txt'%(out_path,subnum,subnum,runnum), cond_pe_lv.values, fmt='%1.3f')

    cond_pe_hv = post_choice_df.query("stimulus == 2 | stimulus == 4")[['onset', 'duration', 'PE']]
    cond_pe_hv.PE = cond_pe_hv.PE - cond_pe_hv.PE.mean()
    if len(cond_pe_hv)<1:
        cond_pe_hv = pd.DataFrame(data={'onset': [0], 'duration': [0], 'PE': [0]})[['onset', 'duration', 'PE']]
    np.savetxt(r'%s%s/sub-%s_task-machinegame_run-%s_cond_pe_hv.txt'%(out_path,subnum,subnum,runnum), cond_pe_hv.values, fmt='%1.3f')

    df['response_shift'] = df.response.shift(-1)
    cond_junk = df.query('response == 0 & response_shift == 0')[['onset', 'duration']]
    cond_junk['junk'] = 1
    if len(cond_junk)<1:
        cond_junk = pd.DataFrame(data={'onset': [0], 'duration': [0], 'junk': [0]})[['onset', 'duration', 'junk']]
    np.savetxt(r'%s%s/sub-%s_task-machinegame_run-%s_cond_junk.txt'%(out_path,subnum,subnum,runnum), cond_junk.values, fmt='%1.3f')

    print('Done saving condition files for sub-%s run-%s'%(subnum, runnum))


#low var machines: 1, 3; high var machines: 2, 4
#PLUS:
#Temporal derivatives
#24 motion parameters
#scrub volumes
