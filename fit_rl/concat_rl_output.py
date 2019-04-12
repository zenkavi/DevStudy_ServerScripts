import glob
import os
import pandas as pd
from string import digits
from argparse import ArgumentParser

#python concat_rl_output.py -r preds
#python concat_rl_output.py -r preds -m Fit_alpha-beta-exp_Fix_

parser.add_argument("-m", "--model_name", default='all', help="model name")
parser.add_argument("-r", "--rl_output", help="output type: preds/fits")
args = parser.parse_args()

model_name = args.model_name
rl_output = args.rl_output

data_dir = os.environ['SERVER_SCRIPTS']+"/fit_rl/.%s/" %(rl_output)

#helper function
remove_digits = str.maketrans('', '', digits)

if model_name == 'all':
    #remove .csv and numbers and get unique
    all_models = list(set([s.strip('.csv').translate(remove_digits) for s in os.listdir(data_dir)]))
else:
    all_models = [model_name]

for model in all_models:
    filenames = glob.glob(data_dir+model+'*')
    all_fits = pd.concat( [ pd.read_csv(f) for f in filenames ] , sort=True)
    all_fits['model'] = model
    all_fits.reset_index()
    all_fits.to_csv(data_dir+model+'All.csv')
