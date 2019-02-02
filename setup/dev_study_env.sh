# change paths and modules depending on cluster
# sherlock
if [ $HOME == '/home/users/zenkavi' ]; then
  module load system
  module load x11
  module load libmng
  source activate dev_study
  export TODO_PATH=/oak/stanford/groups/russpold/data/ds000054/todo
  export SERVER_SCRIPTS=/oak/stanford/groups/russpold/users/zenkavi/DevStudy_ServerScripts
  export DATA_LOC=/oak/stanford/groups/russpold/data/ds000054/0.0.2
  export R_LIB=/home/groups/russpold/software/miniconda/envs/dev_study/lib/R/library
# tacc
else
  source activate dev_study
  export TODO_PATH=/corral-repl/utexas/poldracklab/users/zenkavi/dev_study/todo
  export SERVER_SCRIPTS=/corral-repl/utexas/poldracklab/users/zenkavi/dev_study/DevStudy_ServerScripts
  export DATA_LOC=/corral-repl/utexas/poldracklab/users/zenkavi/dev_study/data
  export R_LIB=/work/04127/zenkavi/.r_library
  # module load dcm2niix/7July2016
  # module load Rstats/3.2.1
fi
