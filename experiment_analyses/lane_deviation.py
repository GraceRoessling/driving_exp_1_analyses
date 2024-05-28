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

import numpy as np
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
    # Calculate the total arc length
    arc_length_total = arc_length(center_x, center_z)[-1]

    # Interpolate the line to get a higher resolution using arc length parameterization
    num_points = resolution  # Increase this value for higher resolution
    arc_lengths = np.linspace(0, arc_length_total, num_points)
    x_new = np.interp(arc_lengths, arc_length(center_x, center_z), center_x)
    z_new = np.interp(arc_lengths, arc_length(center_x, center_z), center_z)
    
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

def check(list):
    return all(i == list[0] for i in list)

def trim_trajectory_line(trajectory,centerline):
    start_collect_closest_points = []
    end_collect_closest_points = []
    # iterate through first few points along trajectory line
    for count, point in enumerate(trajectory):
        # get distance between point and center_line
        min_distance, closest_point = distance_to_centerline(point, centerline)
        start_collect_closest_points.append(closest_point)

        if check(start_collect_closest_points) != True: # all the elements are not the same
            unchopped_point_idx = count
            trimmed_traj = trajectory[unchopped_point_idx:]
            # trim_x, trim_z = separate_xy_values(trimmed_line)

            # now trim the end of the list
            
            reverse_traj = trimmed_traj[::-1]
            reverse_centerline = centerline[::-1]

            for count, point in enumerate(reverse_traj):
                # get distance between point and center_line
                min_distance, closest_point = distance_to_centerline(point, reverse_centerline)
                end_collect_closest_points.append(closest_point)
                if check(start_collect_closest_points) != True: # all the elements are not the same
                    unchopped_point_idx = count
                    reverese_trimmed_traj = reverse_traj[unchopped_point_idx:]
                    final_trimmed_traj = reverese_trimmed_traj[::-1]
                    trim_x, trim_z = separate_xy_values(final_trimmed_traj)
                    return(trim_x, trim_z)


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

# x = left_turn_short_df["x"].to_numpy()
# z = left_turn_short_df["z"].to_numpy()
# x = x.astype(float)
# z = z.astype(float)

# # resolution = 1000  # Number of points to generate
# # x_new = np.linspace(x.min(), x.max(), resolution)
# # z_new = np.interp(x_new, x, z)

# # dzdx = diff(z)/diff(x)
# # dzdx= np.insert(dzdx,0,0)
# # dzdx = np.gradient(x, z) 


# plt.plot(x, z, c = "red")
# #plt.plot(x_new, z_new, c = "green")
# plt.show()