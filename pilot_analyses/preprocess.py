import pandas as pd
import numpy as np
import os
import analysis_functions


# Preprocess data before conducting analysis ======================================================================================

# Load CSV files using condition and subject number
def get_clean_dataframes_for_subject(condition,subj_number):
    file_path = "C:/Users/graci/Dropbox/PAndA/Thesis Experiment 1/scripts/pilot_data"
    subject_folder = f"{file_path}/{condition}/{subj_number}"

    cam_position_df = pd.read_csv(f"{subject_folder}/main_camera_movement_T010.csv")
    vehicle_position_df = pd.read_csv(f"{subject_folder}/vehicle_movement_T010.csv")

    if condition == "familiar":
        driving_vars_df = pd.read_csv(f"{subject_folder}/Vehicle_DrivingSim_10_Familiar_T010.csv")
    elif condition == "unfamiliar":
        driving_vars_df = pd.read_csv(f"{subject_folder}/Vehicle_DrivingSim_10_Unfamiliar_T010.csv")

    return(cam_position_df,vehicle_position_df,driving_vars_df)

# Remove NA values across all dataframes for consistency
def remove_NA(cam_position_df,vehicle_position_df,driving_vars_df):
    na_indices = list(driving_vars_df.loc[pd.isna(driving_vars_df["current_track_piece"]), :].index)
    driving_vars_df = driving_vars_df.drop(index = na_indices).reset_index()
    vehicle_position_df = vehicle_position_df.drop(index = na_indices).reset_index()
    cam_position_df = cam_position_df.drop(index = na_indices).reset_index()
    return(cam_position_df,vehicle_position_df,driving_vars_df)

# Get indices for track piece segments
def get_track_piece_indices(track_piece,cam_position_df,vehicle_position_df,driving_vars_df):
    indices_for_track_piece = list(driving_vars_df.index[driving_vars_df['current_track_piece'].str.contains(track_piece)])
    track_piece_driving_var = driving_vars_df[driving_vars_df['current_track_piece'].str.contains(track_piece)]
    first_index,last_index = indices_for_track_piece[0],indices_for_track_piece[-1]
    track_piece_cam_pos = cam_position_df.iloc[first_index:last_index+1]
    track_piece_vehicle_pos = vehicle_position_df.iloc[first_index:last_index+1]
    return(track_piece_driving_var,track_piece_vehicle_pos,track_piece_cam_pos)

# Segment data into 8 sub_dfs to analyze different track segments
def break_down_dfs_by_track(cam_position_df,vehicle_position_df,driving_vars_df):
    track_pieces = sorted((list(set(driving_vars_df["current_track_piece"]))))
    dict_of_track_piece_dfs = {}
    for i in range(0,len(track_pieces)):
        track_piece_driving_var,track_piece_vehicle_pos,track_piece_cam_pos = get_track_piece_indices(track_pieces[i],cam_position_df,vehicle_position_df,driving_vars_df)
        dict_of_track_piece_dfs[track_pieces[i]] = {"Driving_variable_df":track_piece_driving_var,"Vehicle_pos_df":track_piece_vehicle_pos,"Camera_pos_df":track_piece_cam_pos}
    return(track_pieces,dict_of_track_piece_dfs)

# Save sub_dfs as csv files for dataframes!
def get_dfs_for_subject(condition,subj_number, window_size):
    cam_position_df,vehicle_position_df,driving_vars_df = get_clean_dataframes_for_subject(condition,subj_number)
    cam_position_df,vehicle_position_df,driving_vars_df = remove_NA(cam_position_df,vehicle_position_df,driving_vars_df)
    
    # calculate speed via position
    cam_position_df = analysis_functions.get_speed_via_pos(cam_position_df)
    vehicle_position_df = analysis_functions.get_speed_via_pos(vehicle_position_df)

    # remove faulty noise off the bat before smoothing
    cam_position_df["speed"] = analysis_functions.replace_over_30(cam_position_df["speed"])
    vehicle_position_df["speed"] = analysis_functions.replace_over_30(vehicle_position_df["speed"])
    cam_position_df["speed"] = analysis_functions.replace_if_diff_greater_than_10(cam_position_df["speed"])
    vehicle_position_df["speed"] = analysis_functions.replace_if_diff_greater_than_10(vehicle_position_df["speed"])

    # apply rolling window
    cam_position_df['moving_avg_speed'] = cam_position_df['speed'].rolling(window=window_size).mean()
    vehicle_position_df['moving_avg_speed'] = vehicle_position_df['speed'].rolling(window=window_size).mean()

    # shift window accordingly
    cam_position_df["moving_avg_speed"] = cam_position_df["moving_avg_speed"].shift(int(window_size/2)*-1)
    vehicle_position_df["moving_avg_speed"] = vehicle_position_df["moving_avg_speed"].shift(int(window_size/2)*-1)

    # convert steering input to steering angle
    driving_vars_df = analysis_functions.convert_steering_value(driving_vars_df)

    track_pieces,dict_of_track_piece_dfs = break_down_dfs_by_track(cam_position_df,vehicle_position_df,driving_vars_df)

    return(cam_position_df,vehicle_position_df,driving_vars_df,track_pieces,dict_of_track_piece_dfs)



def save_dfs_for_subject(condition, subj_number,driving_vars_df,vehicle_position_df,cam_position_df,track_pieces,dict_of_track_piece_dfs):
    # save pre-processed DFs as CSV files that contain all the data from trial 10
    file_path = "C:/Users/graci/Dropbox/PAndA/Thesis Experiment 1/scripts/pilot_data"
    trial_10_csv_path = f"{file_path}/{condition}/{subj_number}/trial_10_preprocessed_CSV"
    os.makedirs(trial_10_csv_path, exist_ok=True)

    driving_vars_df.to_csv(f"{trial_10_csv_path}/trial_10_drive_var.csv")
    vehicle_position_df.to_csv(f"{trial_10_csv_path}/trial_10_vehicle_pos.csv")
    cam_position_df.to_csv(f"{trial_10_csv_path}/trial_10_cam_pos.csv")

    # break down these DFs into the different track pieces and save as CSV files   
    for i in range(0, len(track_pieces)):
        current_track_piece = track_pieces[i]
        track_piece_path = f"{file_path}/{condition}/{subj_number}/track_piece_csv/{current_track_piece}"
        os.makedirs(track_piece_path, exist_ok=True)
        sub_dict_of_track_piece = dict_of_track_piece_dfs[current_track_piece]

        drive_var_sub_df = sub_dict_of_track_piece["Driving_variable_df"]
        vehicle_pos_sub_df = sub_dict_of_track_piece["Vehicle_pos_df"]
        cam_pos_sub_df = sub_dict_of_track_piece["Camera_pos_df"]

        drive_var_sub_df.to_csv(f"{track_piece_path}/drive_var.csv")
        vehicle_pos_sub_df.to_csv(f"{track_piece_path}/vehicle_pos.csv")
        cam_pos_sub_df.to_csv(f"{track_piece_path}/cam_pos.csv")

def run_all_subjects(condition,window_size):
    groups = ["familiar", "unfamiliar"]
    num_of_subjects = ["1", "2", "3"]
    track_pieces = ['left_turn_long_collider', 'left_turn_med_collider', 'left_turn_short_collider', 'right_turn_short_collider', 
                    's_turn_short_collider', 'straight_long_collider', 'straight_short_collider', 'u_turn_long_collider']
    
    fam_sub1_cam_position_df,fam_sub1_vehicle_position_df,fam_sub1_driving_vars_df,track_pieces,fam_sub1_dict_of_track_piece_dfs = get_dfs_for_subject("familiar","1",window_size)
    fam_sub2_cam_position_df,fam_sub2_vehicle_position_df,fam_sub2_driving_vars_df,track_pieces,fam_sub2_dict_of_track_piece_dfs = get_dfs_for_subject("familiar","2",window_size)
    fam_sub3_cam_position_df,fam_sub3_vehicle_position_df,fam_sub3_driving_vars_df,track_pieces,fam_sub3_dict_of_track_piece_dfs = get_dfs_for_subject("familiar","3",window_size)


    unfam_sub1_cam_position_df,unfam_sub1_vehicle_position_df,unfam_sub1_driving_vars_df,track_pieces,unfam_sub1_dict_of_track_piece_dfs = get_dfs_for_subject("unfamiliar","1",window_size)
    unfam_sub2_cam_position_df,unfam_sub2_vehicle_position_df,unfam_sub2_driving_vars_df,track_pieces,unfam_sub2_dict_of_track_piece_dfs = get_dfs_for_subject("unfamiliar","2",window_size)
    unfam_sub3_cam_position_df,unfam_sub3_vehicle_position_df,unfam_sub3_driving_vars_df,track_pieces,unfam_sub3_dict_of_track_piece_dfs = get_dfs_for_subject("unfamiliar","3",window_size)


    fam_sub1_straight_long_driving_vars_df = fam_sub1_dict_of_track_piece_dfs["straight_long_collider"]["Driving_variable_df"]
    fam_sub1_straight_long_cam_position_df = fam_sub1_dict_of_track_piece_dfs["straight_long_collider"]["Camera_pos_df"]
    fam_sub1_s_turn_short_driving_vars_df = fam_sub1_dict_of_track_piece_dfs["s_turn_short_collider"]["Driving_variable_df"]
    fam_sub1_s_turn_short_cam_position_df = fam_sub1_dict_of_track_piece_dfs["s_turn_short_collider"]["Camera_pos_df"]

    fam_sub2_straight_long_driving_vars_df = fam_sub2_dict_of_track_piece_dfs["straight_long_collider"]["Driving_variable_df"]
    fam_sub2_straight_long_cam_position_df = fam_sub2_dict_of_track_piece_dfs["straight_long_collider"]["Camera_pos_df"]
    fam_sub2_s_turn_short_driving_vars_df = fam_sub2_dict_of_track_piece_dfs["s_turn_short_collider"]["Driving_variable_df"]
    fam_sub2_s_turn_short_cam_position_df = fam_sub2_dict_of_track_piece_dfs["s_turn_short_collider"]["Camera_pos_df"]

    fam_sub3_straight_long_driving_vars_df = fam_sub3_dict_of_track_piece_dfs["straight_long_collider"]["Driving_variable_df"]
    fam_sub3_straight_long_cam_position_df = fam_sub3_dict_of_track_piece_dfs["straight_long_collider"]["Camera_pos_df"]
    fam_sub3_s_turn_short_driving_vars_df = fam_sub3_dict_of_track_piece_dfs["s_turn_short_collider"]["Driving_variable_df"]
    fam_sub3_s_turn_short_cam_position_df = fam_sub3_dict_of_track_piece_dfs["s_turn_short_collider"]["Camera_pos_df"]

    unfam_sub1_straight_long_driving_vars_df = unfam_sub1_dict_of_track_piece_dfs["straight_long_collider"]["Driving_variable_df"]
    unfam_sub1_straight_long_cam_position_df = unfam_sub1_dict_of_track_piece_dfs["straight_long_collider"]["Camera_pos_df"]
    unfam_sub1_s_turn_short_driving_vars_df = unfam_sub1_dict_of_track_piece_dfs["s_turn_short_collider"]["Driving_variable_df"]
    unfam_sub1_s_turn_short_cam_position_df = unfam_sub1_dict_of_track_piece_dfs["s_turn_short_collider"]["Camera_pos_df"]
    
    unfam_sub2_straight_long_driving_vars_df = unfam_sub2_dict_of_track_piece_dfs["straight_long_collider"]["Driving_variable_df"]
    unfam_sub2_straight_long_cam_position_df = unfam_sub2_dict_of_track_piece_dfs["straight_long_collider"]["Camera_pos_df"]
    unfam_sub2_s_turn_short_driving_vars_df = unfam_sub2_dict_of_track_piece_dfs["s_turn_short_collider"]["Driving_variable_df"]
    unfam_sub2_s_turn_short_cam_position_df = unfam_sub2_dict_of_track_piece_dfs["s_turn_short_collider"]["Camera_pos_df"]

    unfam_sub3_straight_long_driving_vars_df = unfam_sub3_dict_of_track_piece_dfs["straight_long_collider"]["Driving_variable_df"]
    unfam_sub3_straight_long_cam_position_df = unfam_sub3_dict_of_track_piece_dfs["straight_long_collider"]["Camera_pos_df"]
    unfam_sub3_s_turn_short_driving_vars_df = unfam_sub3_dict_of_track_piece_dfs["s_turn_short_collider"]["Driving_variable_df"]
    unfam_sub3_s_turn_short_cam_position_df = unfam_sub3_dict_of_track_piece_dfs["s_turn_short_collider"]["Camera_pos_df"]

    if condition == "familiar":
        return(fam_sub1_straight_long_driving_vars_df,fam_sub1_straight_long_cam_position_df,fam_sub1_s_turn_short_driving_vars_df,fam_sub1_s_turn_short_cam_position_df,
               fam_sub2_straight_long_driving_vars_df,fam_sub2_straight_long_cam_position_df,fam_sub2_s_turn_short_driving_vars_df,fam_sub2_s_turn_short_cam_position_df,
               fam_sub3_straight_long_driving_vars_df,fam_sub3_straight_long_cam_position_df,fam_sub3_s_turn_short_driving_vars_df,fam_sub3_s_turn_short_cam_position_df)
    
    elif condition == "unfamiliar":
        return(unfam_sub1_straight_long_driving_vars_df,unfam_sub1_straight_long_cam_position_df,unfam_sub1_s_turn_short_driving_vars_df,unfam_sub1_s_turn_short_cam_position_df,
               unfam_sub2_straight_long_driving_vars_df,unfam_sub2_straight_long_cam_position_df,unfam_sub2_s_turn_short_driving_vars_df,unfam_sub2_s_turn_short_cam_position_df,
               unfam_sub3_straight_long_driving_vars_df,unfam_sub3_straight_long_cam_position_df,unfam_sub3_s_turn_short_driving_vars_df,unfam_sub3_s_turn_short_cam_position_df)





