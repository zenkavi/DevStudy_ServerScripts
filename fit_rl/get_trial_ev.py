import glob
import math
import numpy as np
import os
import pandas as pd
import re
from argparse import ArgumentParser

#input: get_trial_ev.py --model Fit_alpha-beta-exp_neg-exp_pos_Fix_ --data_path --out_path
#output: /oak/stanford/groups/russpold/data/ds000054/0.0.2/derivatives/level_1/sub-*/sub-*_task-machinegame_run-*_ev_rpe.csv

try:
    todo_path = os.environ['TODO_PATH']
    server_scripts = os.environ['SERVER_SCRIPTS']
    data_loc = os.environ['DATA_LOC']
except KeyError:
    os.system('source /oak/stanford/groups/russpold/users/zenkavi/DevStudy_ServerScripts/setup/dev_study_env.sh')
    todo_path = os.environ['TODO_PATH']
    server_scripts = os.environ['SERVER_SCRIPTS']
    data_loc = os.environ['DATA_LOC']

parser = ArgumentParser()
parser.add_argument("-m", "--model", help="model name")
parser.add_argument("-dp", "--data_path", default=todo_path+'/behav_data_tb_organized/machine_game/' , help="data path")
parser.add_argument("-op", "--output_path", default=data_loc+'/derivatives/level_1/', help="output path")
args = parser.parse_args()

machine_game_data = glob.glob('%s/ProbLearn*'%(data_path))
machine_game_data.sort()

model_pars_data = pd.read_csv(server_scripts+'/fit_rl/.fits/LearningParams_'+model_name+'_All.csv')

model_pars_data = model_pars_data[model_pars_data['neglogprob'] == model_pars_data.groupby('sub_id')['neglogprob'].transform('min')]
model_pars_data = model_pars_data.sort_values('neglogprob').drop_duplicates('sub_id')

def get_ev_rpe_df(data, pars_dict):
    TrialNum = data.Trial_type
    Response = data.Response
    Outcome = data.Points_earned
    EV = [0,0,0,0]
    Prediction_Error = 0
    choiceprob = np.zeros((len(TrialNum)))
    data['EV'] = np.nan
    data['PE'] = np.nan
    if 'alpha' in pars_dict.keys():
        alpha=pars_dict['alpha']
    else:
        alphaneg=pars_dict['alpha_neg']
        alphapos=pars_dict['alpha_pos']
    beta=pars_dict['beta']
    if 'exp' in pars_dict.keys():
        exp=pars_dict['exp']
    else:
        expneg=pars_dict['exp_neg']
        exppos=pars_dict['exp_pos']
    for i in range(len(TrialNum)):
        if Response[i] == 0:
            choiceprob[i] = 1
        if Response[i] == 1:
            choiceprob[i] = math.exp(EV[int(TrialNum[i]-1)]*beta)/(math.exp(EV[int(TrialNum[i]-1)]*beta)+1)
        if Response[i] == 2:
            choiceprob[i] = 1-math.exp(EV[int(TrialNum[i]-1)]*beta)/(math.exp(EV[int(TrialNum[i]-1)]*beta)+1)
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
            if Outcome[i] < EV[int(TrialNum[i]-1)]:
                if 'alpha' in vars() or 'alpha' in globals():
                    if 'exp' in vars() or 'exp' in globals():
                        Prediction_Error = -1*alpha*(EV[int(TrialNum[i]-1)]-Outcome[i])**exp
                    else:
                        Prediction_Error = -1*alpha*(EV[int(TrialNum[i]-1)]-Outcome[i])**expneg
                elif 'exp' in vars() or 'exp' in globals():
                    Prediction_Error = -1*alphaneg*(EV[int(TrialNum[i]-1)]-Outcome[i])**exp
                else:
                    Prediction_Error = -1*alphaneg*(EV[int(TrialNum[i]-1)]-Outcome[i])**expneg
            if Outcome[i] == EV[int(TrialNum[i]-1)]:
                Prediction_Error = 0
            data.EV[i] = EV[int(TrialNum[i]-1)]
            data.PE[i] = Prediction_Error
            EV[int(TrialNum[i]-1)] += Prediction_Error
    return(data)

for subject_data in machine_game_data:
    df = pd.read_csv(subject_data)
    subnum = re.findall('\d+', os.path.basename(subject_data))[0]

    pars_row = model_pars_data.query("sub_id == %s"%(float(subnum)))
    pars_dict = pars_row.filter(regex='xopt').to_dict('records')[0]
    pars_dict = {x.replace('xopt_', ''): v for x, v in pars_dict.items()}

    for (k,v) in pars_dict.items():
        if np.isnan(v):
            fix_row = model_pars_data.query("sub_id == %s"%(float(subnum)))
            fix_dict = fix_row.filter(regex='x0').to_dict('records')[0]
            fix_dict = {x.replace('x0_', ''): v for x, v in fix_dict.items()}
            pars_dict[k] = fix_dict[k]

    df = get_ev_rpe_df(data=df, pars_dict=pars_dict)
    df = df[['Trial_type', 'Response', 'Points_earned', 'EV', 'PE']]

    file_length = df.shape[0]
    N=30
    for i in range(file_length//N):
        run_rows = df[N*(i+1)-(N):N*(i+1)]
        run_rows.to_csv(os.path.join(output_path, 'sub-%s'%(subnum),'sub-'+str(subnum)+'_task-machinegame_run-0'+str(i+1)+'_ev_rpe.csv'))
