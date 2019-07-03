singularity exec -B ${DATA_LOC}:${DATA_LOC},${FS_LICENSE}:${FS_LICENSE},${OAK}/data/templateflow:/opt/templateflow /share/PI/russpold/singularity_images/poldracklab_fmriprep_1.4.1rc4-2019-06-11-34c2d062eb37.simg fmriprep $DATA_LOC $DATA_LOC/derivatives/fmriprep_1.4.0 participant -w /tmp/work --participant_label  400742 --mem-mb 50000 --nthreads 10 --omp-nthreads 8 -vv --skip_bids_validation
