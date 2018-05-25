#!/usr/bin/env python
import os

mat_file_names = os.listdir(todo_path+"behav_data_tb_organized/bart")

sub_ids = [ x.split("_")[0] for x in mat_file_names ]

tsv_file_names = [ x.split(".")[0]+(".tsv") for x in mat_file_names]

json_file_names = [ x.split(".")[0]+(".json") for x in mat_file_names]

for i in range(len(mat_file_names)):
	command = 'Rscript --vanilla $SERVER_SCRIPTS/bidsify/convertBARTmat2tsv.R $TODO_PATH/behav_data_tb_organized/bart/' + mat_file_names[i] + ' $DATA_LOC/sub-' + sub_ids[i] + '/beh/' + tsv_file_names[i] + ' $DATA_LOC/sub-'+sub_ids[i]+'/beh/'+ json_file_names[i]
	print(command)

#sub-<participant_label>[_ses-<session_label>]_task-<task_name>_beh.tsv
#sub-<participant_label>[_ses-<session_label>]_task-<task_name>_beh.json
