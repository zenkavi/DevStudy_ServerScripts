jobnum=0
while read task; do
  ((jobnum++))
  sed -e "s/{TASK}/$task/g" -e "s/{JOBNUM}/$jobnum/g" run_heudiconv.batch | sbatch
done <heudiconv_tasklist.txt
