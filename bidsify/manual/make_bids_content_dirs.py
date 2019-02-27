#!/usr/bin/env python
import os

server_scripts = os.environ['SERVER_SCRIPTS']
data_loc = os.environ['DATA_LOC']

dir_names = open(server_scripts+"/bidsify/sub_dirname_list.txt")

for line in dir_names:
	os.mkdir(data_loc+"/sub-"+line.strip()+"/anat")
	os.mkdir(data_loc+"/sub-"+line.strip()+"/func")
	os.mkdir(data_loc+"/sub-"+line.strip()+"/fmap")
	os.mkdir(data_loc+"/sub-"+line.strip()+"/beh")

dir_names.close()
