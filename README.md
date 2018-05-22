File descriptions
==========================

`check_bold_vols.py`: Script from Mumford video tutorials to check the volume of all bold niftis.

`convertBARTmat2tsv.R`: R script to convert Matlab output files for the BART behavioral data in to tsv's that can be saved sub/behav BIDS directories

`dev_study_env.sh`: Shell script to setup the environment used for the analyses for this study.

`exec_convert_bart_mat_to_tsv.sh`: Shell script with commands calling the R script that converts the .mat behavioral BART data to .tsv's and saves in sub/behav BIDS directories

`exec_convert_dicoms_to_niftis.sh`: Shell script with commands to python script that converts the dicoms to niftis for each subject (separate commands for each subject for parallelization of batch job)

`exec_fix_fmap_jsons.sh`: Shell script with commands calling python script on each subject's BIDS directory to take the fieldmap json's output by dcm2niix by default and add the two echo times to each of them to be able to run the fieldmap workflow.

`exec_make_run_events.sh`: Shell script with commands to call python script that split the fMRI behavioral data in to tsv's with onsets for each event in each run for sub/func BIDS directories

`exec_move_niftis_to_bids.sh`: Shell script with commands to call python script for each subject that moves the converted nifti's to the correct BIDS directories

`fix_fmap_jsons.py`: Python script to extract both echo time data and add it to the default dcm2niix output for fieldmap image jsons.

`make_bids_content_dirs.py`: Python script that loops through all subject BIDS directories and creates directories for the contents (e.g. anat, func etc.)

`make_bids_subject_dirs.py`: Python script that take in the sub\_dirname\_list.txt file and creates a BIDS directory for each

`make_commands_for_bart_conversion.py`: Python script that populates text file with commands calling BART data conversion R script

`make_commands_for_fmap_jsons.py`: Python script that populate shell script with commands for each subect to fix the fieldmap jsons

`make_commands_for_move_niftis.py`: Python script that makes shell script commands to execute `move_niftis_to_bids.py` on each subject. Requires `sub_dirname_match_list.tsv`.

`make_commands_for_nifti_conversion.py`: Python script to create command for each subject that will be used in shell script to convert dicoms to niftis

`make_commands_for_run_events.py`: Python script that created shell commands to run python script that split the fMRI behavioral data in to csv's for each run for each subject 

`make_nifti_dirs.py`: Python script that creates directories in the path where the dicom files will be converted to niftis. Loops through, not for batch.

`make_run_events.py`: Python script that split the behavioral fMRI data in to runs and converts them to tsv's that will be stored in sub/func BIDS directories

`move_niftis_to_bids.py`: Python script that copies and renames nifti's and json's in a specificied nifti_path to a given bids_path with the appropriate directory structure. 

`sbatch_template.sbatch`: Example batch script (not used)

`sub_dirname_list.txt`: list of subject numbers that will be used to create BIDS directories for each subjects 

`sub_dirname_match_list_tsv`: File containing nifti_paths in first column and bids_paths in second column that will be used to create the shell commands populating the arguments for `move_niftis_to_bids.py`.

`unzip_dicom_dirs.py`: Python script to loop through and unzip the DICOM directories

Command order
==========================

```bash
source dev_study_env.sh

make_bids_subject_dirs.py

make_bids_content_dirs.py

unzip_dicom_dirs.py

python make_commands_for_nifti_conversion.py > exec_convert_dicoms_to_niftis.sh

make_nifti_dirs.py

launch -s /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/scripts/exec_convert_dicoms_to_niftis.sh -j dcm2nii -q normal -m zenkavi@stanford.edu

python make_commands_for_run_events.py > exec_make_run_events.sh

launch -s /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/scripts/exec_make_run_events.sh -j runevs  

python make_commands_for_bart_conversion.py > exec_convert_bart_mat_to_tsv.sh

launch -s /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/scripts/exec_convert_bart_mat_to_tsv.sh -j bartconv

python make_commands_for_move_niftis.py > exec_move_niftis_to_bids.sh

launch -s /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/scripts/exec_move_niftis_to_bids.sh -j movenii

python make_commands_for_fmap_jsons.py > exec_fix_fmap_jsons.sh

laucnch -s /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/scripts/exec_fix_fmap_jsons.sh

```
