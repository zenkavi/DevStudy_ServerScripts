#!/home/groups/russpold/software/miniconda/envs/py38/bin/python
from argparse import ArgumentParser
#Usage: ./comp_mle_vs_nuts.py --alpha 0.1 --beta 3.0

parser = ArgumentParser()
parser.add_argument("--alpha")
parser.add_argument("--beta")
args = parser.parse_args()
alpha = float(args.alpha)
beta = float(args.beta)

import numpy as np
import pandas as pd
import scipy
import pymc3 as pm
import theano
import theano.tensor as tt
from .comp_mle_vs_nuts_helpers import generate_data, llik_td_vectorized, update_Q, theano_llik_td, get_mle_nuts_est

est_df, mle_iters, nuts_posteriors = get_mle_nuts_est(alpha, beta)

est_df.to_csv(".comp_out/est_df_alpha_%s_beta_%s.csv"%(str(alpha), str(beta)), index=False)
mle_iters.to_csv(".comp_out/mle_iters_alpha_%s_beta_%s.csv"%(str(alpha), str(beta)), index=False)
nuts_posteriors.to_csv(".comp_out/nuts_posteriors_alpha_%s_beta_%s.csv"%(str(alpha), str(beta)), index=False)
