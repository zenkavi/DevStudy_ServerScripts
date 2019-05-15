#!/usr/bin/Rscript
library(tidyverse)

pe = TRUE

if(pe){
  tmp1 = data.frame(V1=system("find /oak/stanford/groups/russpold/data/ds000054/0.0.4/derivatives/nistats/level_1 -name 'sub-*_run-*_l1_pe_glm.pkl' | sort", intern=TRUE))
} else{
  tmp1 = data.frame(V1=system("find /oak/stanford/groups/russpold/data/ds000054/0.0.4/derivatives/nistats/level_1 -name 'sub-*_run-*_l1_glm.pkl' | sort", intern=TRUE))
}

tmp2 = read.table("/oak/stanford/groups/russpold/users/zenkavi/DevStudy_ServerScripts/fsl/level_1/level1_task_list.sh")

tmp1 = tmp1 %>%
  mutate(V1 = gsub("/oak/stanford/groups/russpold/data/ds000054/0.0.4/derivatives/nistats/level_1/", "", V1)) %>%
  separate(V1, into = c("a", "b"), sep="/") %>%
  select(b)

if(pe){
  tmp1 = tmp1 %>% mutate(b = gsub("_pe_glm.pkl", "", b))
} else {
  tmp1 = tmp1 %>% mutate(b = gsub("_glm.pkl", "", b))
}

tmp2 = tmp2 %>%
  separate(V2, into=c("a", "b", "c", "d", "e", "f"), sep = '/') %>%
  select(f) %>%
  mutate(f = gsub(".fsf", "",f))

failed_runs = data.frame(tmp2$f[tmp2$f %in% tmp1$b == FALSE])
names(failed_runs) = "V1"
failed_subs = failed_runs %>%
  separate(V1, into = c("a", "b", "c"), sep="_")
failed_subs = unique(failed_subs$a)
failed_subs = gsub("sub-", "", failed_subs)

debug_jobs = data.frame(job = rep(NA, length(failed_subs)))
for(i in 1:length(failed_subs)){
  debug_jobs$job[i] = paste0("python level_1.py -s ", failed_subs[i])
}

print("Saving debug jobs...")
write.table(debug_jobs, file = "/oak/stanford/groups/russpold/users/zenkavi/DevStudy_ServerScripts/nistats/level_1/l1_debug_jobs.sh", quote=FALSE, row.names=FALSE, col.names=FALSE)
print("Submitting debug jobs...")
system("sbatch run_l1_debug_jobs.batch")
