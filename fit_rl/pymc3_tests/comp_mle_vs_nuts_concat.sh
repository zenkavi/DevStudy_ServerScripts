cd /oak/stanford/groups/russpold/users/zenkavi/DevStudy_ServerScripts/fit_rl/pymc3_tests/.comp_out
cat est_df_*.csv > est_df_merged.csv
awk '!a[$0]++' est_df_merged.csv > est_df_merged_clean.csv
rm est_df_merged.csv
mv est_df_merged_clean.csv ./est_df_merged.csv
