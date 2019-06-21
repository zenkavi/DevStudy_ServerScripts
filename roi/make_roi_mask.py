#!/home/groups/russpold/software/miniconda/envs/fmri/bin/python
from nipype.caching import Memory
mem = Memory(base_dir='.')
from nipype.interfaces.fsl import ExtractROI
import os
import pandas as pd

data_loc = os.environ[DATA_LOC]
server_scripts = os.environ[SERVER_SCRIPTS]
out_path = os.path.join(data_loc, 'derivatives', 'rois')
anatfile = '~/datalad/templateflow/tpl-MNI152NLin2009cAsym/tpl-MNI152NLin2009cAsym_res-01_desc-brain_T1w.nii.gz'
centers = pd.read_csv(os.path.join(server_scripts, 'roi', 'sv_roi_centers.csv'))

for i in range(0, center.shape[0]):

    out_file = ...
    ctr = ...
    
    fslroi = ExtractROI(in_file=anatfile,
                        roi_file = out_file,
                        x_min=ctr[0],
                        x_size=5,
                        y_min=ctr[1],
                        y_size=5,
                        z_min=ctr[2],
                        z_size=5)
