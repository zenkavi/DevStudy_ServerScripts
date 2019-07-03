import numpy as np
import pandas as pd

def make_contrasts(design_matrix, pe):
        # first generate canonical contrasts (i.e. regressors vs. baseline)
    contrast_matrix = np.eye(design_matrix.shape[1])
    contrasts = dict([(column, contrast_matrix[i])
                      for i, column in enumerate(design_matrix.columns)])

    dictfilt = lambda x, y: dict([ (i,x[i]) for i in x if i in set(y) ])
    wanted_keys = ['m1', 'm2', 'm3', 'm4','m1_rt', 'm2_rt', 'm3_rt', 'm4_rt','hpe', 'lpe','gain', 'loss','junk']
    contrasts = dictfilt(contrasts, wanted_keys)

    contrasts.update({'task_on': (contrasts['m1'] + contrasts['m2'] + contrasts['m3'] + contrasts['m4']),
    'rt': (contrasts['m1_rt'] + contrasts['m2_rt'] + contrasts['m3_rt'] + contrasts['m4_rt']),
    'var_sen': ((contrasts['m1'] + contrasts['m2']) - (contrasts['m3'] + contrasts['m4'])),
    'ev_sen': ((contrasts['m2'] + contrasts['m3']) - (contrasts['m1'] + contrasts['m4']))})

    if pe:
        if 'hpe' in contrasts.keys() and 'lpe' in contrasts.keys():
            contrasts.update({'pe': contrasts['hpe'] +  contrasts['lpe']})
    return contrasts

def add_transform(dataframe, columns=None, type=None):
    if columns is None:
        columns = dataframe.columns
    if type == "td":
        td = dataframe.loc[:,columns].apply(np.gradient)
        td.iloc[0,:] = 0
        for i,col in td.iteritems():
            insert_loc = dataframe.columns.get_loc(i)
            dataframe.insert(insert_loc+1, i+'_td', col)
    if type == "sq":
        sq = dataframe.loc[:,columns].apply(np.square)
        sq.iloc[0,:] = 0
        for i,col in sq.iteritems():
            insert_loc = dataframe.columns.get_loc(i)
            dataframe.insert(insert_loc+1, i+'_sq', col)

def stdize(X):
    return (X - np.nanmean(X, axis=0))/np.nanstd(X, axis=0)

def get_conditions(cur_events, runnum, mean_rt, sub_pes, pe):
    #process events for GLM
    #events: 4 col events file for WHOLE RUN with onset, duration, trial_type, modulation
    #trial_type column:
        #m1, m2, m3, m4 - onset: stimulus_presentation onset, duration: mean_rt, modulation: 1
        #m1_rt, m2_rt, m3_rt, m4_rt - onset: stimulus_presentation, duration: mean_rt, modulation: rt-mean_rt
        #gain - onset: response onset, duration: response duration, modulation: gain-mean_gain
        #loss - onset: reponse onset, duration: response duration, modulation: loss-mean_loss
        #junk: onset: response onset, duration: response duration, modulation: 1

    cur_events.response_time = cur_events.response_time/1000
    rt = cur_events.response_time
    cur_events.loc[:,'response_time'] = rt - rt[rt>0].mean()
    cur_events['rt_shift'] = cur_events.response_time.shift(-1)
    # scaling the outcomes so the design matrix looks better when plotting. Doesn't make a difference in level1 images either way
    #po = cur_events.points_earned
    #cur_events.points_earned = np.where(po == 5, 0.01, np.where(po == 495, 0.99, np.where(po == 10, 0.02, np.where(po == 100, 0.20, np.where(po == -5, -0.01, np.where(po == -495, -0.99, np.where(po == -10, -0.02, np.where(po == -100, -0.20, 0))))))))

    max_X = int(runnum)*30
    run_pes = sub_pes.query('X<@max_X')

    cond_m1 = cur_events.query('trial_type == "stim_presentation" & stimulus == 1')[['onset']]
    cond_m1['duration'] = mean_rt
    cond_m1['modulation'] = 1
    cond_m1['trial_type'] = 'm1'
    cond_m2 = cur_events.query('trial_type == "stim_presentation" & stimulus == 2')[['onset']]
    cond_m2['duration'] = mean_rt
    cond_m2['modulation'] = 1
    cond_m2['trial_type'] = 'm2'
    cond_m3 = cur_events.query('trial_type == "stim_presentation" & stimulus == 3')[['onset']]
    cond_m3['duration'] = mean_rt
    cond_m3['modulation'] = 1
    cond_m3['trial_type'] = 'm3'
    cond_m4 = cur_events.query('trial_type == "stim_presentation" & stimulus == 4')[['onset']]
    cond_m4['duration'] = mean_rt
    cond_m4['modulation'] = 1
    cond_m4['trial_type'] = 'm4'
    cond_m1_rt = cur_events.query('trial_type == "stim_presentation" & stimulus == 1')[['onset', 'rt_shift']]
    cond_m1_rt['duration'] = mean_rt
    cond_m1_rt['modulation'] = cond_m1_rt['rt_shift']
    cond_m1_rt = cond_m1_rt.drop(['rt_shift'], axis=1)
    cond_m1_rt['trial_type'] = "m1_rt"
    cond_m2_rt = cur_events.query('trial_type == "stim_presentation" & stimulus == 2')[['onset', 'rt_shift']]
    cond_m2_rt['duration'] = mean_rt
    cond_m2_rt['modulation'] = cond_m2_rt['rt_shift']
    cond_m2_rt = cond_m2_rt.drop(['rt_shift'], axis=1)
    cond_m2_rt['trial_type'] = "m2_rt"
    cond_m3_rt = cur_events.query('trial_type == "stim_presentation" & stimulus == 3')[['onset', 'rt_shift']]
    cond_m3_rt['duration'] = mean_rt
    cond_m3_rt['modulation'] = cond_m3_rt['rt_shift']
    cond_m3_rt = cond_m3_rt.drop(['rt_shift'], axis=1)
    cond_m3_rt['trial_type'] = "m3_rt"
    cond_m4_rt = cur_events.query('trial_type == "stim_presentation" & stimulus == 4')[['onset', 'rt_shift']]
    cond_m4_rt['duration'] = mean_rt
    cond_m4_rt['modulation'] = cond_m4_rt['rt_shift']
    cond_m4_rt = cond_m4_rt.drop(['rt_shift'], axis=1)
    cond_m4_rt['trial_type'] = "m4_rt"
    cond_gain = cur_events.query('points_earned>0')[['onset', 'duration','points_earned']]
    cond_gain = cond_gain.rename(index=str, columns={"points_earned": "modulation"})
    cond_gain['trial_type'] =  "gain"
    cond_loss = cur_events.query('points_earned<0')[['onset', 'duration','points_earned']]
    cond_loss = cond_loss.rename(index=str, columns={"points_earned": "modulation"})
    cond_loss['trial_type'] =  "loss"
    cond_loss = cond_loss.rename(index=str, columns={"points_earned": "modulation"})
    cond_pe = cur_events.query('response == 1')
    cond_pe = pd.concat([cond_pe.reset_index(drop=True), run_pes['PE'].reset_index(drop=True)], axis=1)
    cond_hpe = cond_pe.query('stimulus == 1 | stimulus == 2')
    cond_lpe = cond_pe.query('stimulus == 3 | stimulus == 4')
    cond_hpe['PE'] = cond_hpe['PE'].sub(cond_hpe['PE'].mean())
    cond_lpe['PE'] = cond_lpe['PE'].sub(cond_lpe['PE'].mean())
    cond_hpe = cond_hpe[['onset', 'duration', 'PE']]
    cond_hpe = cond_hpe.rename(index=str, columns={"PE": "modulation"})
    cond_hpe['trial_type'] = 'hpe'
    cond_lpe = cond_lpe[['onset', 'duration', 'PE']]
    cond_lpe = cond_lpe.rename(index=str, columns={"PE": "modulation"})
    cond_lpe['trial_type'] = 'lpe'
    cond_junk = cur_events.query('response == 0')[['onset', 'duration']]
    cond_junk['modulation'] = 1
    cond_junk['trial_type'] = "junk"

    if pe:
        formatted_events = pd.concat([cond_m1, cond_m2, cond_m3, cond_m4, cond_m1_rt, cond_m2_rt, cond_m3_rt, cond_m4_rt, cond_hpe, cond_lpe, cond_junk], ignore_index=True)
    else:
        formatted_events = pd.concat([cond_m1, cond_m2, cond_m3, cond_m4, cond_m1_rt, cond_m2_rt, cond_m3_rt, cond_m4_rt, cond_gain, cond_loss, cond_junk], ignore_index=True)

    formatted_events = formatted_events.sort_values(by='onset')

    formatted_events = formatted_events[['onset', 'duration', 'trial_type', 'modulation']].reset_index(drop=True)

    return formatted_events

def get_confounds(cur_confounds):
    formatted_confounds = cur_confounds[['trans_x', 'trans_y', 'trans_z', 'rot_x', 'rot_y', 'rot_z']]
    add_transform(formatted_confounds, type="sq")
    add_transform(formatted_confounds, type="td")
    formatted_confounds[['std_dvars', 'framewise_displacement']] = cur_confounds[['std_dvars', 'framewise_displacement']]
    formatted_confounds['std_dvars'].iloc[0] = 0
    formatted_confounds['framewise_displacement'].iloc[0] = 0
    formatted_confounds['scrub'] = np.where(formatted_confounds.framewise_displacement>0.5,1,0)
    return formatted_confounds
