#!/usr/bin/env python
import os

behav_data_file_names = os.listdir("/corral-repl/utexas/poldracklab/users/zenkavi/dev_study/todo/behav_data_tb_organized/machine_game")

sub_ids = [ int(filter(str.isdigit, x)) for x in behav_data_file_names ]

for i in range(len(behav_data_file_names)):
	command = "python /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/DevStudy_ServerScripts/bidsify/make_run_events.py '/corral-repl/utexas/poldracklab/users/zenkavi/dev_study/todo/behav_data_tb_organized/machine_game/"+behav_data_file_names[i]+"' 30 'machinegame' '"+str(sub_ids[i]) + "' '"+str(sub_ids[i])+"'"
	print(command)
#The commands this prints aren't going to be full proof for all directory names. Manual corrections are made in the exec_make_run_events.sh file
