import numpy as np
import pandas as pd
import os

todo_path = os.environ['TODO_PATH']
server_scripts = os.environ['SERVER_SCRIPTS']

beh_file_names = os.listdir(todo_path+"/behav_data_tb_organized/machine_game")

subjects = [ x.split("ProbLearn")[1].split(".")[0] for x in beh_file_names ]

data_path = todo_path+"/behav_data_tb_organized/machine_game/"

output_path = server_scripts+"fit_rl/.fits"

n_fits = 50

rl_models = pd.read_csv('possible_rl_models.csv')

pars_list = []

for i in range(len(rl_models)):
    
    #cols where row is nan 
    #rl_models.columns[rl_models.iloc[0].isnull()]
    
    fit_pars = list(rl_models.columns[(rl_models == "1").iloc[i]])
    pars = dict(zip(fit_pars, len(fit_pars)*[np.nan]))
    
    #What to fix these too if they are fixed??
    #Fix values:
    #alpha - 0.05
    #beta - 1
    #exp - 0.5
    fix_pars = list(rl_models.columns[(rl_models == "fix").iloc[i]])
    
    for par in fix_pars:
        if 'alpha' in par:
            pars[par] = 0.05
        elif 'exp' in par:
            pars[par] = 0.5
        elif 'beta' in par:
            pars[par] = 1
    
    
    pars_list.append(pars)

for pars in pars_list:
    for subject in subjects:
        command = 'python fit_rl.py ' + str(subject) + ' ' + str(n_fits) + ' ' + data_path + ' ' + output_path + ' ' + str(pars)
        print(command)

#Sample command
#python fit_rl.py {SUBJECT} {N_FITS} {DATA_PATH} {OUTPUT_PATH} {PARS}
