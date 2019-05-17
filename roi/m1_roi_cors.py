import glob
import nibabel as nib
import nistats
import numpy as np
import os
import pandas as pd
import re

data_loc = os.environ['DATA_LOC']
home = os.environ['HOME']

#First looking at relationship between BOLD activity for m1 and drift rates for this machine
sub_img_files = glob.glob(data_loc+'/derivatives/nistats/level_2/sub-*/contrasts/sub-*_m1.nii.gz')
sub_img_files.sort()
roi_img_files = glob.glob(data_loc+'/derivatives/rois/*_bin.nii.gz')
roi_img_files.sort()

out = []
for sub_img_file in sub_img_files:
    #each point in this image is the mean z-score for the regression coefficient between the convolved m1 regressor and BOLD activity across the 6 runs
    sub_num = re.findall('\d+', os.path.basename(sub_img_file))[0]
    print("***********************************************")
    print("Calculating cors for sub-%s"%(sub_num))
    print("***********************************************")
    sub_img = nib.load(sub_img_file)
    sub_img_data = sub_img.get_data().astype('float32')

    for roi_img_file in roi_img_files:
        #question: do the average (?) z-scores from ROIs (one per subject, per ROI) correlate with drift rates differently for each age group?
        roi_name = os.path.basename(roi_img_file).split("_")[0]
        roi_img = nib.load(roi_img_file)
        roi_img_data = roi_img.get_data().astype('bool')

        n_vox = np.argwhere(roi_img_data==True).shape[0]
        print("***********************************************")
        print("Extracting z-values for %s voxels in %s"%(str(n_vox), roi_name))
        print("***********************************************")

        voxs = np.argwhere(roi_img_data==True)
        sub_zvals = []
        for v in voxs:
            x = v[0]
            y = v[1]
            z = v[2]
            v_zval = sub_img_data[x,y,z]
            sub_zvals.append(v_zval)

        m_zvals = np.mean(sub_zvals)
        std_zvals = np.std(sub_zvals)

        out.append({'sub_id':sub_num, 'roi_name': roi_name, 'm_zvals': m_zvals, 'std_zvals': std_zvals})

pd.DataFrame(out).to_csv(data_loc+'/derivatives/rois/m1_roi_mzvals.csv')
