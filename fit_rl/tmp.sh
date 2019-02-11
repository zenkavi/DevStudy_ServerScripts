set -e
for task_list in  fit_beta-exp_neg_fix_alpha-exp_pos_task_list.sh fit_alpha-beta_fix_exp_task_list.sh
do
sed -e "s/{TASK_LIST}/$task_list/g" fit_rl.batch | sbatch
done
