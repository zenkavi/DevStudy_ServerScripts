#!/usr/bin/env python
import csv

with open('/corral-repl/utexas/poldracklab/users/zenkavi/dev_study/DevStudy_ServerScripts/bidsify/sub_dirname_match_list.tsv','rb') as tsvfile:
	reader = csv.reader(tsvfile, delimiter='\t')
	sub_dir_match_list = [line for line in reader]

print('#!/bin/bash')
	
for i in range(len(sub_dir_match_list)):
	command = "python /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/DevStudy_ServerScripts/bidsify/move_niftis_to_bids.py '/corral-repl/utexas/poldracklab/users/zenkavi/dev_study/03_DICOM_to_NIFTI_conversions/"+ sub_dir_match_list[i][0] + "/' '/corral-repl/utexas/poldracklab/users/zenkavi/dev_study/data/" + sub_dir_match_list[i][1] + "/' '" +  sub_dir_match_list[i][1].split("-")[1] + "'"
	print(command)
