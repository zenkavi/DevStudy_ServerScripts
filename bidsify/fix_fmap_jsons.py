#!/usr/bin/env python
from collections import OrderedDict
import glob
import json
import os
import re

try:
    data_loc = os.environ['DATA_LOC']
except KeyError:
    os.system('source /oak/stanford/groups/russpold/users/zenkavi/DevStudy_ServerScripts/setup/dev_study_env.sh')
    data_loc = os.environ['DATA_LOC']

json_files = glob.glob("%s/sub-*/fmap/*.json"%(data_loc))
json_files.sort()

for json_file in json_files:
    subnum = re.findall('\d+', os.path.basename(json_file))[0]
    with open(json_file) as json_data:
        json_dict = json.load(json_data)
        if 'EchoTime' in json_dict:
            echo_times = []
            echo_times = list(set(echo_times))
            echo_times_dict = {}
            for i in range(len(echo_times)):
                echo_times_dict['EchoTime'+str(i+1)]= echo_times[i]
            del(json_dict['EchoTime'])
            json_dict.update(echo_times_dict)
        if 'IntendedFor' not in json_dict:
            bold_files = glob.glob("%s/sub-%s/func/*_bold.nii.gz"%(data_loc, subnum))
            bold_files = ['func/'+os.path.basename(x) for x in bold_files]
            bold_files.sort()
            json_dict.update({'IntendedFor': bold_files})
            json_dict = OrderedDict(sorted(json_dict.items()))
    with open(json_file, "w") as out_file:
        json.dump(json_dict, out_file, indent=2)
    print('Fixed fmap sidecars for %s'%(subnum))
