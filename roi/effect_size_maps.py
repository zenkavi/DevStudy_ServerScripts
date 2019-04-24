import glob
import pickle
import nistats
import os

data_loc = os.environ['DATA_LOC']

models_path = "%s/derivatives/nistats/level_2/sub-*"%(data_loc)

model_files = glob.glob(models_path+'/*_glm.pkl')

f = open(m, 'rb')
model = pickle.load(f)

es_map = model.compute_contrast(output_type='effect_size')

os.mkdir(os.path.dirname(m)+'/contrasts/es_maps')

nib.save(es_map, os.path.dirname(m)+'/contrasts/es_maps/tmp.nii.gz')
