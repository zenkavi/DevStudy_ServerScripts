#!/usr/bin/env python
import os

mat_file_names = os.listdir("/corral-repl/utexas/poldracklab/users/zenkavi/dev_study/todo/behav_data_tb_organized/bart")

sub_ids = [ x.split("_")[0] for x in mat_file_names ]

tsv_file_names = [ x.split(".")[0]+(".tsv") for x in mat_file_names]

json_file_names = [ x.split(".")[0]+(".json") for x in mat_file_names]

print('#!/bin/bash')

for i in range(len(mat_file_names)):
	command = 'Rscript --vanilla /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/DevStudy_TaccScripts/convertBARTmat2tsv.R /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/todo/behav_data_tb_organized/bart/' + mat_file_names[i] + ' /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/data/sub-' + sub_ids[i] + '/behav/' + tsv_file_names[i] + ' /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/data/sub-'+sub_ids[i]+'/behav/'+ json_file_names[i]
	print(command)
