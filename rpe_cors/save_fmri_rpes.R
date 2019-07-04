input_path = '/Users/zeynepenkavi/Dropbox/PoldrackLab/DevStudy_Analyses/input/'

preds = list.files(path=paste0(input_path, "rl_preds/"), pattern = "All")

all_mods_pes = data.frame()

for(f in preds){
  data = read.csv(paste0(input_path, "rl_preds/", f))
  data = data %>% select(PE, sub_id, X, model)
  names(data)[which(names(data)=="PE")] = paste0("PE_",unique(data$model))
  data = data %>% select(-model)
  if(nrow(all_mods_pes)==0){
    all_mods_pes = data
  }
  else{
    all_mods_pes = all_mods_pes %>%
      left_join(data, by=c("sub_id", "X"))
  }
}

all_mods_pes = all_mods_pes %>%
  select(X, sub_id, everything())

rm(data)

names(all_mods_pes) = gsub("PE_Preds_", "", names(all_mods_pes))

exc_models = c("Fit_alpha-beta-exp_Fix_lossave_", "Fit_alpha-beta-exp-lossave_Fix_", "Fit_alpha-beta_Fix_exp-lossave_")

preds = gsub("Preds_", "", preds)
preds = gsub("All.csv", "", preds)
preds = preds[preds %in% exc_models==FALSE]

preds = c(preds, "exp_exp", "alpha_alpha", "exp_alpha")

get_fmri_pe = function(sub_data, model){
  
  if(model == "exp_exp"){
    model = c("Fit_alpha-beta-exp_neg-exp_pos-lossave_Fix_",
              "Fit_alpha-beta-exp_neg-exp_pos_Fix_lossave_",
              "Fit_alpha_neg-alpha_pos-beta-exp_neg-exp_pos_Fix_lossave_", 
              "Fit_alpha_neg-alpha_pos-beta-exp_neg-exp_pos-lossave_Fix_",
              "Fit_alpha_neg-alpha_pos-beta-exp-lossave_Fix_", 
              "Fit_alpha_neg-alpha_pos-beta-exp_Fix_lossave_")
  }
  
  if(model == "alpha_alpha"){
    model = c("Fit_alpha_neg-alpha_pos-beta_Fix_exp-lossave_", 
              "Fit_alpha_neg-alpha_pos-beta-lossave_Fix_exp_",
              "Fit_alpha-beta-lossave_Fix_exp_")
  }
  
  if(model == "exp_alpha"){
    model = c("Fit_alpha-beta-exp_neg-exp_pos-lossave_Fix_",
              "Fit_alpha-beta-exp_neg-exp_pos_Fix_lossave_",
              "Fit_alpha_neg-alpha_pos-beta-exp_neg-exp_pos_Fix_lossave_", 
              "Fit_alpha_neg-alpha_pos-beta-exp_neg-exp_pos-lossave_Fix_",
              "Fit_alpha_neg-alpha_pos-beta-exp-lossave_Fix_", 
              "Fit_alpha_neg-alpha_pos-beta-exp_Fix_lossave_",
              "Fit_alpha_neg-alpha_pos-beta_Fix_exp-lossave_", 
              "Fit_alpha_neg-alpha_pos-beta-lossave_Fix_exp_",
              "Fit_alpha-beta-lossave_Fix_exp_")
  }
  
  sub_data = sub_data %>%
    select(X, sub_id, one_of(model))
  
  #drop a column if all the predictions for that subject are NA
  drop_cols = c()
  for(col in model){
    if(sum(is.na(sub_data[,col]))==180){
      drop_cols = c(drop_cols, col)
    }
  }
  
  rem_cols = setdiff(model, drop_cols)
  
  if(length(rem_cols)>0){
    sub_data = sub_data %>%
      mutate(PE = rowSums(select(., rem_cols))/length(rem_cols)) %>%
      select(X, sub_id, PE) %>%
      filter(is.na(PE) == FALSE)
    
    
  } else{
    sub_data = data.frame(X=NA, sub_id = unique(sub_data$sub_id), PE=NA)
  }
  return(sub_data)
}

for(i in 1:length(preds)){
  fmri_pes = all_mods_pes %>%
    group_by(sub_id) %>%
    do(get_fmri_pe(., model = preds[i])) %>%
    filter(is.na(PE) == FALSE)
  
  write.csv(fmri_pes, paste0('/Users/zeynepenkavi/Dropbox/PoldrackLab/DevStudy_ServerScripts/rpe_cors/pred_rpes/',preds[i],'.csv'), row.names=FALSE)
  
}

