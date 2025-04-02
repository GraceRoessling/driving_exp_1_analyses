import dataframe_helper_functions
import pandas as pd
import os

class Map:
    "This is the map class. A map is an environment that contains the track that the subject drives on. There is one map per trial."
    map_pieces_dict = {
        "1" : {"high_visibility": ["long_straight","short_straight_1","u_turn","short_straight_2","turn_4","short_straight_3","y_turn","short_straight_4","turn_1","short_straight_5","lane_convergence","short_straight_6","turn_2","short_straight_7","turn_3","short_straight_8"],
        "low_visibility": ["zig_zag"]},

        "2": {"high_visibility": ["long_straight","large_horseshoe","short_straight_1","short_straight_2","turn_4","short_straight_3","y_turn","short_straight_4","turn_3","short_straight_5","lane_convergence","short_straight_6","turn_2","short_straight_7","turn_1","short_straight_8"],
        "low_visibility": ["u_turn"]},

        "3" :{"high_visibility": ["long_straight","turn_2","short_straight_1","zig_zag","short_straight_2","lane_convergence","short_straight_3","small_horseshoe","short_straight_4","short_straight_5","y_turn","short_straight_6","turn_4","short_straight_7","short_straight_8"],
        "low_visibility": ["turn_3"]},

        "4":{"high_visibility": ["long_straight","turn_1","short_straight_1","short_straight_2","small_horseshoe","short_straight_3","u_turn","short_straight_4","turn_1","short_straight_5","turn_3","short_straight_6","lane_convergence","short_straight_7","turn_4","short_straight_8"],
        "low_visibility": ["y_turn"]},

        "5": {"high_visibility": ["long_straight","turn_2","short_straight_1","turn_3","short_straight_2","short_straight_3","zig_zag","short_straight_4","large_horseshoe","short_straight_5","y_turn","short_straight_6","lane_convergence","short_straight_7","turn_1","short_straight_8"],
        "low_visibility": ["turn_4"]},

        "6": {"high_visibility": ["long_straight","turn_3","short_straight_1","y_turn","short_straight_2","lane_convergence","short_straight_3","turn_4","short_straight_4","short_straight_5","turn_1","short_straight_6","turn_2","short_straight_7","zig_zag","short_straight_8"],
        "low_visibility": ["small_horseshoe"]},

        "7": {"high_visibility": ["long_straight", "turn_3", "short_straight_1", "lane_convergence","short_straight_2","large_horseshoe","short_straight_3","y_turn","short_straight_4","turn_2","short_straight_5","turn_3","short_straight_6","turn_4","short_straight_7","short_straight_8"],
        "low_visibility": ["zig_zag"]},

        "8": {"high_visibility": ["long_straight","short_straight_1","u_turn","short_straight_2","turn_1","short_straight_3","small_horseshoe","short_straight_4","lane_convergence","short_straight_5","turn_3","short_straight_6","y_turn","short_straight_7","turn_5","short_straight_8"],
        "low_visibility": ["turn_2"]},

        "9": {"high_visibility": ["long_straight","turn_4","short_straight_1","turn_4","short_straight_2","u_turn","short_straight_3","lane_convergence","short_straight_4","short_straight_5","zig_zag","short_straight_6","turn_2","short_straight_7","turn_1","short_straight_8"],
        "low_visibility": ["y_turn"]},

        "10": {"high_visibility": ["long_straight","chicane","short_straight_1","short_straight_2","short_straight_3","traffic_circle","short_straight_4","asymmetric_parabolic_2","short_straight_5","short_straight_6","asymmetric_parabolic_1","short_straight_7","spiral","short_straight_8"],
        "low_visibility": ["triple_s","symmetric_parabolic","t_turn"]},

        "11": {"high_visibility": ["long_straight","short_straight_1","short_straight_2","short_straight_3","short_straight_4","short_straight_5","short_straight_6","short_straight_7","short_straight_8"],
        "low_visibility": [None]}
        }
    
    ordinal_map_pieces_dict = {
        "1":["long_straight","zig_zag","short_straight_1","u_turn","short_straight_2","turn_4","short_straight_3","y_turn","short_straight_4","turn_1","short_straight_5","lane_convergence","short_straight_6","turn_2","short_straight_7","turn_3","short_straight_8"],
        "2":["long_straight","large_horseshoe","short_straight_1","u_turn","short_straight_2","turn_4","short_straight_3","y_turn","short_straight_4","turn_3","short_straight_5","lane_convergence","short_straight_6","turn_2","short_straight_7","turn_1","short_straight_8"],
        "3":["long_straight","turn_2","short_straight_1","zig_zag","short_straight_2","lane_convergence","short_straight_3","small_horseshoe","short_straight_4","turn_3","short_straight_5","y_turn","short_straight_6","turn_4","short_straight_7","turn_3","short_straight_8"],
        "4":["long_straight","turn_1","short_straight_1","y_turn","short_straight_2","small_horseshoe","short_straight_3","u_turn","short_straight_4","turn_1","turn_3","short_straight_5","lane_convergence","short_straight_6","turn_4","short_straight_7","short_straight_8"],
        "5":["long_straight","turn_2","short_straight_1","turn_3","short_straight_2","turn_4","short_straight_3","zig_zag","short_straight_4","large_horseshoe","short_straight_5","y_turn","short_straight_6","lane_convergence","short_straight_7","turn_1","short_straight_8"],
        "6":["long_straight","turn_3","short_straight_1","y_turn","short_straight_2","lane_convergence","turn_4","short_straight_3","small_horseshoe","short_straight_4","turn_1","short_straight_5","turn_2","short_straight_6","zig_zag","short_straight_7"],
        "7":["long_straight", "turn_3", "short_straight_1", "lane_convergence","short_straight_2","large_horseshoe","short_straight_3","y_turn","short_straight_4","turn_2","short_straight_5","zig_zag","short_straight_6","turn_3","short_straight_7","turn_4","short_straight_8"],
        "8":["long_straight","turn_2","short_straight_1","u_turn","short_straight_2","turn_1","short_straight_3","small_horseshoe","short_straight_4","lane_convergence","short_straight_5","turn_3","short_straight_6","y_turn","short_straight_7","turn_5","short_straight_8"],
        "9":["long_straight","turn_4","short_straight_1","turn_4","short_straight_2","u_turn","short_straight_3","lane_convergence","short_straight_4","y_turn","short_straight_5","zig_zag","short_straight_6","turn_2","short_straight_7","turn_1","short_straight_8"],
        "10":["long_straight","chicane","short_straight_1","triple_s","short_straight_2","symmetric_parabolic","short_straight_3","traffic_circle","short_straight_4","asymmetric_parabolic_2","short_straight_5","t_turn","short_straight_6","asymmetric_parabolic_1","short_straight_7","spiral","short_straight_8"],
        "11":["long_straight","short_straight_1","short_straight_2","short_straight_3","short_straight_4","short_straight_5","short_straight_6","short_straight_7","short_straight_8"],
    }
   
    def __init__(self,subject,trial):
        self.subject_id = subject.id
        self.trial = trial
        self.map_number,self.pieces,self.dict = self.get_ordinal_map(trial)
        self.reset_counts_dict = self.get_instances_of_repeating_sequences(trial, self.map_number)
        self.centerline_df = self.get_centerline_for_map(self.map_number)

    def get_ordinal_map(self, trial):
        trial_file_name = trial.driving_sim_filename
        map_number = str(dataframe_helper_functions.extract_map_number(trial_file_name))
        map_of_interest = self.map_pieces_dict[map_number]
        specific_map_track_pieces = self.ordinal_map_pieces_dict[map_number]
        return(map_number,specific_map_track_pieces,map_of_interest)

    def get_instances_of_repeating_sequences(self,trial,map_number):
        driving_sim_df = trial.paths["Vehicle_DrivingSim"]
        cam_position_df = trial.paths["main_camera"]
        vehicle_position_df = trial.paths["vehicle_movement"]
        if map_number == "11": 
            reset_counts_dict = {}
        else:
            trial.paths["Vehicle_DrivingSim"], trial.paths["main_camera"],trial.paths["vehicle_movement"],reset_counts_dict = dataframe_helper_functions.clean_track_data(driving_sim_df,cam_position_df,vehicle_position_df)
        trial.paths["Vehicle_DrivingSim"] = dataframe_helper_functions.modify_duplicate_sequences(driving_sim_df)
        # current_track_column = driving_sim_df["current_track_piece"]
        # trial.paths["main_camera"]["current_track_piece"] = current_track_column
        # trial.paths["vehicle_movement"]["current_track_piece"] = current_track_column

        return(reset_counts_dict)

    def get_centerline_for_map(self,map_number):
        center_points_dir = 'C:/Users/graci/Dropbox/PAndA/Thesis Experiment 2/rhino_and_grasshopper/grasshopper_points'
        if map_number == "11":
            centerline_df = pd.read_csv(os.path.join(center_points_dir, f"map_10_points.csv"), header=None, names=['segment', 'x', 'y'])
        else:
            centerline_df = pd.read_csv(os.path.join(center_points_dir, f"map_{map_number}_points.csv"), header=None, names=['segment', 'x', 'y'])
        return centerline_df