#!/usr/bin/env python
import os

dir_names = open("/corral-repl/utexas/poldracklab/users/zenkavi/dev_study/DevStudy_ServerScripts/bidsify/sub_dirname_list.txt")

for line in dir_names:
	os.mkdir("/corral-repl/utexas/poldracklab/users/zenkavi/dev_study/data/sub-"+line.strip())

dir_names.close()
