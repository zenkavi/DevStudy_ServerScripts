#!/usr/bin/env python
import os
import re

data_loc = os.environ['DATA_LOC']

sub_dirnames = [f for f in os.listdir(data_loc) if re.match(r'sub', f)]

for i in sub_dirnames:
	command = 'singularity exec -B ${DATA_LOC}:${DATA_LOC} /share/PI/russpold/singularity_images/poldracklab_mriqc_0.14.2-2018-08-21-070e53b20a43.img mriqc $DATA_LOC $DATA_LOC/derivative/mriqc_0.14.2/ participant -w $LOCAL_SCRATCH/work --participant_label ' + i + ' --mem_gb 50 --n_procs 10 --ants-nthreads 8 -vvv'
	print(command)
