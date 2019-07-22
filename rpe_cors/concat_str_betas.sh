cd /oak/stanford/groups/russpold/data/ds000054/0.0.4/derivatives/rpe_cors
cat *.csv > /oak/stanford/groups/russpold/data/ds000054/0.0.4/derivatives/rpe_cors/all_str_pe_betas.csv
awk '!a[$0]++' all_str_pe_betas.csv > all_str_pe_betas_clean.csv
rm all_str_pe_betas.csv
mv all_str_pe_betas_clean.csv ./all_str_pe_betas.csv
