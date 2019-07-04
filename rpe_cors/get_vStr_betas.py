#!/home/groups/russpold/software/miniconda/envs/fmri/bin/python
import glob
import numpy as np
import nibabel as nib
import nilearn.plotting
import os
import pandas as pd
import re

data_loc = os.environ['DATA_LOC']
server_scripts = os.environ['SERVER_SCRIPTS']

#contrasts = hpe, lpe, pe

regions = ['l_vstr', 'r_vstr']

models = glob.glob(os.path.join(server_scripts, 'rpe_cors/pred_rpes/*.csv'))
models = [os.path.splitext(os.path.basename(x))[0] for x in models]

all_betas = pd.DataFrame()

for model in models:
    #contrast images with betas
    beta_img_paths = glob.glob('%s/derivatives/rpe_cors/%s/sub-*/contrasts/sub-*_run-*_*pe_betas.nii.gz'%(data_loc, model))

    for region in regions:
        #check for matching dimensions
        #resample mask if they don't match
        tmp_img_file_name = beta_img_paths[0]
        tmp_img = nib.load(tmp_img_file_name)
        mask_file_name = '/oak/stanford/groups/russpold/data/ds000054/0.0.4/derivatives/rois/tpl-MNI152NLin2009cAsym_res-01_desc-brain_T1w/%s_bin.nii.gz'%(region)
        mask = nib.load(mask_file_name)
        tmp_img_data = tmp_img.get_fdata()
        mask_data = mask.get_fdata()
        if tmp_img_data.shape != mask_data.shape:
            mask = nilearn.image.resample_to_img(mask, tmp_img)
            mask_data = mask.get_fdata()
            #binarize resampled mask data
            mask_data = np.where(mask_data >0.1,1,0)
            mask = nilearn.image.new_img_like(tmp_img, mask_data)

            for cur_beta_img in beta_img_paths:
                img_data = nib.load(cur_beta_img).get_fdata()
                roi_data = np.where(mask_data == 1,img_data,0)
                roi_data = roi_data[roi_data != 0]
                cur_betas = pd.DataFrame()
                cur_betas["beta"] = roi_data
                cur_betas["sub_num"] = re.findall('\d+', os.path.basename(cur_beta_img))[0] #take from cur_beta_img
                cur_betas["run_num"] = re.findall('\d+', os.path.basename(cur_beta_img))[1] #take from cur_beta_img
                cur_betas["pe_type"] = os.path.basename(cur_beta_img).split("_")[2] #take from cur_beta_img
                cur_betas["roi"] = region
                cur_betas["model"] = model
                all_betas = all_betas.append(cur_betas, ignore_index= True)

all_betas.to_csv('%s/derivatives/rpe_cors/all_vstr_pe_betas.csv'%(data_loc))
