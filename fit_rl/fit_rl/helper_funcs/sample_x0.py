import copy
import numpy as np
import pandas as pd
import random
from scipy.stats import truncnorm

def sample_x0(pars):

      pars_copy = copy.copy(pars)
      x0 = []
      #Fix vs fit params
      for key in sorted(pars_copy.keys()):
          #if NaN then fit param; so sample from prior; otherwise leave as is
          if np.isnan(pars_copy[key]):
              #Priors
              #UPDATING X0 FOR ALL PARS THAT WILL BE FITTED AFTER SAMPLING FROM PRIOR TO make sure x0 has the correct order and only values for parameters that will be fittd!
              if key == 'alpha':
                  #pars_copy[key] = random.uniform(0,1)
                  pars_copy[key] = np.random.beta(1.2,1.2)
                  x0.append(pars_copy[key])
              if key == 'alpha_neg':
                  #pars_copy[key] = random.uniform(0,1)
                  pars_copy[key] = np.random.beta(1.2,1.2)
                  x0.append(pars_copy[key])
              if key == 'alpha_pos':
                  #pars_copy[key] = random.uniform(0,1)
                  pars_copy[key] = np.random.beta(1.2,1.2)
                  x0.append(pars_copy[key])
              if key == 'beta':
                  #pars_copy[key] = random.uniform(0,5)
                  pars_copy[key] = np.random.gamma(2,1)
                  x0.append(pars_copy[key])
              if key == 'exp':
                  pars_copy[key] = np.random.beta(1.2,1.2)
                  x0.append(pars_copy[key])
              if key == 'exp_neg':
                  pars_copy[key] = np.random.beta(1.2,1.2)
                  x0.append(pars_copy[key])
              if key == 'exp_pos':
                  pars_copy[key] = np.random.beta(1.2,1.2)
                  x0.append(pars_copy[key])
              if key == 'lossave':
                  # Based on: https://github.com/kieranrcampbell/blog-notebooks/blob/master/Fast%20vectorized%20sampling%20from%20truncated%20normal%20distributions%20in%20python.ipynb
                  pars_copy[key] = truncnorm.rvs((0 - 2) / 2, (10 - 2) / 2, 2, 2)
                  x0.append(pars_copy[key])

      return(x0)

def get_bounds(pars):
    bnds = []
    if "alpha" in pars.keys() and np.isnan(pars['alpha']):
        bnds.append((0.05,2))
    if "alpha_neg" in pars.keys() and np.isnan(pars['alpha_neg']):
        bnds.append((0.05,2))
    if "alpha_pos" in pars.keys() and np.isnan(pars['alpha_pos']):
        bnds.append((0.05,2))
    if "beta" in pars.keys() and np.isnan(pars['beta']):
        bnds.append((0,15))
    if "exp" in pars.keys() and np.isnan(pars['exp']):
        bnds.append((0.05,2))
    if "exp_neg" in pars.keys() and np.isnan(pars['exp_neg']):
        bnds.append((0.05,2))
    if "exp_pos" in pars.keys() and np.isnan(pars['exp_pos']):
        bnds.append((0.05,2))
    if "lossave" in pars.keys() and np.isnan(pars['lossave']):
        bnds.append((0,10))
    bnds = tuple(bnds)
    return(bnds)
