#!/usr/bin/env python
import os
import sys
import shutil
from collections import Counter
#sys.path.append('/corral-repl/utexas/poldracklab/users/wtriplet/opt/anaconda2/lib/python2.7/site-packages')
sys.path = ['',
 '/opt/apps/intel16/python/2.7.11/lib/python2.7/site-packages/setuptools-20.2.2-py2.7.egg',
 '/opt/apps/intel16/python/2.7.11/lib/python2.7/site-packages/pip-8.1.0-py2.7.egg',
 '/opt/apps/intel16/python/2.7.11/lib/python2.7/site-packages/matplotlib-1.5.1-py2.7-linux-x86_64.egg',
 '/opt/apps/intel16/python/2.7.11/lib/python2.7/site-packages/pyparsing-2.1.0-py2.7.egg',
 '/opt/apps/intel16/python/2.7.11/lib/python2.7/site-packages/cycler-0.10.0-py2.7.egg',
 '/opt/apps/intel16/python/2.7.11/lib/python2.7/site-packages/pytz-2015.7-py2.7.egg',
 '/opt/apps/intel16/python/2.7.11/lib/python2.7/site-packages/python_dateutil-2.5.0-py2.7.egg',
 '/opt/apps/intel16/python/2.7.11/lib/python2.7/site-packages',
 '/opt/apps/intel16/python/2.7.11/bin',
 '/opt/apps/intel16/cray_mpich_7_3/python/2.7.11/lib/python2.7/site-packages',
 '/work/01329/poldrack/lonestar/software_lonestar5/anaconda/Anaconda2-4.1.1/lib/python2.7/site-packages',
 '/opt/apps/intel16/python/2.7.11/lib/python27.zip',
 '/opt/apps/intel16/python/2.7.11/lib/python2.7',
 '/opt/apps/intel16/python/2.7.11/lib/python2.7/plat-linux2',
 '/opt/apps/intel16/python/2.7.11/lib/python2.7/lib-tk',
 '/opt/apps/intel16/python/2.7.11/lib/python2.7/lib-old',
 '/opt/apps/intel16/python/2.7.11/lib/python2.7/lib-dynload',
 '/opt/apps/intel16/python/2.7.11/lib/python2.7/site-packages/IPython/extensions',
 '/home1/04127/zenkavi/.ipython']

import nibabel as nb

if len(sys.argv) < 3:
    sys.exit("Usage: moveNiftisToBids.py nifti_path bids_path sub_id")

nifti_path = sys.argv[1] #make sure paths end with '/'
bids_path = sys.argv[2]
sub_id = sys.argv[3]

contents = os.listdir(nifti_path)

def setExtension(file_name):
	extension = os.path.splitext(file_name)[1]
	extension = '.nii.gz' if extension == '.gz' else '.json'
	return extension

def getNameAssignment(name_string, assignment_dict):
	return assignment_dict[name_string.split(".")[0]]

##################################################################

anat_files =  [s for s in contents if "T1w" in s]

[ shutil.copyfile(nifti_path+x, bids_path+'anat/sub-'+sub_id+'_T1w'+setExtension(x)) for x in anat_files ]

if len(os.listdir(bids_path+'anat/'))<2:
	print('Post anat_image move: Double check '+sub_id+'/anat')

##################################################################

fmap_files = [s for s in contents if "fieldmap" in s]

scan_numbers = [int(filter(str.isdigit, x.split("_")[3])) for x in fmap_files]

mag_images = []
phasediff_images = []

for i in range(len(scan_numbers)):
	if Counter(scan_numbers)[scan_numbers[i]] == 4:
		mag_images.append(fmap_files[i])
	else:
		phasediff_images.append(fmap_files[i])
		
mag_image_unique_names = list(set([x.split(".")[0] for x in mag_images]))

mag_image_name_assignments = {}

for i in range(len(mag_image_unique_names)):
	mag_image_name_assignments[mag_image_unique_names[i]] = 'sub-'+sub_id+'_magnitude'+str(i+1)

for i in range(len(mag_images)):
	shutil.copy(nifti_path+mag_images[i], bids_path+'fmap/'+getNameAssignment(mag_images[i], mag_image_name_assignments)+setExtension(mag_images[i]))
	
if len(os.listdir(bids_path+'fmap/'))<4:
	print('Post mag_image move: Double check '+sub_id+'/fmap')

phasediff_image_unique_names = list(set([x.split(".")[0] for x in phasediff_images]))

phasediff_image_name_assignments = {}

for i in range(len(phasediff_image_unique_names)):
	if len(phasediff_image_unique_names) == 1:
		phasediff_image_name_assignments[phasediff_image_unique_names[i]] = 'sub-'+sub_id+'_phasediff'
	else:		
		phasediff_image_name_assignments[phasediff_image_unique_names[i]] = 'sub-'+sub_id+'_phasediff'+str(i+1)

for i in range(len(phasediff_images)):
	shutil.copy(nifti_path+phasediff_images[i], bids_path+'fmap/'+getNameAssignment(phasediff_images[i], phasediff_image_name_assignments)+setExtension(phasediff_images[i]))
	
if len(os.listdir(bids_path+'fmap/'))<6:
	print('Post phasediff_image move: Double check '+sub_id+'/fmap')

##################################################################

func_files = [s for s in contents if "task" in s]

func_images = [x for x in func_files if os.path.splitext(x)[1] != '.json']

func_scans = [x for x in func_images if len(nb.load(nifti_path+x).header.get_data_shape()) == 4]

sbref_scans = [x for x in func_images if len(nb.load(nifti_path+x).header.get_data_shape()) == 3]
		
func_image_unique_names = list(set([x.split(".")[0] for x in func_scans]))

sbref_image_unique_names = list(set([x.split(".")[0] for x in sbref_scans]))

func_image_name_assignments = {}

for i in range(len(func_image_unique_names)):
	func_image_name_assignments[func_image_unique_names[i]] = 'sub-'+sub_id+'_task-machinegame_run-0'+str(int(filter(str.isdigit,func_image_unique_names[i].split("_")[2])))+'_bold'

sbref_image_name_assignments = {}

for i in range(len(sbref_image_unique_names)):
	sbref_image_name_assignments[sbref_image_unique_names[i]] = 'sub-'+sub_id+'_task-machinegame_run-0'+str(int(filter(str.isdigit,sbref_image_unique_names[i].split("_")[2])))+'_sbref'
	
func_to_copy = [x for x in func_files if x.split(".")[0] in func_image_unique_names]

sbref_to_copy = [x for x in func_files if x.split(".")[0] in sbref_image_unique_names]

for i in range(len(func_to_copy)):
	shutil.copy(nifti_path+func_to_copy[i], bids_path+'func/'+getNameAssignment(func_to_copy[i], func_image_name_assignments)+setExtension(func_to_copy[i]))
	
if len(os.listdir(bids_path+'func/'))<18:
	print('Post func_image move: Double check '+sub_id+'/func')

for i in range(len(sbref_to_copy)):
	shutil.copy(nifti_path+sbref_to_copy[i], bids_path+'func/'+getNameAssignment(sbref_to_copy[i], sbref_image_name_assignments)+setExtension(sbref_to_copy[i])) 

if len(os.listdir(bids_path+'func/'))<30:
	print('Post sbref_image move: Double check '+sub_id+'/func')
