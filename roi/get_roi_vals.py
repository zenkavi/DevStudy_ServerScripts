import nibabel as nib
import numpy as np
import nilearn
def get_roi_vals(mask, img):
    #mask and image can be paths or niftis
    #Load nifti's if they are strings
    if type(mask) == str:
        mask = nib.load(mask)
    if type(img) == str:
        img = nib.load(img)

    #resample mask to image dimensions if they don't match
    img_data = img.get_fdata()
    mask_data = mask.get_fdata()
    if img_data.shape != mask_data.shape[:3]:
        print("Image dimensions: %s"%(img_data.shape,))
        print("Mask dimensions: %s"%(mask_data.shape,))
        print("Resampling mask ...")
        mask = nilearn.image.resample_to_img(mask, img)
        mask_data = mask.get_fdata()
        #binarize resampled mask data
        mask_data = np.where(mask_data >0.1,1,0)
        #mask = nilearn.image.new_img_like(img, mask_data)

    roi_data = np.where(mask_data == 1,img_data,0)
    roi_data = roi_data[roi_data != 0]

    return roi_data
