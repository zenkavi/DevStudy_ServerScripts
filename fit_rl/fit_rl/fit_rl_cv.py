from fit_rl.helper_funcs import select_optimal_parameters, get_predicted_df
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

#assign cv folds to subject data
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

    #summarize prediction accuracy
