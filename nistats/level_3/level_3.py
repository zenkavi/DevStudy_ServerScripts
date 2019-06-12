import glob
import nibabel as nib
from nilearn.image import concat_imgs, smooth_img
from nistats.second_level_model import SecondLevelModel
import numpy as np
import os
import pandas as pd
import pickle
import re
from argparse import ArgumentParser

#Usage: python level_3.py -m MNUM -r REG --runstats

parser = ArgumentParser()
parser.add_argument("-m", "--mnum", help="model number")
parser.add_argument("-r", "--reg", help="regressor name")
parser.add_argument("--runstats", help="run GLM and save contrasts", action='store_true')
args = parser.parse_args()
mnum = args.mnum
reg = args.reg
runstats = args.runstats
if runstats == "False":
    runstats = False

data_loc = os.environ['DATA_LOC']
server_scripts = os.environ['SERVER_SCRIPTS']
in_path = "%s/derivatives/nistats/level_2/sub-*/contrasts"%(data_loc)

out_path = "%s/derivatives/nistats/level_3/%s/%s"%(data_loc,mnum,reg)
if not os.path.exists(out_path):
    os.makedirs(out_path)

contrasts_path = "%s/contrasts"%(out_path)
if not os.path.exists(contrasts_path):
    os.mkdir(contrasts_path)

if mnum != "model4":
    level2_images = glob.glob('%s/sub-*_%s.nii.gz'%(in_path, reg))
    level2_images.sort()
else:
    level2_first_half_images = glob.glob('%s/sub-*_%s_first_half.nii.gz'%(in_path, reg))
    level2_first_half_images.sort()
    level2_second_half_images = glob.glob('%s/sub-*_%s_second_half.nii.gz'%(in_path, reg))
    level2_second_half_images.sort()
    level2_first_half_images.extend(level2_second_half_images)
    level2_images = level2_first_half_images
    del level2_first_half_images, level2_second_half_images

if reg=="rt":
    exclude = ['m1', 'm2', 'm3', 'm4']
    filter_func = lambda s: not any(x in s for x in exclude)
    level2_images = [x for x in level2_images if filter_func(x)]

print("***********************************************")
print("Concatenating level 2 images for %s contrast %s"%(mnum, reg))
print("***********************************************")
smooth_l2s = []
for l in level2_images:
    smooth_l2 = smooth_img(l, 5)
    smooth_l2s.append(smooth_l2)
all_l2_images = concat_imgs(smooth_l2s, auto_resample=True)
print("***********************************************")
print("Saving level 2 images for %s contrast %s"%(mnum, reg))
print("***********************************************")
nib.save(all_l2_images, '%s/all_l2_%s_%s.nii.gz'%(out_path, mnum, reg))

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

#model1: everyone vs. baseline
if mnum == "model1":
    design_matrix = pd.DataFrame([1] * len(level2_images),columns=['intercept'])
    if not os.path.exists("%s/rand"%(out_path)):
        os.mkdir("%s/rand"%(out_path))

#model2: age group differences
if mnum == "model2":
    design_matrix = age_info[['kid', 'teen', 'adult']]
    design_matrix['intercept'] = [1] * len(level2_images)
    if not os.path.exists("%s/rand"%(out_path)):
        os.mkdir("%s/rand"%(out_path))

#model3: learners vs non-learners
if mnum == "model3":
    design_matrix = learner_info[['learner', 'non_learner']]
    design_matrix['intercept'] = [1] * len(level2_images)
    if not os.path.exists("%s/rand"%(out_path)):
        os.mkdir("%s/rand"%(out_path))

model = SecondLevelModel(smoothing_fwhm=5.0)

if runstats:
    print("***********************************************")
    print("Running GLM for %s contrast %s"%(mnum, reg))
    print("***********************************************")
    model = model.fit(level2_images, design_matrix=design_matrix)

    print("***********************************************")
    print("Saving GLM for %s contrast %s"%(mnum, reg))
    print("***********************************************")
    f = open('%s/%s_%s_glm.pkl' %(out_path,mnum,reg), 'wb')
    pickle.dump(model, f)
    f.close()

    print("***********************************************")
    print("Running contrasts for %s contrast %s"%(mnum, reg))
    print("***********************************************")
    if mnum == "model1":
        z_map = model.compute_contrast(output_type='z_score')
        nib.save(z_map, '%s/%s_%s.nii.gz'%(contrasts_path, mnum, reg))

    if mnum == "model2":
        for c in ['kid', 'teen', 'adult']:
            z_map = model.compute_contrast(c,output_type='z_score')
            nib.save(z_map, '%s/%s_%s_%s.nii.gz'%(contrasts_path, mnum, reg, c))

    if mnum == "model3":
        for c in ['learner', 'non_learner']:
            z_map = model.compute_contrast(c,output_type='z_score')
            nib.save(z_map, '%s/%s_%s_%s.nii.gz'%(contrasts_path, mnum, reg, c))

    print("***********************************************")
    print("Done saving contrast for %s contrast %s"%(mnum, reg))
    print("***********************************************")
