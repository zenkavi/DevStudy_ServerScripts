module load system
export DATA_LOC=/oak/stanford/groups/russpold/data/ds000054/0.0.2
export SERVER_SCRIPTS=/oak/stanford/groups/russpold/users/zenkavi/DevStudy_ServerScripts
singularity exec /share/PI/russpold/singularity_images/poldracklab_fmriprep_1.2.5-2018-12-04-2ef6b23ede2a.img bids-validator --verbose $DATA_LOC > $SERVER_SCRIPTS/bidsify/validator_out.txt
