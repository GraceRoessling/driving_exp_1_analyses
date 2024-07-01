import lane_deviation
import numpy as np
import map

# wrap correction ------------------------------
def hacky_index(x):
    y = x[1:] - x[:-1]
    return np.where(y < 0)[0][0]

def check_if_wrap_correction_needed(map_num, track_name):
    map_dict = map.Map.track_piece_wrap_issue
    if track_name in map_dict[map_num]:
        return True
    elif track_name not in map.Map.track_piece_wrap_issue[map_num]:
        return False

# rotation correction --------------------------------
def check_if_rotation_or_translation_correction_needed(map_num, track_name):
    map_dict = map.Map.track_piece_rotation_issue
    if track_name in map_dict[map_num] :
        return True 
    elif track_name not in map_dict[map_num]:
        return False
    
def get_needed_rotation(map_num, track_name):
    map_dict = map.Map.track_piece_rotation_issue
    rotation = map_dict[map_num][track_name]
    return(rotation)

def check_if_flip(map_num, track_name):
    map_dict = map.Map.track_piece_rotation_issue
    if isinstance(map_dict[map_num][track_name], int):
        return False
    elif isinstance(map_dict[map_num][track_name], str):
        return True

# Trim correction ---------------------------------------
def check(list):
    return all(i == list[0] for i in list)

def trim_trajectory_line(trajectory,centerline):
    start_collect_closest_points = []
    end_collect_closest_points = []
    # iterate through first few points along trajectory line
    for count, point in enumerate(trajectory):
        # get distance between point and center_line
        min_distance, closest_point = lane_deviation.distance_to_centerline(point, centerline)
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
                min_distance, closest_point = lane_deviation.distance_to_centerline(point, reverse_centerline)
                end_collect_closest_points.append(closest_point)
                if check(start_collect_closest_points) != True: # all the elements are not the same
                    unchopped_point_idx = count
                    reverese_trimmed_traj = reverse_traj[unchopped_point_idx:]
                    final_trimmed_traj = reverese_trimmed_traj[::-1]
                    # trim_x, trim_z = separate_xy_values(final_trimmed_traj)
                    return(final_trimmed_traj)
        elif count == 20 and check(start_collect_closest_points) == True:
            return(None)
        


