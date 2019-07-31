#!/home/groups/russpold/software/miniconda/envs/fmri/bin/python
from argparse import ArgumentParser
import os
import sys
sys.path.append(os.path.join(os.environ['SERVER_SCRIPTS'], 'nistats/level_1'))
from level_1_utils import run_ppi_level1
#Usage: python level_1.py -s SUBNUM -pe

parser = ArgumentParser()
parser.add_argument("-s", "--subnum", help="subject number")
args = parser.parse_args()
subnum = args.subnum
data_loc = os.environ['DATA_LOC']
server_scripts = os.environ['SERVER_SCRIPTS']

run_ppi_level1(subnum = subnum, out_path = "%s/derivatives/func_con/ppi/level_1/sub-%s"%(data_loc,subnum), beta=True, seed_name="l_vstr", tasks = ['m1', 'm2','m3', 'm4'])
