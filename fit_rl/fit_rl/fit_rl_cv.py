import copy
import json
import math
import numpy as np
import os
import pandas as pd
import random
from scipy.stats import truncnorm
from argparse import ArgumentParser
from .fit_rl_mcmc import fit_rl_mcmc
from helper_funcs.get_predicted_df import get_predicted_df
from helper_funcs.extract_pars import get_model_name

todo_path = os.environ['TODO_PATH']
server_scripts = os.environ['SERVER_SCRIPTS']

parser = ArgumentParser()
parser.add_argument("-s", "--subject", help="subject number")
parser.add_argument("-dp", "--data_path", default=todo_path+'/behav_data_tb_organized/machine_game/' , help="data path")
parser.add_argument("-op", "--output_path", default=server_scripts+'/fit_rl/.cv_fits/', help="output path")
parser.add_argument("-f", "--fold_nums", default=4, help="number of cv folds")
parser.add_argument("-p", "--pars", help="parameters dictionary")
args = parser.parse_args()

#initialize arguments
subject = args.subject

data_path = args.data_path
fold_nums = int(args.fold_nums)
output_path = args.output_path
if not os.path.exists(output_path):
    os.makedirs(output_path)
pars = args.pars

#read in subject data
data =  pd.read_csv(data_path+'ProbLearn'+str(subject)+'.csv')

model_name = get_model_name(pars)

#assign cv folds to subject data (in this case try 25% vs 75% so 4 fold)

#EXCLUDE first five encounters of each condition and
data['con_count'] = data.groupby('Trial_type').cumcount()
data = data.query('con_count>4')

#BALANCED FOLDS!
# Each condition has 40 trials left with 160 total trials
# For k=4 CV
# Train on 160-(160/k) = 120 trials
# Test on 160/k = 40 trials
# Each fold should have a balanced number of TrialType
# Have one fold num column
# It should be of length = 40
# Shuffle it
# Assign it to sub dfs filtered by trial type

fold_nums_col = list(range(1,fold_nums+1))*int(data.shape[0]/fold_nums/len(data.Trial_type.unique()))
r_seed = random.randint(1000, 9999999)
random.seed(r_seed)
random.shuffle(fold_nums_col)
def assign_fold_nums(df):
    df['fold_nums'] = fold_nums_col
    return df
data = data.groupby('Trial_type').apply(assign_fold_nums)

#for each fold:
for cur_fold in range(1,fold_nums+1):

    print("***********************************************")
    print('Running fold: %s for subject: %s'%(str(cur_fold), subject))
    print("***********************************************")

    if fold_nums>1:
        #slice data
        train_data = data[data.fold_nums != cur_fold]
        train_data.reset_index(inplace=True, drop=True)
        test_data = data[data.fold_nums == cur_fold]
        test_data.reset_index(inplace=True, drop=True)
    else:
        train_data = data
        test_data = data

    #get parameters
    #opt_pars_dict = select_optimal_parameters(data=train_data, subject=subject, n_fits=n_fits, pars = pars)
    opt_pars_dict = fit_rl_mcmc(data=train_data, subject=subject, pars = pars)

    #make prediction
    pred_df = get_predicted_df(data=test_data, pars_dict=opt_pars_dict)

    #summarize prediction accuracy
    fold_out = pd.DataFrame.from_dict(opt_pars_dict, orient='index').transpose()
    fold_out = fold_out.add_prefix('xopt_')
    fold_out['fold'] =  cur_fold
    fold_out['seed'] = r_seed
    fold_out['sub_id'] = subject
    fold_out['pred_acc'] = sum(pred_df['pred_correct'])/pred_df.shape[0]
    fold_out['model_name'] = model_name

    if cur_fold == 1:
        all_folds_out = fold_out
    else:
        all_folds_out = all_folds_out.append(fold_out)

all_folds_out.to_csv(output_path+ 'CV_'+model_name+'_'+str(subject)+'.csv')

print("***********************************************")
print('Saving output for subject: %s in %s'%(subject, output_path))
print("***********************************************")
