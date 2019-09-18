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
from helper_functions.select_optimal_parameters import select_optimal_parameters
from helper_functions.get_predicted_df import get_predicted_df

todo_path = os.environ['TODO_PATH']
server_scripts = os.environ['SERVER_SCRIPTS']

parser = ArgumentParser()
parser.add_argument("-s", "--subject", help="subject number")
parser.add_argument("-n", "--n_fits", default=50, help="Number of iterations for model")
parser.add_argument("-dp", "--data_path", default=todo_path+'/behav_data_tb_organized/machine_game/' , help="data path")
parser.add_argument("-op", "--output_path", default=server_scripts+'/fit_rl/.fits', help="output path")
parser.add_argument("-f", "--folds", default=1, help="number of cv folds")
parser.add_argument("-p", "--pars", help="parameters dictionary")
args = parser.parse_args()

#initialize arguments
subject = args.subject
n_fits = args.n_fits
data_path = args.data_path
folds = int(args.folds)
if(folds == 1):
    output_path = args.output_path + '/'
else:
    output_path = args.output_path+ '_'+ str(folds) + '_fold_cv/'
print("Output will be saved in %s"%(output_path))
if not os.path.exists(output_path):
    os.makedirs(output_path)
pars = args.pars

#read in subject data
data =  pd.read_csv(data_path+'ProbLearn'+str(subject)+'.csv')

model_name = get_model_name(pars)

#assign cv folds to subject data (in this case try 25% vs 75% so 4 fold)
fold_nums = list(range(1,fold_nums+1))*data.shape[0]/fold_nums
random.seed(42354)
random.shuffle(fold_nums)
if len(fold_nums) != data.shape[0]:
    fold_nums = fold_nums[:data.shape[0]]
data['fold_nums'] = fold_nums

#for each fold:
for cur_fold in range(1,fold_nums+1):

    #slice data
    train_data = data.query("fold_nums != cur_fold")
    test_data = data.query("fold_nums == cur_fold")

    #get parameters
    opt_pars_dict = select_optimal_parameters(data=train_data, subject=subject, n_fits=50, pars = pars)

    #make prediction
    pred_df = get_predicted_df(data=test_df, pars_dict=opt_pars_dict)

    #summarize prediction accuracy
    fold_out
    all_folds_out = all_folds_out.append(fold_out)
    sub_summary_out

    opt pars, pred accuracy, cv fold per subject
    then summarize this one step further with ave pred accuracy per subject

    #outputs
