while read task; do
  sed "s/{TASK}/$task/g" run_heudiconv.batch | sbatch
done <heudiconv_tasklist.txt
