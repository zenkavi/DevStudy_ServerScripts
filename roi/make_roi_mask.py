#!/home/groups/russpold/software/miniconda/envs/fmri/bin/python
from argparse import ArgumentParser
import glob
from nipype.caching import Memory
mem = Memory(base_dir='.')
import numpy as np
import os
import pandas as pd

#Usage: ./make_roi_mask.py -x -y -z --name --template -o

parser = ArgumentParser()
parser.add_argument("-x", "--x")
parser.add_argument("-y", "--y",)
parser.add_argument("-z", "--z",)
parser.add_argument("-s", "--sphere",)
parser.add_argument("--name", default=np.nan)
parser.add_argument("--template", default="MNI152_T1_1mm_brain.nii.gz")
parser.add_argument("-o", "--out_dir", default=np.nan)
args = parser.parse_args()
coords = [int(args.x), int(args.y), int(args.z)]
sphere = args.sphere
name = args.name
template = args.template
out_dir = args.out_dir

def make_roi_mask(coords):

    print("***********************************************")
    print("Extracting point %s from template %s" %(coords, template))
    print("***********************************************")

    print("***********************************************")
    print("Saving point from template %s to %s" %(template, out_dir))
    print("***********************************************")

    print("***********************************************")
    print("Making %s mm sphere around %s" %(sphere, coords))
    print("***********************************************")

    print("***********************************************")
    print("Saving spherical mask to %s" %(out_dir))
    print("***********************************************")

    print("***********************************************")
    print("Binarizing spherical mask")
    print("***********************************************")

    print("***********************************************")
    print("Saving binarized spherical mask to %s"(out_dir))
    print("***********************************************")

    return

make_roi_mask(coords)
