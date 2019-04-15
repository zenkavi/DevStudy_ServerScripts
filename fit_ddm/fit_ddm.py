import glob
import os
import pandas as pd
import numpy as np
import hddm
import re

todo_path = os.environ['TODO_PATH']
server_scripts = os.environ['SERVER_SCRIPTS']

#python fit_ddm.py

parser = ArgumentParser()
parser.add_argument("-s", "--subject", help="subject number", default='all')
parser.add_argument("-dp", "--data_path", default=todo_path+'/behav_data_tb_organized/machine_game/' , help="data path")
parser.add_argument("-op", "--output_path", default=server_scripts+'/fit_ddm/.fits/', help="output path")
args = parser.parse_args()

subject = args.subject
data_path = args.data_path
output_path = args.output_path

def EZ_diffusion(df, condition = "Trial_type", correct_col = "play1_pass0", rt_col = "Reaction_time"):
    assert correct_col in df.columns, 'Did not find binary decision column for EZ DDM'
    assert rt_col in df.columns, 'Did not find rt column for EZ DDM'
    df = df.copy()
    # convert reaction time to seconds to match with HDDM
    df[rt_col] = df[rt_col]/1000
    # ensure there are no missed responses or extremely short responses (to fit with EZ)
    df = df.query('{0} > .05'.format(rt_col))
    # convert any perfect accuracies to .95

    EZ_dvs = {}
    # calculate EZ params for each condition
    if condition:
        conditions = df[condition].unique()
        conditions = conditions[~pd.isnull(conditions)]
        for c in conditions:
            subset = df[df[condition] == c]
            pc = subset[correct_col].mean()
            # edge case correction using the fourth suggestion from
            # Stanislaw, H., & Todorov, N. (1999). Calculation of signal detection theory measures.
            if pc == 1:
                pc = 1-(.5/len(subset))
            vrt = np.var(subset.query('{0} == True'.format(correct_col))[rt_col])
            mrt = np.mean(subset.query('{0} == True'.format(correct_col))[rt_col])
            try:
                drift, thresh, non_dec = hddm.utils.EZ(pc, vrt, mrt)
                EZ_dvs['EZ_drift_' + str(c)] = drift
                EZ_dvs['EZ_thresh_' + str(c)] = thresh
                EZ_dvs['EZ_non_decision_' + str(c)] = non_dec
            except ValueError:
                continue
    else:
        # calculate EZ params
        try:
            pc = df[correct_col].mean()
            # edge case correct
            if pc == 1:
                pc = 1-(1.0/(2*len(df)))
            vrt = np.var(df.query('{0} == 1'.format(correct_col))[rt_col])
            mrt = np.mean(df.query('{0} == 1'.format(correct_col))[rt_col])
            drift, thresh, non_dec = hddm.utils.EZ(pc, vrt, mrt)
            EZ_dvs['EZ_drift'] = drift
            EZ_dvs['EZ_thresh'] = thresh
            EZ_dvs['EZ_non_decision'] = non_dec
        except ValueError:
            return {}
    return EZ_dvs

results = {}
if subject=="all":
    all_files = glob.glob(data_path+'ProbLearn*.csv')
    for f in all_files:
        data = pd.read_csv(f)
        data = data.query("Response!=0")
        data['play1_pass0'] = np.where(data['Response']==1,1,np.where(data['Response']==2,0,np.nan))
        subnum= re.findall(r'\d+', os.path.basename(f))[0]
        print("Fitting EZ DDM for %s"%(os.path.basename(f)))
        sub_results=EZ_diffusion(data)
        results[subnum] = sub_results
    del results['406989']
    results = pd.DataFrame.from_dict(results, orient="index")
    results.to_csv(output_path+'EZ_ddm_fits_all.csv')
else:
    data =  pd.read_csv(data_path+'ProbLearn'+str(subject)+'.csv')
    data = data.query("Response!=0")
    data['play1_pass0'] = np.where(data['Response']==1,1,np.where(data['Response']==2,0,np.nan))
    print("Fitting EZ DDM for %s"%(subject))
    sub_results = EZ_diffusion(data)
    results[subject] = sub_results
    results = pd.DataFrame.from_dict(results, orient="index")
    results.to_csv(output_path+'EZ_ddm_fits_%s.csv'%(subject))
