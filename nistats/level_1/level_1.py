import glob
import nibabel as nib
from nistats.first_level_model import FirstLevelModel
import numpy as np
import os
import pandas as pd
import re
from argparse import ArgumentParser

#Usage: python level_1.py -s SUBNUM
#Outputs:
#WHAT DOES RANDOMISE NEED FOR LATER MULTIPLE COMPARISON CORRECTIONS?

parser = ArgumentParser()
parser.add_argument("-s", "--sub_num", help="subject number")
sub_num = args.sub_num
data_loc = os.environ['DATA_LOC']

events_files = glob.glob('%s/sub-*/func/sub-*_task-machinegame_run-*_events.tsv'%(data_loc))
events_files.sort()

out_path = "%s/derivatives/nistats/level_1/sub-%s"%(data_loc,subnum)
if not os.path.exists(out_path):
    os.mkdir(out_path)

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

    # Add more complex contrasts
    contrasts['task_on'] = (contrasts['m1'] + contrasts['m2'] + contrasts['m3'] + contrasts['m4'])
    contrasts['rt'] = (contrasts['m1_rt'] + contrasts['m2_rt'] + contrasts['m3_rt'] + contrasts['m4_rt'])
    contrasts['gain-loss'] = contrasts['gain'] - contrasts['loss']
    contrasts['loss-gain'] = contrasts['loss'] - contrasts['gain']

    return contrasts

for run_events in sub_events:

    runnum = re.findall('\d+', os.path.basename(run_events))[1]

    #fmri_img: path to preproc_bold that the model will be fit on
    fmri_img = os.path.join(data_loc,"derivatives/fmriprep_1.3.0/fmriprep/sub-%s/func/sub-%s_task-machinegame_run-%s_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"%(subnum, subnum, runnum))

    #read in preproc_bold for that run
    cur_img = nib.load(fmri_img)
    #CHANGE THIS TO CORRECT HEADER ATTRIBUTE
    cur_img_tr = cur_img.header['pixdim'][4]

    #read in events.tsv for that run

    #process events for GLM
    #events: 4 col events file for WHOLE RUN with onset, duration, trial_type, modulation
    #trial_type column:
        #m1, m2, m3, m4 - onset: stimulus_presentation onset, duration: mean_rt, modulation: 1
        #m1_rt, m2_rt, m3_rt, m4_rt - onset: stimulus_presentation, duration: mean_rt, modulation: rt-mean_rt
        #gain - onset: response onset, duration: response duration, modulation: gain-mean_gain
        #loss - onset: reponse onset, duration: response duration, modulation: loss-mean_loss
        #junk: onset: response onset, duration: response duration, modulation: 1
    #confounds:
        #6 movement + squares
        #scrubbing ?

    #define GLM parmeters
    fmri_glm = FirstLevelModel(t_r=cur_img_tr,
                           noise_model='ar1',
                           standardize=False,
                           hrf_model='spm + derivative',
                           drift_model='cosine',
                           smoothing_fwhm=5)

    #fit glm to run image using run events
    fmri_glm = fmri_glm.fit(fmri_img, events)

    #OUTPUTs:
    #Design matrix image
    design_matrix = fmri_glm.design_matrices_[0]
    plot_design_matrix(design_matrix, output_file=os.path.join(outdir, 'sub-%s_run-%s_level1_design_matrix.png' %(subnum, runnum)))

    #Design matrix itself

    #Model object that will be fed into level2s

    #Whatever randomise needs

    #Contrast zmaps

    #Whatever else Ian is saving
