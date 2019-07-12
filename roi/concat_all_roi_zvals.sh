cd /oak/stanford/groups/russpold/data/ds000054/0.0.4/derivatives/rois/tpl-MNI152NLin2009cAsym_res-02_desc-brain_T1w
cat *zvals.csv > /oak/stanford/groups/russpold/data/ds000054/0.0.4/derivatives/rois/tpl-MNI152NLin2009cAsym_res-02_desc-brain_T1w/all_roi_pe_zvals.csv
awk '!a[$0]++' all_roi_pe_zvals.csv > all_roi_pe_zvals_clean.csv
rm all_roi_pe_zvals.csv
mv all_roi_pe_zvals_clean.csv ./all_roi_pe_zvals.csv
