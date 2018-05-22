import os
dicom_dirs = os.listdir('/corral-repl/utexas/poldracklab/users/zenkavi/dev_study/02_DICOM_data_after_unzipping/')
for i in range(len(dicom_dirs)):
    os.mkdir('/corral-repl/utexas/poldracklab/users/zenkavi/dev_study/03_DICOM_to_NIFTI_conversions/'+dicom_dirs[i])
