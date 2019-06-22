#!/home/groups/russpold/software/miniconda/envs/fmri/bin/python
from nipype.caching import Memory
mem = Memory(base_dir='.')
from nipype.interfaces.fsl import ExtractROI
import os
import pandas as pd

data_loc = os.environ["DATA_LOC"]
server_scripts = os.environ["SERVER_SCRIPTS"]
out_path = os.path.join(data_loc, 'derivatives', 'rois')
anatfile = os.path.join(out_path, 'tpl-MNI152NLin2009cAsym_res-01_desc-brain_T1w','tpl-MNI152NLin2009cAsym_res-01_desc-brain_T1w.nii.gz')
anatfile_mul = os.path.join(out_path, 'tpl-MNI152NLin2009cAsym_res-01_desc-brain_T1w','tpl-MNI152NLin2009cAsym_res-01_desc-brain_T1w_mul.nii.gz')
anatfile_add = os.path.join(out_path, 'tpl-MNI152NLin2009cAsym_res-01_desc-brain_T1w','tpl-MNI152NLin2009cAsym_res-01_desc-brain_T1w_add.nii.gz')
space = os.path.basename(anatfile)
space = os.path.splitext(os.path.splitext(space)[0])[0]
centers = pd.read_csv(os.path.join(server_scripts, 'roi', 'sv_roi_centers.csv'))
size = 5


if not os.path.exists(anatfile_add):
    binaryMaths = mem.cache(fsl.BinaryMaths)
    binaryMaths(in_file=anatfile,
                operation = "mul",
                operand_value = 0,
                out_file = anatfile_mul)
    binaryMaths(in_file= anatfile_mul,
                operation = "add",
                operand_value = 1,
                out_file = anatfile_add)

for i in range(0, centers.shape[0]):

    cur_row = centers.iloc[i]
    out_file_name = os.path.join(out_path, space, cur_row['Name']+'.nii.gz')
    if not os.path.exists(os.path.dirname(out_file_name)):
        os.makedirs(os.path.dirname(out_file_name))

    fslroi = ExtractROI(in_file=anatfile_add,
                        roi_file = out_file_name,
                        x_min=cur_row.x,
                        x_size=size,
                        y_min=cur_row.y,
                        y_size=size,
                        z_min=cur_row.z,
                        z_size=size,
                        t_min = 0,
                        t_size = 1)
    fslroi.run()

    print("***********************************************")
    print("ROI saved in %s"%(out_file_name))
    print("***********************************************")
