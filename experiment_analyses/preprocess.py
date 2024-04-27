import pandas as pd
import numpy as np
import os
import subject
import trial
import piece
import map
from IPython import embed
import dataframe_helper_functions

# ----------------------------------------------------------------------------------------------------------------------
# Helper funcs
def initialize_subjects():
    subject_obj_dict = dict()
    subj_id_with_conditions_dict = subject.Subject.subject_id_dict
    familiar_id,unfamiliar_id = subj_id_with_conditions_dict.values()
    all_subj_ids = familiar_id+unfamiliar_id
    for subject_id in all_subj_ids:
        condition = (next(k for k, v in subj_id_with_conditions_dict.items() if subject_id in v))
        subject_object = subject.Subject(subject_id, condition)
        subject_obj_dict[subject_id] = subject_object
    return subject_obj_dict

def initialize_trials_for_one_subject(subject):
    trial_object_list = []
    for count, trial_string in enumerate(trial.Trial.trial_str_list):
        trial_id = trial_string
        trial_num = count +1
        trial_object = trial.Trial(trial_id,trial_num, subject)
        trial_object_list.append(trial_object)
    subject.trials = trial_object_list

def initialize_maps_and_pieces(subject):
    piece_obj_dict = dict() # nested dictionary that contains all values associated to each piece
    for i in range(0,10): # iterate through all ten trials
        # iterate through track pieces for a given subject
        trial = subject.trials[i]
        map_object = map.Map(subject,trial)
        for track_id in map_object.pieces:
            piece_object = piece.Piece(track_id,subject,trial,map_object)
            piece_obj_dict[track_id] = piece_object
        trial.map = map_object
        trial.pieces = piece_obj_dict

# ----------------------------------------------------------------------------------------------------------------------
# Main

subject_dict = initialize_subjects()
for subject_id in subject_dict:
    if subject_id == "wad":
        pass
    else:
        subject_object = subject_dict[subject_id]
        subject_object.speed,subject_object.steering,subject_object.lap_time = dict(),dict(),dict()
        initialize_trials_for_one_subject(subject_object)
        initialize_maps_and_pieces(subject_object)

        for i in range(0,10):
            total_speed_dict,track_piece_speed_dict = dataframe_helper_functions.get_metrics_for_each_track_piece_for_one_trial("speed",subject_object.trials[i],subject_object.trials[i].map)
            total_steering_dict,track_piece_steering_dict = dataframe_helper_functions.get_metrics_for_each_track_piece_for_one_trial("steering",subject_object.trials[i],subject_object.trials[i].map)
            entire_trial_lap_time,track_piece_time_dict = dataframe_helper_functions.get_lap_time_for_each_track_piece_for_one_trial(subject_object.trials[i],subject_object.trials[i].map)
            subject_object.speed[i+1] = {f"trial_total":total_speed_dict,f"trial_piece":track_piece_speed_dict}
            subject_object.steering[i+1] = {f"trial_total":total_steering_dict,f"trial_piece":track_piece_steering_dict}
            subject_object.lap_time[i+1] = {f"trial_total":entire_trial_lap_time,f"trial_piece":track_piece_time_dict}