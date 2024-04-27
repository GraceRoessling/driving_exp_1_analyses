import pandas as pd
import dataframe_helper_functions
import map

## ONLY WORKS FOR TRIAL 10 ATM! Will add other map track pieces later.

class Piece:
    "This is the piece class. A piece is a single track piece of a certain shape (i.e. S-turn) in a given map. Each map has 6 pieces."

    # map_1_landmark_pieces = ["left_turn_med","right_turn_short","s_turn_short"] # note: these are low visibility...
    
    def __init__(self, id, subject, trial,map):
        self.id = id
        self.subject_id = subject.id
        self.trial_id = trial.id
        self.piece_dict = map.dict
        self.dataframes = self.filter_dataframes(trial)
        self.visibility = self.get_visibility(trial)

    def filter_dataframes(self,trial):
        main_cam_df = trial.paths["main_camera"]
        vehicle_df = trial.paths["vehicle_movement"]
        driving_sim_df = trial.paths["Vehicle_DrivingSim"]
        track_piece_main_cam_df,track_piece_vehicle_df,track_piece_driving_sim_df = dataframe_helper_functions.get_track_piece_indices(self.id,main_cam_df,vehicle_df,driving_sim_df)
        piece_dfs = {"main_camera":track_piece_main_cam_df,
                    "vehicle_movement":track_piece_vehicle_df,
                    "Vehicle_DrivingSim":track_piece_driving_sim_df}
        return(piece_dfs)
    
    def get_visibility(self,trial):
        trial_num = str(trial.number) # get trial number
        map_dict = map.Map.map_pieces_dict[trial_num]
        for key, values in map_dict.items():
            if self.id in values:
                return key



        



        


        
        
    