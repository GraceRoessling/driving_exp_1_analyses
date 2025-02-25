import subject
import trial
import piece
import map
from IPython import embed
import dataframe_helper_functions
import parse_path_center_csv
import track_piece_correction
import lane_deviation

# ----------------------------------------------------------------------------------------------------------------------
# Helper funcs
def initialize_subjects(dir_path):
    subject_obj_dict = dict()
    subj_id_with_conditions_dict = subject.Subject.subject_id_dict
    familiar_id,unfamiliar_id = subj_id_with_conditions_dict.values()
    all_subj_ids = familiar_id+unfamiliar_id
    for subject_id in all_subj_ids:
        condition = (next(k for k, v in subj_id_with_conditions_dict.items() if subject_id in v))
        subject_object = subject.Subject(subject_id, condition,  dir_path)
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

# No need to modify this function to remove lane deviation calculations -- it simply stores the center of the track pieces
def initialize_maps_and_pieces(subject):
    for i in range(0,11): # iterate through 11 trials
        piece_obj_dict = dict() # nested dictionary that contains all values associated to each piece
        # iterate through track pieces for a given subject
        trial_object = subject.trials[i]
        map_object = map.Map(subject,trial_object)

        for track_id in map_object.pieces:
            print(track_id)
            piece_object = piece.Piece(track_id,subject,trial_object,map_object)
            piece_object.trajectory_df = dataframe_helper_functions.get_agent_trajectory_for_each_piece(piece_object)

        trial_object.number = i
        trial_object.map = map_object
        trial_object.pieces = piece_obj_dict

# ----------------------------------------------------------------------------------------------------------------------
# Main

def test_run(SUBJECT_PATH):
    subject_dict = initialize_subjects(SUBJECT_PATH)
    for subject_id in subject_dict:
        subject_object = subject_dict[subject_id]
        initialize_trials_for_one_subject(subject_object)
        initialize_maps_and_pieces(subject_object)
        print(subject_object.trials[0].pieces[0].number)

# def run(SUBJECT_PATH, LANE_DEVIATION_PATH):
#     subject_dict = initialize_subjects(SUBJECT_PATH)

#     # With subjects, create trial, map, and piece classes with the appropriate data
#     for subject_id in subject_dict:
#         subject_object = subject_dict[subject_id]
#         initialize_trials_for_one_subject(subject_object)
#         initialize_maps_and_pieces(subject_object)

#     # Attach data attributes (speed, steering, laptime, and lane deviation to objects)
#     for subject_id in subject_dict:
#         subject_object = subject_dict[subject_id]
#         # lane_deviation.grab_lane_deviation_data(subject_object, LANE_DEVIATION_PATH)
#         subject_object.speed,subject_object.steering,subject_object.lap_time,subject_object.lane_dev,subject_object.steering_acceleration = dict(),dict(),dict(),dict(),dict()
#         for i in range(0,10):
#             total_speed_dict,track_piece_speed_dict = dataframe_helper_functions.get_metrics_for_each_track_piece_for_one_trial("speed",subject_object.trials[i],subject_object.trials[i].map)
#             total_steering_dict,track_piece_steering_dict = dataframe_helper_functions.get_metrics_for_each_track_piece_for_one_trial("steering",subject_object.trials[i],subject_object.trials[i].map)
#             entire_trial_lap_time,track_piece_time_dict = dataframe_helper_functions.get_lap_time_or_steering_ac_for_each_track_piece_for_one_trial("lap_time",subject_object.trials[i],subject_object.trials[i].map)
#             total_lane_dev_dict,track_piece_lane_dev_dict = dataframe_helper_functions.get_metrics_for_each_track_piece_for_one_trial("lane_dev",subject_object.trials[i],subject_object.trials[i].map)
#             entire_trial_steering_acc,track_piece_steering_acc_dict = dataframe_helper_functions.get_lap_time_or_steering_ac_for_each_track_piece_for_one_trial("steering_acc",subject_object.trials[i],subject_object.trials[i].map)
#             subject_object.speed[i+1] = {f"trial_total":total_speed_dict,f"trial_piece":track_piece_speed_dict}
#             subject_object.steering[i+1] = {f"trial_total":total_steering_dict,f"trial_piece":track_piece_steering_dict}
#             subject_object.lap_time[i+1] = {f"trial_total":entire_trial_lap_time,f"trial_piece":track_piece_time_dict}
#             subject_object.lane_dev[i+1] = {f"trial_total":total_lane_dev_dict,f"trial_piece":track_piece_lane_dev_dict}
#             subject_object.steering_acceleration[i+1] = {f"trial_total":entire_trial_steering_acc,f"trial_piece":track_piece_steering_acc_dict}
#     return(subject_dict)

# def run_one_subject(SUBJECT_PATH, TRACK_CENTER_PATH, LANE_DEVIATION_PATH):
#     subject_dict = initialize_subjects(SUBJECT_PATH)

#     # With subjects, create trial, map, and piece classes with the appropriate data
#     for subject_id in subject_dict:
#         subject_object = subject_dict[subject_id]
#         initialize_trials_for_one_subject(subject_object)
#         initialize_maps_and_pieces(subject_object, TRACK_CENTER_PATH)

#     # Apply corrections to the ten maps 
#     master_dict,non_interp_dict = lane_deviation.generate_track_piece_dict(subject_dict)
#     track_piece_correction.correct_position_for_entire_dataset(subject_dict,master_dict)

#     # get metrics
#     subject_object = subject_dict["depth"]
#     lane_deviation.grab_lane_deviation_data(subject_object, LANE_DEVIATION_PATH)
#     subject_object.speed,subject_object.steering,subject_object.lap_time,subject_object.lane_dev,subject_object.steering_acceleration = dict(),dict(),dict(),dict(),dict()
#     for i in range(0,10):
#         total_speed_dict,track_piece_speed_dict = dataframe_helper_functions.get_metrics_for_each_track_piece_for_one_trial("speed",subject_object.trials[i],subject_object.trials[i].map)
#         total_steering_dict,track_piece_steering_dict = dataframe_helper_functions.get_metrics_for_each_track_piece_for_one_trial("steering",subject_object.trials[i],subject_object.trials[i].map)
#         entire_trial_lap_time,track_piece_time_dict = dataframe_helper_functions.get_lap_time_or_steering_ac_for_each_track_piece_for_one_trial("lap_time",subject_object.trials[i],subject_object.trials[i].map)
#         total_lane_dev_dict,track_piece_lane_dev_dict = dataframe_helper_functions.get_metrics_for_each_track_piece_for_one_trial("lane_dev",subject_object.trials[i],subject_object.trials[i].map)
#         entire_trial_steering_acc,track_piece_steering_acc_dict = dataframe_helper_functions.get_lap_time_or_steering_ac_for_each_track_piece_for_one_trial("steering_acc",subject_object.trials[i],subject_object.trials[i].map)
#         subject_object.speed[i+1] = {f"trial_total":total_speed_dict,f"trial_piece":track_piece_speed_dict}
#         subject_object.steering[i+1] = {f"trial_total":total_steering_dict,f"trial_piece":track_piece_steering_dict}
#         subject_object.lap_time[i+1] = {f"trial_total":entire_trial_lap_time,f"trial_piece":track_piece_time_dict}
#         subject_object.lane_dev[i+1] = {f"trial_total":total_lane_dev_dict,f"trial_piece":track_piece_lane_dev_dict}
#         subject_object.steering_acceleration[i+1] = {f"trial_total":entire_trial_steering_acc,f"trial_piece":track_piece_steering_acc_dict}
#         # print(subject_object.steering_acceleration[i+1])
#     return(subject_dict,master_dict,non_interp_dict)





