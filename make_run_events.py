#!/usr/bin/python
from __future__ import division
import csv
import sys

if len(sys.argv) < 5:
    sys.exit("Usage: makeRunEvents.py file.csv number_of_trials task_name sub_id sub_dir_name")

filename = sys.argv[1]
file_length = sum(1 for row in csv.reader(open(filename,'rb'))) - 1
N = int(sys.argv[2])
task_name = sys.argv[3]
sub_id = sys.argv[4]
sub_dir_name = sys.argv[5]

#Cols: onset, duration, trial_type, response, stimulus, rt, points_earned
#Rows based on trial_type: stim_presentation, response, [ITI - make this a column instead]
																
#Read in each file, process by run
#For each run the first Trial_start_time == run_start_time
#For trial_type == stim_presentation: onset == Trial_start_time - run_start_time
#For trial_type == stim_presentation: duration ==  Stim_end_time - Trial_start_time
#For trial_type == response: onset == (Trial_start_time + Reaction_time)-run_start_time
#For trial_type == response: duration == Stim_end_time-(Trial_start_time+Reaction_time)

#Create each two trial_type onset df separately and then put them together

#Note response duration and stim_presentation durations will be overlapping if defined this way (Duration for trial_type == response doesn't seem to make much sense anyway)
#Each run will start at 0 onset for stim presentation (because the scanner triggers the beginning of stimulus presentation in each run)

#run_events_list should be a list of len 31 with header for the first row and run data for the rest of the rows
def makeStimPresentationOnset(run_events_list):
	noheader = run_events_list[1:len(run_events_list)]
	
	#annoying but I don't want to hard code col numbers	
	trial_start_time_index = run_events_list[0].index('Trial_start_time')
	stim_end_time_index = run_events_list[0].index('Stim_end_time')
	stim_index = run_events_list[0].index('Trial_type')
	iti_start_time_index = run_events_list[0].index('ITI_start_time')
	iti_length_index = run_events_list[0].index('ITI_length')
	
	run_start_time = int(noheader[0][trial_start_time_index])	
	onsets = [(int(x[trial_start_time_index]) - run_start_time)/1000 for x in noheader]
	durations = [(int(x[stim_end_time_index]) - int(x[trial_start_time_index]))/1000 for x in noheader]
	trial_type = 'stim_presentation'
	response = 'n/a'
	stimulus = [x[stim_index] for x in noheader]
	rt = 'n/a'
	points_earned = 'n/a'
	iti_start_time = [int(x[iti_start_time_index])/1000 for x in noheader]
	iti_length = [int(x[iti_length_index].split(".")[0])/1000 for x in noheader]
	
	output = []
	for i in range(len(onsets)):
		output.append([onsets[i],durations[i], trial_type, response, stimulus[i], rt, points_earned, iti_start_time[i], iti_length[i]])
	return output
	
def makeResponseOnset(run_events_list):
	noheader = run_events_list[1:len(run_events_list)]
	
	#annoying but I don't want to hard code col numbers	
	trial_start_time_index = run_events_list[0].index('Trial_start_time')
	stim_end_time_index = run_events_list[0].index('Stim_end_time')
	stim_index = run_events_list[0].index('Trial_type')
	reaction_time_index = run_events_list[0].index('Reaction_time')
	response_index = run_events_list[0].index('Response')	
	points_earned_index = run_events_list[0].index('Points_earned')
	iti_start_time_index = run_events_list[0].index('ITI_start_time')
	iti_length_index = run_events_list[0].index('ITI_length')
	
	run_start_time = int(noheader[0][trial_start_time_index])	
		
	onsets = [((int(x[trial_start_time_index]) + int(x[reaction_time_index])) - run_start_time)/1000 for x in noheader]	
	durations = [(int(x[stim_end_time_index]) - (int(x[trial_start_time_index])) + int(x[reaction_time_index]))/1000 for x in noheader]
	
	trial_type = 'response'
	response = [x[response_index] for x in noheader]
	stimulus = [x[stim_index] for x in noheader]
	rt = [x[reaction_time_index] for x in noheader]
	points_earned = [x[points_earned_index] for x in noheader]
	iti_start_time = [int(x[iti_start_time_index])/1000 for x in noheader]
	iti_length = [int(x[iti_length_index].split(".")[0])/1000 for x in noheader]
	
	output = []
	for i in range(len(onsets)):
		output.append([onsets[i],durations[i], trial_type, response[i], stimulus[i], rt[i], points_earned[i], iti_start_time[i], iti_length[i]])
		
	#Remove trials where there wasn't a response
	output = [x for x in output if x[3] != 0]
	
	return output
	
with open(filename) as csvfile:
	allcontent = list(csv.reader(csvfile))
	header = allcontent[0]
	noheader = allcontent[1:len(allcontent)]
	for i in range(file_length//N):
		run_events_list = [header] + noheader[N*(i+1)-(N):N*(i+1)]
		stim_presentation_onset = makeStimPresentationOnset(run_events_list)
		response_onset= makeResponseOnset(run_events_list)
		run_onsets = stim_presentation_onset+response_onset
		run_onsets.sort()
		run_onsets_header = ["onset", "duration", "trial_type", "response", "stimulus", "response_time", "points_earned", "iti_start_time", "iti_length"]
		with open('/corral-repl/utexas/poldracklab/users/zenkavi/DevStudy_TaccScripts/data/sub-'+sub_dir_name+'/func/sub-'+sub_id+'_task-'+task_name+'_run-0'+str(i+1)+'_events.tsv', 'wb') as tsvfile:
#		with open('./Downloads/test_task-machinegame_run-0'+str(i+1)+'_events.tsv', 'wb') as tsvfile:
			writer = csv.writer(tsvfile, quoting=csv.QUOTE_NONE, delimiter='\t', quotechar='')
			writer.writerow(run_onsets_header)
			writer.writerows(run_onsets);

