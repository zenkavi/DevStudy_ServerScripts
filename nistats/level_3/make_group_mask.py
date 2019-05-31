

brainmasks = glob.glob("%s/derivatives/fmriprep_1.3.0/fmriprep/sub-*/func/*brain_mask.nii*"%(data_loc))

mean_mask = nilearn.image.mean_img(brainmasks)
group_mask = nilearn.image.math_img("a>=0.95", a=mean_mask)



group_mask = nilearn.image.resample_to_img(group_mask, copes_concat, interpolation='nearest')
group_mask.to_filename("%s/derivatives/nistats/level_3/model1/group_mask_%s.nii.gz"%(..., reg))
