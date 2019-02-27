jobnum=0
while read task; do
  jobnum=$[$jobnum +1]
  sed "s/{TASK}/$task/g" "s/{JOBNUM}/$jobnum/g" run_heudiconv.batch | sbatch
done <heudiconv_tasklist.txt
