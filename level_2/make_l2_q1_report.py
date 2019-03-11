import os
import glob

try:
    data_loc = os.environ['DATA_LOC']
except KeyError:
    os.system('source /oak/stanford/groups/russpold/users/zenkavi/DevStudy_ServerScripts/setup/dev_study_env.sh')
    data_loc = os.environ['DATA_LOC']

outfile = "%s/derivatives/level_2/l2_qa.html"%(data_loc)

all_feats = glob.glob("%s/derivatives/level_2/*/model/*.gfeat"%(data_loc))
all_feats.sort()

f = open(outfile, "w")
for file in all_feats:
    f.write("<p>==============================================")
    f.write("<p>%s"%(file))
    f.write("<IMG SRC=\"https://login.sherlock.stanford.edu/pun/sys/files/fs/%s/inputreg/maskunique_overlay.png\">"%(file))
f.close()

https://login.sherlock.stanford.edu/pun/sys/files/fs/oak/stanford/groups/russpold/data/ds000054/0.0.4/derivatives/level_2/sub-100003/model/100003.gfeat/inputreg/
