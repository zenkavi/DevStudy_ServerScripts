import json
import numpy as np
import pandas as pd

#text wrangling to turn the pars string to dictionary

def extract_pars(pars):
    try:
        pars = json.loads(pars.replace('nan', '"nan"').replace("'", "\""))
    except:
        pars = json.loads(pars[0].replace('nan', '"nan"').replace("'", "\""))

    for (k,v) in pars.items():
        if v == "nan":
            pars[k] = np.nan
    
    fixparams = []
    fitparams = []

    for key in sorted(pars.keys()):
        if np.isnan(pars[key]):
            fitparams.append(key)
        else:
            fixparams.append(key)

    out = {'fitparams':fitparams, 'fixparams':fixparams}

    return(out)
