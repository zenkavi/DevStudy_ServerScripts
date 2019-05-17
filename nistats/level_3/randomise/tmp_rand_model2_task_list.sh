randomise -i $MODEL_DIR/var_sen/all_l2_model2_var_sen.nii.gz -o $MODEL_DIR/var_sen/rand_anova/group_diff -d $MODEL_DIR/var_sen/model2_var_sen.mat -t $MODEL_DIR/design.con -n 1000 -T
randomise -i $MODEL_DIR/ev_sen/all_l2_model2_ev_sen.nii.gz -o $MODEL_DIR/ev_sen/rand_anova/group_diff -d $MODEL_DIR/ev_sen/model2_ev_sen.mat -t $MODEL_DIR/design.con -n 1000 -T
