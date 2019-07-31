#!/home/groups/russpold/software/miniconda/envs/fmri/bin/python
import os
import sys
import pandas as pd
from nilearn import input_data, plotting
import numpy as np
sys.path.append(os.path.join(os.environ['SERVER_SCRIPTS'],'nistats/level_1'))
from level_1_utils import get_confounds
from nilearn.connectome import ConnectivityMeasure
from nilearn.input_data import NiftiSpheresMasker
from argparse import ArgumentParser
import glob

parser = ArgumentParser()
parser.add_argument("-s", "--subnum", help="subject number")
args = parser.parse_args()
subnum = args.subnum
data_loc = os.environ['DATA_LOC']

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

seed_dict = {0:"l_vstr",1:"r_vstr",2:"vmpfc",3:"l_ains",4:"r_ains",5:"pcc",6:"acc",7:"pre_sma",8:"r_dstr"}

func_files = glob.glob('%s/derivatives/fmriprep_1.4.0/fmriprep/sub-%s/func/sub-%s_task-machinegame_run-*_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz' %(data_loc, subnum, subnum))
func_files.sort()

for func_filename in func_files:
    runnum = re.findall('\d+', os.path.basename(func_filename))[1]

    formatted_confounds = get_confounds(pd.read_csv(os.path.join(data_loc,"derivatives/fmriprep_1.4.0/fmriprep/sub-%s/func/sub-%s_task-machinegame_run-%s_desc-confounds_regressors.tsv"%(subnum, subnum, runnum)), sep='\t'))

    # Create masker object to extract average signal within spheres
    masker = NiftiSpheresMasker(sphere_center, radius=sphere_radius, detrend=True,
                                standardize=True, low_pass=0.1, high_pass=0.01,
                                t_r=1.0, verbose=1, memory="nilearn_cache", memory_level=2)

    # Extract average signal in spheres with masker object
    time_series = masker.fit_transform(func_filename, confounds=formatted_confounds.values)

    connectivity_measure = ConnectivityMeasure(kind='partial correlation')
    partial_correlation_matrix = connectivity_measure.fit_transform([time_series])[0]

    #Save flattened partial correlation matrix with runnum, subnum and seen names
    flat_partial_correlation_matrix = pd.DataFrame(partial_correlation_matrix).stack().reset_index()
    flat_partial_correlation_matrix = flat_partial_correlation_matrix.rename(columns={"level_0": "seed1", "level_1": "seed2", 0: "cor_val"})
    flat_partial_correlation_matrix['drop'] = np.where(flat_partial_correlation_matrix.seed1>flat_partial_correlation_matrix.seed2,1,0)
    flat_partial_correlation_matrix = flat_partial_correlation_matrix.query("drop == 0 & cor_val<1").reset_index().drop(columns=['drop', 'index'])
    flat_partial_correlation_matrix["seed1"] = flat_partial_correlation_matrix["seed1"].map(seed_dict)
    flat_partial_correlation_matrix["seed2"] = flat_partial_correlation_matrix["seed2"].map(seed_dict)
    flat_partial_correlation_matrix["subnum"] = subnum
    flat_partial_correlation_matrix["runnum"] = runnum

    outpath = ('%s/derivatives/func_con/seed2seed/sub-%s/'%(data_loc, subnum))
    if not os.path.exists(outpath):
        os.makedirs(outpath)

    print("***********************************************")
    print("Saving partial correlation matrix for sub-%s run-%s"%(subnum, runnum))
    print("***********************************************")

    flat_partial_correlation_matrix.to_csv('%s/sub-%s_run-%s_partial-correlation-matrix.csv'%(outpath, subnum, runnum))
