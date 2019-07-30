#!/home/groups/russpold/software/miniconda/envs/fmri/bin/python
from argparse import ArgumentParser
import glob
import os
import sys
import pandas as pd
import nibabel as nib
from nilearn.image import mean_img
import numpy as np
import re
sys.path.append(os.path.join(os.environ['SERVER_SCRIPTS'],'nistats/level_1'))
from level_1_utils import get_confounds
from get_seed_to_vox_corrs import get_seed_to_vox_corrs

#Usage = ./get_ts_cors.py -s 100003 -c "l_vstr"

parser = ArgumentParser()
parser.add_argument("-s", "--subnum", help="subject number")
parser.add_argument("-c", "--seed_name", help="seed name coordinates", default = "l_vstr")
args = parser.parse_args()
subnum = args.subnum
seed_name = args.seed_name
data_loc = os.environ['DATA_LOC']

out_path = '%s/derivatives/func_con/sub-%s/'%(data_loc, subnum)
if not os.path.exists(out_path):
    os.makedirs(out_path)

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

func_files = glob.glob('%s/derivatives/fmriprep_1.4.0/fmriprep/sub-%s/func/sub-%s_task-machinegame_run-*_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz' %(data_loc, subnum, subnum))
func_files.sort()

for func_filename in func_files:
    runnum = re.findall('\d+', os.path.basename(func_filename))[1]
    formatted_confounds = get_confounds(pd.read_csv(os.path.join(data_loc,'derivatives/fmriprep_1.4.0/fmriprep/sub-%s/func/sub-%s_task-machinegame_run-%s_desc-confounds_regressors.tsv'%(subnum, subnum, runnum)), sep='\\t'))
    seed_to_vox_corr_img = get_seed_to_vox_corrs(func_file=func_filename, confounds = formatted_confounds, seed=seed_coords)
    #save each run image
    nib.save(seed_to_vox_corr_img, '%s/sub-%s_run-%s_%s_cor_img.nii.gz'%(out_path, subnum, runnum, seed_name))
    print("***********************************************")
    print("Done saving cor image for sub-%s run-%s for %s"%(subnum, runnum, seed_name))
    print("***********************************************")

#make average subject image
run_cor_imgs = glob.glob('%s/sub-%s_run-*_%s_cor_img.nii.gz'%(out_path, subnum, seed_name))
mean_cor_img = mean_img(run_cor_imgs)
nib.save(mean_cor_img, '%s/sub-%s_run-ave_%s_cor_img.nii.gz'%(out_path, subnum, seed_name))
print("***********************************************")
print("Done saving average cor image for sub-%s for %s"%(subnum, seed_name))
print("***********************************************")
