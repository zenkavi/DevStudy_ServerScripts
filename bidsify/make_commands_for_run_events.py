#!/usr/bin/env python
import os
import re

try:
    todo_path = os.environ['TODO_PATH']
except KeyError:
    os.system('source /oak/stanford/groups/russpold/users/zenkavi/DevStudy_ServerScripts/setup/dev_study_env.sh')
    todo_path = os.environ['TODO_PATH']

behav_data_file_names = os.listdir(os.path.join(todo_path, "/behav_data_tb_organized/machine_game"))

sub_ids = [ int(filter(str.isdigit, x)) for x in behav_data_file_names ]

server_scripts = os.environ['SERVER_SCRIPTS']

for i in range(len(behav_data_file_names)):
	command = "python " + server_scripts + "/bidsify/make_run_events.py '" +todo_path+ "/behav_data_tb_organized/machine_game/"+behav_data_file_names[i]+"' 30 'machinegame' '"+str(sub_ids[i]) + "' '"+str(sub_ids[i])+"'"
	print(command)

#The commands this prints aren't going to be full proof for all directory names. Manual corrections are made in the exec_make_run_events.sh file
