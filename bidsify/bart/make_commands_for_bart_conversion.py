#!/usr/bin/env python
import os

todo_path = os.environ['TODO_PATH']

mat_file_names = os.listdir(todo_path+"/behav_data_tb_organized/bart")

sub_ids = [ x.split("_")[0] for x in mat_file_names ]

for i in range(len(mat_file_names)):
	command = 'Rscript --vanilla $SERVER_SCRIPTS/bidsify/convertBARTmat2tsv.R $TODO_PATH/behav_data_tb_organized/bart/' + mat_file_names[i] + ' $DATA_LOC/sub-' + sub_ids[i] + '/beh/sub-' + sub_ids[i]+ '_task-bart_beh'
	print(command)
