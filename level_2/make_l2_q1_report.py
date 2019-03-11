import os
import glob

try:
    data_loc = os.environ['DATA_LOC']
    server_scripts = os.environ['SERVER_SCRIPTS']
except KeyError:
    os.system('source /oak/stanford/groups/russpold/users/zenkavi/DevStudy_ServerScripts/setup/dev_study_env.sh')
    data_loc = os.environ['DATA_LOC']
    server_scripts = os.environ['SERVER_SCRIPTS']

outfile = "%s/derivatives/level_2/l2_qa.html"%(data_loc)

all_feats = "%s/derivatives/level_2/*/model/*.gfeat"
all_feats.sort()

f = open(outfile, "w")
for file in all_feats:
    f.write("<p>==============================================")
    f.write("<p>%s"%(file))
    f.write("<IMG SRC=\"%s/inputreg/maskunique_overlay.png\">"%(file))
f.close()
