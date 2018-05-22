#!/usr/bin/env python
import os

sub_dir_list = os.listdir("/corral-repl/utexas/poldracklab/users/zenkavi/dev_study/02_DICOM_data_after_unzipping")

print('#!/bin/bash')

for i in sub_dir_list:
	os.mkdir("/corral-repl/utexas/poldracklab/users/zenkavi/dev_study/03_DICOM_to_NIFTI_conversions/"+i)
	scan_dir_list = os.listdir("/corral-repl/utexas/poldracklab/users/zenkavi/dev_study/02_DICOM_data_after_unzipping/"+i+"/scans/")
	for j in scan_dir_list:
		command = "dcm2niix -o /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/03_DICOM_to_NIFTI_conversions/" + i + " -z y -b y /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/02_DICOM_data_after_unzipping/" + i + "/scans/" + j + "/resources/DICOM/files"
		print(command)
