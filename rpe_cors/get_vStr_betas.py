#!/home/groups/russpold/software/miniconda/envs/fmri/bin/python
from argparse import ArgumentParser
import glob
import numpy as np
import nibabel as nib
import os
import pandas as pd
import re
import sys
sys.path.append(os.path.join(os.environ['SERVER_SCRIPTS'],'roi'))
from get_roi_vals import get_roi_vals

data_loc = os.environ['DATA_LOC']
server_scripts = os.environ['SERVER_SCRIPTS']

parser = ArgumentParser()
parser.add_argument("-m", "--models")
args = parser.parse_args()
models = [args.models]

if models is None:
    models = glob.glob(os.path.join(server_scripts, 'rpe_cors/pred_rpes/*.csv'))
    models = [os.path.splitext(os.path.basename(x))[0] for x in models]
    models.sort()

regions = ['l_vstr', 'r_vstr']

all_betas = pd.DataFrame()

for model in models:
    #contrast images with betas
    beta_img_paths = glob.glob('%s/derivatives/rpe_cors/%s/sub-*/contrasts/sub-*_run-*_*pe_betas.nii.gz'%(data_loc, model))
    beta_img_paths.sort()

    for region in regions:
        mask_file_name = '/oak/stanford/groups/russpold/data/ds000054/0.0.4/derivatives/rois/tpl-MNI152NLin2009cAsym_res-02_desc-brain_T1w/%s_bin.nii.gz'%(region)

        print("Getting betas for %s from %s"%(model, region))

        for cur_beta_img in beta_img_paths:
            print("Getting betas for sub-%s"%(re.findall('\d+', os.path.basename(cur_beta_img))[0]))
            cur_betas = pd.DataFrame()
            cur_betas["beta"] = get_roi_vals(mask_file_name, cur_beta_img)
            cur_betas["sub_num"] = re.findall('\d+', os.path.basename(cur_beta_img))[0] #take from cur_beta_img
            cur_betas["run_num"] = re.findall('\d+', os.path.basename(cur_beta_img))[1] #take from cur_beta_img
            cur_betas["pe_type"] = os.path.basename(cur_beta_img).split("_")[2] #take from cur_beta_img
            cur_betas["roi"] = region
            cur_betas["model"] = model
            all_betas = all_betas.append(cur_betas, ignore_index= True)

if len(models)==12:
    all_betas.to_csv('%s/derivatives/rpe_cors/all_vstr_pe_betas.csv'%(data_loc))
else:
    all_betas.to_csv('%s/derivatives/rpe_cors/%s_vstr_pe_betas.csv'%(data_loc, models[0]))
