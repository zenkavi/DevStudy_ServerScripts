#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)

#Usage
#Rscript --vanilla summarize_mriqc.R /oak/stanford/groups/russpold/data/ds000054/0.0.2/derivatives mriqc_0.10.5 T1w /oak/stanford/groups/russpold/users/zenkavi/DevStudy_ServerScripts/mriqc
#Rscript --vanilla summarize_mriqc.R /oak/stanford/groups/russpold/data/ds000054/0.0.2/derivatives mriqc_0.10.5 bold /oak/stanford/groups/russpold/users/zenkavi/DevStudy_ServerScripts/mriqc

input_path <- args[1]
mriqc_ver <- paste0('/',args[2], '_')
file_name <- args[3]
output_path <- args[4]

data = read.csv(paste0(input_path, mriqc_ver, file_name, '.csv'))

lib_path = Sys.getenv()[["R_LIB"]]
#install.packages(c('tidyverse'), repos='http://cran.rstudio.com/', lib = lib_path)
library(tidyverse, lib.loc = lib_path)

#"pos" if higher better, "neg" if lower better, NA if neither/unknown
valence_list = list(cjv = "neg",
                  cnr = "pos",
                  efc = "neg",
                  fber = "pos",
                  fwhm_avg = "neg",
                  fwhm_x = "neg",
                  fwhm_y = "neg",
                  fwhm_z = "neg",
                  icvs_csf = NA,
                  icvs_gm = NA,
                  icvs_wm = NA,
                  inu_med = NA,
                  inu_range = NA,
                  qi_1 = "neg",
                  qi_2 = NA,
                  rpve_csf = "neg",
                  rpve_gm = "neg",
                  rpve_wm = "neg",
                  size_x = NA,
                  size_y = NA,
                  size_z = NA,
                  snr_csf = "pos",
                  snr_gm = "pos",
                  snr_total = "pos",
                  snr_wm = "pos",
                  snrd_csf = "pos",
                  snrd_gm = "pos",
                  snrd_total = "pos",
                  snrd_wm = "pos",
                  spacing_x = NA,
                  spacing_y = NA,
                  spacing_z = NA,
                  summary_bg_k = NA,
                  summary_bg_mad = NA,
                  summary_bg_mean = NA,
                  summary_bg_median = NA,
                  summary_bg_n = NA,
                  summary_bg_p05 = NA,
                  summary_bg_p95 = NA,
                  summary_bg_stdv = NA,
                  summary_csf_k = NA,
                  summary_csf_mad = NA,
                  summary_csf_mean = NA,
                  summary_csf_median = NA,
                  summary_csf_n = NA,
                  summary_csf_p05 = NA,
                  summary_csf_p95 = NA,
                  summary_csf_stdv = NA,
                  summary_gm_k = NA,
                  summary_gm_mad = NA,
                  summary_gm_mean = NA,
                  summary_gm_median = NA,
                  summary_gm_n = NA,
                  summary_gm_p05 = NA,
                  summary_gm_p95 = NA,
                  summary_gm_stdv = NA,
                  summary_wm_k = NA,
                  summary_wm_mad = NA,
                  summary_wm_mean = NA,
                  summary_wm_median = NA,
                  summary_wm_n = NA,
                  summary_wm_p05 = NA,
                  summary_wm_p95 = NA,
                  summary_wm_stdv = NA,
                  tpm_overlap_csf = NA,
                  tpm_overlap_gm = NA,
                  tpm_overlap_wm = NA,
                  wm2max = NA,
                  aor = NA,
                  aqi = NA,
                  dummy_trs = NA,
                  dvars_nstd = NA,
                  dvars_std = NA,
                  dvars_vstd = NA,
                  fd_mean = NA,
                  fd_num = NA,
                  fd_perc = NA,
                  gcor = NA,
                  gsr_x = NA,
                  gsr_y = NA,
                  size_t = NA,
                  snr = "pos",
                  spacing_tr = NA,
                  summary_fg_k = NA,
                  summary_fg_mad = NA,
                  summary_fg_mean = NA,
                  summary_fg_median = NA,
                  summary_fg_n = NA,
                  summary_fg_p05 = NA,
                  summary_fg_p95 = NA,
                  summary_fg_stdv = NA,
                  tsnr = NA)

#strike if in the worst x if !is.na(var_df$var) else 2SD's away in either direction

out = data.frame()

for(var in names(data)[-which(names(data) %in% c("subject_id", "task_id", "run_id"))]){

  if(valence_list[var] == "pos"){
    tmp = data %>% arrange(!! as.name(var))
    strikers = tmp[1:10,"subject_id"]
  }
  if(valence_list[var] == "neg"){
    tmp = data %>% arrange(-!! as.name(var))
    strikers = tmp[1:10,"subject_id"]
  }
  if(is.na(valence_list[var])){
    tmp = data
    tmp[,var] = abs(scale(tmp[,var]))
    tmp = tmp %>%
      mutate(strike = ifelse(!!as.name(var)>2,1,0)) %>%
      filter(strike == 1)
    strikers = tmp[, "subject_id"]
  }

  if(length(strikers)>0){
    tmp_out = data.frame(var = var, strikers = strikers)
  }

  out = plyr::rbind.fill(out, tmp_out)
}

get_strike_vars = function(x){
  return(data.frame(vars = paste(c(as.character(x$var)), collapse = ', ')))
}

a = out %>%
  group_by(strikers) %>%
  tally

b = out %>%
  group_by(strikers) %>%
  do(get_strike_vars(.))

out_df = a %>%
  left_join(b, by = c("strikers")) %>%
  rename(num_strikes=n) %>%
  arrange(-num_strikes)

write.csv(out_df, paste0(output_path, mriqc_ver, file_name, '_summary.csv'))
