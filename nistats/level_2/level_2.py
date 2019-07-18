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
parser.add_argument("-pe", "--pred_err", help="use prediction error regressor", default= True)
parser.add_argument("-hv", "--halves", help="compute means for separate halves", default= True)
parser.add_argument("-ev", "--exp_val", help="use expected value regressor", default= False)
args = parser.parse_args()
subnum = args.subnum
pe = args.pred_err
ev = args.exp_val
halves = args.halves
data_loc = os.environ['DATA_LOC']

if ev:
    in_path = "%s/derivatives/nistats/level_1_ev/sub-%s/contrasts"%(data_loc,subnum)
    out_path = "%s/derivatives/nistats/level_2_ev/sub-%s"%(data_loc,subnum)
else:
    in_path = "%s/derivatives/nistats/level_1/sub-%s/contrasts"%(data_loc,subnum)
    out_path = "%s/derivatives/nistats/level_2/sub-%s"%(data_loc,subnum)

if not os.path.exists(out_path):
    os.mkdir(out_path)

contrasts_path = "%s/contrasts"%(out_path)
if not os.path.exists(contrasts_path):
    os.mkdir(contrasts_path)

sub_contrasts = os.listdir(in_path)

if pe:
    if ev:
        contrasts = ['m1_ev', 'm2_ev', 'm3_ev', 'm4_ev', 'm1_rt', 'm2_rt', 'm3_rt', 'm4_rt', 'hpe', 'lpe', 'pe', 'junk', 'task_on', 'rt', 'var_sen', 'ev_sen']
    else:
        contrasts = ['m1.', 'm2.', 'm3.', 'm4.', 'm1_rt', 'm2_rt', 'm3_rt', 'm4_rt', 'hpe', 'lpe', 'pe', 'junk', 'task_on', 'rt', 'var_sen', 'ev_sen']
else:
    if ev:
        contrasts = ['m1_ev', 'm2_ev', 'm3_ev', 'm4_ev', 'm1_rt', 'm2_rt', 'm3_rt', 'm4_rt', 'gain.', 'loss.', 'junk', 'task_on', 'rt', 'gain-loss', 'loss-gain', 'var_sen', 'ev_sen']
    else:
        contrasts = ['m1.', 'm2.', 'm3.', 'm4.', 'm1_rt', 'm2_rt', 'm3_rt', 'm4_rt', 'gain.', 'loss.', 'junk', 'task_on', 'rt', 'gain-loss', 'loss-gain', 'var_sen', 'ev_sen']

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

if halves:
    for c in contrasts:
        second_level_input = [os.path.join(in_path,x) for x in sub_contrasts if c in x]
        a = [1]*math.floor(len(second_level_input)/2)
        a.extend([0]*(len(second_level_input)-len(a)))
        design_matrix = pd.DataFrame({'first_half': a, 'second_half': [1-x for x in a]})
        print("***********************************************")
        print("First half has %s runs; second half has %s runs"%(str(sum(design_matrix.first_half)), str(sum(design_matrix.second_half))))
        print("***********************************************")
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
            f = open('%s/sub-%s_%s_l2_glm_halves.pkl' %(out_path,subnum, c), 'wb')
            pickle.dump(model, f)
            f.close()

            print("***********************************************")
            print("Running contrasts for sub-%s contrast %s"%(subnum, c))
            print("***********************************************")
            for h in ['first_half', 'second_half']:
                z_map = model.compute_contrast(h,output_type='z_score')
                nib.save(z_map, '%s/sub-%s_%s_%s.nii.gz'%(contrasts_path, subnum, c, h))

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
