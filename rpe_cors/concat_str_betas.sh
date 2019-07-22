cd /oak/stanford/groups/russpold/data/ds000054/0.0.4/derivatives/rpe_cors
cat *.csv > /oak/stanford/groups/russpold/data/ds000054/0.0.4/derivatives/rpe_cors/all_vstr_pe_betas.csv
awk '!a[$0]++' all_vstr_pe_betas.csv > all_vstr_pe_betas_clean.csv
rm all_vstr_pe_betas.csv
mv all_vstr_pe_betas_clean.csv ./all_vstr_pe_betas.csv
