import lane_deviation
import numpy as np
import map
import matplotlib.pyplot as plt
import pandas as pd

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

# rotation correction ---------------------------------------------------------------------

def check_if_rotation_needed(subject_object, trial_number, track_piece):
    # get map for given trial
    map_number = subject_object.trials[trial_number].map.map_number
    pieces_needing_correction_dict = map.Map.track_piece_rotation_issue[map_number]
    
    # if the track piece is in the dictionary AND contains a nonzero value, return true
    if track_piece in pieces_needing_correction_dict and pieces_needing_correction_dict[track_piece] != 0: return "translation and rotation"
    elif track_piece in pieces_needing_correction_dict and pieces_needing_correction_dict[track_piece] == 0: return "translation"
    else: return "none"

def rotate_line_90_degrees(x_list, y_list):
    # Calculate the centroid of the line
    centroid_x = sum(x_list) / len(x_list)
    centroid_y = sum(y_list) / len(y_list)
    
    # Rotate each point 90 degrees around the centroid
    rotated_x = []
    rotated_y = []
    
    for x, y in zip(x_list, y_list):
        # Translate point to origin
        translated_x = x - centroid_x
        translated_y = y - centroid_y
        
        # Rotate 90 degrees (multiply by rotation matrix)
        rotated_x.append(-translated_y + centroid_x)
        rotated_y.append(translated_x + centroid_y)
    
    return rotated_x, rotated_y

def connect_lines(line1_x, line1_y, line2_x, line2_y, line1_point, line2_point):
    if line1_point not in ["start", "end"] or line2_point not in ["start", "end"]:
        raise ValueError("line1_point and line2_point must be either 'start' or 'end'")

    # Determine the connection points
    if line1_point == "start":
        line1_connect_x, line1_connect_y = line1_x[0], line1_y[0]
    else:  # end
        line1_connect_x, line1_connect_y = line1_x[-1], line1_y[-1]

    if line2_point == "start":
        line2_connect_x, line2_connect_y = line2_x[0], line2_y[0]
    else:  # end
        line2_connect_x, line2_connect_y = line2_x[-1], line2_y[-1]

    # Calculate the translation needed
    translation_x = line2_connect_x - line1_connect_x
    translation_y = line2_connect_y - line1_connect_y

    # Translate line1
    translated_line1_x = [x + translation_x for x in line1_x]
    translated_line1_y = [y + translation_y for y in line1_y]

    return translated_line1_x, translated_line1_y

def execute_rotation_and_translation(subject_object, trial_number, master_dict,track_piece, connector_piece,line_one_connector,line_two_connector):
    # get center and trajectory lines
    center_x, center_z, traj_x,traj_z = lane_deviation.get_track_piece_of_interest(subject_object,trial_number,master_dict,track_piece)
    connector_center_x, connector_center_z, connector_traj_x,connector_traj_z = lane_deviation.get_track_piece_of_interest(subject_object,trial_number,master_dict,connector_piece)
    
    # rotate the center line for correction
    rotated_x, rotated_z = rotate_line_90_degrees(center_x, center_z)
    
    # translate the rotated center line for correction
    translated_x, translated_z = connect_lines(rotated_x, rotated_z, connector_center_x, connector_center_z, line_one_connector,line_two_connector)

    translated_center_line,trajectory = lane_deviation.combine_lists(translated_x, translated_z),lane_deviation.combine_lists(traj_x,traj_z)

    return(connector_center_x,connector_center_z,translated_center_line,trajectory)

def execute_translation_only(subject_object, trial_number, master_dict,track_piece, connector_piece,line_one_connector,line_two_connector):
    # get center and trajectory lines
    center_x, center_z, traj_x,traj_z = lane_deviation.get_track_piece_of_interest(subject_object,trial_number,master_dict,track_piece)
    connector_center_x, connector_center_z, connector_traj_x,connector_traj_z = lane_deviation.get_track_piece_of_interest(subject_object,trial_number,master_dict,connector_piece)
    
    # translate the rotated center line for correction
    translated_x, translated_z = connect_lines(center_x, center_z, connector_center_x, connector_center_z, line_one_connector,line_two_connector)

    translated_center_line,trajectory = lane_deviation.combine_lists(translated_x, translated_z),lane_deviation.combine_lists(traj_x,traj_z)

    return(connector_center_x,connector_center_z,translated_center_line,trajectory)
    

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
            # trim_x, trim_z = lane_deviation.separate_xy_values(trimmed_traj)

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
                    # trim_x, trim_z = lane_deviation.separate_xy_values(final_trimmed_traj)
                    return(final_trimmed_traj)
        elif count == 20 and check(start_collect_closest_points) == True:
            return(None)
    
    # All the above to visualize ---------------------------

def save_corrected_lines(subject, trial_number, master_dict,track_piece,center_x,center_z,traj_x,traj_z):
    # save newly corrected center points and trimmed trajectory
    map_num = subject.trials[trial_number].map.map_number
    master_dict[str(map_num)][track_piece]['x'] = center_x
    master_dict[str(map_num)][track_piece]['z'] = center_z
    
    # #save newly trimmed track piece
    # track_piece_df = subject.trials[trial_number].pieces[track_piece].trajectory_df
    # track_piece_df["pos_x"] = pd.Series(traj_x)
    # track_piece_df["pos_z"] = pd.Series(traj_z)


def correct_and_plot(angle, subject, trial_number, master_dict,track_piece,connector_piece,connector_1,connector_2):

    # if rotation correction is necessary
    if angle == 90:
        connector_center_x,connector_center_z,center,trajectory= execute_rotation_and_translation(subject, trial_number, master_dict,track_piece,connector_piece,connector_1,connector_2)  

    elif angle == 0:
        connector_center_x,connector_center_z,center,trajectory = execute_translation_only(subject, trial_number, master_dict,track_piece, connector_piece,connector_1,connector_2)
    # # trim trajectory for lane deviation analysis
    # trajectory = trim_trajectory_line(trajectory,center)
    traj_x,traj_z = lane_deviation.separate_xy_values(trajectory)
    center_x,center_z = lane_deviation.separate_xy_values(center)

    # # get closest point
    # min_distance, closest_point = lane_deviation.distance_to_centerline(trajectory[lane_dev_idx], center) # get lane deviation
    
    #plot
    # fig1, ax1 = plt.subplots()

    # plot lines for reference
    # ax1.plot(connector_center_x, connector_center_z, c="green") # connector track piece
    # ax1.plot(center_x, center_z, c="blue") # rotated and translated center piece
    # ax1.plot(traj_x,traj_z, c="purple") # trimmed trajectory

    # plot points for reference
    # ax1.plot(trajectory[lane_dev_idx][0], trajectory[lane_dev_idx][1], 'o', markersize=5, c="purple")
    # ax1.plot(closest_point[0], closest_point[1], 'o', markersize = 5, c = "green")
    # plt.show()
    
    return(center_x,center_z,traj_x,traj_z)

def correct_position_for_entire_dataset(subject_dict,master_dict):
    # specify subject to get trajectories as reference points
    subject = subject_dict["chess"]
    
    # get list of maps in order of trials
    list_of_trials_in_order = []
    for i in range(0,10):
        list_of_trials_in_order.append(subject.trials[i].map.map_number)
    
    # get the dictionary
    track_piece_rotation_issue = map.Map.track_piece_rotation_issue
    
    # iterate through dictionary to correct the pieces
    for idx, map_number in enumerate(track_piece_rotation_issue):
        # print("MAP NUMBER: ",map_number)
        for track_piece in track_piece_rotation_issue[map_number]:
            # print("TRACK PIECE", track_piece)
            list_entry = track_piece_rotation_issue[map_number][track_piece]
            angle, connector_track, connector_tuple = list_entry[0],list_entry[1],list_entry[2]
            
            # select trial number based on map number
            trial_number = list_of_trials_in_order.index(map_number)
            
            # execute track correction
            center_x,center_z,traj_x,traj_z = correct_and_plot(angle,subject,trial_number,master_dict,track_piece,connector_track,connector_tuple[0],connector_tuple[1])
            save_corrected_lines(subject, trial_number, master_dict,track_piece,center_x,center_z,traj_x,traj_z)
    
            #plot
            # fig1, ax1 = plt.subplots()
            # center_x, center_z, traj_x,traj_z = lane_deviation.get_track_piece_of_interest(subject,trial_number,master_dict,track_piece)
            # ax1.plot(center_x, center_z, c = "red") # center from dictionary
            # ax1.plot(traj_x, traj_z, c = "green") # human trajectory
            # plt.show()




