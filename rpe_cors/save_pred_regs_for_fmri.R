input_path = '/Users/zeynepenkavi/Dropbox/PoldrackLab/DevStudy_Analyses/input/'

source('/Users/zeynepenkavi/Dropbox/PoldrackLab/DevStudy_Analyses/code/helper_functions/rbind_all_columns.R')

preds = list.files(path=paste0(input_path, "rl_preds/"), pattern = "All")

all_mods_preds = data.frame()

for(f in preds){
  data = read.csv(paste0(input_path, "rl_preds/", f))
  all_mods_preds = rbind.all.columns(all_mods_preds,data.frame(data))
}

rm(data)

all_mods_preds$model = gsub("Preds_", "", all_mods_preds$model)

all_mods_pes = all_mods_preds %>%
  select(X, PE, sub_id, model) %>%
  spread(model, PE)

all_mods_evs = all_mods_preds %>%
  select(X, EV, sub_id, model) %>%
  spread(model, EV)

exc_models = c("Fit_alpha-beta-exp_Fix_lossave_", "Fit_alpha-beta-exp-lossave_Fix_", "Fit_alpha-beta_Fix_exp-lossave_")

preds = gsub("Preds_", "", preds)
preds = gsub("All.csv", "", preds)
preds = preds[preds %in% exc_models==FALSE]

preds = c(preds, "exp_exp", "alpha_alpha", "exp_alpha")

get_fmri_reg = function(sub_data, model, type="pe"){
  
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
    if(type == "pe"){
      sub_data = sub_data %>%
        mutate(PE = rowSums(select(., rem_cols))/length(rem_cols)) %>%
        select(X, sub_id, PE) %>%
        filter(is.na(PE) == FALSE)
    }
    if(type == "ev"){
      sub_data = sub_data %>%
        mutate(EV = rowSums(select(., rem_cols))/length(rem_cols)) %>%
        select(X, sub_id, EV)
    }
  } else{
    if(type == "pe"){
      sub_data = data.frame(X=NA, sub_id = unique(sub_data$sub_id), PE=NA)
    }
    if(type == "ev"){
      sub_data = data.frame(X=NA, sub_id = unique(sub_data$sub_id), EV=NA)
    }
  }
  return(sub_data)
}

type = "ev"

for(i in 1:length(preds)){
  
  if(type == "pe"){
    fmri_pes = all_mods_pes %>%
      group_by(sub_id) %>%
      do(get_fmri_reg(., model = preds[i], type="pe")) %>%
      filter(is.na(PE) == FALSE)
    
    write.csv(fmri_pes, paste0('/Users/zeynepenkavi/Dropbox/PoldrackLab/DevStudy_ServerScripts/rpe_cors/pred_rpes/',preds[i],'.csv'), row.names=FALSE) 
  }
  if(type == "ev"){
    fmri_evs = all_mods_evs %>%
      group_by(sub_id) %>%
      do(get_fmri_reg(., model = preds[i], type="ev")) %>%
      mutate(EV=ifelse(is.na(EV), 0, EV))
    
    write.csv(fmri_evs, paste0('/Users/zeynepenkavi/Dropbox/PoldrackLab/DevStudy_ServerScripts/rpe_cors/pred_evs/',preds[i],'.csv'), row.names=FALSE) 
  }
  
}

