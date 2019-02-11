set -e
for task_list in  fit_alpha_neg-alpha_pos-beta_fix_exp_task_list.sh fit_alpha-beta_fix_exp_task_list.sh
do
sed -e "s/{TASK_LIST}/$task_list/g" fit_rl.batch | sbatch
done
