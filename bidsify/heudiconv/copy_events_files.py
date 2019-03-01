#!/usr/bin/env python
import glob
import os
import re
import shutil

try:
    data_loc = os.environ['DATA_LOC']
except KeyError:
    os.system('source /oak/stanford/groups/russpold/users/zenkavi/DevStudy_ServerScripts/setup/dev_study_env.sh')
    data_loc = os.environ['DATA_LOC']

events_files = glob.glob("%s/sub-*/func/*_events.tsv"%(data_loc))
events_files.sort()

for ef in events_files:
    source_ef = ef.replace("0.0.4", "0.0.2").replace("run-00", "run-0")
    shutil.copy(source_ef, ef)
