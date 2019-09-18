import glob
import math
import numpy as np
import os
import pandas as pd
import re
from argparse import ArgumentParser

def get_predicted_df(data, pars_dict):
    data = data.reset_index()
    TrialNum = data.Trial_type
    Response = data.Response
    Outcome = data.Points_earned
    EV = [0,0,0,0]
    Prediction_Error = 0
    choiceprob = np.zeros((len(TrialNum)))
    data['EV'] = np.nan
    data['PE'] = np.nan
    data['choiceprob'] = np.nan
    if 'alpha' in pars_dict.keys():
        alpha=pars_dict['alpha']
    else:
        alphaneg=pars_dict['alpha_neg']
        alphapos=pars_dict['alpha_pos']
    beta=pars_dict['beta']
    if 'exp' in pars_dict.keys():
        exp=pars_dict['exp']
    else:
        expneg=pars_dict['exp_neg']
        exppos=pars_dict['exp_pos']
    lossave=pars_dict['lossave']
    for i in range(len(TrialNum)):
        if Response[i] == 0:
            choiceprob[i] = 1
        if Response[i] == 1:
            if EV[int(TrialNum[i]-1)] < 0:
                choiceprob[i] = math.exp(lossave*EV[int(TrialNum[i]-1)]*beta)/(math.exp(lossave*EV[int(TrialNum[i]-1)]*beta)+1)
            else:
                choiceprob[i] = math.exp(EV[int(TrialNum[i]-1)]*beta)/(math.exp(EV[int(TrialNum[i]-1)]*beta)+1)
        if Response[i] == 2:
            if EV[int(TrialNum[i]-1)] < 0:
                choiceprob[i] = 1-math.exp(lossave*EV[int(TrialNum[i]-1)]*beta)/(math.exp(lossave*EV[int(TrialNum[i]-1)]*beta)+1)
            else:
                choiceprob[i] = 1-math.exp(EV[int(TrialNum[i]-1)]*beta)/(math.exp(EV[int(TrialNum[i]-1)]*beta)+1)
        if Outcome[i] != 0:
            if Outcome[i] > EV[int(TrialNum[i]-1)]:
                if 'alpha' in vars() or 'alpha' in globals():
                    if 'exp' in vars() or 'exp' in globals():
                        Prediction_Error = alpha*(Outcome[i] - EV[int(TrialNum[i]-1)])**exp
                    else:
                        Prediction_Error = alpha*(Outcome[i] - EV[int(TrialNum[i]-1)])**exppos
                elif 'exp' in vars() or 'exp' in globals():
                    Prediction_Error = alphapos*(Outcome[i] - EV[int(TrialNum[i]-1)])**exp
                else:
                    Prediction_Error = alphapos*(Outcome[i] - EV[int(TrialNum[i]-1)])**exppos
            if Outcome[i] < EV[int(TrialNum[i]-1)]:
                if 'alpha' in vars() or 'alpha' in globals():
                    if 'exp' in vars() or 'exp' in globals():
                        Prediction_Error = -1*alpha*(EV[int(TrialNum[i]-1)]-Outcome[i])**exp
                    else:
                        Prediction_Error = -1*alpha*(EV[int(TrialNum[i]-1)]-Outcome[i])**expneg
                elif 'exp' in vars() or 'exp' in globals():
                    Prediction_Error = -1*alphaneg*(EV[int(TrialNum[i]-1)]-Outcome[i])**exp
                else:
                    Prediction_Error = -1*alphaneg*(EV[int(TrialNum[i]-1)]-Outcome[i])**expneg
            if Outcome[i] == EV[int(TrialNum[i]-1)]:
                Prediction_Error = 0
            data.EV[i] = EV[int(TrialNum[i]-1)]
            data.PE[i] = Prediction_Error
            data.choiceprob[i] = choiceprob[i]
            EV[int(TrialNum[i]-1)] += Prediction_Error
        elif Outcome[i] == 0:
            data.EV[i] = EV[int(TrialNum[i]-1)]
            data.choiceprob[i] = choiceprob[i]
    data = data[['Trial_type', 'Response', 'Points_earned', 'EV', 'PE', 'choiceprob']]
    return(data)
