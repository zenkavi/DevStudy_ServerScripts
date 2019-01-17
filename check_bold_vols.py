#!/usr/bin/env python

import glob
import os

path = '/oak/stanford/groups/russpold/data/ds000054/0.0.1/'

boldfiles = glob.glob('%s/sub-[0-9][0-9][0-9][0-9][0-9][0-9]/func/sub-[0-9][0-9][0-9][0-9][0-9][0-9]_task-machinegame_run-0[0-9]_bold.nii.gz'%(path))

for file in boldfiles:
    print file
    print(os.system('fslnvols %s'%(file)))
