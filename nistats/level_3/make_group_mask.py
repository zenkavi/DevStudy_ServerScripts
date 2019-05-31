import os
import glob
import nibabel as nib
from nilearn.image import mean_img, math_img

#Usage: python make_group_mask.py

data_loc = os.environ['DATA_LOC']

brainmasks = glob.glob("%s/derivatives/fmriprep_1.3.0/fmriprep/sub-*/func/*brain_mask.nii*"%(data_loc))

mean_mask = mean_img(brainmasks)
group_mask = math_img("a>=0.95", a=mean_mask)

mnums = ['model1', 'model2', 'model3']
regs = ['m1', 'm2', 'm3', 'm4', 'hpe', 'lpe', 'pe', 'task_on', 'rt', 'ev_sen', 'var_sen']

for mnum in mnums:
    for reg in regs:
        copes_concat = nib.load("all_l2_%s_%s.nii.gz"%(mnum, reg))
        group_mask = nilearn.image.resample_to_img(group_mask, copes_concat, interpolation='nearest')
        group_mask.to_filename("%s/derivatives/nistats/level_3/%s/group_mask_%s_%s.nii.gz"%(data_loc, mnum, mnum,reg))
        rint("***********************************************")
        print("Group mask saved for: %s"%(mnum, reg))
        print("***********************************************")
