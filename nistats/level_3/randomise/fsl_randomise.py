from  nipype.interfaces import fsl
from nipype.caching import Memory
mem = Memory(base_dir='.')
from argparse import ArgumentParser

#Usage = python fsl_randomise.py --mnum model1 --reg hpe -tf -np

arser = ArgumentParser()
parser.add_argument("-m", "--mnum", help="model number")
parser.add_argument("-r", "--reg", help="regressor name")
parser.add_argument("-tf", "--tfce", help="tfce", default=True)
parser.add_argument("-np", "--num_perm", help="number of permutations", default=1000)
args = parser.parse_args()
mnum = args.mnum
reg = args.reg
one = False
if mnum == "model1":
    one = True
tfce = args.tfce
num_perm = args.num_perm

data_loc = os.environ['DATA_LOC']
server_scripts = os.environ['SERVER_SCRIPTS']
in_path = "%s/derivatives/nistats/level_3/%s/%s"%(data_loc, mnum, reg)

randomise = mem.cache(fsl.Randomise)
randomise_results = randomise(in_file=glob.glob('all*', in_path),
                              mask=os.path.join(datadir, "derivatives", "custom_modelling", "group_mask.nii.gz"),
                              one_sample_group_mean=one,
                              tfce=tfce,
                              vox_p_values=True,
                              num_perm=num_perm)
