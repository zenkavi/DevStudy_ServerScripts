fslmaths $FSLDIR/data/standard/MNI152_T1_2mm.nii.gz -mul 0 -add 1 -roi 44 1 86 1 32 1 0 1 VMPFC_point -odt float
fslmaths VMPFC_point.nii.gz -kernel sphere 5 -fmean VMPFC_sphere -odt float
fslmaths VMPFC_sphere.nii.gz -bin VMPFC_bin.nii.gz

fslmaths $FSLDIR/data/standard/MNI152_T1_2mm.nii.gz -mul 0 -add 1 -roi 39 1 69 1 33 1 0 1 LVStr_point -odt float
fslmaths LVStr_point.nii.gz -kernel sphere 5 -fmean LVStr_sphere -odt float
fslmaths LVStr_sphere.nii.gz -bin LVStr_bin.nii.gz

fslmaths $FSLDIR/data/standard/MNI152_T1_2mm.nii.gz -mul 0 -add 1 -roi 51 1 68 1 33 1 0 1 RVStr_point -odt float
fslmaths RVStr_point.nii.gz -kernel sphere 5 -fmean RVStr_sphere -odt float
fslmaths RVStr_sphere.nii.gz -bin RVStr_bin.nii.gz

fslmaths $FSLDIR/data/standard/MNI152_T1_2mm.nii.gz -mul 0 -add 1 -roi 30 1 74 1 33 1 0 1 LaIns_point -odt float
fslmaths LaIns_point.nii.gz -kernel sphere 5 -fmean LaIns_sphere -odt float
fslmaths LaIns_sphere.nii.gz -bin LaIns_bin.nii.gz

fslmaths $FSLDIR/data/standard/MNI152_T1_2mm.nii.gz -mul 0 -add 1 -roi 61 1 73 1 33 1 0 1 RaIns_point -odt float
fslmaths RaIns_point.nii.gz -kernel sphere 5 -fmean RaIns_sphere -odt float
fslmaths RaIns_sphere.nii.gz -bin RaIns_bin.nii.gz

fslmaths $FSLDIR/data/standard/MNI152_T1_2mm.nii.gz -mul 0 -add 1 -roi 43 1 48 1 54 1 0 1 PCC_point -odt float
fslmaths PCC_point.nii.gz -kernel sphere 5 -fmean PCC_sphere -odt float
fslmaths PCC_sphere.nii.gz -bin PCC_bin.nii.gz

fslmaths $FSLDIR/data/standard/MNI152_T1_2mm.nii.gz -mul 0 -add 1 -roi 44 1 77 1 50 1 0 1 ACC_point -odt float
fslmaths ACC_point.nii.gz -kernel sphere 5 -fmean ACC_sphere -odt float
fslmaths ACC_sphere.nii.gz -bin ACC_bin.nii.gz

fslmaths $FSLDIR/data/standard/MNI152_T1_2mm.nii.gz -mul 0 -add 1 -roi 44 1 71 1 59 1 0 1 preSMA_point -odt float
fslmaths preSMA_point.nii.gz -kernel sphere 5 -fmean preSMA_sphere -odt float
fslmaths preSMA_sphere.nii.gz -bin preSMA_bin.nii.gz
