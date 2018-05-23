#!/usr/bin/env python
#Usage: python fix_fmap_json.py sub_dir_name
import os, sys, json
sys.path = ['',
 '/opt/apps/intel16/python/2.7.11/lib/python2.7/site-packages/setuptools-20.2.2-py2.7.egg',
 '/opt/apps/intel16/python/2.7.11/lib/python2.7/site-packages/pip-8.1.0-py2.7.egg',
 '/opt/apps/intel16/python/2.7.11/lib/python2.7/site-packages/matplotlib-1.5.1-py2.7-linux-x86_64.egg',
 '/opt/apps/intel16/python/2.7.11/lib/python2.7/site-packages/pyparsing-2.1.0-py2.7.egg',
 '/opt/apps/intel16/python/2.7.11/lib/python2.7/site-packages/cycler-0.10.0-py2.7.egg',
 '/opt/apps/intel16/python/2.7.11/lib/python2.7/site-packages/pytz-2015.7-py2.7.egg',
 '/opt/apps/intel16/python/2.7.11/lib/python2.7/site-packages/python_dateutil-2.5.0-py2.7.egg',
 '/opt/apps/intel16/python/2.7.11/lib/python2.7/site-packages',
 '/opt/apps/intel16/python/2.7.11/bin',
 '/opt/apps/intel16/cray_mpich_7_3/python/2.7.11/lib/python2.7/site-packages',
 '/work/01329/poldrack/lonestar/software_lonestar5/anaconda/Anaconda2-4.1.1/lib/python2.7/site-packages',
 '/opt/apps/intel16/python/2.7.11/lib/python27.zip',
 '/opt/apps/intel16/python/2.7.11/lib/python2.7',
 '/opt/apps/intel16/python/2.7.11/lib/python2.7/plat-linux2',
 '/opt/apps/intel16/python/2.7.11/lib/python2.7/lib-tk',
 '/opt/apps/intel16/python/2.7.11/lib/python2.7/lib-old',
 '/opt/apps/intel16/python/2.7.11/lib/python2.7/lib-dynload',
 '/opt/apps/intel16/python/2.7.11/lib/python2.7/site-packages/IPython/extensions',
 '/home1/04127/zenkavi/.ipython']

if len(sys.argv) < 1:
    sys.exit("Usage: fix_fmap_jsons.py sub_dir_name")

fmap_path = sys.argv[1]+'/fmap/' #make sure paths end with '/'

json_file_names = [s for s in os.listdir(fmap_path) if ".json" in s]

echo_times = []

for i in json_file_names:
	with open(fmap_path+i) as data_file:
	    data = json.load(data_file)
	    echo_times.append(data['EchoTime'])

echo_times = list(set(echo_times))

echo_times_json = {}

for i in range(len(echo_times)):
	echo_times_json['EchoTime'+str(i+1)]= echo_times[i]

for i in json_file_names:
	with open(fmap_path+i) as data_file:
		data = json.load(data_file)
		del(data['EchoTime'])
		data.update(echo_times_json)
	with open(fmap_path+i, "w") as out_file:
		json.dump(data, out_file)
