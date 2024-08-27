import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from numpy import diff
import numpy as np
import math
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree
import os
import json
import itertools
import map
#import tensorflow as tf

# Grab lane deviation data and integrate it with every subject's dataframe ----------------------


def sort_dataframes_for_one_trial_df(trial, dataframe_dict):
    map_number = trial.map.map_number
    ordinal_list_of_track_pieces = map.Map.ordinal_map_pieces_dict[map_number]
    
    pox_x_column = []
    pox_z_column = []
    lane_dev_column = []
    
    for track_piece in ordinal_list_of_track_pieces:
        lane_dev_df = dataframe_dict[track_piece]
        pox_x_column.append(list(lane_dev_df["pos_x"]))
        pox_z_column.append(list(lane_dev_df["pos_z"]))
        lane_dev_column.append(list(lane_dev_df["lane_dev"]))
        
    pox_x_column = list(itertools.chain.from_iterable(pox_x_column))
    pox_z_column = list(itertools.chain.from_iterable(pox_z_column))
    lane_dev_column = list(itertools.chain.from_iterable(lane_dev_column))
    
    trial_lane_dev_df = pd.DataFrame({"pos_x": pox_x_column, "pos_z": pox_z_column, "lane_dev": lane_dev_column}) 
    return(trial_lane_dev_df)

def grab_lane_deviation_data(subject, lane_deviation_file_path):
    for i in range(0,10): # iterate through ten trials and generate dataframes for lane deviation
        trial_number = i
        trial = subject.trials[trial_number]
        path_to_trial_folder = lane_deviation_file_path + f"/{subject.condition}/{subject.id}/trial_{trial.number}_map_{trial.map.map_number}/"
        #list_of_track_pieces = map.Map.ordinal_map_pieces_dict[trial.map.map_number] 

        lane_dev_dict = {}

        # go through the folder, get the json files with lane deviation values, and save them in a dataframe for track_piece objects
        for filename in os.listdir(path_to_trial_folder):
            track_piece = filename.replace('.json','')
            # open individual track piece json
            with open(path_to_trial_folder + filename) as f: 
                track_piece_dict = json.load(f)
            
            # get trajectory x,z values for dataframe 
            track_piece_df = subject.trials[trial.number].pieces[track_piece].trajectory_df
            traj_x = track_piece_df["pos_x"]
            traj_z = track_piece_df["pos_z"]
            
            # get the lane deviation values and shorten the list so that it matches the length of the trajectory
            lane_deviation_values = list(track_piece_dict.values())
            traj_length, ld_length = len(traj_x), len(lane_deviation_values)
            diff_in_length = traj_length - ld_length
            # lane_deviation_values = lane_deviation_values[:-diff_in_length]

            
            
            # get trajectory x,z values for dataframe 
            track_piece_df = subject.trials[trial.number].pieces[track_piece].trajectory_df
            traj_x = track_piece_df["pos_x"].tolist()[:-diff_in_length]
            traj_z = track_piece_df["pos_z"].tolist()[:-diff_in_length]
            
            # from IPython import embed;embed()
            # create dataframe for individual track pieces (with corresponding trimmed x,y trajectories)
            track_piece_lane_dev_df = pd.DataFrame({"pos_x": traj_x, "pos_z": traj_z, "lane_dev": lane_deviation_values})
            trial.pieces[track_piece].lane_dev_df = track_piece_lane_dev_df
            #print(track_piece_lane_dev_df)

            # save into list to sew into larger dataframe
            lane_dev_dict[track_piece] = track_piece_lane_dev_df
            
        # create dataframe for entire trial (with corresponding trimmed x,y trajectories)
        trial.lane_dev_dict = lane_dev_dict
        trial_lane_dev_df = sort_dataframes_for_one_trial_df(trial, lane_dev_dict)
        trial.trial_lane_dev_df = trial_lane_dev_df


# General helper functions ------------------------------------------------
def separate_xy_values(points):
    x_values = []
    y_values = []
    
    for x, y in points:
        x_values.append(x)
        y_values.append(y)
    
    return x_values, y_values

def combine_lists(list1, list2):
    combined_list = []
    for i in range(min(len(list1), len(list2))):
        combined_list.append((list1[i], list2[i]))
    return combined_list

# Interpolation functions ----------------------------------------------------

def interpolate_line(x_values, y_values, resolution):
    interp_func = interp1d(x_values, y_values, kind='linear') 
    new_x = np.linspace(min(x_values), max(x_values), resolution)
    new_y = interp_func(new_x)

    return new_x, new_y

def calculate_line_length(x_values, y_values):
    total_length = 0
    # Iterate through the values and calculate the length between consecutive points
    for i in range(len(x_values) - 1):
        x1, y1 = x_values[i], y_values[i]
        x2, y2 = x_values[i + 1], y_values[i + 1]
        segment_length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        total_length += segment_length

    return total_length

def curve_length(x_coords, y_coords):
    length = 0
    for i in range(len(x_coords) - 1):
        dx = x_coords[i + 1] - x_coords[i]
        dy = y_coords[i + 1] - y_coords[i]
        length += math.sqrt(dx**2 + dy**2)
    return length

def arc_length(x, y):
    dx = np.gradient(x)
    dy = np.gradient(y)
    ds = np.sqrt(dx**2 + dy**2)
    return np.cumsum(ds)


# Make master dictionary for centerline correction ------------------------------

def get_xz_for_track_piece(center_x,center_z,resolution):
    arc_lengths = arc_length(center_x, center_z)

    # Calculate the total arc length
    arc_length_total = arc_lengths[-1]

    # Interpolate the line to get a higher resolution using arc length parameterization
    num_points = resolution  # Increase this value for higher resolution
    interp_space = np.linspace(0, arc_length_total, num_points)
    x_new = np.interp(interp_space, arc_lengths, center_x)
    z_new = np.interp(interp_space, arc_lengths, center_z)
    
    return(x_new,z_new)

def generate_track_piece_dict(subject_dict):
    interp_master_dict = {"1": {},"2": {},"3": {},"4": {},"5": {},"6": {},"7": {},"8": {},"9": {},"10": {},}
    non_interp_master_dict = {"1": {},"2": {},"3": {},"4": {},"5": {},"6": {},"7": {},"8": {},"9": {},"10": {},}
    # grab an unfamiliar subject 
    subject = subject_dict["chess"]

    # iterate through their trials to get all ten maps
    for trial_num in range(0,10):
        map = subject.trials[trial_num].map
        high_vis,low_vis = map.dict.values()
        all_track_pieces = high_vis + low_vis
        interp_master_dict[map.map_number] = {track_piece: {} for track_piece in all_track_pieces}
        
        # iterate through track pieces in a given map
        for track_piece in all_track_pieces:
            track_piece_df = subject_dict[subject.id].trials[trial_num].map.center_dict[track_piece]
            center_x = track_piece_df["x"].to_numpy().astype(float)
            center_z = track_piece_df["z"].to_numpy().astype(float)
            
            if "straight" not in track_piece:
                length = curve_length(center_x, center_z)
                resolution = int(length * 1000)
                x_new,z_new = get_xz_for_track_piece(center_x,center_z,resolution)
                
            elif "straight" in track_piece:
                length = calculate_line_length(center_x,center_z)
                resolution = int(length * 1000)
                x_new,z_new = interpolate_line(center_x, center_z, resolution)
                
            interp_master_dict[map.map_number][track_piece] = {"x":x_new, "z":z_new}
            non_interp_master_dict[map.map_number][track_piece] = {"x":center_x, "z":center_z}
    return(interp_master_dict,non_interp_master_dict)

def get_track_piece_of_interest(subject,trial_num,master_dict,track_piece):
    # get center position
    map_num = subject.trials[trial_num].map.map_number
    center_x = master_dict[str(map_num)][track_piece]['x']
    center_z = master_dict[str(map_num)][track_piece]['z']

    # get x,z trajectory
    track_piece_df = subject.trials[trial_num].pieces[track_piece].trajectory_df
    traj_x = list(track_piece_df["pos_x"])
    traj_z = list(track_piece_df["pos_z"])
    
    return(center_x, center_z, traj_x,traj_z)

# Lane deviation calculations ---------------------------------------

def distance_to_centerline(point, centerline):

    x, y = point
    min_distance = float('inf')

    for i in range(len(centerline)):
        x1, y1 = centerline[i]

        # Calculate the distance between the point and the segment
        distance = math.sqrt((x - x1) ** 2 + (y - y1) ** 2)

        # Update the minimum distance and closest point
        if distance < min_distance:
            min_distance = distance
            closest_point = (x1, y1)

    return min_distance, closest_point

def distance_to_centerline_signed_efficient(point, centerline):
    x, y = point

    # Build k-d tree from centerline points
    tree = cKDTree(centerline)

    # Find the 2 nearest neighbors
    distances, indices = tree.query([x, y], k=2)

    min_distance = float('inf')
    closest_index = None

    # Check the segment between the two nearest points and their adjacent segments
    for i in range(min(indices[0], indices[1]) - 1, max(indices[0], indices[1]) + 1):
        if i < 0 or i >= len(centerline) - 1:
            continue

        x1, y1 = centerline[i]
        x2, y2 = centerline[i + 1]

        # Vector from start to end of the segment
        segment_vector = (x2 - x1, y2 - y1)
        
        # Vector from start of the segment to the point
        point_vector = (x - x1, y - y1)
        
        # Calculate the projection of point_vector onto segment_vector
        segment_length_squared = segment_vector[0]**2 + segment_vector[1]**2
        projection = (point_vector[0] * segment_vector[0] + point_vector[1] * segment_vector[1]) / segment_length_squared
        
        # Find the closest point on the segment
        if projection <= 0:
            closest = (x1, y1)
            segment_closest_index = i
        elif projection >= 1:
            closest = (x2, y2)
            segment_closest_index = i + 1
        else:
            closest = (x1 + projection * segment_vector[0], y1 + projection * segment_vector[1])
            # Choose the nearer of the two segment endpoints
            segment_closest_index = i if projection < 0.5 else i + 1
        
        # Calculate the distance between the point and the closest point on the segment
        distance = math.sqrt((x - closest[0])**2 + (y - closest[1])**2)
        
        # Update the minimum distance and closest index
        if distance < min_distance:
            min_distance = distance
            closest_index = segment_closest_index

    # Determine the side of the centerline
    if closest_index is not None:
        if closest_index > 0:
            segment_start = centerline[closest_index - 1]
            segment_end = centerline[closest_index]
        else:
            segment_start = centerline[closest_index]
            segment_end = centerline[closest_index + 1]
        
        segment_vector = (segment_end[0] - segment_start[0], 
                          segment_end[1] - segment_start[1])
        point_vector = (point[0] - segment_start[0], 
                        point[1] - segment_start[1])
        
        # Calculate the cross product
        cross_product = segment_vector[0] * point_vector[1] - segment_vector[1] * point_vector[0]
        
        # Adjust the sign of the distance based on the cross product
        if cross_product > 0:
            min_distance = -min_distance  # Point is on the left side

    return min_distance, closest_index