import glob
import nibabel as nib
from nistats.first_level_model import FirstLevelModel
import numpy as np
import os
import pandas as pd
import pickle
import re
import sys
sys.path.append(os.path.join(os.environ['SERVER_SCRIPTS'], 'func_con'))
from seed2vox.get_seed_to_vox_corrs import get_seed_timeseries

def make_contrasts(design_matrix, pe, ev, ppi=False):
        # first generate canonical contrasts (i.e. regressors vs. baseline)
    contrast_matrix = np.eye(design_matrix.shape[1])
    contrasts = dict([(column, contrast_matrix[i])
                      for i, column in enumerate(design_matrix.columns)])

    dictfilt = lambda x, y: dict([ (i,x[i]) for i in x if i in set(y) ])
    if ppi:
        wanted_keys =  [col for col in design_matrix.columns if 'ppi' in col]
        contrasts = dictfilt(contrasts, wanted_keys)
        contrasts.update({'ppi_m1_con': (contrasts['ppi_m1']*3 - (contrasts['ppi_m2']+contrasts['ppi_m3']+contrasts['ppi_m4'])),
                'ppi_m2_con': (contrasts['ppi_m2']*3 - (contrasts['ppi_m1']+contrasts['ppi_m3']+contrasts['ppi_m4'])),
                'ppi_m3_con': (contrasts['ppi_m3']*3 - (contrasts['ppi_m2']+contrasts['ppi_m1']+contrasts['ppi_m4'])),
                'ppi_m4_con': (contrasts['ppi_m4']*3 - (contrasts['ppi_m2']+contrasts['ppi_m3']+contrasts['ppi_m1']))})

    else:
        wanted_keys = ['m1', 'm2', 'm3', 'm4', 'm1_ev', 'm2_ev', 'm3_ev', 'm4_ev', 'm1_rt', 'm2_rt', 'm3_rt', 'm4_rt','hpe', 'lpe','gain', 'loss','junk']
        contrasts = dictfilt(contrasts, wanted_keys)

        contrasts.update({'rt': (contrasts['m1_rt'] + contrasts['m2_rt'] + contrasts['m3_rt'] + contrasts['m4_rt'])})

        if ev:
            contrasts.update({'task_on': (contrasts['m1_ev'] + contrasts['m2_ev'] + contrasts['m3_ev'] + contrasts['m4_ev']),
            'var_sen': ((contrasts['m1_ev'] + contrasts['m2_ev']) - (contrasts['m3_ev'] + contrasts['m4_ev'])),
            'ev_sen': ((contrasts['m2_ev'] + contrasts['m3_ev']) - (contrasts['m1_ev'] + contrasts['m4_ev']))})
        else:
            contrasts.update({'task_on': (contrasts['m1'] + contrasts['m2'] + contrasts['m3'] + contrasts['m4']),
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

def get_conditions(cur_events, runnum, mean_rt, sub_pes, pe, sub_evs, ev):
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
    run_evs = sub_evs.query('X<@max_X')

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
    cond_ev = cur_events.query('trial_type == "stim_presentation"')
    cond_ev = pd.concat([cond_ev.reset_index(drop=True), run_evs['EV'].reset_index(drop=True)], axis=1)
    cond_m1_ev = cond_ev.query('trial_type == "stim_presentation" & stimulus == 1')
    cond_m2_ev = cond_ev.query('trial_type == "stim_presentation" & stimulus == 2')
    cond_m3_ev = cond_ev.query('trial_type == "stim_presentation" & stimulus == 3')
    cond_m4_ev = cond_ev.query('trial_type == "stim_presentation" & stimulus == 4')
    #Demeaning for parametric regressors
    cond_m1_ev['EV'] = cond_m1_ev['EV'].sub(cond_m1_ev['EV'].mean())
    cond_m2_ev['EV'] = cond_m2_ev['EV'].sub(cond_m2_ev['EV'].mean())
    cond_m3_ev['EV'] = cond_m3_ev['EV'].sub(cond_m3_ev['EV'].mean())
    cond_m4_ev['EV'] = cond_m4_ev['EV'].sub(cond_m4_ev['EV'].mean())
    cond_m1_ev = cond_m1_ev[['onset', 'duration', 'EV']]
    cond_m1_ev = cond_m1_ev.rename(index=str, columns={"EV": "modulation"})
    cond_m1_ev['trial_type'] = 'm1_ev'
    cond_m2_ev = cond_m2_ev.rename(index=str, columns={"EV": "modulation"})
    cond_m2_ev['trial_type'] = 'm2_ev'
    cond_m3_ev = cond_m3_ev.rename(index=str, columns={"EV": "modulation"})
    cond_m3_ev['trial_type'] = 'm3_ev'
    cond_m4_ev = cond_m4_ev.rename(index=str, columns={"EV": "modulation"})
    cond_m4_ev['trial_type'] = 'm4_ev'
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
    #Demeaning for parametric regressors
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
        if ev:
            formatted_events = pd.concat([cond_m1_ev, cond_m2_ev, cond_m3_ev, cond_m4_ev, cond_m1_rt, cond_m2_rt, cond_m3_rt, cond_m4_rt, cond_hpe, cond_lpe, cond_junk], ignore_index=True)
        else:
            formatted_events = pd.concat([cond_m1, cond_m2, cond_m3, cond_m4, cond_m1_rt, cond_m2_rt, cond_m3_rt, cond_m4_rt, cond_hpe, cond_lpe, cond_junk], ignore_index=True)
    else:
        if ev:
            formatted_events = pd.concat([cond_m1_ev, cond_m2_ev, cond_m3_ev, cond_m4_ev, cond_m1_rt, cond_m2_rt, cond_m3_rt, cond_m4_rt, cond_gain, cond_loss, cond_junk], ignore_index=True)
        else:
            formatted_events = pd.concat([cond_m1, cond_m2, cond_m3, cond_m4, cond_m1_rt, cond_m2_rt, cond_m3_rt, cond_m4_rt, cond_gain, cond_loss, cond_junk], ignore_index=True)

    formatted_events = formatted_events.sort_values(by='onset')

    formatted_events = formatted_events[['onset', 'duration', 'trial_type', 'modulation']].reset_index(drop=True)

    return formatted_events

def get_confounds(cur_confounds):
    if "trans_x_derivative1" not in cur_confounds.columns:
        formatted_confounds = cur_confounds[['trans_x', 'trans_y', 'trans_z', 'rot_x', 'rot_y', 'rot_z']]
        add_transform(formatted_confounds, type="sq")
        add_transform(formatted_confounds, type="td")
    else:
        motion_cols = ['trans_x', 'trans_y', 'trans_z', 'rot_x', 'rot_y', 'rot_z']
        formatted_confounds = cur_confounds[[s for s in cur_confounds.columns if any(xs in s for xs in motion_cols)]]
        where_are_NaNs = np.isnan(formatted_confounds)
        formatted_confounds[where_are_NaNs] = 0
    formatted_confounds[['std_dvars', 'framewise_displacement']] = cur_confounds[['std_dvars', 'framewise_displacement']]
    formatted_confounds['std_dvars'].iloc[0] = 0
    formatted_confounds['framewise_displacement'].iloc[0] = 0
    formatted_confounds['scrub'] = np.where(formatted_confounds.framewise_displacement>0.5,1,0)
    return formatted_confounds

def run_level1(subnum, out_path, pe, pe_path, ev, ev_path, beta):

    data_loc = os.environ['DATA_LOC']
    events_files = glob.glob('%s/sub-*/func/sub-*_task-machinegame_run-*_events.tsv'%(data_loc))
    events_files.sort()

    if not os.path.exists(out_path):
        os.makedirs(out_path)

    contrasts_path = "%s/contrasts"%(out_path)
    if not os.path.exists(contrasts_path):
        os.makedirs(contrasts_path)

    #all_events = pd.DataFrame()
    #for cur_ef in events_files:
    #    df = pd.read_csv(cur_ef, sep = '\t')
    #    all_events = all_events.append(df, ignore_index= True)
    #all_events = all_events[all_events['response_time'].notnull()]
    #all_events.response_time = all_events.response_time/1000
    #mean_rt = all_events.response_time.mean()
    #del all_events
    mean_rt = 1.1206937019969279

    sub_events = [x for x in events_files if subnum in x]

    if pe:
        all_pes = pd.read_csv(pe_path)
        sub_pes = all_pes.query('sub_id == @subnum')
        del all_pes
    else:
        sub_pe = None

    if ev:
        all_evs = pd.read_csv(ev_path)
        sub_evs = all_evs.query('sub_id == @subnum')
        del all_evs
    else:
        sub_evs = None

    for run_events in sub_events:

        runnum = re.findall('\d+', os.path.basename(run_events))[1]

        exists = os.path.isfile(os.path.join(data_loc,"derivatives/fmriprep_1.4.0/fmriprep/sub-%s/func/sub-%s_task-machinegame_run-%s_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"%(subnum, subnum, runnum)))

        if exists:

            #fmri_img: path to preproc_bold that the model will be fit on
            fmri_img = os.path.join(data_loc,"derivatives/fmriprep_1.4.0/fmriprep/sub-%s/func/sub-%s_task-machinegame_run-%s_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"%(subnum, subnum, runnum))

            #read in preproc_bold for that run
            cur_img = nib.load(fmri_img)
            cur_img_tr = cur_img.header['pixdim'][4]

            #read in events.tsv for that run
            cur_events = pd.read_csv(run_events, sep = '\t')
            formatted_events = get_conditions(cur_events, runnum, mean_rt, sub_pes, pe, sub_evs, ev)

            #process confounds
            #['X','Y','Z','RotX','RotY','RotY','<-firsttemporalderivative','stdDVARs','FD','scrub']
            cur_confounds = pd.read_csv(os.path.join(data_loc,"derivatives/fmriprep_1.4.0/fmriprep/sub-%s/func/sub-%s_task-machinegame_run-%s_desc-confounds_regressors.tsv"%(subnum, subnum, runnum)), sep='\t')
            formatted_confounds = get_confounds(cur_confounds)

            #define GLM parmeters
            fmri_glm = FirstLevelModel(t_r=cur_img_tr,
                                   noise_model='ar1',
                                   standardize=False,
                                   hrf_model='spm + derivative',
                                   drift_model='cosine',
                                   smoothing_fwhm=5,
                                   mask='%s/derivatives/fmriprep_1.4.0/fmriprep/sub-%s/func/sub-%s_task-machinegame_run-%s_space-MNI152NLin2009cAsym_desc-brain_mask.nii.gz'%(data_loc, subnum, subnum, runnum))

            #fit glm to run image using run events
            print("***********************************************")
            print("Running GLM for sub-%s run-%s"%(subnum, runnum))
            print("***********************************************")
            fmri_glm = fmri_glm.fit(fmri_img, events = formatted_events, confounds = formatted_confounds)

            print("***********************************************")
            print("Saving GLM for sub-%s run-%s"%(subnum, runnum))
            print("***********************************************")
            if pe:
                f = open('%s/sub-%s_run-%s_l1_%s_glm.pkl' %(out_path,subnum, runnum, 'pe'), 'wb')
            else:
                f = open('%s/sub-%s_run-%s_l1_glm.pkl' %(out_path,subnum, runnum), 'wb')
            pickle.dump(fmri_glm, f)
            f.close()

            #Save design matrix
            design_matrix = fmri_glm.design_matrices_[0]
            print("***********************************************")
            print("Saving design matrix for sub-%s run-%s"%(subnum, runnum))
            print("***********************************************")
            if pe:
                design_matrix.to_csv(os.path.join(out_path, 'sub-%s_run-%s_level1_%s_design_matrix.csv' %(subnum, runnum, 'pe')))
            else:
                design_matrix.to_csv(os.path.join(out_path, 'sub-%s_run-%s_level1_design_matrix.csv' %(subnum, runnum)))

            print("***********************************************")
            print("Running contrasts for sub-%s run-%s"%(subnum, runnum))
            print("***********************************************")
            contrasts = make_contrasts(design_matrix, pe, ev)
            for index, (contrast_id, contrast_val) in enumerate(contrasts.items()):
                z_map = fmri_glm.compute_contrast(contrast_val, output_type='z_score')
                nib.save(z_map, '%s/sub-%s_run-%s_%s.nii.gz'%(contrasts_path, subnum, runnum, contrast_id))
                if beta:
                    b_map = fmri_glm.compute_contrast(contrast_val, output_type='effect_size')
                    nib.save(b_map, '%s/sub-%s_run-%s_%s_betas.nii.gz'%(contrasts_path, subnum, runnum, contrast_id))
            print("***********************************************")
            print("Done saving contrasts for sub-%s run-%s"%(subnum, runnum))
            print("***********************************************")

        else:
            print("***********************************************")
            print("No pre-processed BOLD found for sub-%s run-%s"%(subnum, runnum))
            print("***********************************************")

def run_ppi_level1(subnum, out_path, beta, seed_name, tasks):

    if seed_name == "l_vstr":
        seed_coords = [(-12, 12, -6)]
    if seed_name == "r_vstr":
        seed_coords = [(12, 10, -6)]
    if seed_name == "vmpfc":
        seed_coords = [(2, 46, -8)]
    if seed_name == "l_ains":
        seed_coords = [(-30, 22, -6)]
    if seed_name == "r_ains":
        seed_coords = [(32, 20, -6)]
    if seed_name == "pcc":
        seed_coords = [(-4, -30, 36)]
    if seed_name == "acc":
        seed_coords = [(-2, 28, 28)]
    if seed_name == "pre_sma":
        seed_coords = [(-2, 16, 46)]

    data_loc = os.environ['DATA_LOC']

    if not os.path.exists(out_path):
        os.makedirs(out_path)

    contrasts_path = "%s/contrasts"%(out_path)
    if not os.path.exists(contrasts_path):
        os.makedirs(contrasts_path)

    run_files = glob.glob(os.path.join(data_loc,"derivatives/fmriprep_1.4.0/fmriprep/sub-*/func/sub-*_task-machinegame_run-*_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"))
    sub_runs = [x for x in run_files if subnum in x]
    sub_runs.sort()

    for cur_run in sub_runs:

        runnum = re.findall('\d+', os.path.basename(cur_run))[1]

        #read in preproc_bold for that run
        cur_img = nib.load(cur_run)
        cur_img_tr = cur_img.header['pixdim'][4]

        fmri_glm = FirstLevelModel(t_r=cur_img_tr,
                               noise_model='ar1',
                               standardize=False,
                               hrf_model='spm + derivative',
                               drift_model='cosine',
                               smoothing_fwhm=5,
                               mask='%s/derivatives/fmriprep_1.4.0/fmriprep/sub-%s/func/sub-%s_task-machinegame_run-%s_space-MNI152NLin2009cAsym_desc-brain_mask.nii.gz'%(data_loc, subnum, subnum, runnum))

        level_1_design = pd.read_csv('%s/derivatives/nistats/level_1/sub-%s/sub-%s_run-%s_level1_pe_design_matrix.csv'%(data_loc, subnum, subnum, runnum))
        formatted_confounds = get_confounds(pd.read_csv(os.path.join(data_loc,'derivatives/fmriprep_1.4.0/fmriprep/sub-%s/func/sub-%s_task-machinegame_run-%s_desc-confounds_regressors.tsv'%(subnum, subnum, runnum)), sep='\\t'))
        seed_ts = get_seed_timeseries(func_file=cur_run, confounds=formatted_confounds, seed=seed_coords)
        #normalize
        seed_ts = (seed_ts - seed_ts.mean()) / (seed_ts.max() - seed_ts.min())
        ppi_design = level_1_design.copy()
        ppi_design['seed'] = seed_ts

        for cur_task in tasks:
            cur_task = [cur_task]
            cur_task.append('seed')
            ppi_design['ppi_%s'%(cur_task[0])] = ppi_design[cur_task].apply(np.prod, axis=1)

        #fit glm to run image using run events
        print("***********************************************")
        print("Running PPI for sub-%s run-%s"%(subnum, runnum))
        print("***********************************************")
        fmri_glm = fmri_glm.fit(cur_run, design_matrices = ppi_design)

        print("***********************************************")
        print("Running contrasts for sub-%s run-%s"%(subnum, runnum))
        print("***********************************************")
        contrasts = make_contrasts(ppi_design, pe=False, ev=False, ppi=True)
        for index, (contrast_id, contrast_val) in enumerate(contrasts.items()):
            z_map = fmri_glm.compute_contrast(contrast_val, output_type='z_score')
            nib.save(z_map, '%s/sub-%s_run-%s_%s.nii.gz'%(contrasts_path, subnum, runnum, contrast_id))
            if beta:
                b_map = fmri_glm.compute_contrast(contrast_val, output_type='effect_size')
                nib.save(b_map, '%s/sub-%s_run-%s_%s_betas.nii.gz'%(contrasts_path, subnum, runnum, contrast_id))
        print("***********************************************")
        print("Done saving contrasts for sub-%s run-%s"%(subnum, runnum))
        print("***********************************************")
