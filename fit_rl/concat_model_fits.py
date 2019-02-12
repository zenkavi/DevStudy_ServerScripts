import glob
import os
import pandas as pd
from string import digits
import sys

#python concat_model_fits.py
#python concat_model_fits.py LearningParams_Fit_alpha-beta-exp_Fix_

try:
    model_name = sys.argv[1]
except:
    model_name = 'all'

data_dir = os.environ['SERVER_SCRIPTS']+"/fit_rl/.fits/"

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
