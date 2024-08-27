import pandas as pd
import piece
import math
import IPython
import numpy as np
from collections import defaultdict
import steering_acceleration_analysis

# filter dataframes --------------------------------------------------------------------------
def check_repeating_sequences(df):
    # Convert the column to a list for easier manipulation
    col_list = df["current_track_piece"].tolist()
    
    # Dictionary to store the count of sequences for each unique value
    sequence_counts = {}
    
    current_value = None
    sequence_started = False
    
    for value in col_list:
        if value != current_value:
            # New value encountered
            if sequence_started:
                sequence_counts[current_value] = sequence_counts.get(current_value, 0) + 1
            current_value = value
            sequence_started = True
        elif not sequence_started:
            # Continuing a sequence
            sequence_started = True
    
    # Check the last sequence
    if sequence_started:
        sequence_counts[current_value] = sequence_counts.get(current_value, 0) + 1
    
    # Check if any value has more than one sequence
    return any(count > 1 for count in sequence_counts.values())

def modify_duplicate_sequences(df):
    # Convert the column to a list for easier manipulation
    col_list = df["current_track_piece"].tolist()
    
    # Find all unique values in the column
    unique_values = set(col_list)
    
    for value in unique_values:
        # Find all occurrences of sequences of the value
        sequences = []
        start = 0
        while start < len(col_list):
            try:
                start = col_list.index(value, start)
                end = start
                while end < len(col_list) and col_list[end] == value:
                    end += 1
                sequences.append((start, end))
                start = end
            except ValueError:
                break
        
        # If there are at least two sequences of the same value
        if len(sequences) >= 2:
            # Modify the first sequence
            for i in range(sequences[0][0], sequences[0][1]):
                col_list[i] = f"{col_list[i]}_1"
            
            # Modify the second sequence
            for i in range(sequences[1][0], sequences[1][1]):
                col_list[i] = f"{col_list[i]}_2"
    
    # Update the DataFrame column with the modified list
    df["current_track_piece"] = col_list
    
    return df

def find_ranges(lst, target):
    result = []
    start = -1
    
    for i, item in enumerate(lst):
        if item == target:
            if start == -1:
                start = i
        elif start != -1:
            result.extend([start, i-1])
            start = -1
    
    if start != -1:
        result.extend([start, len(lst)-1])

    return result


def remove_NA(cam_position_df,vehicle_position_df,driving_vars_df):
    na_indices = list(driving_vars_df.loc[pd.isna(driving_vars_df["current_track_piece"]), :].index)
    driving_vars_df = driving_vars_df.drop(index = na_indices).reset_index()
    vehicle_position_df = vehicle_position_df.drop(index = na_indices).reset_index()
    cam_position_df = cam_position_df.drop(index = na_indices).reset_index()
    return(cam_position_df,vehicle_position_df,driving_vars_df)

def get_track_piece_indices(piece_object,cam_position_df,vehicle_position_df,driving_vars_df):
    driving_vars_df['current_track_piece'] = remove_substring(driving_vars_df['current_track_piece'], "_collider")
    indices_for_track_piece = list(driving_vars_df.index[driving_vars_df['current_track_piece'].str.contains(piece_object.id)])
    track_piece_driving_var = driving_vars_df[driving_vars_df['current_track_piece'].str.contains(piece_object.id)]    
    first_index,last_index = indices_for_track_piece[0],indices_for_track_piece[-1]
    track_piece_cam_pos = cam_position_df.iloc[first_index:last_index+1]
    track_piece_vehicle_pos = vehicle_position_df.iloc[first_index:last_index+1]
    return(track_piece_cam_pos,track_piece_vehicle_pos,track_piece_driving_var)

def remove_substring(string_list, substring):
    cleaned_list = []
    for string in string_list:
        cleaned_string = string.replace(substring, '')
        cleaned_list.append(cleaned_string)
    return cleaned_list

def get_agent_trajectory_for_each_map(trial):
    trajectory_df = trial.paths["vehicle_movement"]
    trajectory_df = trajectory_df[["time", "pos_x", "pos_z"]]
    return(trajectory_df)

def get_agent_trajectory_for_each_piece(piece):   
    trajectory_piece_df = piece.dataframes["vehicle_movement"]
    trajectory_piece_df = trajectory_piece_df[["time", "pos_x", "pos_z"]]
    return(trajectory_piece_df)

# transformation functions ------------------------------------------------------------------------
# function for calculating speed
speed = lambda x,y,z: math.sqrt(x*x + y*y + z*z)
def get_speed_per_frame(driving_vars_df):
    driving_vars_df = driving_vars_df.copy()
    velocity_x = list(driving_vars_df["velocity_x"])
    velocity_y = list(driving_vars_df["velocity_y"])
    velocity_z = list(driving_vars_df["velocity_z"])

    speed_array = []
    
    for i in range(0,len(velocity_x)):
        x,y,z = velocity_x[i],velocity_y[i],velocity_z[i]
        current_speed = speed(x,y,z)
        speed_array.append(current_speed)
    
    driving_vars_df.loc[:,'velocity_magnitude'] = speed_array
    return(driving_vars_df)

map_to_steering_angle = lambda input,input_start,input_end,output_start,output_end: output_start + ((output_end - output_start) / (input_end - input_start)) * (input - input_start)
def convert_steering_value(driving_vars_df):
    input_start, input_end = -1, 1
    output_start, output_end = -135, 135
    
    # take steering input and convert from -1 to 1 --> 0 --> 35 degrees
    steering_array = driving_vars_df['steering_angle'].tolist()
    steering_angle_array = []
    for current_steering_input in steering_array:
        steering_angle = round(map_to_steering_angle(current_steering_input, input_start, input_end, output_start, output_end), 3)
        steering_angle_array.append(steering_angle)
    
    driving_vars_df.loc[:, 'steering_angle'] = steering_angle_array
    return(driving_vars_df)

# conduct analyses across groups -----------------------------------------------------------
# general var function!
def get_metrics_for_each_track_piece_for_one_trial(metric_type_as_string,trial,map):
    whole_trial_driving_sim_df = trial.paths["Vehicle_DrivingSim"]
    total_var_dict = dict() # collect total
    track_piece_dict = dict() # collect data for each piece

    if metric_type_as_string == "speed":
        whole_trial_df_column = whole_trial_driving_sim_df["velocity_magnitude"]
    elif metric_type_as_string == "steering":
        whole_trial_df_column = whole_trial_driving_sim_df["steering_angle"]
    elif metric_type_as_string == "lane_dev":
        whole_trial_df_column = trial.trial_lane_dev_df["lane_dev"]
        whole_trial_df_column = whole_trial_df_column.replace([np.inf, -np.inf], 0)
        whole_trial_df_column = whole_trial_df_column.abs()

    # get total trial time
    whole_trial_mean = whole_trial_df_column.mean()
    whole_trial_var = whole_trial_df_column.var()
    whole_trial_sd = whole_trial_df_column.std()
    total_var_dict = {f"mean_{metric_type_as_string}":whole_trial_mean, f"var_{metric_type_as_string}":whole_trial_var, f"sd_{metric_type_as_string}":whole_trial_sd}

    # iterate through track pieces and get speed info for each
    all_track_pieces = map.pieces # list of pieces associated to a given map
    for track_piece_id in all_track_pieces:
        track_piece_object = trial.pieces[track_piece_id]
        driving_sim_df = track_piece_object.dataframes["Vehicle_DrivingSim"]  

        if metric_type_as_string == "speed":
            piece_df_column = driving_sim_df["velocity_magnitude"]
        elif metric_type_as_string == "steering":
            piece_df_column = driving_sim_df["steering_angle"]
        elif metric_type_as_string == "lane_dev":
            piece_df_column = track_piece_object.lane_dev_df["lane_dev"]
            piece_df_column = piece_df_column.replace([np.inf, -np.inf], 0)
            piece_df_column = piece_df_column.abs()
        piece_mean = piece_df_column.mean()
        piece_var = piece_df_column.var()
        piece_sd = piece_df_column.std()
                
        track_piece_dict[track_piece_id] = {f"mean_{metric_type_as_string}":piece_mean, f"var_{metric_type_as_string}":piece_var, f"sd_{metric_type_as_string}":piece_sd}
    return(total_var_dict,track_piece_dict)


def get_lap_time_or_steering_ac_for_each_track_piece_for_one_trial(metric_type_as_string,trial,map):
    # collect speed information in this dictionary
    track_piece_dict = dict()

    # get total trial time
    whole_trial_driving_sim_df = trial.paths["Vehicle_DrivingSim"]

    if metric_type_as_string == "lap_time":
        entire_trial_first_time_step = whole_trial_driving_sim_df["time"].iloc[0]
        entire_trial_last_time_step = whole_trial_driving_sim_df["time"].iloc[-1]
        entire_trial = entire_trial_last_time_step - entire_trial_first_time_step

    elif metric_type_as_string == "steering_acc":
        steering_accelerations = steering_acceleration_analysis.calculate_average_steering_acceleration(whole_trial_driving_sim_df)
        entire_trial = np.mean(steering_accelerations)
    # collapse the dictionary into a list
    all_track_pieces = map.pieces # list of pieces associated to a given map

    # iterate through track pieces and get speed info for each
    for track_piece_id in all_track_pieces:
        track_piece_object = trial.pieces[track_piece_id]
        driving_sim_df = track_piece_object.dataframes["Vehicle_DrivingSim"]
        
        if metric_type_as_string == "lap_time":
            first_time_step = driving_sim_df["time"].iloc[0]
            last_time_step = driving_sim_df["time"].iloc[-1]
            total_lap_time = last_time_step - first_time_step
            track_piece_dict[track_piece_id] = {"lap_time":total_lap_time}
        
        elif metric_type_as_string == "steering_acc":
            piece_steering_accelerations = steering_acceleration_analysis.calculate_average_steering_acceleration(driving_sim_df)
            piece_steering_acc = np.mean(piece_steering_accelerations)
            track_piece_dict[track_piece_id] = {"steering_acceleration":piece_steering_acc}
    return(entire_trial,track_piece_dict)

def get_unique_consecutive_strings(string_list):
    unique_strings = []
    prev_string = None
    
    for curr_string in string_list:
        if curr_string != prev_string:
            unique_strings.append(curr_string)
            prev_string = curr_string
    
    return unique_strings