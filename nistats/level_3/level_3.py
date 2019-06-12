#!/home/groups/russpold/software/miniconda/envs/fmri/bin/python
from argparse import ArgumentParser
import glob
import nibabel as nib
from nilearn.image import concat_imgs, smooth_img, mean_img, math_img, resample_to_img
from  nipype.interfaces import fsl
from nipype.caching import Memory
mem = Memory(base_dir='.')
import numpy as np
import os
import pandas as pd
import pickle
import re
import save_randomise
randomise = mem.cache(fsl.Randomise)

#Usage: python level_3.py -m MNUM -r REG

parser = ArgumentParser()
parser.add_argument("-m", "--mnum", help="model number")
parser.add_argument("-r", "--reg", help="regressor name")
parser.add_argument("-tf", "--tfce", help="tfce", default='store_true')
parser.add_argument("-c", "--c_thresh", help="cluster_threshold", default=3)
parser.add_argument("-np", "--num_perm", help="number of permutations", default=1000)
parser.add_argument("-vs", "--var_smooth", help="variance smoothing", default=5)
args = parser.parse_args()
mnum = args.mnum
reg = args.reg
if mnum == "model1":
    one = True
c_thresh = int(args.c_thresh)
num_perm = int(args.num_perm)
var_smooth = int(args.var_smooth)

data_loc = os.environ['DATA_LOC']
server_scripts = os.environ['SERVER_SCRIPTS']
l2_in_path = "%s/derivatives/nistats/level_2/sub-*/contrasts"%(data_loc)
l3_in_path = "%s/derivatives/nistats/level_3/%s/%s"%(data_loc, mnum, reg)

out_path = "%s/derivatives/nistats/level_3/%s/%s"%(data_loc,mnum,reg)
if not os.path.exists(out_path):
    os.makedirs(out_path)

if mnum != "model4":
    level2_images = glob.glob('%s/sub-*_%s.nii.gz'%(l2_in_path, reg))
    level2_images.sort()
else:
    level2_first_half_images = glob.glob('%s/sub-*_%s_first_half.nii.gz'%(l2_in_path, reg))
    level2_first_half_images.sort()
    level2_second_half_images = glob.glob('%s/sub-*_%s_second_half.nii.gz'%(l2_in_path, reg))
    level2_second_half_images.sort()
    level2_first_half_images.extend(level2_second_half_images)
    level2_images = level2_first_half_images
    del level2_first_half_images, level2_second_half_images

if reg=="rt":
    exclude = ['m1', 'm2', 'm3', 'm4']
    filter_func = lambda s: not any(x in s for x in exclude)
    level2_images = [x for x in level2_images if filter_func(x)]

print("***********************************************")
print("Concatenating level 2 images for %s regressor %s"%(mnum, reg))
print("***********************************************")
smooth_l2s = []
for l in level2_images:
    smooth_l2 = smooth_img(l, 5)
    smooth_l2s.append(smooth_l2)
all_l2_images = concat_imgs(smooth_l2s, auto_resample=True)
print("***********************************************")
print("Saving level 2 images for %s regressor %s"%(mnum, reg))
print("***********************************************")
nib.save(all_l2_images, '%s/all_l2_%s_%s.nii.gz'%(out_path, mnum, reg))

if mnum == "model1":
    binaryMaths = mem.cache(fsl.BinaryMaths)
    print("***********************************************")
    print("Saving negative level 2 images for %s regressor %s"%(mnum, reg))
    print("***********************************************")
    binaryMaths(in_file='%s/all_l2_%s_%s.nii.gz'%(out_path, mnum, reg),
                operation = "mul",
                operand_value = -1,
                out_file = '%s/neg_all_l2_%s_%s.nii.gz'%(out_path, mnum, reg))

print("***********************************************")
print("Making group_mask")
print("***********************************************")
brainmasks = glob.glob("%s/derivatives/fmriprep_1.3.0/fmriprep/sub-*/func/*brain_mask.nii*"%(data_loc))
mean_mask = mean_img(brainmasks)
group_mask = math_img("a>=0.95", a=mean_mask)
group_mask = resample_to_img(group_mask, all_l2_images, interpolation='nearest')
group_mask.to_filename("%s/group_mask_%s_%s.nii.gz"%(out_path,mnum,reg))
print("***********************************************")
print("Group mask saved for: %s %s"%(mnum, reg))
print("***********************************************")

print("***********************************************")
print("Making design matrix")
print("***********************************************")
# Read in group info for models 2 and 3
age_info = pd.read_csv('%s/participants.tsv'%(data_loc), sep='\t')
age_info['kid'] = np.where(age_info['age']<13,1,0)
age_info['teen'] = np.where((age_info['age']>12) & (age_info['age']<19),1,0)
age_info['adult'] = np.where(age_info['age']>18,1,0)
age_info = age_info.sort_values(by=['participant_id']).reset_index(drop=True)
subs = [os.path.basename(x).split("_")[0] for x in level2_images]
age_info = age_info[age_info.participant_id.isin(subs)].reset_index(drop=True)

learner_info = pd.read_csv('%s/nistats/level_3/learner_info.csv'%(server_scripts))
learner_info = learner_info[learner_info.Sub_id.isin(subs)].reset_index(drop=True)

#model2: age group differences
if mnum == "model2":
    design_matrix = age_info[['kid', 'teen', 'adult']]
    #design_matrix['intercept'] = [1] * len(level2_images)
    deshdr="""/NumWaves	3
/NumPoints	74
/PPheights		1.000000e+00	1.000000e+00	1.000000e+00

/Matrix
    """

#model3: learners vs non-learners
#Design and contrast matrices based on https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/GLM#Two-Group_Difference_.28Two-Sample_Unpaired_T-Test.29
if mnum == "model3":
    design_matrix = learner_info[['learner', 'non_learner']]
    #design_matrix['intercept'] = [1] * len(level2_images)
    deshdr="""/NumWaves	2
/NumPoints	74
/PPheights		1.000000e+00	1.000000e+00

/Matrix
    """

print("***********************************************")
print("Saving design matrix")
print("***********************************************")
if mnum != "model1":
    np.savetxt('%s/%s_%s_design.mat'%(l3_in_path, mnum, reg),design_matrix.values,fmt='%1.0f',header=deshdr,comments='')

print("***********************************************")
print("Beginning randomise")
print("***********************************************")
if mnum == "model1":
    randomise_results = randomise(in_file="%s/all_l2_%s_%s.nii.gz"%(l3_in_path, mnum, reg),
                              mask= "%s/group_mask_%s_%s.nii.gz"%(l3_in_path, mnum, reg),
                              one_sample_group_mean=one,
                              tfce=tfce,
                              c_thresh = c_thresh,
                              vox_p_values=True,
                              num_perm=num_perm,
                              var_smooth = var_smooth)
    save_randomise(randomise_results, l3_in_path, mnum, reg)

    randomise_results = randomise(in_file="%s/neg_all_l2_%s_%s.nii.gz"%(l3_in_path, mnum, reg),
                              mask= "%s/group_mask_%s_%s.nii.gz"%(l3_in_path, mnum, reg),
                              one_sample_group_mean=one,
                              tfce=tfce,
                              c_thresh = c_thresh,
                              vox_p_values=True,
                              num_perm=num_perm,
                              var_smooth = var_smooth)
    save_randomise(randomise_results, l3_in_path, mnum+'_neg', reg)

if mnum == "model2":
    randomise_results = randomise(in_file="%s/all_l2_%s_%s.nii.gz"%(l3_in_path, mnum, reg),
                              mask= "%s/group_mask_%s_%s.nii.gz"%(l3_in_path, mnum, reg),
                              design_mat = "%s/%s_%s_design.mat"%(l3_in_path, mnum, reg),
                              tcon="%s/derivatives/nistats/level_3/%s/%s_design.con"%(data_loc, mnum, mnum),
                              fcon="%s/derivatives/nistats/level_3/%s/%s_design.fts"%(data_loc, mnum, mnum),
                              tfce=tfce,
                              c_thresh = c_thresh,
                              vox_p_values=True,
                              num_perm=num_perm,
                              var_smooth = var_smooth)
    save_randomise(randomise_results, l3_in_path, mnum, reg)

if mnum == "model3":
    randomise_results = randomise(in_file="%s/all_l2_%s_%s.nii.gz"%(l3_in_path, mnum, reg),
                              mask= "%s/group_mask_%s_%s.nii.gz"%(l3_in_path, mnum, reg),
                              design_mat = "%s/%s_%s_design.mat"%(l3_in_path, mnum, reg),
                              tcon="%s/derivatives/nistats/level_3/%s/%s_design.con"%(data_loc, mnum, mnum),
                              tfce=tfce,
                              c_thresh = c_thresh,
                              vox_p_values=True,
                              num_perm=num_perm,
                              var_smooth = var_smooth)
    save_randomise(randomise_results, l3_in_path, mnum, reg)

if mnum == "model4":
    randomise_results = randomise(in_file="%s/all_l2_%s_%s.nii.gz"%(l3_in_path, mnum, reg),
                              mask= "%s/group_mask_%s_%s.nii.gz"%(l3_in_path, mnum, reg),
                              design_mat = "%s/%s_%s_design.mat"%(l3_in_path, mnum, reg),
                              tcon="%s/derivatives/nistats/level_3/%s/%s_design.con"%(data_loc, mnum, mnum),
                              tfce=tfce,
                              c_thresh = c_thresh,
                              vox_p_values=True,
                              num_perm=num_perm,
                              var_smooth = var_smooth)
    save_randomise(randomise_results, l3_in_path, mnum, reg)
