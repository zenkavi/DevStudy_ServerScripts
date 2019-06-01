from argparse import ArgumentParser
import glob
from  nipype.interfaces import fsl
from nipype.caching import Memory
mem = Memory(base_dir='.')
import os
import pandas as pd
import numpy as np

#Usage = python fsl_randomise.py --mnum model1 --reg hpe -tf -np -vs

parser = ArgumentParser()
parser.add_argument("-m", "--mnum", help="model number")
parser.add_argument("-r", "--reg", help="regressor name")
parser.add_argument("-tf", "--tfce", help="tfce", default=True)
parser.add_argument("-np", "--num_perm", help="number of permutations", default=1000)
parser.add_argument("-vs", "--var_smooth", help="variance smoothing", default=5)
args = parser.parse_args()
mnum = args.mnum
reg = args.reg
if mnum == "model1":
    one = True
tfce = args.tfce
num_perm = int(args.num_perm)
var_smooth = int(args.var_smooth)

data_loc = os.environ['DATA_LOC']
server_scripts = os.environ['SERVER_SCRIPTS']
in_path = "%s/derivatives/nistats/level_3/%s/%s"%(data_loc, mnum, reg)

# Read in group info for models 2 and 3
age_info = pd.read_csv('%s/participants.tsv'%(data_loc), sep='\t')
age_info['kid'] = np.where(age_info['age']<13,1,0)
age_info['teen'] = np.where((age_info['age']>12) & (age_info['age']<19),1,0)
age_info['adult'] = np.where(age_info['age']>18,1,0)
age_info = age_info.sort_values(by=['participant_id']).reset_index(drop=True)
level2_images = glob.glob('%s/sub-*_%s.nii.gz'%(in_path, reg))
level2_images.sort()
subs = [os.path.basename(x).split("_")[0] for x in level2_images]
age_info = age_info[age_info.participant_id.isin(subs)].reset_index(drop=True)
learner_info = pd.read_csv('%s/nistats/level_3/learner_info.csv'%(server_scripts))
learner_info = learner_info[learner_info.Sub_id.isin(subs)].reset_index(drop=True)

if mnum == 'model2':
    deshdr="""/NumWaves	3
/NumPoints	74
/PPheights		1.000000e+00	1.000000e+00	1.000000e+00

/Matrix
    """

if mnum == 'model3':
    deshdr="""/NumWaves	2
/NumPoints	74
/PPheights		1.000000e+00	1.000000e+00

/Matrix
    """
#model2: age group differences
if mnum == "model2":
    design_matrix = age_info[['kid', 'teen', 'adult']]

#model3: learners vs non-learners
if mnum == "model3":
    design_matrix = learner_info[['learner', 'non_learner']]

if mnum != "model1":
    np.savetxt('%s/%s_%s_design.mat'%(in_path, mnum, reg),design_matrix.values,fmt='%1.0f',header=deshdr,comments='')

randomise = mem.cache(fsl.Randomise)

if mnum == "model1":
    randomise_results = randomise(in_file="%s/all_l2_%s_%s.nii.gz"%(in_path, mnum, reg),
                              mask= "%s/group_mask_%s_%s.nii.gz"%(in_path, mnum, reg),
                              one_sample_group_mean=one,
                              tfce=tfce,
                              vox_p_values=True,
                              num_perm=num_perm,
                              var_smooth = var_smooth)

if mnum == "model2":
    randomise_results = randomise(in_file="%s/all_l2_%s_%s.nii.gz"%(in_path, mnum, reg),
                              mask= "%s/group_mask_%s_%s.nii.gz"%(in_path, mnum, reg),
                              design_mat = "%s/%s_%s_design.mat"%(in_path, mnum, reg),
                              tcon="%s/derivatives/nistats/level_3/%s/%s_design.con"%(data_loc, mnum),
                              fcon="%s/derivatives/nistats/level_3/%s/%s_design.fts"%(data_loc, mnum),
                              tfce=tfce,
                              vox_p_values=True,
                              num_perm=num_perm,
                              var_smooth = var_smooth)

if mnum == "model3":
    randomise_results = randomise(in_file="%s/all_l2_%s_%s.nii.gz"%(in_path, mnum, reg),
                              mask= "%s/group_mask_%s_%s.nii.gz"%(in_path, mnum, reg),
                              design_mat = "%s/%s_%s_design.mat"%(in_path, mnum, reg),
                              tcon="%s/derivatives/nistats/level_3/%s/%s_design.con"%(data_loc, mnum),
                              tfce=tfce,
                              vox_p_values=True,
                              num_perm=num_perm,
                              var_smooth = var_smooth)

#save outputs
if len(randomise_results.outputs.tstat_files)>0:
    for i in range(0,len(randomise_results.outputs.tstat_files)):
        os.rename(randomise_results.outputs.tstat_files[i], "%s/rand/rand_%s_%s_tstat%s.nii.gz.nii.gz"%(in_path,mnum, reg, str(i+1)))
        print("***********************************************")
        print("Saved tstat_file for: %s %s"%(mnum, reg))
        print("***********************************************")

if len(randomise_results.outputs.fstat_files)>0:
    for i in range(0,len(randomise_results.outputs.fstat_files)):
        os.rename(randomise_results.outputs.fstat_files[i],"%s/rand/rand_%s_%s_fstat%s.nii.gz.nii.gz"%(in_path,mnum, reg, str(i+1)))
        print("***********************************************")
        print("Saved fstat_file for: %s %s"%(mnum, reg))
        print("***********************************************")

if len(randomise_results.outputs.t_p_files)>0:
    for i in range(0,len(randomise_results.outputs.t_p_files)):
        os.rename(randomise_results.outputs.t_p_files[i], "%s/rand/rand_%s_%s_t_p%s.nii.gz.nii.gz"%(in_path,mnum, reg, str(i+1)))
        print("***********************************************")
        print("Saved t_p_file for: %s %s"%(mnum, reg))
        print("***********************************************")

if len(randomise_results.outputs.f_p_files)>0:
    for i in range(0,len(randomise_results.outputs.f_p_files)):
        os.rename(randomise_results.outputs.f_p_files[i],"%s/rand/rand_%s_%s_f_p%s.nii.gz.nii.gz"%(in_path,mnum, reg, str(i+1)))
        print("***********************************************")
        print("Saved f_p_file for: %s %s"%(mnum, reg))
        print("***********************************************")

if len(randomise_results.outputs.t_corrected_p_files)>0:
    for i in range(0,len(randomise_results.outputs.t_corrected_p_files)):
        os.rename(randomise_results.outputs.t_corrected_p_files[i],"%s/rand/rand_%s_%s_tfce_corrp_tstat%s.nii.gz.nii.gz"%(in_path,mnum, reg, str(i+1)))
        print("***********************************************")
        print("Saved t_corrected_p_file for: %s %s"%(mnum, reg))
        print("***********************************************")

if len(randomise_results.outputs.f_corrected_p_files)>0:
    for i in range(0,len(randomise_results.outputs.f_corrected_p_files)):
        os.rename(randomise_results.outputs.f_corrected_p_files[i],"%s/rand/rand_%s_%s_tfce_corrp_fstat%s.nii.gz.nii.gz"%(in_path,mnum, reg, str(i+1)))
        print("***********************************************")
        print("Saved t_corrected_p_file for: %s %s"%(mnum, reg))
        print("***********************************************")
