import glob
import nibabel as nib
from nistats.second_level_model import SecondLevelModel
import numpy as np
import os
import pandas as pd
import pickle
import re
from argparse import ArgumentParser

#Usage: python level_2.py -s SUBNUM -pe

parser = ArgumentParser()
parser.add_argument("-s", "--subnum", help="subject number")
parser.add_argument("-pe", "--pred_err", help="use prediction error regressor", default= True)
args = parser.parse_args()
subnum = args.subnum
pe = args.pred_err
data_loc = os.environ['DATA_LOC']

in_path = "%s/derivatives/nistats/level_1/sub-%s/contrasts"%(data_loc,subnum)

out_path = "%s/derivatives/nistats/level_2/sub-%s"%(data_loc,subnum)
if not os.path.exists(out_path):
    os.mkdir(out_path)

contrasts_path = "%s/contrasts"%(out_path)
if not os.path.exists(contrasts_path):
    os.mkdir(contrasts_path)

sub_contrasts = os.listdir(in_path)

if pe:
    contrasts = ['m1.', 'm2.', 'm3.', 'm4.', 'm1_rt', 'm2_rt', 'm3_rt', 'm4_rt', 'hpe', 'lpe', 'junk', 'task_on', 'rt']
else:
    contrasts = ['m1.', 'm2.', 'm3.', 'm4.', 'm1_rt', 'm2_rt', 'm3_rt', 'm4_rt', 'gain.', 'loss.', 'junk', 'task_on', 'rt', 'gain-loss', 'loss-gain']

for c in contrasts:
    second_level_input = [os.path.join(in_path,x) for x in sub_contrasts if c in x]
    design_matrix = pd.DataFrame([1] * len(second_level_input), columns=['intercept'])
    model = SecondLevelModel(smoothing_fwhm=5.0)

    c = re.sub("\.","",c)

    if len(second_level_input)>1:
        print("***********************************************")
        print("Running GLM for sub-%s contrast %s"%(subnum, c))
        print("***********************************************")
        model = model.fit(second_level_input, design_matrix=design_matrix)

        print("***********************************************")
        print("Saving GLM for sub-%s contrast %s"%(subnum, c))
        print("***********************************************")
        f = open('%s/sub-%s_%s_l2_glm.pkl' %(out_path,subnum, c), 'wb')
        pickle.dump(model, f)
        f.close()

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
