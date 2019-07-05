import glob
from bs4 import BeautifulSoup
import urllib
import os

data_loc = os.environ['DATA_LOC']
fmriprep_reports = glob.glob('%s/derivatives/fmriprep_1.4.0/fmriprep/*.html'%(data_loc))
fmriprep_reports.sort()

for report_path in fmriprep_reports:
    report_html  = open(report_path, "r").read()
    soup = BeautifulSoup(report_html, 'html.parser')
    if str(soup.find(id= "errors").find('li')) != '<li>No errors to report!</li>':
        print(os.path.basename(report_path))
