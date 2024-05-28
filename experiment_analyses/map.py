import dataframe_helper_functions

class Map:
    "This is the map class. A map is an environment that contains the track that the subject drives on. There is one map per trial."
    map_pieces_dict = {
        "1" : {"high_visibility": ["straight_long","u_turn_long","left_turn_short","left_turn_long","straight_short"],
        "low_visibility": ["left_turn_med","right_turn_short", "s_turn_short"]},

        "2": {"high_visibility": ["straight_long", "left_turn_short", "s_turn_short", "u_turn_long","right_turn_short", "left_turn_long", "straight_short"],
        "low_visibility": ["left_turn_med"]},

        "3" :{"high_visibility": ["right_turn_med", "right_turn_long","straight_long", "s_turn_long", "u_turn_short", "right_turn_short", "straight_short"],
        "low_visibility": ["left_turn_short"]},

        "4":{"high_visibility": ["left_turn_short", "s_turn_long", "straight_short", "right_turn_short", "straight_long", "right_turn_long", "left_turn_med"],
        "low_visibility": ["u_turn_short"]},

        "5": {"high_visibility": ["straight_short", "straight_long", "left_turn_short", "s_turn_long", "right_turn_short", "right_turn_med", "left_turn_med"],
        "low_visibility": ["left_turn_long"]},

        "6": {"high_visibility": ["straight_short", "right_turn_short", "left_turn_long", "right_turn_med", "straight_long", "s_turn_long", "right_turn_short"],
        "low_visibility": ["left_turn_med"]},

        "7": {"high_visibility": ["straight_long", 'right_turn_short', 'left_turn_med', "s_turn_long", "left_turn_long", "right_turn_med", "straight_short"],
        "low_visibility": ["left_turn_short"]},

        "8": {"high_visibility": ["left_turn_short", "u_turn_long", "straight_long", "left_turn_long", "right_turn_short", "left_turn_med", "straight_short"],
        "low_visibility": ["right_turn_med"]},

        "9": {"high_visibility": ["straight_long", "left_turn_med", "right_turn_med", "left_turn_short", "u_turn_long", "right_turn_short", "straight_short"],
        "low_visibility": ["left_turn_long"]},

        "10": {"high_visibility": ["straight_long", "right_turn_med", "right_turn_long", "left_turn_med", "u_turn_long", "left_turn_short","straight_short"],
        "low_visibility": ["right_turn_short"]}
        }
    
    ordinal_map_pieces_dict = {
        "1":["straight_long","left_turn_med", "u_turn_long", "right_turn_short", "left_turn_short","s_turn_short", "left_turn_long", "straight_short"],
        "2":["straight_long", "left_turn_med", "left_turn_short", "s_turn_short", "u_turn_long", "right_turn_short", "left_turn_long", "straight_short"],
        "3":["right_turn_med","right_turn_long", "straight_long","s_turn_long","u_turn_short","right_turn_short", "left_turn_short", "straight_short"],
        "4":["left_turn_short","s_turn_long", "u_turn_short", "straight_short", "right_turn_short", "straight_long", "right_turn_long", "left_turn_med"],
        "5":["straight_short", "straight_long", "left_turn_short", "s_turn_long", "right_turn_short", "left_turn_long", "right_turn_med", "left_turn_med"],
        "6":["straight_short", "right_turn_short", "left_turn_long", "right_turn_med", "left_turn_med", "straight_long", "s_turn_long", "right_turn_short"],
        "7":["straight_long", "right_turn_short", "left_turn_med", "s_turn_long", "left_turn_long", "right_turn_med", 'left_turn_short', "straight_short"],
        "8":["left_turn_short", "u_turn_long", "straight_long", "right_turn_med", "left_turn_long", "right_turn_short", "left_turn_med", "straight_short"],
        "9":["straight_long", "left_turn_med", "right_turn_med", "left_turn_short", "u_turn_long", "right_turn_short", "left_turn_long", "straight_short"],
        "10":["straight_long", "right_turn_med", "right_turn_long", "right_turn_short", "left_turn_med", "u_turn_long", "left_turn_short","straight_short"],
    }
    
    def __init__(self,subject,trial):
        self.subject_id = subject.id
        self.trial = trial
        self.map_number,self.pieces,self.dict = self.get_ordinal_map(trial,subject)



    def get_ordinal_map(self, trial,subject):
        # get desired map dictionary
        if subject.condition == "familiar":
            map_of_interest = self.map_pieces_dict["1"]
            high_vis,low_vis = map_of_interest.values()
            specific_map_track_pieces = high_vis + low_vis
            map_number = str(1)

        elif subject.condition == "unfamiliar":
            driving_sim_df = trial.paths["Vehicle_DrivingSim"]
            all_track_pieces = dataframe_helper_functions.get_unique_consecutive_strings(driving_sim_df["current_track_piece"])
            all_track_pieces = dataframe_helper_functions.remove_substring(all_track_pieces, "_collider")

            map_1,map_2,map_3,map_4,map_5,map_6,map_7,map_8,map_9,map_10 = self.ordinal_map_pieces_dict.values()
            list_of_map_dicts = [map_1,map_2,map_3,map_4,map_5,map_6,map_7,map_8,map_9,map_10]
            for count,specific_map_track_pieces in enumerate(list_of_map_dicts):
                if all_track_pieces == specific_map_track_pieces:
                    map_number = str(count +1)
                    map_of_interest = self.map_pieces_dict[map_number]
                    break #exit the loop
                # else:
                #     print("aint nothin here boy")
                #     print("count:", count,"\n",
                #           all_track_pieces,"\n",
                #           specific_map_track_pieces)
                #     print(subject.id, trial.id)
        return(map_number,specific_map_track_pieces,map_of_interest)

        


        
    

