import dataframe_helper_functions
import pandas as pd
import os

class Map:
    "This is the map class. A map is an environment that contains the track that the subject drives on. There is one map per trial."
    map_pieces_dict = {
        "1" : {"high_visibility": ["long_straight","symmetric_parabolic","short_straight_1","short_straight_2","triple_s","short_straight_3","chicane","short_straight_4","t_turn","short_straight_5","asymmetric_parabolic_2","short_straight_6","asymmetric_parabolic_1","short_straight_7","spiral","short_straight_8"],
        "low_visibility": ["traffic_circle"]},

        "2": {"high_visibility": ["long_straight","spiral","short_straight_1","t_turn","short_straight_2","asymmetric_parabolic_2","short_straight_3","short_straight_4","symmetric_parabolic","short_straight_5","triple_s","short_straight_6","asymmetric_parabolic_1","short_straight_7","traffic_circle","short_straight_8"],
        "low_visibility": ["chicane"]},

        "3" :{"high_visibility": ["long_straight","traffic_circle","short_straight_1","short_straight_2","chicane","short_straight_3","triple_s","short_straight_4","t_turn","short_straight_5","asymmetric_parabolic_1","short_straight_6","spiral","short_straight_7","symmetric_parabolic","short_straight_8"],
        "low_visibility": ["asymmetric_parabolic_2"]},

        "4":{"high_visibility": ["long_straight","t_turn","short_straight_1","traffic_circle","short_straight_2","chicane","short_straight_3","triple_s","short_straight_4","asymmetric_parabolic_1","short_straight_5","short_straight_6","symmetric_parabolic","short_straight_7","asymmetric_parabolic_2","short_straight_8"],
        "low_visibility": ["spiral"]},

        "5": {"high_visibility": ["long_straight","t_turn","short_straight_1","triple_s","short_straight_2","chicane","short_straight_3","spiral","short_straight_4","symmetric_parabolic","short_straight_5","traffic_circle","short_straight_6","short_straight_7","asymmetric_parabolic_1","short_straight_8"],
        "low_visibility": ["asymmetric_parabolic_2"]},

        "6": {"high_visibility": ["long_straight","traffic_circle","short_straight_1","spiral","short_straight_2","asymmetric_parabolic_1","short_straight_3","asymmetric_parabolic_2","short_straight_4","symmetric_parabolic","short_straight_5","short_straight_6","triple_s","short_straight_7","t_turn","short_straight_8"],
        "low_visibility": ["chicane"]},

        "7": {"high_visibility": ["long_straight","symmetric_parabolic","short_straight_1","chicane","short_straight_2","short_straight_3","asymmetric_parabolic_2","short_straight_4","t_turn","short_straight_5","triple_s","short_straight_6","asymmetric_parabolic_1","short_straight_7","spiral","short_straight_8"],
        "low_visibility": ["traffic_circle"]},

        "8": {"high_visibility": ["long_straight","asymmetric_parabolic_2","short_straight_1","chicane","short_straight_2","short_straight_3","t_turn","short_straight_4","triple_s","short_straight_5","asymmetric_parabolic_1","short_straight_6","traffic_circle","short_straight_7","symmetric_parabolic","short_straight_8"],
        "low_visibility": ["spiral"]},

        "9": {"high_visibility": ["long_straight","short_straight_1","t_turn","short_straight_2","traffic_circle","short_straight_3","chicane","short_straight_4","spiral","short_straight_5","symmetric_parabolic","short_straight_6","triple_s","short_straight_7","asymmetric_parabolic_1","short_straight_8"],
        "low_visibility": ["asymmetric_parabolic_2"]},

        "10": {"high_visibility": ["long_straight","chicane","short_straight_1","short_straight_2","short_straight_3","traffic_circle","short_straight_4","asymmetric_parabolic_2","short_straight_5","short_straight_6","asymmetric_parabolic_1","short_straight_7","spiral","short_straight_8"],
        "low_visibility": ["triple_s","symmetric_parabolic","t_turn"]},

        "11": {"high_visibility": ["chicane","triple_s","symmetric_parabolic","traffic_circle","asymmetric_parabolic_2","t_turn","asymmetric_parabolic_1","spiral","short_straight_8"],
        "low_visibility": [None]}
        }
    
    ordinal_map_pieces_dict = {
        "1":["long_straight","symmetric_parabolic","short_straight_1","traffic_circle","short_straight_2","triple_s","short_straight_3","chicane","short_straight_4","t_turn","short_straight_5","asymmetric_parabolic_2","short_straight_6","asymmetric_parabolic_1","short_straight_7","spiral","short_straight_8"],
        "2":["long_straight","spiral","short_straight_1","t_turn","short_straight_2","asymmetric_parabolic_2","short_straight_3","chicane","short_straight_4","symmetric_parabolic","short_straight_5","triple_s","short_straight_6","asymmetric_parabolic_1","short_straight_7","traffic_circle","short_straight_8"],
        "3":["long_straight","traffic_circle","short_straight_1","asymmetric_parabolic_2","short_straight_2","chicane","short_straight_3","triple_s","short_straight_4","t_turn","short_straight_5","asymmetric_parabolic_1","short_straight_6","spiral","short_straight_7","symmetric_parabolic","short_straight_8"],
        "4":["long_straight","t_turn","short_straight_1","traffic_circle","short_straight_2","chicane","short_straight_3","triple_s","short_straight_4","asymmetric_parabolic_1","short_straight_5","spiral","short_straight_6","symmetric_parabolic","short_straight_7","asymmetric_parabolic_2","short_straight_8"],
        "5":["long_straight","t_turn","short_straight_1","triple_s","short_straight_2","chicane","short_straight_3","spiral","short_straight_4","symmetric_parabolic","short_straight_5","traffic_circle","short_straight_6","asymmetric_parabolic_2","short_straight_7","asymmetric_parabolic_1","short_straight_8"],
        "6":["long_straight","traffic_circle","short_straight_1","spiral","short_straight_2","asymmetric_parabolic_1","short_straight_3","asymmetric_parabolic_2","short_straight_4","symmetric_parabolic","short_straight_5","chicane","short_straight_6","triple_s","short_straight_7","t_turn","short_straight_8"],
        "7":["long_straight","symmetric_parabolic","short_straight_1","chicane","short_straight_2","traffic_circle","short_straight_3","asymmetric_parabolic_2","short_straight_4","t_turn","short_straight_5","triple_s","short_straight_6","asymmetric_parabolic_1","short_straight_7","spiral","short_straight_8"],
        "8":["long_straight","asymmetric_parabolic_2","short_straight_1","chicane","short_straight_2","spiral","short_straight_3","t_turn","short_straight_4","triple_s","short_straight_5","asymmetric_parabolic_1","short_straight_6","traffic_circle","short_straight_7","symmetric_parabolic","short_straight_8"],
        "9":["long_straight","asymmetric_parabolic_2","short_straight_1","t_turn","short_straight_2","traffic_circle","short_straight_3","chicane","short_straight_4","spiral","short_straight_5","symmetric_parabolic","short_straight_6","triple_s","short_straight_7","asymmetric_parabolic_1","short_straight_8"],
        "10":["long_straight","chicane","short_straight_1","triple_s","short_straight_2","symmetric_parabolic","short_straight_3","traffic_circle","short_straight_4","asymmetric_parabolic_2","short_straight_5","t_turn","short_straight_6","asymmetric_parabolic_1","short_straight_7","spiral","short_straight_8"],
        "11":["chicane","triple_s","symmetric_parabolic","traffic_circle","asymmetric_parabolic_2","t_turn","asymmetric_parabolic_1","spiral","short_straight_8"],
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
        current_track_column = driving_sim_df["current_track_piece"]
        trial.paths["main_camera"]["current_track_piece"] = current_track_column
        trial.paths["vehicle_movement"]["current_track_piece"] = current_track_column

        return(reset_counts_dict)

    def get_centerline_for_map(self,map_number):
        center_points_dir = 'C:/Users/graci/Dropbox/PAndA/Thesis Experiment 3/rhino_and_grasshopper/grasshopper_points'
        if map_number == "11":
            centerline_df = pd.read_csv(os.path.join(center_points_dir, f"map_10_points.csv"), header=None, names=['segment', 'x', 'y'])
        else:
            centerline_df = pd.read_csv(os.path.join(center_points_dir, f"map_{map_number}_points.csv"), header=None, names=['segment', 'x', 'y'])
        return centerline_df