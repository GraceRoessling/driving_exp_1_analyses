import pandas as pd
import numpy as np
import os
import subject
import trial
import piece
import map
from IPython import embed
import dataframe_helper_functions
import parse_path_center_csv

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
        trial_object.trajectory_df = dataframe_helper_functions.get_agent_trajectory_for_each_map(trial_object)
        trial_object_list.append(trial_object)
    subject.trials = trial_object_list

def initialize_maps_and_pieces(subject):
    for i in range(0,10): # iterate through all ten trials
        piece_obj_dict = dict() # nested dictionary that contains all values associated to each piece
        # iterate through track pieces for a given subject
        trial_object = subject.trials[i]
        map_object = map.Map(subject,trial_object)
        map_object.center_dict = parse_path_center_csv.add_dicts_to_map_object(map_object.map_number)
        count = 1

        for track_id in map_object.pieces:
            piece_object = piece.Piece(track_id,subject,trial_object,map_object)
            piece_object.trajectory_df = dataframe_helper_functions.get_agent_trajectory_for_each_piece(piece_object)

            # for map six, there are technically two instances of a given track piece. iterate through and label each as separate instances
            if map_object.pieces.count(track_id) > 1:
                piece_obj_dict[f"{track_id}_{count}"] = piece_object
                count += 1
            elif map_object.pieces.count(track_id) == 1:
                piece_obj_dict[track_id] = piece_object
            piece_object.center_of_track_df = map_object.center_dict[track_id]

        trial_object.map = map_object
        trial_object.pieces = piece_obj_dict
        # if map_object.map_number == "6": 
        #     print(trial_object.number)
        #     print(map_object.pieces)
        #     print(trial_object.pieces)
        #     print("#-----------------------------")

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





