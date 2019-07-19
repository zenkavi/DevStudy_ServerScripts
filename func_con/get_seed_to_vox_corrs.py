#!/home/groups/russpold/software/miniconda/envs/fmri/bin/python
import os
import sys
import nibabel as nib
from nilearn import input_data
import numpy as np

def get_seed_to_vox_corrs(func_file, confounds, seed):

    TR = nib.load(func_file).header['pixdim'][4]

    seed_masker = input_data.NiftiSpheresMasker(
        seed, radius=8,
        detrend=True, standardize=True,
        low_pass=0.1, high_pass=0.01, t_r=TR,
        memory='nilearn_cache', memory_level=1, verbose=0)

    seed_time_series = seed_masker.fit_transform(func_file, confounds=confounds.values)

    brain_masker = input_data.NiftiMasker(
        smoothing_fwhm=6,
        detrend=True, standardize=True,
        low_pass=0.1, high_pass=0.01, t_r=TR,
        memory='nilearn_cache', memory_level=1, verbose=0)

    brain_time_series = brain_masker.fit_transform(func_file, confounds=confounds.values)

    seed_to_voxel_correlations = (np.dot(brain_time_series.T, seed_time_series) / seed_time_series.shape[0])

    seed_to_voxel_correlations_img = brain_masker.inverse_transform(seed_to_voxel_correlations.T)

    return(seed_to_voxel_correlations_img)
