#!/usr/bin/env Rscript

#Bash command: Rscript --vanilla tmp.R path/to/input.mat data.csv grid.csv out.csv
args = commandArgs(trailingOnly=TRUE)

sim_data3 <- args[1]
grid_search_exp_df <- args[2]
out <- args[3]

library(plyr, lib.loc = '/work/04127/zenkavi/.r_library/')

sim_data3 <- read.csv(sim_data3)
grid_search_exp_df <- read.csv(grid_search_exp_df)

neg.log.lik.exp.fix <- function(par, data, fix_par, par_name){
  
  #par_name = vector of strings denoting the parameter to be estimated. Values: 'alpha', 'beta', 'gamma' or any combination
  #fix_par = df with names alpha, beta, gamma containing the values the parameters are fixed at.
  #par = vector of starting values that will be specified in optim. order matters: beta, alpha, gamma 
  
  beta = ifelse('beta' %in% par_name & length(par_name) == 1, par, ifelse('beta' %in% par_name & length(par_name) == 2, par[1], fix_par$beta))
  alpha = ifelse('alpha' %in% par_name & length(par_name) == 1, par, ifelse('alpha' %in% par_name & length(par_name) == 2 & 'beta' %in% par_name, p[2], ifelse('alpha' %in% par_name & length(par_name) == 2 & 'gamma' %in% par_name, p[1], fix_par$alpha)))
  gamma = ifelse('gamma' %in% par_name & length(par_name) == 1, par, ifelse('gamma' %in% par_name & length(par_name) == 2, par[2], fix_par$gamma))
  
  prob <- rep(0, nrow(data))
  err <- rep(0, nrow(data))
  ev <- c(0,0,0,0)
  for(i in 1:nrow(data)){
    prob[i] = exp(ev[data$Trial_type[i]]*beta)/(exp(ev[data$Trial_type[i]]*beta)+1)
    ev[data$Trial_type[i]] <- ifelse(data$Response[i]==1 & data$Points_earned[i] > 0, ev[data$Trial_type[i]]+alpha*(data$Points_earned[i]^gamma-ev[data$Trial_type[i]]), ifelse(data$Response[i]==1 & data$Points_earned[i] < 0, alpha*((-1)*(abs(data$Points_earned[i])^gamma)-ev[data$Trial_type[i]]), ev[data$Trial_type[i]]))
  }
  prob <- ifelse(prob == 1, 0.999999999999, 
                 ifelse(prob == 0, 0.000000000001, prob))
  err <- data$Response * log(prob) + (1 - data$Response)*log(1-prob)
  sumerr <- -sum(err)
  return(sumerr)  
}

single.alpha.exp.grid.one.row <- function(row, data){
  par <- row$beta
  tryCatch(neg.log.lik.exp.fix(par = par, data=data, fix_par = data.frame(alpha = row$alpha, gamma = row$gamma), par_name = c('beta')),error = function(e){return(NA)}) 
}

# single.alpha.exp.grid.one.row(grid_search_exp_df[1,], data=sim_data3)

tmp <- ddply(grid_search_exp_df, .(index), .progress='text',.parallel=TRUE,single.alpha.exp.grid.one.row, data=sim_data3)

write.csv(tmp, out)
