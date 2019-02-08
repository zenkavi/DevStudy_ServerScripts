#!/usr/bin/env python
import os
import re

data_loc = os.environ['DATA_LOC']

sub_dirnames = [f for f in os.listdir(data_loc) if re.match(r'sub', f)]

for i in sub_dirnames:
	command = 'singularity exec -B ${DATA_LOC}:${DATA_LOC} /share/PI/russpold/singularity_images/poldracklab_fmriprep_1.3.0-1-2019-02-08-1b5ad521ee2a.simg  $DATA_LOC $DATA_LOC/derivatives/fmriprep_1.3.0 participant -w /tmp/work --participant_label ' + i + ' --mem-mb 50000 --nthreads 10 --omp-nthreads 8 -vv --skip_bids_validation'
	print(command)
