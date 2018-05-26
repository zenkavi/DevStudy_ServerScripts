#!/usr/bin/env Rscript

#Bash command: Rscript --vanilla convertBARTmat2tsv.R path/to/input.mat path/to/out.tsv path/to/out.json
args = commandArgs(trailingOnly=TRUE)

#lib_path = Sys.getenv()[["R_LIB"]]
#todo_path = Sys.getenv()[["TODO_PATH"]]
#data_path = Sys.getenv()[["DATA_LOC"]]

#inputPath <- paste0(todo_path,args[1])
#outputPath <- paste0(data_path,args[2])

inputPath <- args[1]
outputPath <- args[2]

#install.packages(c('R.matlab', 'RJSONIO', 'plyr'), repos='http://cran.rstudio.com/', lib = '/work/04127/zenkavi/.r_library/')
library(R.matlab, lib.loc = lib_path)
library(RJSONIO, lib.loc = lib_path)
library(plyr, lib.loc = lib_path)

mat <- readMat(inputPath)

listForJson <- list(ans = mat$ans,
                    script.name = mat$script.name,
                    revision.data = mat$revision.date,
                    script.version = mat$script.version,
                    subject.code = mat$subject.code,
                    c = mat$c,
                    logfile = mat$logfile,
                    MRI = mat$MRI,
                    pixelSize = mat$pixelSize,
                    fid = mat$fid,
                    ptb.RootPath = mat$ptb.RootPath,
                    ptb.ConfigPath = mat$ptb.ConfigPath,
                    numDevices = mat$numDevices,
                    devices = mat$devices,
                    n = mat$n,
                    inputDevice = mat$inputDevice,
                    screens = mat$screens,
                    screenNumber = mat$screenNumber,
                    w = mat$w,
                    wWidth = mat$wWidth,
                    wHeight = mat$wHeight,
                    grayLevel = mat$grayLevel,
                    theFont = mat$theFont,
                    FontSize = mat$FontSize,
                    black = mat$black,
                    white = mat$white,
                    xcenter = mat$xcenter,
                    ycenter = mat$ycenter,
                    stim.images = mat$stim.images,
                    balloon.img = mat$balloon.img,
                    exploded.img = mat$exploded.img,
                    base.window.size = mat$base.window.size,
                    tmp = mat$tmp,
                    x = mat$x,
                    starting.value = mat$starting.value,
                    nsizes = mat$nsizes,
                    scale.factor = mat$scale.factor,
                    imgwindow = mat$imgwindow,
                    cumulative.ctr = mat$cumulative.ctr,
                    nconds = mat$nconds,
                    payoff.level = mat$payoff.level,
                    explode.trial.num = mat$explode.trial.num,
                    rt = mat$rt,
                    ntrials = mat$ntrials,
                    resp = mat$resp,
                    total.pres.time = mat$total.pres.time,
                    ctr = mat$ctr,
                    t = mat$t,
                    balloon.num = mat$balloon.num,
                    accept.resp = mat$accept.resp,
                    reject.resp = mat$reject.resp,
                    ISI = mat$ISI,
                    ITI = mat$ITI,
                    accept.wait = mat$accept.wait,
                    noresp = mat$noresp,
                    keyIsDown = mat$keyIsDown,
                    secs = mat$secs,
                    keyCode = mat$keyCode,
                    anchor = mat$anchor,
                    trial = mat$trial,
                    still.playing = mat$still.playing,
                    trial.round = mat$trial.round,
                    trial.counter = mat$trial.counter,
                    start.time = mat$start.time,
                    tmp1 = mat$tmp1,
                    tmp2 = mat$tmp2,
                    tmpTime = mat$tmpTime,
                    accept = mat$accept,
                    isi = mat$tmp.isi,
                    iti = mat$tmp.iti,
                    outfile = mat$outfile,
                    run.info = mat$run.info)

jsonOutputList <- toJSON(listForJson)

#Save jsonOutput
write(jsonOutputList, paste0(outputPath, '.json'))

#Process event info stored in trial.info
trial.info <- mat$trial.info

#Function to process data for a given trial
makeTrialDf <- function(listElement){

  #create the empty df that will be filled with the trial info
  #nrow is the # of responses
  out <- data.frame(matrix(data=NA, nrow = length(listElement$resp), ncol = length(names(listElement))))
  names(out) <- names(listElement)

  #Take pertinent variable and reformat it to be part of df
  out$payoff.level <- as.numeric(listElement$payoff.level)
  out$balloon <- as.numeric(listElement$balloon)
  out$rt <- listElement$rt[,2]
  out$trial.start <- listElement$rt[,1]
  out$trial.end <- listElement$rt[,3]
  out$resp <- as.numeric(unlist(listElement$resp))
  out$explode.trial <- as.numeric(listElement$explode.trial)
  out$explode.time <- ifelse(length(as.numeric(listElement$explode.time)) == 0 , NA, as.numeric(listElement$explode.time))
  out$finish.time <- ifelse(length(as.numeric(listElement$finish.time)) == 0 , NA, as.numeric(listElement$finish.time))
  out$exploded <- as.numeric(listElement$exploded)
  out$trial.total <- as.numeric(listElement$trial.total)
  out$cumulative.total <- as.numeric(listElement$cumulative.total)
  out$finished <- as.numeric(listElement$finished)

  return(out)
}

#First apply function to get a list of lists for each trial
trialsList <- apply(trial.info, c(3,2) , makeTrialDf)

#Then turn them to a list of dataframes for each trial
trialsDfs <- apply(trialsList, c(1), function(x) as.data.frame(x))

#Finally turn all output in to a single df for a subject
tsvDf <- rbind.fill(trialsDfs)

#Add trial number
tsvDf$trial.num <- factor(tsvDf$explode.trial, levels = unique(tsvDf$explode.trial), labels = 1:length(unique(tsvDf$explode.trial)))

#Additional variables that might be necessary for analysis
tsvDf$secs <- ifelse(length(as.numeric(mat$secs)) == 0 , NA, as.numeric(mat$secs))
tsvDf$start.time <-ifelse(length(as.numeric(mat$start.time)) == 0 , NA, as.numeric(mat$start.time))
tsvDf$iti <- ifelse(length(as.numeric(mat$ITI)) == 0 , NA, as.numeric(mat$ITI))
tsvDf$isi <- ifelse(length(as.numeric(mat$ISI)) == 0 , NA, as.numeric(mat$ISI))

#Save tsvOutput
write.table(tsvDf, file = paste(outputPath, '.tsv'), row.names=FALSE, sep="\t")
