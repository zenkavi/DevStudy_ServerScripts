import copy
import json
import math
import numpy as np
import os
import pandas as pd
import random
import scipy.optimize
from scipy.stats import truncnorm
from argparse import ArgumentParser
from helper_funcs.select_optimal_parameters import select_optimal_parameters
from helper_funcs.get_predicted_df import get_predicted_df
from helper_funcs.extract_pars import get_model_name

todo_path = os.environ['TODO_PATH']
server_scripts = os.environ['SERVER_SCRIPTS']

parser = ArgumentParser()
parser.add_argument("-s", "--subject", help="subject number")
parser.add_argument("-n", "--n_fits", default=50, help="Number of iterations for model")
parser.add_argument("-dp", "--data_path", default=todo_path+'/behav_data_tb_organized/machine_game/' , help="data path")
parser.add_argument("-op", "--output_path", default=server_scripts+'/fit_rl/.cv_fits/', help="output path")
parser.add_argument("-f", "--fold_nums", default=4, help="number of cv folds")
parser.add_argument("-p", "--pars", help="parameters dictionary")
args = parser.parse_args()

#initialize arguments
subject = args.subject
n_fits = args.n_fits
data_path = args.data_path
fold_nums = int(args.fold_nums)
if not os.path.exists(output_path):
    os.makedirs(output_path)
pars = args.pars

#read in subject data
data =  pd.read_csv(data_path+'ProbLearn'+str(subject)+'.csv')

model_name = get_model_name(pars)

#assign cv folds to subject data (in this case try 25% vs 75% so 4 fold)
fold_nums = list(range(1,fold_nums+1))*int(data.shape[0]/fold_nums)
r_seed = random.randint(1000, 9999999)
random.seed(r_seed)
random.shuffle(fold_nums)
if len(fold_nums) != data.shape[0]:
    fold_nums = fold_nums[:data.shape[0]]
data['fold_nums'] = fold_nums

#for each fold:
for cur_fold in range(1,fold_nums+1):

    print('Running fold: %s for subject: %s'%(str(cur_fold), subject))

    #slice data
    train_data = data[data.fold_nums != cur_fold]
    test_data = data[data.fold_nums == cur_fold]

    #get parameters
    opt_pars_dict = select_optimal_parameters(data=train_data, subject=subject, n_fits=n_fits, pars = pars)

    #make prediction
    pred_df = get_predicted_df(data=test_df, pars_dict=opt_pars_dict)

    #summarize prediction accuracy
    fold_out = pd.DataFrame.from_dict(opt_pars_dict)
    fold_out = df.add_prefix('xopt_')
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
