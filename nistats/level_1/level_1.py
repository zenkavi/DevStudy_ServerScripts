import glob
import nibabel as nib
from nistats.first_level_model import FirstLevelModel
import numpy as np
import os
import pandas as pd
import pickle
import re
from argparse import ArgumentParser

#Usage: python level_1.py -s SUBNUM

parser = ArgumentParser()
parser.add_argument("-s", "--subnum", help="subject number")
args = parser.parse_args()
subnum = args.subnum
data_loc = os.environ['DATA_LOC']

events_files = glob.glob('%s/sub-*/func/sub-*_task-machinegame_run-*_events.tsv'%(data_loc))
events_files.sort()

out_path = "%s/derivatives/nistats/level_1/sub-%s"%(data_loc,subnum)
if not os.path.exists(out_path):
    os.mkdir(out_path)

contrasts_path = "%s/contrasts"%(out_path)
if not os.path.exists(contrasts_path):
    os.mkdir(contrasts_path)

all_events = pd.DataFrame()

for cur_ef in events_files:
    df = pd.read_csv(cur_ef, sep = '\t')
    all_events = all_events.append(df, ignore_index= True)

all_events = all_events[all_events['response_time'].notnull()]
all_events.response_time = all_events.response_time/1000
mean_rt = all_events.response_time.mean()

del all_events

sub_events = [x for x in events_files if subnum in x]

def make_contrasts(design_matrix):
        # first generate canonical contrasts (i.e. regressors vs. baseline)
    contrast_matrix = np.eye(design_matrix.shape[1])
    contrasts = dict([(column, contrast_matrix[i])
                      for i, column in enumerate(design_matrix.columns)])
    contrasts = {
        'm1': contrasts['m1'],
        'm2': contrasts['m2'],
        'm3': contrasts['m3'],
        'm4': contrasts['m4'],
        'm1_rt': contrasts['m1_rt'],
        'm2_rt': contrasts['m2_rt'],
        'm3_rt': contrasts['m3_rt'],
        'm4_rt': contrasts['m4_rt'],
        'gain': contrasts['gain'],
        'loss': contrasts['loss'],
        'junk': contrasts['junk'],
        'task_on': (contrasts['m1'] + contrasts['m2'] + contrasts['m3'] + contrasts['m4']),
        'rt': (contrasts['m1_rt'] + contrasts['m2_rt'] + contrasts['m3_rt'] + contrasts['m4_rt']),
        'gain-loss' : contrasts['gain'] - contrasts['loss'],
        'loss-gain' : contrasts['loss'] - contrasts['gain']}

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

for run_events in sub_events:

    runnum = re.findall('\d+', os.path.basename(run_events))[1]

    exists = os.path.isfile(os.path.join(data_loc,"derivatives/fmriprep_1.3.0/fmriprep/sub-%s/func/sub-%s_task-machinegame_run-%s_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"%(subnum, subnum, runnum)))

    if exists:

        #fmri_img: path to preproc_bold that the model will be fit on
        fmri_img = os.path.join(data_loc,"derivatives/fmriprep_1.3.0/fmriprep/sub-%s/func/sub-%s_task-machinegame_run-%s_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"%(subnum, subnum, runnum))

        #read in preproc_bold for that run
        cur_img = nib.load(fmri_img)
        cur_img_tr = cur_img.header['pixdim'][4]

        #read in events.tsv for that run
        cur_events = pd.read_csv(run_events, sep = '\t')

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
        #cur_events['gain_loss'] = np.where(cur_events.points_earned>0, 1, np.where(cur_events.points_earned<0, -1, 0))
        #po = cur_events.points_earned
        #cur_events.points_earned = np.where(po == 5, 0.01, np.where(po == 495, 0.99, np.where(po == 10, 0.02, np.where(po == 100, 0.20, np.where(po == -5, -0.01, np.where(po == -495, -0.99, np.where(po == -10, -0.02, np.where(po == -100, -0.20, 0))))))))

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
        cond_junk = cur_events.query('response == 0')[['onset', 'duration']]
        cond_junk['modulation'] = 1
        cond_junk['trial_type'] = "junk"

        formatted_events = pd.concat([cond_m1, cond_m2, cond_m3, cond_m4, cond_m1_rt, cond_m2_rt, cond_m3_rt, cond_m4_rt, cond_gain, cond_loss, cond_junk], ignore_index=True)

        formatted_events = formatted_events.sort_values(by='onset')

        formatted_events = formatted_events[['onset', 'duration', 'trial_type', 'modulation']].reset_index(drop=True)

        #process confounds
        #['X','Y','Z','RotX','RotY','RotY','<-firsttemporalderivative','stdDVARs','FD','scrub']
        cur_confounds = pd.read_csv(os.path.join(data_loc,"derivatives/fmriprep_1.3.0/fmriprep/sub-%s/func/sub-%s_task-machinegame_run-%s_desc-confounds_regressors.tsv"%(subnum, subnum, runnum)), sep='\t')

        formatted_confounds = cur_confounds[['trans_x', 'trans_y', 'trans_z', 'rot_x', 'rot_y', 'rot_z']]
        add_transform(formatted_confounds, type="sq")
        add_transform(formatted_confounds, type="td")
        formatted_confounds[['std_dvars', 'framewise_displacement']] = cur_confounds[['std_dvars', 'framewise_displacement']]
        formatted_confounds['std_dvars'].iloc[0] = 0
        formatted_confounds['framewise_displacement'].iloc[0] = 0
        formatted_confounds['scrub'] = np.where(formatted_confounds.framewise_displacement>0.5,1,0)

        #define GLM parmeters
        fmri_glm = FirstLevelModel(t_r=cur_img_tr,
                               noise_model='ar1',
                               standardize=False,
                               hrf_model='spm + derivative',
                               drift_model='cosine',
                               smoothing_fwhm=5,
                               mask='%s/derivatives/fmriprep_1.3.0/fmriprep/sub-%s/func/sub-%s_task-machinegame_run-%s_space-MNI152NLin2009cAsym_desc-brain_mask.nii.gz'%(data_loc, subnum, subnum, runnum))

        #fit glm to run image using run events
        print("***********************************************")
        print("Running GLM for sub-%s run-%s"%(subnum, runnum))
        print("***********************************************")
        fmri_glm = fmri_glm.fit(fmri_img, events = formatted_events, confounds = formatted_confounds)

        print("***********************************************")
        print("Saving GLM for sub-%s run-%s"%(subnum, runnum))
        print("***********************************************")
        f = open('%s/sub-%s_run-%s_l1_glm.pkl' %(out_path,subnum, runnum), 'wb')
        pickle.dump(fmri_glm, f)
        f.close()

        #Save design matrix
        design_matrix = fmri_glm.design_matrices_[0]
        print("***********************************************")
        print("Saving design matrix for sub-%s run-%s"%(subnum, runnum))
        print("***********************************************")
        design_matrix.to_csv(os.path.join(out_path, 'sub-%s_run-%s_level1_design_matrix.csv' %(subnum, runnum)))

        print("***********************************************")
        print("Running contrasts for sub-%s run-%s"%(subnum, runnum))
        print("***********************************************")
        contrasts = make_contrasts(design_matrix)
        for index, (contrast_id, contrast_val) in enumerate(contrasts.items()):
            z_map = fmri_glm.compute_contrast(contrast_val, output_type='z_score')
            nib.save(z_map, '%s/sub-%s_run-%s_%s.nii.gz'%(contrasts_path, subnum, runnum, contrast_id))
        print("***********************************************")
        print("Done saving contrasts for sub-%s run-%s"%(subnum, runnum))
        print("***********************************************")

    else:
        print("***********************************************")
        print("No pre-processed BOLD found for sub-%s run-%s"%(subnum, runnum))
        print("***********************************************")

    #OUTPUTs:
    #Whatever randomise needs: group level nifti, design matrix, contrast file
    #group level nifti: filtered_func_data for one sample test
