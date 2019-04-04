import glob
import nibabel as nib
from nilearn.image import concat_imgs
from nistats.second_level_model import SecondLevelModel
import numpy as np
import os
import pandas as pd
import pickle
import re
from argparse import ArgumentParser

#Usage: python level_3.py -m MNUM -r REG -s True

parser = ArgumentParser()
parser.add_argument("-m", "--mnum", help="model number")
parser.add_argument("-r", "--reg", help="regressor name")
parser.add_argument("-s", "--runstats", help="run GLM and save contrasts", default=True)
args = parser.parse_args()
mnum = args.mnum
reg = args.reg
runstats = args.runstats

data_loc = os.environ['DATA_LOC']
in_path = "%s/derivatives/nistats/level_2/sub-*/contrasts"%(data_loc)

out_path = "%s/derivatives/nistats/level_3/%s/%s"%(data_loc,mnum,reg)
if not os.path.exists(out_path):
    os.makedirs(out_path)

contrasts_path = "%s/contrasts"%(out_path)
if not os.path.exists(contrasts_path):
    os.mkdir(contrasts_path)

level2_images = glob.glob('%s/sub-*_%s.nii.gz'%(in_path, reg))
level2_images.sort()
print("***********************************************")
print("Concatenating level 2 images for %s contrast %s"%(mnum, reg))
print("***********************************************")
all_l2_images = concat_imgs(level2_images)
print("***********************************************")
print("Saving level 2 images for %s contrast %s"%(mnum, reg))
print("***********************************************")
nib.save(all_l2_images, '%s/all_l2_%s_%s.nii.gz'%(out_path, mnum, reg))

age_info = pd.read_csv('%s/participants.tsv'%(data_loc), sep='\t')
age_info['kid'] = np.where(age_info['age']<13,1,0)
age_info['teen'] = np.where((age_info['age']>12) & (age_info['age']<19),1,0)
age_info['adult'] = np.where(age_info['age']>18,1,0)
age_info = age_info.sort_values(by=['participant_id']).reset_index(drop=True)
subs = [os.path.basename(x).split("_")[0] for x in level2_images]
age_info = age_info[age_info.participant_id.isin(subs)].reset_index(drop=True)

#model1: everyone vs. baseline
if mnum == "model1":
    design_matrix = pd.DataFrame([1] * len(level2_images),columns=['intercept'])

#model2: age group differences
if mnum == "model2":
    design_matrix = age_info[['kid', 'teen', 'adult']]
    design_matrix['intercept'] = [1] * len(level2_images)
    if not os.path.exists("%s/rand_anova"%(out_path)):
        os.mkdir("%s/rand_anova"%(out_path))

#model3: continuous age differences
if mnum == "model3":
    design_matrix = age_info[['age']]
    design_matrix['intercept'] = [1] * len(level2_images)

replacements = {"NPTS": str(design_matrix.shape[0])}
with open("%s/derivatives/nistats/level_3/%s/design_mat_header.mat"%(data_loc, mnum)) as infile:
  with open('%s/%s_%s.mat'%(out_path, mnum, reg), 'w') as outfile:
      for line in infile:
        for src, target in replacements.items():
          line = line.replace(src, target)
        outfile.write(line)
f=open('%s/%s_%s.mat'%(out_path, mnum, reg),'ab')
np.savetxt(f,design_matrix.values, fmt='%1.3f')
f.close()
with open("%s/derivatives/nistats/level_3/%s/design_grp_header.grp"%(data_loc, mnum)) as infile:
  with open('%s/%s_%s.grp'%(out_path, mnum, reg), 'w') as outfile:
      for line in infile:
        for src, target in replacements.items():
          line = line.replace(src, target)
        outfile.write(line)
f=open('%s/%s_%s.grp'%(out_path, mnum, reg),'ab')
np.savetxt(f,[1] * len(level2_images),fmt='%1.0f')
f.close()

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
        z_map = model.compute_contrast('age',output_type='z_score')
        nib.save(z_map, '%s/%s_%s_age.nii.gz'%(contrasts_path, mnum, reg))

    print("***********************************************")
    print("Done saving contrast for %s contrast %s"%(mnum, reg))
    print("***********************************************")
