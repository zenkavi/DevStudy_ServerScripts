#!/home/groups/russpold/software/miniconda/envs/fmri/bin/python
from argparse import ArgumentParser
from level_1_utils import run_level1
#Usage: python level_1.py -s SUBNUM -pe

parser = ArgumentParser()
parser.add_argument("-s", "--subnum", help="subject number")
args = parser.parse_args()
subnum = args.subnum
data_loc = os.environ['DATA_LOC']
server_scripts = os.environ['SERVER_SCRIPTS']

run_level1(subnum = subnum, out_path = "%s/derivatives/nistats/level_1/sub-%s"%(data_loc,subnum), pe=True, pe_path='%s/nistats/level_1/%s.csv'%(server_scripts, pe_model), beta=False)
