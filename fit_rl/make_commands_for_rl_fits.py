read in a csv of models
for each row in the csv create list of fix and fit vars
get col names where value is 1 -> fit vars
get col names where value is fix
concat in pars form dictionary
append to list of models

import os

todo_path = os.environ['TODO_PATH']
server_scripts = os.environ['SERVER_SCRIPTS']

beh_file_names = os.listdir(todo_path+"/behav_data_tb_organized/machine_game")

subjects = [ x.split("ProbLearn")[1].split(".")[0] for x in beh_file_names ]

data_path = todo_path+"/behav_data_tb_organized/machine_game/"

output_path = server_scripts+"fit_rl/.fits"

for pars in pars_list:
    for subject in subjects:
        command = 'python fit_rl.py ' + subject + ' ' + n_fits + ' ' + data_path + ' ' + output_path + ' ' + pars
        print(command)

#Sample command
#python fit_rl.py {SUBJECT} {N_FITS} {DATA_PATH} {OUTPUT_PATH} {PARS}
