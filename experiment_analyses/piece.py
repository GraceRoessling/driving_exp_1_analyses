import pandas as pd
import dataframe_helper_functions
import map
import subject

class Piece:
    "This is the piece class. A piece is a single track piece of a certain shape (i.e. S-turn) in a given map. Each map has 6 pieces."
    
    def __init__(self, id, subject, trial,map):
        self.id = id
        self.subject_id = subject.id
        self.trial_id = trial.id
        self.piece_dict = map.dict
        self.map_number = map.map_number
        self.dataframes = self.filter_dataframes(trial)
        self.visibility = self.get_visibility(map.map_number)
        self.centerline_df = self.get_centerline_for_piece(map)

    def filter_dataframes(self,trial):
        main_cam_df = trial.paths["main_camera"]
        vehicle_df = trial.paths["vehicle_movement"]
        driving_sim_df = trial.paths["Vehicle_DrivingSim"]
        track_piece_main_cam_df,track_piece_vehicle_df,track_piece_driving_sim_df = dataframe_helper_functions.get_track_piece_indices(self,main_cam_df,vehicle_df,driving_sim_df)
        piece_dfs = {"main_camera":track_piece_main_cam_df,
                    "vehicle_movement":track_piece_vehicle_df,
                    "Vehicle_DrivingSim":track_piece_driving_sim_df}
        return(piece_dfs)
    
    def get_visibility(self,map_number):
        map_dict = map.Map.map_pieces_dict[map_number]
        for key, values in map_dict.items():
            if self.id in values:
                return key 

    def get_centerline_for_piece(self, map):
        entire_track_centerline_df = map.centerline_df 
        all_segments_list = list(map.ordinal_map_pieces_dict[map.map_number]) # get index of track piece of interest
        piece_index_number = all_segments_list.index(self.id)
        if map.map_number == "11": # remove the track segments that are not captured in Trial 11
            entire_track_centerline_df = entire_track_centerline_df[
                (entire_track_centerline_df['segment'] % 2 != 0) | (entire_track_centerline_df['segment'] == 0)
            ]
            entire_track_centerline_df = entire_track_centerline_df.reset_index(drop=True)
        centerline_df = entire_track_centerline_df[entire_track_centerline_df['segment'] == piece_index_number]
        return centerline_df


        



        


        
        
    