import copy
import math
import numpy as np
import os
import pandas as pd
import random
import scipy.optimize
from scipy.stats import truncnorm
from argparse import ArgumentParser
from .extract_pars import extract_pars, get_model_name
from .sample_x0 import sample_x0, get_bounds

def calculate_neglogprob(x0,data, pars):

    TrialNum = data.Trial_type
    Response = data.Response
    Outcome = data.Points_earned

    EV = [0,0,0,0]
    Prediction_Error = 0
    choiceprob = np.zeros((len(TrialNum)))

    #x0 only has values for parameters that will be fitted; so we can't use numerical indices to extract from the list and assign as the parameter value to be used
    #to fix this we add the argument pars to the function and use it to create to helper lists of parameters that will be fixed and those that will be fit
    pars = extract_pars(pars)
    fixparams = pars['fixparams']
    fitparams = pars['fitparams']

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


def select_optimal_parameters(data, subject, n_fits=50, pars = {'alpha_neg':np.nan, 'alpha_pos':np.nan, 'beta':np.nan,  'exp_neg':np.nan, 'exp_pos':np.nan, 'lossave': np.nan}, save=False, output_path=np.nan):

    #data =  pd.read_csv(data_path+'ProbLearn'+str(subject)+'.csv')

    cols = ['x0_'+s for s in list(sorted(pars.keys()))] +['xopt_'+s for s in list(sorted(pars.keys()))] + ['neglogprob', 'sub_id', 'seed']

    Results = pd.DataFrame(np.nan, columns=cols, index=range(int(n_fits)))

    pars_copy = extract_pars(copy.copy(pars))
    fixparams = pars_copy['fixparams']
    fitparams = pars_copy['fitparams']

    model_name = get_model_name(pars)
    bnds = get_bounds(pars)

    for i in range(n_fits):

        n = random.randint(1000,99999999)
        random.seed(n)
        np.random.seed(n)

        x0=sample_x0(pars)
        x0_dict = dict(zip(fitparams,x0))

        try:
            print("Sampled starting parameters are:")
            print(x0_dict)

            #Fit model
            try:
                #xopt = scipy.optimize.fmin(calculate_neglogprob,x0,args=(data,pars,),xtol=1e-6,ftol=1e-6)
                #xopt = scipy.optimize.minimize(calculate_neglogprob,x0, method = "Nelder-Mead",args=(data,pars,),tol=1e-6).x
                xopt = scipy.optimize.minimize(calculate_neglogprob,x0, method = "L-BFGS-B",args=(data,pars,),bounds=bnds,tol=1e-6).x
            except OverflowError:
                xopt = [float('inf')]*len(x0)

            #convert xopt to dictionary for easier update of Results df
            xopt_dict = dict(zip(fitparams,list(xopt)))
            print("Estimated optimal parameters are:")
            print(xopt_dict)

            #fill in Results df with x0 and xopt for the fitted params
            for key in fitparams:
                Results['x0_'+key][i] = x0_dict[key]
                Results['xopt_'+key][i] = xopt_dict[key]

            #fill in Results df with x0 and xopt for the fixed params
            for key in fixparams:
                Results['x0_'+key][i] = pars[key]
                Results['xopt_'+key][i] = pars[key]

            #add neg log of fit to Results output
            Results.neglogprob[i] = calculate_neglogprob(xopt,data,pars)

            #add subject column
            Results.sub_id[i] = subject
            Results.seed[i] = n

        except:
            print("fmin error")

    if save:
        #write out sorted data
        Results.sort_values(by=['neglogprob']).to_csv(output_path+ model_name+'_'+str(subject)+'.csv')
        print("Estimated parameters saved in: %s"%(output_path+ model_name+'_'+str(subject)+'.csv'))

    #return the optimal parameters
    opt_pars_dict = Results.sort_values(by=['neglogprob']).filter(regex='xopt').to_dict('records')[0]
    opt_pars_dict = {x.replace('xopt_', ''): v for x, v in opt_pars_dict.items()}
    return(opt_pars_dict)
