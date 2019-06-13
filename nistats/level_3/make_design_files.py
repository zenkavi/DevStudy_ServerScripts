#!/home/groups/russpold/software/miniconda/envs/fmri/bin/python
import glob
import numpy as np
import pandas as pd
import os

def make_design_files(mnum):

    data_loc = os.environ['DATA_LOC']
    server_scripts = os.environ['SERVER_SCRIPTS']
    mnum_path = "%s/derivatives/nistats/level_3/%s"%(data_loc, mnum)
    if not os.path.exists(mnum_path):
        os.makedirs(mnum_path)

    l2_in_path = "%s/derivatives/nistats/level_2/sub-*/contrasts"%(data_loc)
    level2_images = glob.glob('%s/sub-*_m1.nii.gz'%(l2_in_path))
    level2_images.sort()
    subs = [os.path.basename(x).split("_")[0] for x in level2_images]

    #model2: age group differences
    #Design and contrast matrices based on: https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/GLM#F-Tests_.28Inter-Group_differences.2C_no_repeated_measures.29
    if mnum == "model2":
        age_info = pd.read_csv('%s/participants.tsv'%(data_loc), sep='\t')
        age_info['kid'] = np.where(age_info['age']<13,1,0)
        age_info['teen'] = np.where((age_info['age']>12) & (age_info['age']<19),1,0)
        age_info['adult'] = np.where(age_info['age']>18,1,0)
        age_info = age_info.sort_values(by=['participant_id']).reset_index(drop=True)
        age_info = age_info[age_info.participant_id.isin(subs)].reset_index(drop=True)
        design_matrix = age_info[['kid', 'teen', 'adult']]
        #design_matrix['intercept'] = [1] * len(level2_images)
        deshdr="""/NumWaves	3
/NumPoints	74
/PPheights		1.000000e+00	1.000000e+00	1.000000e+00

/Matrix
        """
        conhdr = """/ContrastName1	kids
/ContrastName2	teens
/ContrastName3	adults
/NumWaves	3
/NumContrasts	3
/PPheights		1.000000e+00	1.000000e+00	1.000000e+00
/RequiredEffect		0.767	0.948	0.739

/Matrix
        """
        contrast_matrix = np.array([[1,0,0],[0,1,0],[0,0,1]])

        desfhdr = """/NumWaves	3
/NumContrasts	1

/Matrix
        """
        design_fts = np.array([[1,1,1]])

    #model3: learners vs non-learners
    #Design and contrast matrices based on https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/GLM#Two-Group_Difference_.28Two-Sample_Unpaired_T-Test.29
    if mnum == "model3":
        learner_info = pd.read_csv('%s/nistats/level_3/learner_info.csv'%(server_scripts))
        learner_info = learner_info[learner_info.Sub_id.isin(subs)].reset_index(drop=True)
        design_matrix = learner_info[['learner', 'non_learner']]
        #design_matrix['intercept'] = [1] * len(level2_images)
        deshdr="""/NumWaves	2
/NumPoints	74
/PPheights		1.000000e+00	1.000000e+00

/Matrix
        """
        conhdr = """/ContrastName1	learner>non_learner
/ContrastName2	learner<non_learner
/NumWaves	2
/NumContrasts	2
/PPheights		1.000000e+00	1.000000e+00

/Matrix
        """
        contrast_matrix = np.array([[1,-1],[-1,1]])

    #model4: learners vs non-learners and first vs. second half
    #Design and contrast matrices based on https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/GLM#ANOVA:_2-factors_2-levels_.282-way_between-subjects_ANOVA.29
    if mnum == "model4":
        regs = ['m1', 'm2', 'm3', 'm4', 'hpe', 'lpe', 'pe', 'task_on', 'rt', 'var_sen', 'ev_sen']
        for reg in regs:
            reg_path = "%s/%s"%(mnum_path, reg)
            if not os.path.exists(reg_path):
                os.makedirs(reg_path)
            level2_first_half_images = glob.glob('%s/sub-*_%s_first_half.nii.gz'%(l2_in_path, reg))
            level2_first_half_images.sort()
            level2_second_half_images = glob.glob('%s/sub-*_%s_second_half.nii.gz'%(l2_in_path, reg))
            level2_second_half_images.sort()
            level2_first_half_subs = [os.path.basename(x).split("_")[0] for x in level2_first_half_images]
            level2_second_half_subs = [os.path.basename(x).split("_")[0] for x in level2_second_half_images]
            subs = [x for x in level2_first_half_subs if x in level2_second_half_subs]
            learner_info = pd.read_csv('%s/nistats/level_3/learner_info.csv'%(server_scripts))
            learner_info = learner_info[learner_info.Sub_id.isin(subs)].reset_index(drop=True)
            design_matrix = learner_info[['learner']].append(learner_info[['learner']])
            design_matrix['second_half'] = sorted([1,0]*int(design_matrix.shape[0]/2))
            design_matrix['first_half_learner'] = np.where((design_matrix['learner'] == 1) & (design_matrix['second_half'] == 0), 1, 0)
            design_matrix['first_half_non_learner'] = np.where((design_matrix['learner'] == 0) & (design_matrix['second_half'] == 0), 1, 0)
            design_matrix['second_half_learner'] = np.where((design_matrix['learner'] == 1) & (design_matrix['second_half'] == 1), 1, 0)
            design_matrix['second_half_non_learner'] = np.where((design_matrix['learner'] == 0) & (design_matrix['second_half'] == 1), 1, 0)
            design_matrix = design_matrix.drop(columns=['learner', 'second_half'])

            deshdr="""/NumWaves	4
/NumPoints	%s
/PPheights		1.000000e+00	1.000000e+00	1.000000e+00	1.000000e+00

/Matrix
            """%(str(design_matrix.shape[0]))

            print("***********************************************")
            print("Saving design matrix for %s reg %s"%(mnum, reg))
            print("***********************************************")
            np.savetxt('%s/%s_%s_design.mat'%(reg_path, mnum, reg),design_matrix.values,fmt='%1.0f',header=deshdr,comments='')


        conhdr = """/ContrastName1	main_half
/ContrastName2	main_learner
/ContrastName3	interaction
/NumWaves	3
/NumContrasts	3
/PPheights		1.000000e+00	1.000000e+00	1.000000e+00
/RequiredEffect		0.767	0.948	0.739

/Matrix
        """
        contrast_matrix = np.array([[1,1,-1,-1], [1,-1,1,-1], [1,-1,-1,1]])

        desfhdr = """/NumWaves	4
/NumContrasts	3

/Matrix
        """
        design_fts = np.array([[1,0,0],[0,1,0],[0,0,1]])


    if mnum != "model4":
        print("***********************************************")
        print("Saving design matrix for %s"%(mnum))
        print("***********************************************")
        np.savetxt('%s/%s_design.mat'%(mnum_path, mnum),design_matrix.values,fmt='%1.0f',header=deshdr,comments='')

    print("***********************************************")
    print("Saving contrast matrix for %s"%(mnum))
    print("***********************************************")
    np.savetxt('%s/%s_design.con'%(mnum_path, mnum),contrast_matrix,fmt='%1.0f',header=conhdr,comments='')

    if mnum != "model3":
        print("***********************************************")
        print("Saving design.fts for %s"%(mnum))
        print("***********************************************")
        np.savetxt('%s/%s_design.fts'%(mnum_path, mnum),design_fts,fmt='%1.0f',header=desfhdr,comments='')

mnums = ["model2", "model3", "model4"]
for mnum in mnums:
    make_design_files(mnum)
