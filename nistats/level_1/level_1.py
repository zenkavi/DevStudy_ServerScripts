import glob
import nibabel as nib
from nistats.first_level_model import FirstLevelModel
import numpy as np
import os
import pandas as pd
import pickle
import re
from argparse import ArgumentParser
from level_1_utils import make_contrasts, add_transform, stdize, get_conditions, get_confounds
#Usage: python level_1.py -s SUBNUM -pe

parser = ArgumentParser()
parser.add_argument("-s", "--subnum", help="subject number")
parser.add_argument("-pe", "--pred_err", help="use prediction error regressor", default= True)
args = parser.parse_args()
subnum = args.subnum
pe = args.pred_err
data_loc = os.environ['DATA_LOC']
server_scripts = os.environ['SERVER_SCRIPTS']

def run_level1(subnum, out_path, pe, pe_path):
    events_files = glob.glob('%s/sub-*/func/sub-*_task-machinegame_run-*_events.tsv'%(data_loc))
    events_files.sort()

    if not os.path.exists(out_path):
        os.mkdir(out_path)

    contrasts_path = "%s/contrasts"%(out_path)
    if not os.path.exists(contrasts_path):
        os.mkdir(contrasts_path)

    all_events = pd.DataFrame()

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

    all_pes = pd.read_csv(pe_path)
    sub_pes = all_pes.query('sub_id == @subnum')

    del all_pes

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
            formatted_events = get_conditions(cur_events, runnum, mean_rt, sub_pes, pe)

            #process confounds
            #['X','Y','Z','RotX','RotY','RotY','<-firsttemporalderivative','stdDVARs','FD','scrub']
            cur_confounds = pd.read_csv(os.path.join(data_loc,"derivatives/fmriprep_1.3.0/fmriprep/sub-%s/func/sub-%s_task-machinegame_run-%s_desc-confounds_regressors.tsv"%(subnum, subnum, runnum)), sep='\t')
            formatted_confounds = get_confounds(cur_confounds)

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
            contrasts = make_contrasts(design_matrix, pe)
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

run_level1(subnum = subnum, out_path = "%s/derivatives/nistats/level_1/sub-%s"%(data_loc,subnum), pe=pe, pe_path='%s/nistats/level_1/%s.csv'%(server_scripts, pe_model))
