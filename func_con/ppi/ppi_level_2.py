#!/home/groups/russpold/software/miniconda/envs/fmri/bin/python
import glob
import math
import nibabel as nib
from nistats.second_level_model import SecondLevelModel
import numpy as np
import os
import pandas as pd
import pickle
import re
from argparse import ArgumentParser

#Usage: python level_2.py -s SUBNUM -pe -hv

parser = ArgumentParser()
parser.add_argument("-s", "--subnum", help="subject number")
args = parser.parse_args()
subnum = args.subnum
data_loc = os.environ['DATA_LOC']

in_path = "%s/derivatives/func_con/ppi/level_1/sub-%s/contrasts"%(data_loc,subnum)
out_path = "%s/derivatives/func_con/ppi/level_2/sub-%s"%(data_loc,subnum)

if not os.path.exists(out_path):
    os.mkdirs(out_path)

contrasts_path = "%s/contrasts"%(out_path)
if not os.path.exists(contrasts_path):
    os.mkdirs(contrasts_path)

sub_contrasts = os.listdir(in_path)

contrasts = ['ppi_m1_con','ppi_m2_con', 'ppi_m3_con', 'ppi_m4_con']

for c in contrasts:
    second_level_input = [os.path.join(in_path,x) for x in sub_contrasts if c in x]
    design_matrix = pd.DataFrame([1] * len(second_level_input), columns=['intercept'])
    model = SecondLevelModel(smoothing_fwhm=5.0)

    if len(second_level_input)>1:
        print("***********************************************")
        print("Running GLM for sub-%s contrast %s"%(subnum, c))
        print("***********************************************")
        model = model.fit(second_level_input, design_matrix=design_matrix)

        print("***********************************************")
        print("Running contrasts for sub-%s contrast %s"%(subnum, c))
        print("***********************************************")
        z_map = model.compute_contrast(output_type='z_score')

        nib.save(z_map, '%s/sub-%s_%s.nii.gz'%(contrasts_path, subnum, c))
        print("***********************************************")
        print("Done saving contrasts for sub-%s contrast %s"%(subnum, c))
        print("***********************************************")

    elif len(second_level_input) == 1:
        print("***********************************************")
        print("1 level 1 image found for sub-%s contrast %s"%(subnum, c))
        print("Skipping level 2 for sub-%s contrast %s"%(subnum, c))
        print("Saving level 1 for level 2 for sub-%s contrast %s"%(subnum, c))
        z_map = nib.load(second_level_input[0])
        nib.save(z_map, '%s/sub-%s_%s.nii.gz'%(contrasts_path, subnum, c))
        print("***********************************************")
    else:
        print("***********************************************")
        print("No level 1 image found for sub-%s contrast %s"%(subnum, c))
        print("***********************************************")
