import glob
import nibabel as nib
from nistats.second_level_model import SecondLevelModel
import numpy as np
import os
import pandas as pd
import pickle
import re
from argparse import ArgumentParser

#Usage: python level_2.py -s SUBNUM

parser = ArgumentParser()
parser.add_argument("-s", "--subnum", help="subject number")
subnum = args.subnum
contrasts = args.contrasts
data_loc = os.environ['DATA_LOC']

level_1_models = glob.glob('%s/derivatives/nistats/level_1/sub-*/contrasts/sub-*_run-*_l1_glm.pkl'%(data_loc))
level_1_models.sort()

out_path = "%s/derivatives/nistats/level_2/sub-%s"%(data_loc,subnum)
if not os.path.exists(out_path):
    os.mkdir(out_path)

contrasts_path = "%s/contrasts"%(out_path)
if not os.path.exists(contrasts_path):
    os.mkdir(contrasts_path)

sub_l1s = [x for x in level_1_models if subnum in x]
