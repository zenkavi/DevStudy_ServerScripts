cd /oak/stanford/groups/russpold/data/ds000054/0.0.4/derivatives/func_con/seed2seed
cat ./*/sub-*_run-0*_partial-correlation-matrix.csv > all_seed2seed_cors.csv
awk '!a[$0]++' all_seed2seed_cors.csv >all_seed2seed_cors_clean.csv
rm all_seed2seed_cors.csv
mv all_seed2seed_cors_clean.csv ./all_seed2seed_cors.csv
