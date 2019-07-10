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
parser.add_argument("-o", "--out_path", default = "/oak/stanford/groups/russpold/data/ds000054/0.0.4/derivatives/rois/")
parser.add_argument("-t", "--template", default = "tpl-MNI152NLin2009cAsym_res-02_desc-brain_T1w")
parser.add_argument("-l", "--location")
parser.add_argument("-r", "--regressor")
parser.add_argument("-v", "--value")
args = parser.parse_args()
out_path = os.path.join(args.out_path, args.template)
template = args.template
location = args.location
regressor = args.regressor
value = args.value

all_vals = pd.DataFrame()

if value == "beta":
    img_paths = glob.glob('%s/derivatives/rpe_cors/exp_exp/sub-*/contrasts/sub-*_run-*_%s_betas.nii.gz'%(data_loc, regressor))
else:
    img_paths = glob.glob('%s/derivatives/rpe_cors/exp_exp/sub-*/contrasts/sub-*_run-*_%s.nii.gz'%(data_loc, regressor))
img_paths.sort()

mask_file_name = '/oak/stanford/groups/russpold/data/ds000054/0.0.4/derivatives/rois/tpl-MNI152NLin2009cAsym_res-02_desc-brain_T1w/%s_bin.nii.gz'%(location)

print("Getting betas for %s from %s"%(regressor, location))

for cur_img in img_paths:
    print("Getting values for sub-%s"%(re.findall('\d+', os.path.basename(cur_img))[0]))
    cur_vals = pd.DataFrame()
    cur_vals["value"] = get_roi_vals(mask_file_name, cur_img)
    cur_vals["value_type"] = value
    cur_vals["sub_num"] = re.findall('\d+', os.path.basename(cur_beta_img))[0] #take from cur_beta_img
    cur_vals["run_num"] = re.findall('\d+', os.path.basename(cur_beta_img))[1] #take from cur_beta_img
    cur_vals["regressor"] = regressor#take from cur_beta_img
    cur_vals["roi"] = location
    all_vals = all_vals.append(cur_vals, ignore_index= True)

all_vals.to_csv('%s/%s_%s_%ss.csv'%(out_path, regressor, location, value))
