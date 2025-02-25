import dataframe_helper_functions

class Map:
    "This is the map class. A map is an environment that contains the track that the subject drives on. There is one map per trial."
    map_pieces_dict = {
        "1" : {"high_visibility": ["long_straight","short_straight","u_turn","short_straight","turn_4","short_straight","y_turn","short_straight","turn_1","short_straight","lane_convergence","short_straight","turn_2","short_straight","turn_3","short_straight"],
        "low_visibility": ["zig_zag"]},

        "2": {"high_visibility": ["long_straight","large_horseshoe","short_straight","short_straight","turn_4","short_straight","y_turn","short_straight","turn_3","short_straight","lane_convergence","short_straight","turn_2","short_straight","turn_1","short_straight"],
        "low_visibility": ["u_turn"]},

        "3" :{"high_visibility": ["long_straight","turn_2","short_straight","zig_zag","short_straight","lane_convergence","short_straight","small_horseshoe","short_straight","short_straight","y_turn","short_straight","turn_4","short_straight","turn_3","short_straight"],
        "low_visibility": ["turn_3"]},

        "4":{"high_visibility": ["long_straight","turn_1","short_straight","short_straight","small_horseshoe","short_straight","u_turn","short_straight","turn_1","turn_3","short_straight","lane_convergence","short_straight","turn_4","short_straight"],
        "low_visibility": ["y_turn"]},

        "5": {"high_visibility": ["long_straight","turn_2","short_straight","turn_3","short_straight","short_straight","zig_zag","short_straight","large_horseshoe","short_straight","y_turn","short_straight","lane_convergence","short_straight","turn_1","short_straight"],
        "low_visibility": ["turn_4"]},

        "6": {"high_visibility": ["long_straight","turn_3","short_straight","y_turn","short_straight","lane_convergence","short_straight","turn_4","short_straight","short_straight","turn_1","short_straight","turn_2","short_straight","zig_zag","short_straight"],
        "low_visibility": ["small_horseshoe"]},

        "7": {"high_visibility": ["long_straight", "turn_3", "short_straight", "lane_convergence","short_straight","large_horseshoe","short_straight","y_turn","short_straight","turn_2","short_straight","short_straight","turn_3","short_straight","turn_4","short_straight"],
        "low_visibility": ["zig_zag"]},

        "8": {"high_visibility": ["long_straight","short_straight","u_turn","short_straight","turn_1","short_straight","small_horseshoe","short_straight","lane_convergence","short_straight","turn_3","short_straight","y_turn","short_straight","turn_5","short_straight"],
        "low_visibility": ["turn_2"]},

        "9": {"high_visibility": ["long_straight","turn_4","short_straight","turn_4","short_straight","u_turn","short_straight","lane_convergence","short_straight","short_straight","zig_zag","short_straight","turn_2","short_straight","turn_1","short_straight"],
        "low_visibility": ["y_turn"]},

        "10": {"high_visibility": ["long_straight","chicane","short_straight","short_straight","short_straight","traffic_circle","short_straight","asymmetric_parabolic_2","short_straight","short_straight","asymmetric_parabolic_1","short_straight","spiral","short_straight"],
        "low_visibility": ["triple_s","symmetric_parabolic","t_turn"]},

        "11": {"high_visibility": ["long_straight","short_straight_1","short_straight_2","short_straight_3","short_straight_4","short_straight_5","short_straight_6","short_straight_7","short_straight_8"],
        "low_visibility": [None]}
        }
    
    ordinal_map_pieces_dict = {
        "1":["long_straight","zig_zag","short_straight","u_turn","short_straight","turn_4","short_straight","y_turn","short_straight","turn_1","short_straight","lane_convergence","short_straight","turn_2","short_straight","turn_3","short_straight"],
        "2":["long_straight","large_horseshoe","short_straight","u_turn","short_straight","turn_4","short_straight","y_turn","short_straight","turn_3","short_straight","lane_convergence","short_straight","turn_2","short_straight","turn_1","short_straight"],
        "3":["long_straight","turn_2","short_straight","zig_zag","short_straight","lane_convergence","short_straight","small_horseshoe","short_straight","turn_3","short_straight","y_turn","short_straight","turn_4","short_straight","turn_3","short_straight"],
        "4":["long_straight","turn_1","short_straight","y_turn","short_straight","small_horseshoe","short_straight","u_turn","short_straight","turn_1","turn_3","short_straight","lane_convergence","short_straight","turn_4","short_straight"],
        "5":["long_straight","turn_2","short_straight","turn_3","short_straight","turn_4","short_straight","zig_zag","short_straight","large_horseshoe","short_straight","y_turn","short_straight","lane_convergence","short_straight","turn_1","short_straight"],
        "6":["long_straight","turn_3","short_straight","y_turn","short_straight","lane_convergence","short_straight","turn_4","short_straight","small_horseshoe","short_straight","turn_1","short_straight","turn_2","short_straight","zig_zag","short_straight"],
        "7":["long_straight", "turn_3", "short_straight", "lane_convergence","short_straight","large_horseshoe","short_straight","y_turn","short_straight","turn_2","short_straight","zig_zag","short_straight","turn_3","short_straight","turn_4","short_straight"],
        "8":["long_straight","turn_2","short_straight","u_turn","short_straight","turn_1","short_straight","small_horseshoe","short_straight","lane_convergence","short_straight","turn_3","short_straight","y_turn","short_straight","turn_5","short_straight"],
        "9":["long_straight","turn_4","short_straight","turn_4","short_straight","u_turn","short_straight","lane_convergence","short_straight","y_turn","short_straight","zig_zag","short_straight","turn_2","short_straight","turn_1","short_straight"],
        "10":["long_straight","chicane","short_straight","triple_s","short_straight","symmetric_parabolic","short_straight","traffic_circle","short_straight","asymmetric_parabolic_2","short_straight","t_turn","short_straight","asymmetric_parabolic_1","short_straight","spiral","short_straight"],
        "11":["long_straight","short_straight_1","short_straight_2","short_straight_3","short_straight_4","short_straight_5","short_straight_6","short_straight_7","short_straight_8"],
    }
   
    def __init__(self,subject,trial):
        self.subject_id = subject.id
        self.trial = trial
        self.map_number,self.pieces,self.dict = self.get_ordinal_map(trial)
        self.track_state = self.get_instances_of_repeating_sequences(trial)

    def get_ordinal_map(self, trial):
        trial_file_name = trial.driving_sim_filename
        map_number = str(dataframe_helper_functions.extract_map_number(trial_file_name))
        map_of_interest = self.map_pieces_dict[map_number]
        specific_map_track_pieces = self.ordinal_map_pieces_dict[map_number]
        return(map_number,specific_map_track_pieces,map_of_interest)

    def get_instances_of_repeating_sequences(self,trial):
        driving_sim_df = trial.paths["Vehicle_DrivingSim"]
        #trial.paths["Vehicle_DrivingSim"] = dataframe_helper_functions.modify_duplicate_sequences(driving_sim_df)
        trial.paths["Vehicle_DrivingSim"] = dataframe_helper_functions.clean_track_data(driving_sim_df)
        #print(trial.paths["Vehicle_DrivingSim"])
        # get RESET indice range
        return("modified_track")
        


               

        


        
    



    # def get_ordinal_map(self, trial,subject):
    #     # get desired map dictionary
    #     if subject.condition == "familiar":
    #         map_of_interest = self.map_pieces_dict["10"]
    #         high_vis,low_vis = map_of_interest.values()
    #         specific_map_track_pieces = high_vis + low_vis
    #         map_number = str(10)

    #     elif subject.condition == "unfamiliar":
    #         driving_sim_df = trial.paths["Vehicle_DrivingSim"]

    #         # if DF has repeating track pieces, label them separately (only for map 6)
    #         if dataframe_helper_functions.check_repeating_sequences(driving_sim_df): 
    #             new_driving_sim_df = dataframe_helper_functions.modify_duplicate_sequences(driving_sim_df)

    #             # make sure main dataframe is edited for consistency!
    #             trial.paths["Vehicle_DrivingSim"] = new_driving_sim_df

    #             # get the unique track pieces
    #             all_track_pieces = dataframe_helper_functions.get_unique_consecutive_strings(new_driving_sim_df["current_track_piece"])
    #             all_track_pieces = dataframe_helper_functions.remove_substring(all_track_pieces, "_collider")

    #         # if DF doesn't have repeating track pieces
    #         else:
    #             all_track_pieces = dataframe_helper_functions.get_unique_consecutive_strings(driving_sim_df["current_track_piece"])
    #             all_track_pieces = dataframe_helper_functions.remove_substring(all_track_pieces, "_collider")   
     
    #         map_1,map_2,map_3,map_4,map_5,map_6,map_7,map_8,map_9,map_10 = self.ordinal_map_pieces_dict.values()
    #         list_of_map_dicts = [map_1,map_2,map_3,map_4,map_5,map_6,map_7,map_8,map_9,map_10]
    #         for count,specific_map_track_pieces in enumerate(list_of_map_dicts):
    #             if all_track_pieces == specific_map_track_pieces:
    #                 map_number = str(count +1)
    #                 map_of_interest = self.map_pieces_dict[map_number]
    #                 specific_map_track_pieces = self.ordinal_map_pieces_dict[map_number]
    #                 break #exit the loop
    #             # else:
    #             #     print("aint nothin here boy")
    #             #     print("count:", count,"\n",
    #             #           all_track_pieces,"\n",
    #             #           specific_map_track_pieces)
    #             #     print(subject.id, trial.id)
            
    #     return(map_number,specific_map_track_pieces,map_of_interest)

        


        
    

