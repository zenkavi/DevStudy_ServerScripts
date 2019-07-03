#!/home/groups/russpold/software/miniconda/envs/fmri/bin/python
from argparse import ArgumentParser
import os
import sys
sys.path.append(os.path.join(os.environ['SERVER_SCRIPTS'],'nistats/level_1'))
from level_1_utils import make_contrasts, add_transform, stdize, get_conditions, get_confounds, run_level1
#Usage: python rpe_level_1.py -s SUBNUM

parser = ArgumentParser()
parser.add_argument("-s", "--subnum", help="subject number")
args = parser.parse_args()
subnum = args.subnum
data_loc = os.environ['DATA_LOC']
server_scripts = os.environ['SERVER_SCRIPTS']

pred_rpes = glob.glob(os.path.join(server_scripts, 'rpe_cors/pred_rpes'))

for cur_pes in pred_rpes:
    print("***********************************************")
    print("Running level 1 for sub-%s model %s"%(subnum, os.path.basename(cur_pes)))
    print("***********************************************")
    out_path = os.path.join(data_loc,'derivatives/rpe_cors/%s/sub-%s'%(os.path.basename(cur_pes), subnum))
    run_level1(subnum = subnum, out_path = out_path, pe = True, pe_path = cur_pes, beta = True)
