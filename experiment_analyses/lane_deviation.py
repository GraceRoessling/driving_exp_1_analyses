import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.interpolate import CubicSpline,CubicHermiteSpline,UnivariateSpline,PchipInterpolator
from numpy import diff
import numpy as np
import scipy
import preprocess
import math
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

def separate_xy_values(points):
    x_values = []
    y_values = []
    
    for x, y in points:
        x_values.append(x)
        y_values.append(y)
    
    return x_values, y_values

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

def combine_lists(list1, list2):
    combined_list = []
    for i in range(min(len(list1), len(list2))):
        combined_list.append((list1[i], list2[i]))
    return combined_list


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

def get_track_piece_indices(track_piece,center_of_road_map1):
    indices_for_track_piece = list(center_of_road_map1.index[center_of_road_map1['Road_Name'].str.contains(track_piece)])
    track_piece_center_of_road_map1 = center_of_road_map1[center_of_road_map1['Road_Name'].str.contains(track_piece)]
    return(indices_for_track_piece,track_piece_center_of_road_map1)

def get_center_of_lane_per_track_piece(center_of_road_map1):
    track_pieces = sorted((list(set(center_of_road_map1["Road_Name"]))))
    dict_of_track_piece_dfs = {}
    for i in range(0,len(track_pieces)):
        indices_for_track_piece,track_piece_center_of_road_map1 = get_track_piece_indices(track_pieces[i],center_of_road_map1)
        dict_of_track_piece_dfs[track_pieces[i]] = {"map_1":track_piece_center_of_road_map1}
    return(track_pieces,dict_of_track_piece_dfs)


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

def get_list_of_dataframes_for_road_center_csv(master_dict):
    map_df_list = []

    for i in range(1,11):
        map_df = pd.DataFrame()
        map_key = str(i)
        map_dict = master_dict[map_key]
        track_pieces = list(map_dict.keys())
        for track_piece in track_pieces:
            x = map_dict[track_piece]["x"]
            z = map_dict[track_piece]["z"]
            map_df[f"{track_piece}_x"] = pd.Series(x)
            map_df[f"{track_piece}_z"] = pd.Series(z)
        map_df_list.append(map_df)

    return(map_df_list)

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