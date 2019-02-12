import copy
import glob
import json
import math
import numpy as np
import os
import pandas as pd
import random
import scipy.optimize
from argparse import ArgumentParser

#input: get_trial_ev.py sub_id model data_path out_path
#output: /oak/stanford/groups/russpold/data/ds000054/0.0.2/derivatives/level_1/sub-*/sub-*_task-machinegame_run-*_ev.csv

try:
    todo_path = os.environ['TODO_PATH']
    server_scripts = os.environ['SERVER_SCRIPTS']
except KeyError:
    os.system('source /oak/stanford/groups/russpold/users/zenkavi/DevStudy_ServerScripts/setup/dev_study_env.sh')
    todo_path = os.environ['TODO_PATH']
    server_scripts = os.environ['SERVER_SCRIPTS']

parser = ArgumentParser()
parser.add_argument("-s", "--subject", help="subject number")
parser.add_argument("-dp", "--data_path", default=todo_path+'/behav_data_tb_organized/machine_game/' , help="data path")
parser.add_argument("-op", "--output_path", default=server_scripts+'/oak/stanford/groups/russpold/data/ds000054/0.0.2/derivatives/level_1/', help="output path")
args = parser.parse_args()

machine_game_data = glob.glob('%s/ProbLearn*'%(data_path))
machine_game_data.sort()

def calculate_prediction_error(x0,data, pars):

    TrialNum = data.Trial_type
    Response = data.Response
    Outcome = data.Points_earned

    EV = [0,0,0,0]
    Prediction_Error = 0
    choiceprob = np.zeros((len(TrialNum)))

    #x0 only has values for parameters that will be fitted; so we can't use numerical indices to extract from the list and assign as the parameter value to be used
    #to fix this we add the argument pars to the function and use it to create to helper lists of parameters that will be fixed and those that will be fit
    fixparams = extract_pars(pars)['fixparams']
    fitparams = extract_pars(pars)['fitparams']

    #because the length of x0 and the parameters the values in it correspond to will change depending on what is fixed vs. fit we need a named dictionary
    #we use the list of fitparams for this
    x0_dict = dict(zip(fitparams,x0))

    #now we create a dictionary that will contain all the appropriate numbers for each parameter that will be used in the RPE and EV calculations below
    if 'alpha' in pars.keys():
        if 'exp' in pars.keys():
            all_pars_dict = {'alpha':np.nan, 'beta':np.nan, 'exp':np.nan}
        else:
            all_pars_dict = {'alpha':np.nan, 'beta':np.nan, 'exp_neg':np.nan, 'exp_pos':np.nan}
    elif 'exp' in pars.keys():
        all_pars_dict = {'alpha_neg':np.nan, 'alpha_pos':np.nan, 'beta':np.nan, 'exp':np.nan}
    else:
        all_pars_dict = {'alpha_neg':np.nan, 'alpha_pos':np.nan, 'beta':np.nan, 'exp_neg':np.nan, 'exp_pos':np.nan}

    #we populate each element in this dictionary of all to-be-used parameters by going through each key; checking if it is in fixparams. If so we extract is from the params argument in the function call, otherwise we extract the sampled value from x0
    for par in sorted(all_pars_dict.keys()):
        if par in fixparams:
            all_pars_dict[par] = pars[par]
        else:
            all_pars_dict[par] = x0_dict[par]

    #finally we assign the to-be used parameters to objects to avoid too much typing in the rest of the loops
    if 'alpha' in all_pars_dict.keys():
        alpha=all_pars_dict['alpha']
    else:
        alphaneg=all_pars_dict['alpha_neg']
        alphapos=all_pars_dict['alpha_pos']
    beta=all_pars_dict['beta']
    if 'exp' in all_pars_dict.keys():
        exp=all_pars_dict['exp']
    else:
        expneg=all_pars_dict['exp_neg']
        exppos=all_pars_dict['exp_pos']

    for i in range(len(TrialNum)):
        #First update the choice probabilities for each trial
        if Response[i] == 0:
            choiceprob[i] = 1

        if Response[i] == 1:
            choiceprob[i] = math.exp(EV[int(TrialNum[i]-1)]*beta)/(math.exp(EV[int(TrialNum[i]-1)]*beta)+1)

        if Response[i] == 2:
            choiceprob[i] = 1-math.exp(EV[int(TrialNum[i]-1)]*beta)/(math.exp(EV[int(TrialNum[i]-1)]*beta)+1)

        #If a machine has been played update the RPE
        if Outcome[i] != 0:

            if Outcome[i] > EV[int(TrialNum[i]-1)]:

                if 'alpha' in vars() or 'alpha' in globals():
                    if 'exp' in vars() or 'exp' in globals():
                        Prediction_Error = alpha*(Outcome[i] - EV[int(TrialNum[i]-1)])**exp
                    else:
                        Prediction_Error = alpha*(Outcome[i] - EV[int(TrialNum[i]-1)])**exppos
                elif 'exp' in vars() or 'exp' in globals():
                    Prediction_Error = alphapos*(Outcome[i] - EV[int(TrialNum[i]-1)])**exp
                else:
                    Prediction_Error = alphapos*(Outcome[i] - EV[int(TrialNum[i]-1)])**exppos

            #If the outcome is worst than expected use alphaneg
            if Outcome[i] < EV[int(TrialNum[i]-1)]:

                if 'alpha' in vars() or 'alpha' in globals():
                    if 'exp' in vars() or 'exp' in globals():
                        Prediction_Error = -1*alpha*(EV[int(TrialNum[i]-1)]-Outcome[i])**exp #have to do it this way because you can't put a negative number to an exponent between 0 and 1
                    else:
                        Prediction_Error = -1*alpha*(EV[int(TrialNum[i]-1)]-Outcome[i])**expneg
                elif 'exp' in vars() or 'exp' in globals():
                    Prediction_Error = -1*alphaneg*(EV[int(TrialNum[i]-1)]-Outcome[i])**exp
                else:
                    Prediction_Error = -1*alphaneg*(EV[int(TrialNum[i]-1)]-Outcome[i])**expneg

            if Outcome[i] == EV[int(TrialNum[i]-1)]:
                Prediction_Error = 0

            EV[int(TrialNum[i]-1)] += Prediction_Error

    return(ev_df)

for subject_data in machine_game_data:
    df = pd.read_csv(subject_data)
