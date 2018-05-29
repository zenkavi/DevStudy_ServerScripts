#!/usr/bin/env python
import os
import re

data_loc = os.environ['DATA_LOC']

sub_dirnames = [f for f in os.listdir(data_loc) if re.match(r'sub', f)]

for i in sub_dirnames:
	command = 'singularity run /share/PI/russpold/singularity_images/poldracklab_mriqc_0.10.5-2018-05-28-9954e8c774c2.img $DATA_LOC/ $DATA_LOC/derivatives/mriqc_0.10.5/ participant -w $LOCAL_SCRATCH/work --participant_label ' + i + ' --mem_gb 50 --n_procs 10 --ants-nthreads 8 -vvv'
	print(command)

#ingularity run /share/PI/russpold/singularity_images/poldracklab_mriqc_0.10.5-2018-05-28-9954e8c774c2.img $DATA_LOC/ $DATA_LOC/derivatives/mriqc_0.10.5/ participant -w $LOCAL_SCRATCH/work --participant_label sub-100003 --mem-gb 50 --n_procs 10 --ants-nthreads 8 -vvv
