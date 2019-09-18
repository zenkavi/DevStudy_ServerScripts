import copy
import json
import numpy as np
import pandas as pd

#text wrangling to turn the pars string to dictionary

def make_pars_dict(pars):
    try:
        pars = json.loads(pars.replace('nan', '"nan"').replace("'", "\""))
    except:
        pars = json.loads(pars[0].replace('nan', '"nan"').replace("'", "\""))

    for (k,v) in pars.items():
        if v == "nan":
            pars[k] = np.nan

    return(pars)

def extract_pars(pars):

    pars = make_pars_dict(pars)

    fixparams = []
    fitparams = []

    for key in sorted(pars.keys()):
        if np.isnan(pars[key]):
            fitparams.append(key)
        else:
            fixparams.append(key)

    out = {'fitparams':fitparams, 'fixparams':fixparams}

    return(out)

def get_model_name(pars):

    pars = make_pars_dict(pars)

    pars_copy = extract_pars(copy.copy(pars))
    fixparams = pars_copy['fixparams']
    fitparams = pars_copy['fitparams']
    #make string containing info on fitted pars for output file name
    if len(fixparams) == 0:
        model_name = 'LearningParams_Fit_'+ '-'.join(fitparams) + '_Fix'+ '-'.join(fixparams)
    else:
        model_name = 'LearningParams_Fit_'+ '-'.join(fitparams) + '_Fix_'+ '-'.join(fixparams)

    return(model_name)
