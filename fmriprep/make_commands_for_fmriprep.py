#!/usr/bin/env python
import os
import re

data_loc = os.environ['DATA_LOC']

sub_dirnames = [f for f in os.listdir(data_loc) if re.match(r'sub', f)]

for i in sub_dirnames:
	command = 'singularity run /share/PI/russpold/singularity_images/poldracklab_fmriprep_1.2.5-2018-12-04-2ef6b23ede2a.img $DATA_LOC/ $LOCAL_SCRATCH/out/ participant -w $LOCAL_SCRATCH/work --participant_label ' + i + ' --mem-mb 50000 --nthreads 10 --omp-nthreads 8 -vv'
	print(command)

#singularity run /share/PI/russpold/singularity_images/poldracklab_fmriprep_1.2.5-2018-12-04-2ef6b23ede2a.img $OAK/data/ds000054/0.0.1/ $OAK/data/ds000054/0.0.1/derivatives/ participant -w work --participant_label sub-100003 --mem-mb 50000 --nthreads 10 --omp-nthreads 8 -vv
