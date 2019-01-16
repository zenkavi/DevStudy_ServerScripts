#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)

input_path <- args[1]
mriqc_ver <- paste0('/',args[2], '_')
file_name <- args[3]
output_path <- args[4]

data = read.csv(paste0(input_path, mriqc_ver, file_name, '.csv'))

sum_df = data.frame()

write.csv(sum_df, paste0(output_path, mriqc_ver, file_name, '_summary.csv'))