#!/usr/bin/env python
import glob
import json
import os
import re

try:
    data_loc = os.environ['DATA_LOC']
except KeyError:
    os.system('source /oak/stanford/groups/russpold/users/zenkavi/DevStudy_ServerScripts/setup/dev_study_env.sh')
    data_loc = os.environ['DATA_LOC']

json_files = glob.glob("%s/sub-*/func/*_bold.json"%(data_loc))
json_files.sort()

correct_st = [ 0, 0.21, 0.42, 0.63, 0.84, 0.07, 0.28, 0.49, 0.7, 0.91, 0.14, 0.35, 0.56, 0.77, 0, 0.21, 0.42, 0.63, 0.84, 0.07, 0.28, 0.49, 0.7, 0.91, 0.14, 0.35, 0.56, 0.77, 0, 0.21, 0.42, 0.63, 0.84, 0.07, 0.28, 0.49, 0.7, 0.91, 0.14, 0.35, 0.56, 0.77, 0, 0.21, 0.42, 0.63, 0.84, 0.07, 0.28, 0.49, 0.7, 0.91, 0.14, 0.35, 0.56, 0.77 ]

for json_file in json_files:
    subnum = re.findall('\d+', os.path.basename(json_file))[0]
    runnum = re.findall('\d+', os.path.basename(json_file))[1]
    with open(json_file) as json_data:
        json_dict = json.load(json_data)
        if 'SliceTiming' in json_dict:
            json_dict.update({'SliceTiming': correct_st})
    with open(json_file, "w") as out_file:
        json.dump(json_dict, out_file, indent=2)
    print('Fixed fmap sidecars for %s run %s'%(subnum, runnum))
