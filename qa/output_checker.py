#Usage: python path string num_match
#Example: python output_checker.py -sp /oak/stanford/groups/russpold/data/ds000054/0.0.4/derivatives/level_1/* -ss sub-*_task-machinegame_run-*_cond1.txt -nm 6

import glob
import os
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-sp", "--search_path", help="search pah")
parser.add_argument("-ss", "--search_string", help="search string")
parser.add_argument("-nm", "--num_match", help="num of expected occurences", default='')
args = parser.parse_args()

search_path = args.search_path
search_string = args.search_string
num_match = args.num_match

subjects = ["sub-100003","sub-100009","sub-100042","sub-100051","sub-100057","sub-100059","sub-100062","sub-100063","sub-100068","sub-100103","sub-100104","sub-100105","sub-100110","sub-100128","sub-100129","sub-100143","sub-100152","sub-100169","sub-100180","sub-100185","sub-100188","sub-100191","sub-100207","sub-100214","sub-100241","sub-100243","sub-100244","sub-100247","sub-100250","sub-200025","sub-200056","sub-200061","sub-200085","sub-200088","sub-200133","sub-200148","sub-200156","sub-200162","sub-200164","sub-200166","sub-200168","sub-200173","sub-200199","sub-200211","sub-200213","sub-200249","sub-306065","sub-306587","sub-310949","sub-311047","sub-311283","sub-311444","sub-311479","sub-311760","sub-400285","sub-400742","sub-402997","sub-405027","sub-406620","sub-406925","sub-406980","sub-407209","sub-407260","sub-407672","sub-408394","sub-408511","sub-408662","sub-408952","sub-408988","sub-409381","sub-409850","sub-409874","sub-411256","sub-411477"]

found_files = glob.glob(os.path.join(search_path, search_string))
found_files.sort()

found_files = [os.path.basename(x) for x in found_files]

found_subs = ['sub-'+x.split('sub-')[1][0:6] for x in found_files if x.find('sub') != -1 ]

incomplete_subs = [x for x in subjects if found_subs.count(x) != num_match ]

for inc_sub in incomplete_subs:
    print("%s does not have requested number of matches"%(inc_sub))
    print("\n")
    print("Found files for this subject are:")
    inc_sub_files = [s for s in found_files if inc_sub in s]
    inc_sub_files.sort()
    print(inc_sub_files)
    print("************************************************************************************")
