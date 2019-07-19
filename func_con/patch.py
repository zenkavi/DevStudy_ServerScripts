import glob
import nibabel as nib
from nilearn.image import mean_img
import os

data_loc = os.environ['DATA_LOC']
out_path = '%s/derivatives/func_con/'%(data_loc)

seed_name = "l_vstr"

subs = glob.glob(out_path)

for sub in subs:
    run_cor_imgs = glob.glob('%s/%s/%s_run-*_%s_cor_img.nii.gz'%(out_path, sub, sub, seed_name))
    mean_cor_img = mean_img(run_cor_imgs)
    nib.save(mean_cor_img, '%s/%s/%s_run-ave_%s_cor_img.nii.gz'%(out_path, sub, sub, seed_name))
    print("***********************************************")
    print("Done saving average cor image for sub-%s for %s"%(sub, seed_name))
    print("***********************************************")
