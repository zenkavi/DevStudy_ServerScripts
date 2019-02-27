#!/usr/bin/env python
import os, zipfile

dir_names = os.listdir("/corral-repl/utexas/poldracklab/users/zenkavi/dev_study/01_DICOM_zipfiles_from_XNAT")

zip_dirs = [x for x in dir_names if x.endswith(".zip")]

for i in zip_dirs:
	with zipfile.ZipFile('/corral-repl/utexas/poldracklab/users/zenkavi/dev_study/01_DICOM_zipfiles_from_XNAT/'+ i, 'r') as z:
		z.extractall('/corral-repl/utexas/poldracklab/users/zenkavi/dev_study/02_DICOM_data_after_unzipping')
