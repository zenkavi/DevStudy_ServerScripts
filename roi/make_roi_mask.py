#!/home/groups/russpold/software/miniconda/envs/fmri/bin/python
from nipype.caching import Memory
mem = Memory(base_dir='.')
import nipype.interfaces.fsl as fsl
import os
import pandas as pd

data_loc = os.environ["DATA_LOC"]
server_scripts = os.environ["SERVER_SCRIPTS"]
out_path = os.path.join(data_loc, 'derivatives', 'rois')
anatfile = os.path.join(out_path, 'tpl-MNI152NLin2009cAsym_res-01_desc-brain_T1w','tpl-MNI152NLin2009cAsym_res-01_desc-brain_T1w.nii.gz')
space = os.path.basename(anatfile)
space = os.path.splitext(os.path.splitext(space)[0])[0]
centers = pd.read_csv(os.path.join(server_scripts, 'roi', 'sv_roi_centers.csv'))
size = 5

for i in range(0, centers.shape[0]):

    cur_row = centers.iloc[i]
    if not os.path.exists(os.path.join(out_path, space):
        os.makedirs(os.path.join(out_path, space)

    #fslmaths $FSLDIR/data/standard/MNI152_T1_2mm.nii.gz -mul 0 -add 1 -roi 44 1 86 1 32 1 0 1 VMPFC_point -odt float
    #fslmaths VMPFC_point.nii.gz -kernel sphere 5 -fmean VMPFC_sphere -odt float
    #fslmaths VMPFC_sphere.nii.gz -bin VMPFC_bin.nii.gz

    maths1 = fsl.ImageMaths()
    maths1.inputs.in_file = anatfile
    maths1.inputs.op_string = '-mul 0 -add 1 -roi %s 1 %s 1 %s 1 0 1'(cur_row.x, cur_row.y, cur_row.z)
    maths1.inputs.out_data_type = 'float'
    maths1.inputs.out_file = os.path.join(out_path, space, cur_row['Name']+'_point.nii.gz')
    maths1.cmdline
    maths1.run()

    maths2 = fsl.ImageMaths()
    maths2.inputs.in_file = os.path.join(out_path, space, cur_row['Name']+'_point.nii.gz')
    maths2.inputs.op_string = '-kernel sphere 5 -fmean'
    maths2.inputs.out_data_type = 'float'
    maths2.inputs.out_file = os.path.join(out_path, space, cur_row['Name']+'_sphere.nii.gz')
    maths2.cmdline
    math2.run()

    maths3 = fsl.ImageMaths()
    maths3.inputs.in_file = os.path.join(out_path, space, cur_row['Name']+'_sphere.nii.gz')
    maths3.inputs.op_string = '-bin'
    maths3.inputs.out_file = os.path.join(out_path, space, cur_row['Name']+'_bin.nii.gz')
    maths3.cmdline
    math3.run()

    print("***********************************************")
    print("ROI saved in %s"%(os.path.join(out_path, space, cur_row['Name']+'_bin.nii.gz')))
    print("***********************************************")
