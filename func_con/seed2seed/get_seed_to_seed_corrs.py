import os
import sys
import pandas as pd
from nilearn import input_data, plotting
import numpy as np
sys.path.append(os.path.join(os.environ['SERVER_SCRIPTS'],'nistats/level_1'))
from level_1_utils import get_confounds
from nilearn.connectome import ConnectivityMeasure
from nilearn.input_data import NiftiSpheresMasker

data_loc = os.environ['DATA_LOC']
subnum = '400742'
runnum = '002'
func_filename = '%s/derivatives/fmriprep_1.4.0/fmriprep/sub-%s/func/sub-%s_task-machinegame_run-%s_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz' %(data_loc, subnum, subnum, runnum)
formatted_confounds = get_confounds(pd.read_csv(os.path.join(data_loc,"derivatives/fmriprep_1.4.0/fmriprep/sub-%s/func/sub-%s_task-machinegame_run-%s_desc-confounds_regressors.tsv"%(subnum, subnum, runnum)), sep='\t'))

# Sphere radius in mm
sphere_radius = 8

# Sphere center in MNI-coordinate
# sphere_center = pd.read_csv('%s/roi/sv_roi_centers.csv'%(os.environ['SERVER_SCRIPTS']))[["x", "y", "z"]].values
sphere_center = [(-12,  12,  -6),
       ( 12,  10,  -6),
       (  2,  46,  -8),
       (-30,  22,  -6),
       ( 32,  20,  -6),
       ( -4, -30,  36),
       ( -2,  28,  28),
       ( -2,  16,  46),
       ( 18,  15,  15)]

# Create masker object to extract average signal within spheres
masker = NiftiSpheresMasker(sphere_center, radius=sphere_radius, detrend=True,
                            standardize=True, low_pass=0.1, high_pass=0.01,
                            t_r=1.0, verbose=1, memory="nilearn_cache", memory_level=2)

# Extract average signal in spheres with masker object
time_series = masker.fit_transform(func_filename, confounds=formatted_confounds.values)

connectivity_measure = ConnectivityMeasure(kind='partial correlation')
partial_correlation_matrix = connectivity_measure.fit_transform([time_series])[0]
