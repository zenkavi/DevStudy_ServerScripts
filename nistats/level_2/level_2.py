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

in_path = "%s/derivatives/nistats/level_1/sub-%s/contrasts"%(data_loc,subnum)

out_path = "%s/derivatives/nistats/level_2/sub-%s"%(data_loc,subnum)
if not os.path.exists(out_path):
    os.mkdir(out_path)

contrasts_path = "%s/contrasts"%(out_path)
if not os.path.exists(contrasts_path):
    os.mkdir(contrasts_path)

sub_contrasts = glob.glob(in_path)

design_matrix = pd.DataFrame([1] * len(second_level_input),
                             columns=['intercept'])
