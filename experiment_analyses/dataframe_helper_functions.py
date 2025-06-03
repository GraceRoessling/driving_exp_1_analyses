import pandas as pd
import map
import piece
import math
import re
import IPython
import numpy as np
from collections import defaultdict
import os
import steering_acceleration_analysis
import trial
import re


# filter dataframes --------------------------------------------------------------------------

def extract_map_number(filename):
    filename_lower = filename.lower()
    
    if 'control' in filename_lower or 'landmark' in filename_lower:
        print("map 10")
        return 10
    elif 'ss' and 'trial_11' in filename_lower:
        print("map 11")
        return 11
    elif 'ss' in filename_lower:
        match = re.search(r'map_(\d+)', filename_lower)
        if match:
            print("map", int(match.group(1)))
            return int(match.group(1))
    elif 'trial_11' in filename_lower:
        print("map 11")
        return 11
    print(filename_lower)
    return None  # Return None if no conditions are met

def clean_track_data(driving_vars_df,cam_position_df,vehicle_position_df):
    if "RESET" not in driving_vars_df["current_track_piece"].values:
        return driving_vars_df, cam_position_df, vehicle_position_df, {}  # No RESET, return original dataframe

    indices_to_remove = set()
    reset_clusters = []  # To store separate clusters of "RESET"

    # Identify contiguous clusters of "RESET"
    reset_indices = driving_vars_df.index[driving_vars_df["current_track_piece"] == "RESET"].tolist()
    
    if not reset_indices:
        return driving_vars_df, cam_position_df, vehicle_position_df, {}  # No RESET occurrences, return original dataframe

    reset_counts = {}  # Dictionary to track preceding track names and RESET counts
    # Group contiguous RESET indices into clusters
    cluster = [reset_indices[0]]
    for i in range(1, len(reset_indices)):
        if reset_indices[i] == reset_indices[i - 1] + 1:
            cluster.append(reset_indices[i])
        else:
            reset_clusters.append(cluster)
            cluster = [reset_indices[i]]
    reset_clusters.append(cluster)  # Append last cluster

    # Process each RESET cluster independently
    for cluster in reset_clusters:
        first_reset_idx = cluster[0]  # Start index of the RESET cluster
        
        # Identify the preceding cluster
        if first_reset_idx > 0:
            prev_track_piece = driving_vars_df.loc[first_reset_idx - 1, "current_track_piece"]
            prev_cluster_indices = driving_vars_df.index[driving_vars_df["current_track_piece"] == prev_track_piece].tolist()
            reset_counts[prev_track_piece] = 1

            # Remove only if the previous cluster ends right before RESET
            if prev_cluster_indices and prev_cluster_indices[-1] == first_reset_idx - 1:
                indices_to_remove.update(prev_cluster_indices)

        # Remove the RESET cluster itself
        indices_to_remove.update(cluster)

    # Create a new dataframe without the identified clusters
    driving_vars_df = driving_vars_df.drop(indices_to_remove).reset_index(drop=True)
    # make sure the other dataframes match!
    cam_position_df = cam_position_df.drop(indices_to_remove).reset_index(drop=True)
    vehicle_position_df = vehicle_position_df.drop(indices_to_remove).reset_index(drop=True)

    return driving_vars_df, cam_position_df, vehicle_position_df, reset_counts

def modify_duplicate_sequences(df):
# Identify clusters of "short_straight"
    cluster_count = 0
    prev_value = None
    new_labels = []

    for track_piece in df["current_track_piece"]:
        if track_piece == "short_straight":
            if prev_value != "short_straight":
                cluster_count += 1  # Start a new cluster
            new_labels.append(f"short_straight_{cluster_count}")
        else:
            new_labels.append(track_piece)
        prev_value = track_piece
    df["current_track_piece"] = new_labels
    return df


def trial_11_string_replacement(driving_sim_df):
    driving_sim_df["current_track_piece"] = driving_sim_df["current_track_piece"].replace(trial.Trial.trial_11_dict)
    return(driving_sim_df)

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
    indices_for_track_piece = list(driving_vars_df.index[driving_vars_df['current_track_piece'] == piece_object.id])
    track_piece_driving_var = driving_vars_df[driving_vars_df['current_track_piece'] == piece_object.id]   
    first_index,last_index = indices_for_track_piece[0],indices_for_track_piece[-1]
    track_piece_cam_pos = cam_position_df.iloc[first_index:last_index+1]
    track_piece_vehicle_pos = vehicle_position_df.iloc[first_index:last_index+1]
    return(track_piece_cam_pos,track_piece_vehicle_pos,track_piece_driving_var)

def find_closest_point(camera_position_df, center_x, center_y):
    # Calculate the Euclidean distance between each point in the trajectory and the center point
    distances = np.sqrt((camera_position_df['pos_x'] - center_x) ** 2 + (camera_position_df['pos_z'] - center_y) ** 2)
    # Find the index of the minimum distance
    closest_index = distances.idxmin()
    
    return closest_index

def trim_trial_11_hiccups(df):
    # Compute the differences in pos_x and pos_z
    dx = df['pos_x'].diff().abs()
    dz = df['pos_z'].diff().abs()
    
    # Find the first occurrence where the delta exceeds 30 in either dimension
    mask = (dx > 5) | (dz > 5)
    
    if mask.any():
        trim_index = mask.idxmax()  # Get the index where the jump occurs
        df = df.loc[:trim_index-1]  # Trim the DataFrame before the jump
    
    return df

def trim_traj_for_trial_11_for_dtw_analysis(piece_object):
    # get the centerline for the short straight segment preceding the curved turn of interest
    entire_track_centerline_df = piece_object.map_object.centerline_df
    shifted_piece = next((k for k, v in piece.Piece.trial_11_dict.items() if v == piece_object.id), None)
    all_segments_list = list(map.Map.ordinal_map_pieces_dict["10"])
    piece_index_number = all_segments_list.index(shifted_piece)
    short_straight_centerline_df = entire_track_centerline_df[entire_track_centerline_df['segment'] == piece_index_number]

    # get last two points in the center line df
    end_of_short_straight_center_x, end_of_short_straight_center_y = short_straight_centerline_df.iloc[-1,1],short_straight_centerline_df.iloc[-1,2] # end of the short straight segment
    # get trajectory of track piece of interest
    untrimmed_traj = piece_object.trajectory_df

    # trim trajectory w.r.t. short straight segment
    untrimmed_traj = untrimmed_traj.reset_index()
    idx_of_traj_closest_to_end_of_short_straight = find_closest_point(untrimmed_traj, end_of_short_straight_center_x, end_of_short_straight_center_y) # get index of last short straight segment along traj
    trimmed_traj = untrimmed_traj.iloc[idx_of_traj_closest_to_end_of_short_straight:] # grab all points after this point
    trimmed_traj = trim_trial_11_hiccups(trimmed_traj)
    # trim trajectory w.r.t. hiccups'
    # if piece_object.subject_id == "clerk":
    #     print("========================================================")
    #     print("Piece ID:", piece_object.id)
    #     print("Length of trajectory pre-hiccup trim", len(trimmed_traj))
    #     trimmed_traj = trim_trial_11_hiccups(trimmed_traj)
    #     print("Length of trajectory post-hiccup trim", len(trimmed_traj))

    investigation_dict = {
        "short_centerline_df":short_straight_centerline_df,
        "closest_point_to_short_centerline":[untrimmed_traj['pos_x'][idx_of_traj_closest_to_end_of_short_straight],untrimmed_traj['pos_z'][idx_of_traj_closest_to_end_of_short_straight]],
        "end_of_short_straight":[end_of_short_straight_center_x, end_of_short_straight_center_y],
        "idx_of_traj_closest_to_end_of_short_straight":idx_of_traj_closest_to_end_of_short_straight,
    }
   
    return(trimmed_traj,investigation_dict)


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
    output_start, output_end = -450, 450
    #print("MAPPING HERE")
    
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
        whole_trial_df_column = whole_trial_driving_sim_df["lane_deviation_c"]
        #whole_trial_df_column = whole_trial_df_column.replace([np.inf, -np.inf], 0)
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
            piece_df_column =  driving_sim_df["lane_deviation_c"]
            piece_df_column = piece_df_column - 2.5
            #piece_df_column = piece_df_column.abs()
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