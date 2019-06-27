import copy
import json
import math
import numpy as np
import os
import pandas as pd
import random
import scipy.optimize
from scipy.stats import truncnorm
from argparse import ArgumentParser

todo_path = os.environ['TODO_PATH']
server_scripts = os.environ['SERVER_SCRIPTS']

parser = ArgumentParser()
parser.add_argument("-s", "--subject", help="subject number")
parser.add_argument("-n", "--n_fits", default=50, help="Number of iterations for model")
parser.add_argument("-dp", "--data_path", default=todo_path+'/behav_data_tb_organized/machine_game/' , help="data path")
parser.add_argument("-op", "--output_path", default=server_scripts+'/fit_rl/.fits/', help="output path")
parser.add_argument("-da", "--data_amt", default=1, help="proportion of data the model will be fit to")
parser.add_argument("-p", "--pars", help="parameters dictionary")
args = parser.parse_args()

subject = args.subject
n_fits = args.n_fits
data_path = args.data_path
data_amt = args.data_amt
if(data_amt ==1):
    output_path = args.output_path
else:
    output_path = args.output_path + '_'+ data_amt
if not os.path.exists(output_path):
    os.makedirs(output_path)
pars = args.pars

#text wrangling to turn the pars string to dictionary
try:
    pars = json.loads(pars.replace('nan', '"nan"').replace("'", "\""))
except:
    pars = json.loads(pars[0].replace('nan', '"nan"').replace("'", "\""))

for (k,v) in pars.items():
    if v == "nan":
        pars[k] = np.nan

def extract_pars(pars):
    fixparams = []
    fitparams = []

    for key in sorted(pars.keys()):
        if np.isnan(pars[key]):
            fitparams.append(key)
        else:
            fixparams.append(key)

    out = {'fitparams':fitparams, 'fixparams':fixparams}

    return(out)

def calculate_prediction_error(x0,data, pars):

    TrialNum = data.Trial_type
    Response = data.Response
    Outcome = data.Points_earned

    EV = [0,0,0,0]
    Prediction_Error = 0
    choiceprob = np.zeros((len(TrialNum)))

    #x0 only has values for parameters that will be fitted; so we can't use numerical indices to extract from the list and assign as the parameter value to be used
    #to fix this we add the argument pars to the function and use it to create to helper lists of parameters that will be fixed and those that will be fit
    fixparams = extract_pars(pars)['fixparams']
    fitparams = extract_pars(pars)['fitparams']

    #because the length of x0 and the parameters the values in it correspond to will change depending on what is fixed vs. fit we need a named dictionary
    #we use the list of fitparams for this
    x0_dict = dict(zip(fitparams,x0))

    #now we create a dictionary that will contain all the appropriate numbers for each parameter that will be used in the RPE and EV calculations below
    if 'alpha' in pars.keys():
        if 'exp' in pars.keys():
            all_pars_dict = {'alpha':np.nan, 'beta':np.nan, 'exp':np.nan, 'lossave': np.nan}
        else:
            all_pars_dict = {'alpha':np.nan, 'beta':np.nan, 'exp_neg':np.nan, 'exp_pos':np.nan, 'lossave': np.nan}
    elif 'exp' in pars.keys():
        all_pars_dict = {'alpha_neg':np.nan, 'alpha_pos':np.nan, 'beta':np.nan, 'exp':np.nan, 'lossave': np.nan}
    else:
        all_pars_dict = {'alpha_neg':np.nan, 'alpha_pos':np.nan, 'beta':np.nan, 'exp_neg':np.nan, 'exp_pos':np.nan, 'lossave': np.nan}

    #we populate each element in this dictionary of all to-be-used parameters by going through each key; checking if it is in fixparams. If so we extract is from the params argument in the function call, otherwise we extract the sampled value from x0
    for par in sorted(all_pars_dict.keys()):
        if par in fixparams:
            all_pars_dict[par] = pars[par]
        else:
            all_pars_dict[par] = x0_dict[par]

    #finally we assign the to-be used parameters to objects to avoid too much typing in the rest of the loops
    if 'alpha' in all_pars_dict.keys():
        alpha=all_pars_dict['alpha']
    else:
        alphaneg=all_pars_dict['alpha_neg']
        alphapos=all_pars_dict['alpha_pos']
    beta=all_pars_dict['beta']
    if 'exp' in all_pars_dict.keys():
        exp=all_pars_dict['exp']
    else:
        expneg=all_pars_dict['exp_neg']
        exppos=all_pars_dict['exp_pos']
    lossave=all_pars_dict['lossave']

    for i in range(len(TrialNum)):
        #First update the choice probabilities for each trial
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

        #If a machine has been played update the RPE
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

            #If the outcome is worst than expected use alphaneg
            if Outcome[i] < EV[int(TrialNum[i]-1)]:

                if 'alpha' in vars() or 'alpha' in globals():
                    if 'exp' in vars() or 'exp' in globals():
                        Prediction_Error = -1*alpha*(EV[int(TrialNum[i]-1)]-Outcome[i])**exp #have to do it this way because you can't put a negative number to an exponent between 0 and 1
                    else:
                        Prediction_Error = -1*alpha*(EV[int(TrialNum[i]-1)]-Outcome[i])**expneg
                elif 'exp' in vars() or 'exp' in globals():
                    Prediction_Error = -1*alphaneg*(EV[int(TrialNum[i]-1)]-Outcome[i])**exp
                else:
                    Prediction_Error = -1*alphaneg*(EV[int(TrialNum[i]-1)]-Outcome[i])**expneg

            if Outcome[i] == EV[int(TrialNum[i]-1)]:
                Prediction_Error = 0

            EV[int(TrialNum[i]-1)] += Prediction_Error

    neglogprob = 0
    choiceprob = np.where(choiceprob == 1, 0.99999999, np.where(choiceprob == 0, 0.00000001, choiceprob))
    for each_item in choiceprob:
        neglogprob = neglogprob - math.log(each_item)

    return(neglogprob)


def select_optimal_parameters(subject, inpath, outpath, n_fits=50, pars = {'alpha_neg':np.nan, 'alpha_pos':np.nan, 'beta':np.nan,  'exp_neg':np.nan, 'exp_pos':np.nan, 'lossave': np.nan}, data_amt=1):

    data =  pd.read_csv(data_path+'ProbLearn'+str(subject)+'.csv')

    nrows = round(data.shape[0] * float(data_amt))

    data = data[:nrows]

    cols = ['x0_'+s for s in list(sorted(pars.keys()))] +['xopt_'+s for s in list(sorted(pars.keys()))] + ['neglogprob', 'sub_id', 'seed']

    Results = pd.DataFrame(np.nan, columns=cols, index=range(int(n_fits)))

    fixparams = extract_pars(pars)['fixparams']
    fitparams = extract_pars(pars)['fitparams']

    #make string containing info on fitted pars for output file name
    if len(fixparams) == 0:
        model_name = 'LearningParams_Fit_'+ '-'.join(fitparams) + '_Fix'+ '-'.join(fixparams)
    else:
        model_name = 'LearningParams_Fit_'+ '-'.join(fitparams) + '_Fix_'+ '-'.join(fixparams)

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

    for i in range(n_fits):

        n = random.randint(1000,99999999)
        random.seed(n)
        np.random.seed(n)

        x0=sample_x0(pars)
        x0_dict = dict(zip(fitparams,x0))

        try:
            print(x0_dict)

            #Fit model
            try:
                #xopt = scipy.optimize.fmin(calculate_prediction_error,x0,args=(data,pars,),xtol=1e-6,ftol=1e-6)
                #xopt = scipy.optimize.minimize(calculate_prediction_error,x0, method = "Nelder-Mead",args=(data,pars,),tol=1e-6).x
                xopt = scipy.optimize.minimize(calculate_prediction_error,x0, method = "L-BFGS-B",args=(data,pars,),bounds=bnds,tol=1e-6).x
            except OverflowError:
                xopt = [float('inf')]*len(x0)

            #convert xopt to dictionary for easier update of Results df
            xopt_dict = dict(zip(fitparams,list(xopt)))

            #fill in Results df with x0 and xopt for the fitted params
            for key in fitparams:
                Results['x0_'+key][i] = x0_dict[key]
                Results['xopt_'+key][i] = xopt_dict[key]

            for key in fixparams:
                Results['x0_'+key][i] = pars[key]

            #add neg log of fit to Results output
            Results.neglogprob[i] = calculate_prediction_error(xopt,data,pars)

            #add subject column
            Results.sub_id[i] = subject
            Results.seed[i] = n

        except:
            print("fmin error")

    #write out sorted data
    Results.sort_values(by=['neglogprob']).to_csv(output_path+ model_name+'_'+str(subject)+'.csv')

select_optimal_parameters(subject=int(subject), inpath=data_path, outpath=output_path, n_fits=int(n_fits), pars = pars, data_amt = data_amt)
