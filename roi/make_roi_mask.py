#!/home/groups/russpold/software/miniconda/envs/fmri/bin/python
import nibabel as nib
import nipype.interfaces.fsl as fsl
import os
import pandas as pd
import sys
sys.path.append(os.environ['SERVER_SCRIPTS'])
from utils.mni2vox import mni2vox

data_loc = os.environ["DATA_LOC"]
server_scripts = os.environ["SERVER_SCRIPTS"]
out_path = os.path.join(data_loc, 'derivatives', 'rois')
anatfile = os.path.join(out_path, 'tpl-MNI152NLin2009cAsym_res-01_desc-brain_T1w','tpl-MNI152NLin2009cAsym_res-01_desc-brain_T1w.nii.gz')
space = os.path.basename(anatfile)
space = os.path.splitext(os.path.splitext(space)[0])[0]
centers = pd.read_csv(os.path.join(server_scripts, 'roi', 'sv_roi_centers.csv'))
T = nib.load(anatfile).affine

for i in range(0, centers.shape[0]):

    cur_row = centers.iloc[i]
    vox_cor = mni2vox([cur_row.x, cur_row.y, cur_row.z], T)
    if not os.path.exists(os.path.join(out_path, space)):
        os.makedirs(os.path.join(out_path, space))

    maths1 = fsl.ImageMaths()
    maths1.inputs.in_file = anatfile
    maths1.inputs.op_string = '-mul 0 -add 1 -roi %s 1 %s 1 %s 1 0 1'%(vox_cor[0], vox_cor[1], vox_cor[2])
    maths1.inputs.out_data_type = 'float'
    maths1.inputs.out_file = os.path.join(out_path, space, cur_row['Name']+'_point.nii.gz')
    maths1.run()

    maths2 = fsl.ImageMaths()
    maths2.inputs.in_file = os.path.join(out_path, space, cur_row['Name']+'_point.nii.gz')
    maths2.inputs.op_string = '-kernel sphere 5 -fmean'
    maths2.inputs.out_data_type = 'float'
    maths2.inputs.out_file = os.path.join(out_path, space, cur_row['Name']+'_sphere.nii.gz')
    maths2.run()

    maths3 = fsl.ImageMaths()
    maths3.inputs.in_file = os.path.join(out_path, space, cur_row['Name']+'_sphere.nii.gz')
    maths3.inputs.op_string = '-bin'
    maths3.inputs.out_file = os.path.join(out_path, space, cur_row['Name']+'_bin.nii.gz')
    maths3.run()

    print("***********************************************")
    print("ROI saved in %s"%(os.path.join(out_path, space, cur_row['Name']+'_bin.nii.gz')))
    print("***********************************************")
