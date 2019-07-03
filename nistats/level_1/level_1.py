from argparse import ArgumentParser
from level_1_utils import make_contrasts, add_transform, stdize, get_conditions, get_confounds, run_level1
#Usage: python level_1.py -s SUBNUM -pe

parser = ArgumentParser()
parser.add_argument("-s", "--subnum", help="subject number")
parser.add_argument("-pe", "--pred_err", help="use prediction error regressor", default= True)
args = parser.parse_args()
subnum = args.subnum
pe = args.pred_err
data_loc = os.environ['DATA_LOC']
server_scripts = os.environ['SERVER_SCRIPTS']

run_level1(subnum = subnum, out_path = "%s/derivatives/nistats/level_1/sub-%s"%(data_loc,subnum), pe=pe, pe_path='%s/nistats/level_1/%s.csv'%(server_scripts, pe_model), beta=False)
