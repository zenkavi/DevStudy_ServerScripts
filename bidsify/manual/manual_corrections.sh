#sub-405027 corrections
mv sub-405027_2/ ./sub-405027
rename sub-405027_2 sub-405027 *

#sub-407260 corrections: same as sub-407260
rm -rf sub-407260_b

#remove test scans
rm -rf sub-test

#replace 200067 with 200027 in participants.tsv

#rm second events file for first run for 100110
#because in /corral-repl/utexas/poldracklab/users/shelfins/Developmental_Study/data/machine_game the first tsv is used for parameter calculation as seen in NoHead.csv file
rm sub-100110_2_task-machinegame_run-001_events.tsv

#change multiple fmaps to runs

#Based on /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/02_DICOM_data_after_unzipping/DevStudy_100009/scans
#first fieldmaps intended for runs 1,2
#second fieldmaps intended for runs 3,4,5,6
mv sub-100009_magnitude1.nii.gz ./sub-100009_run-01_magnitude1.nii.gz
mv sub-100009_magnitude1.json ./sub-100009_run-01_magnitude1.json
mv sub-100009_magnitude2.nii.gz ./sub-100009_run-01_magnitude2.nii.gz
mv sub-100009_magnitude2.json ./sub-100009_run-01_magnitude2.json
mv sub-100009_magnitude3.nii.gz ./sub-100009_run-02_magnitude1.nii.gz
mv sub-100009_magnitude3.json ./sub-100009_run-02_magnitude1.json
mv sub-100009_magnitude4.nii.gz ./sub-100009_run-02_magnitude2.nii.gz
mv sub-100009_magnitude4.json ./sub-100009_run-02_magnitude2.json
mv sub-100009_phasediff1.nii.gz ./sub-100009_run-01_phasediff.nii.gz
mv sub-100009_phasediff1.json ./sub-100009_run-01_phasediff.json
mv sub-100009_phasediff2.nii.gz ./sub-100009_run-02_phasediff.nii.gz
mv sub-100009_phasediff2.json ./sub-100009_run-02_phasediff.json

#Based on /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/02_DICOM_data_after_unzipping/devstudy_100051/scans
#first fieldmaps intended for runs -
#second fieldmaps intended for runs 1-6
mv sub-100051_magnitude1.nii.gz ./sub-100051_run-01_magnitude1.nii.gz
mv sub-100051_magnitude1.json ./sub-100051_run-01_magnitude1.json
mv sub-100051_magnitude2.nii.gz ./sub-100051_run-01_magnitude2.nii.gz
mv sub-100051_magnitude2.json ./sub-100051_run-01_magnitude2.json
mv sub-100051_magnitude3.nii.gz ./sub-100051_run-02_magnitude1.nii.gz
mv sub-100051_magnitude3.json ./sub-100051_run-02_magnitude1.json
mv sub-100051_magnitude4.nii.gz ./sub-100051_run-02_magnitude2.nii.gz
mv sub-100051_magnitude4.json ./sub-100051_run-02_magnitude2.json
mv sub-100051_phasediff1.nii.gz ./sub-100051_run-01_phasediff.nii.gz
mv sub-100051_phasediff1.json ./sub-100051_run-01_phasediff.json
mv sub-100051_phasediff2.nii.gz ./sub-100051_run-02_phasediff.nii.gz
mv sub-100051_phasediff2.json ./sub-100051_run-02_phasediff.json

#Based on /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/03_DICOM_to_NIFTI_conversions/100062_DS
#first fieldmaps inteded for runs: 1
#second fieldmaps inteded for runs: -
#third fieldmaps inteded for runs: 2,3,4,5,6
mv sub-100062_magnitude1.nii.gz ./sub-100062_run-01_magnitude1.nii.gz
mv sub-100062_magnitude1.json ./sub-100062_run-01_magnitude1.json
mv sub-100062_magnitude2.nii.gz ./sub-100062_run-01_magnitude2.nii.gz
mv sub-100062_magnitude2.json ./sub-100062_run-01_magnitude2.json
mv sub-100062_magnitude3.nii.gz ./sub-100062_run-02_magnitude1.nii.gz
mv sub-100062_magnitude3.json ./sub-100062_run-02_magnitude1.json
mv sub-100062_magnitude4.nii.gz ./sub-100062_run-02_magnitude2.nii.gz
mv sub-100062_magnitude4.json ./sub-100062_run-02_magnitude2.json
mv sub-100062_magnitude5.nii.gz ./sub-100062_run-03_magnitude1.nii.gz
mv sub-100062_magnitude5.json ./sub-100062_run-03_magnitude1.json
mv sub-100062_magnitude6.nii.gz ./sub-100062_run-03_magnitude2.nii.gz
mv sub-100062_magnitude6.json ./sub-100062_run-03_magnitude2.json
mv sub-100062_phasediff1.nii.gz ./sub-100062_run-01_phasediff.nii.gz
mv sub-100062_phasediff1.json ./sub-100062_run-01_phasediff.json
mv sub-100062_phasediff2.nii.gz ./sub-100062_run-02_phasediff.nii.gz
mv sub-100062_phasediff2.json ./sub-100062_run-02_phasediff.json
mv sub-100062_phasediff3.nii.gz ./sub-100062_run-03_phasediff.nii.gz
mv sub-100062_phasediff3.json ./sub-100062_run-03_phasediff.json

#Based on /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/02_DICOM_data_after_unzipping/DevStudy_100103/scans
#first fieldmaps intended for runs -
#second fieldmaps intended for runs 1-6
mv sub-100103_magnitude1.nii.gz ./sub-100103_run-01_magnitude1.nii.gz
mv sub-100103_magnitude1.json ./sub-100103_run-01_magnitude1.json
mv sub-100103_magnitude2.nii.gz ./sub-100103_run-01_magnitude2.nii.gz
mv sub-100103_magnitude2.json ./sub-100103_run-01_magnitude2.json
mv sub-100103_magnitude3.nii.gz ./sub-100103_run-02_magnitude1.nii.gz
mv sub-100103_magnitude3.json ./sub-100103_run-02_magnitude1.json
mv sub-100103_magnitude4.nii.gz ./sub-100103_run-02_magnitude2.nii.gz
mv sub-100103_magnitude4.json ./sub-100103_run-02_magnitude2.json
mv sub-100103_phasediff1.nii.gz ./sub-100103_run-01_phasediff.nii.gz
mv sub-100103_phasediff1.json ./sub-100103_run-01_phasediff.json
mv sub-100103_phasediff2.nii.gz ./sub-100103_run-02_phasediff.nii.gz
mv sub-100103_phasediff2.json ./sub-100103_run-02_phasediff.json

#Based on /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/02_DICOM_data_after_unzipping/devstudy_100188/scans
#first fieldmaps intended for runs 1-4
#second fieldmaps intended for runs 5-6
mv sub-100188_magnitude1.nii.gz ./sub-100188_run-01_magnitude1.nii.gz
mv sub-100188_magnitude1.json ./sub-100188_run-01_magnitude1.json
mv sub-100188_magnitude2.nii.gz ./sub-100188_run-01_magnitude2.nii.gz
mv sub-100188_magnitude2.json ./sub-100188_run-01_magnitude2.json
mv sub-100188_magnitude3.nii.gz ./sub-100188_run-02_magnitude1.nii.gz
mv sub-100188_magnitude3.json ./sub-100188_run-02_magnitude1.json
mv sub-100188_magnitude4.nii.gz ./sub-100188_run-02_magnitude2.nii.gz
mv sub-100188_magnitude4.json ./sub-100188_run-02_magnitude2.json
mv sub-100188_phasediff1.nii.gz ./sub-100188_run-01_phasediff.nii.gz
mv sub-100188_phasediff1.json ./sub-100188_run-01_phasediff.json
mv sub-100188_phasediff2.nii.gz ./sub-100188_run-02_phasediff.nii.gz
mv sub-100188_phasediff2.json ./sub-100188_run-02_phasediff.json

#Based on /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/02_DICOM_data_after_unzipping/DevStudy_100241/scans
#first fieldmaps intended for runs 1-4
#second fieldmaps intended for runs 5-6
mv sub-100241_magnitude1.nii.gz ./sub-100241_run-01_magnitude1.nii.gz
mv sub-100241_magnitude1.json ./sub-100241_run-01_magnitude1.json
mv sub-100241_magnitude2.nii.gz ./sub-100241_run-01_magnitude2.nii.gz
mv sub-100241_magnitude2.json ./sub-100241_run-01_magnitude2.json
mv sub-100241_magnitude3.nii.gz ./sub-100241_run-02_magnitude1.nii.gz
mv sub-100241_magnitude3.json ./sub-100241_run-02_magnitude1.json
mv sub-100241_magnitude4.nii.gz ./sub-100241_run-02_magnitude2.nii.gz
mv sub-100241_magnitude4.json ./sub-100241_run-02_magnitude2.json
mv sub-100241_phasediff1.nii.gz ./sub-100241_run-01_phasediff.nii.gz
mv sub-100241_phasediff1.json ./sub-100241_run-01_phasediff.json
mv sub-100241_phasediff2.nii.gz ./sub-100241_run-02_phasediff.nii.gz
mv sub-100241_phasediff2.json ./sub-100241_run-02_phasediff.json

#Based on /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/03_DICOM_to_NIFTI_conversions/DevStudy_200056
#first fieldmaps intended for runs -
#second fieldmaps intended for runs 1-6
mv sub-200056_magnitude1.nii.gz ./sub-200056_run-01_magnitude1.nii.gz
mv sub-200056_magnitude1.json ./sub-200056_run-01_magnitude1.json
mv sub-200056_magnitude2.nii.gz ./sub-200056_run-01_magnitude2.nii.gz
mv sub-200056_magnitude2.json ./sub-200056_run-01_magnitude2.json
mv sub-200056_magnitude3.nii.gz ./sub-200056_run-02_magnitude1.nii.gz
mv sub-200056_magnitude3.json ./sub-200056_run-02_magnitude1.json
mv sub-200056_magnitude4.nii.gz ./sub-200056_run-02_magnitude2.nii.gz
mv sub-200056_magnitude4.json ./sub-200056_run-02_magnitude2.json
mv sub-200056_phasediff1.nii.gz ./sub-200056_run-01_phasediff.nii.gz
mv sub-200056_phasediff1.json ./sub-200056_run-01_phasediff.json
mv sub-200056_phasediff2.nii.gz ./sub-200056_run-02_phasediff.nii.gz
mv sub-200056_phasediff2.json ./sub-200056_run-02_phasediff.json

#Based on /corral-repl/utexas/poldracklab/users/zenkavi/dev_study/03_DICOM_to_NIFTI_conversions/devstudy_306065
#first fieldmaps intended for runs 1
#second fieldmaps intended for runs -
#third fieldmaps intended for runs 2-6
mv sub-306065_magnitude1.nii.gz ./sub-306065_run-01_magnitude1.nii.gz
mv sub-306065_magnitude1.json ./sub-306065_run-01_magnitude1.json
mv sub-306065_magnitude2.nii.gz ./sub-306065_run-01_magnitude2.nii.gz
mv sub-306065_magnitude2.json ./sub-306065_run-01_magnitude2.json
mv sub-306065_magnitude3.nii.gz ./sub-306065_run-02_magnitude1.nii.gz
mv sub-306065_magnitude3.json ./sub-306065_run-02_magnitude1.json
mv sub-306065_magnitude4.nii.gz ./sub-306065_run-02_magnitude2.nii.gz
mv sub-306065_magnitude4.json ./sub-306065_run-02_magnitude2.json
mv sub-306065_magnitude5.nii.gz ./sub-306065_run-03_magnitude1.nii.gz
mv sub-306065_magnitude5.json ./sub-306065_run-03_magnitude1.json
mv sub-306065_magnitude6.nii.gz ./sub-306065_run-03_magnitude2.nii.gz
mv sub-306065_magnitude6.json ./sub-306065_run-03_magnitude2.json
mv sub-306065_phasediff1.nii.gz ./sub-306065_run-01_phasediff.nii.gz
mv sub-306065_phasediff1.json ./sub-306065_run-01_phasediff.json
mv sub-306065_phasediff2.nii.gz ./sub-306065_run-02_phasediff.nii.gz
mv sub-306065_phasediff2.json ./sub-306065_run-02_phasediff.json
mv sub-306065_phasediff3.nii.gz ./sub-306065_run-03_phasediff.nii.gz
mv sub-306065_phasediff3.json ./sub-306065_run-03_phasediff.json
