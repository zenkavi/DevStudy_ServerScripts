import glob
import nibabel
import numpy as np
import os
import pandas as pd
import re
os.system('source activate fmri')
from nistats.first_level_model import FirstLevelModel
from argparse import ArgumentParser

#Usage: python level_1.py -s SUBNUM
#Outputs:
#WHAT DOES RANDOMISE NEED FOR LATER MULTIPLE COMPARISON CORRECTIONS?

parser = ArgumentParser()
parser.add_argument("-s", "--sub_num", help="subjectl number")
sub_num = args.sub_num
data_loc = os.environ['DATA_LOC']

events_files = glob.glob('%s/sub-*/func/sub-*_task-machinegame_run-*_events.tsv'%(data_loc))
events_files.sort()

out_path = "%s/derivatives/level_1/sub-"%(data_loc)

all_events = pd.DataFrame()

for cur_ef in events_files:
    df = pd.read_csv(cur_ef, sep = '\t')
    all_events = all_events.append(df, ignore_index= True)

all_events = all_events[all_events['response_time'].notnull()]
all_events.response_time = all_events.response_time/1000
mean_rt = all_events.response_time.mean()

del all_events

sub_events = [x for x in events_files if str(sub_num) in x]

def make_contrasts(design_matrix):
    """ returns a dictionary of four contrasts, given the design matrix"""

    # first generate canonical contrasts (i.e. regressors vs. baseline)
    contrast_matrix = np.eye(design_matrix.shape[1])
    contrasts = dict([(column, contrast_matrix[i])
                      for i, column in enumerate(design_matrix.columns)])

    # Add more complex contrasts
    contrasts['task_on'] = (contrasts['m1']
                          + contrasts['m2']
                          + contrasts['m3']
                          + contrasts['m4']
                          )
    contrasts['rt'] = (contrasts['m1_rt']
                          + contrasts['m2_rt']
                          + contrasts['m3_rt']
                          + contrasts['m4_rt']
                          )
    contrasts['gain-loss'] = contrasts['gain'] - contrasts['loss']
    contrasts['loss-gain'] = contrasts['loss'] + contrasts['gain']

    return contrasts

for run_events in sub_events:

    fmri_img = #PATH TO RUN BOLD

    #read in preproc_bold for that run
    cur_img = nib.load(fmri_img)
    #CHANGE THIS TO CORRECT HEADER ATTRIBUTE
    cur_img_tr = cur_img.header['...']

    #read in events.tsv for that run


    fmri_glm = FirstLevelModel(t_r=cur_img_tr,
                           noise_model='ar1',
                           standardize=False,
                           hrf_model='spm + derivative',
                           drift_model='cosine',
                           smoothing_fwhm=5)

#fmri_img: preproc_bold that the model will be fit on
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

    fmri_glm = fmri_glm.fit(fmri_img, events)

#Things to save from the model fit:
#Design matrix

    design_matrix = fmri_glm.design_matrices_[0]

    outdir = '...'
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    plot_design_matrix(design_matrix, output_file=os.path.join(outdir, 'sub-%s_run-%s_level1_design_matrix.png' %(subnum, runnum)))

#Model object that will be fed into level2s
