#!/usr/bin/env python
import os

sub_dir_names = os.listdir("/corral-repl/utexas/poldracklab/users/zenkavi/dev_study/data")

print('#!/bin/bash')

for sub_dir_name in sub_dir_names:
	command = 'python /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/scripts/fix_fmap_jsons.py "/corral-repl/utexas/poldracklab/users/zenkavi/dev_study/data/'+sub_dir_name+'"'
	print(command)
