import pandas as pd
import os

directory = r"C:\Users\graci\Dropbox\PAndA\Thesis Experiment 1\data\track_piece_center"

def get_map_csv_files(map_string):
    map_specific_dir = directory + f"\{map_string}"
    list_of_track_pieces = []
    dict_of_center_csvs = {}
    for filename in os.listdir(map_specific_dir):
        f = os.path.join(map_specific_dir, filename)
        center_of_road = pd.read_csv(f,header=None)
        track_name = filename.replace(".csv","")
        dict_of_center_csvs[track_name] = center_of_road
        list_of_track_pieces.append(track_name)
    return(dict_of_center_csvs,list_of_track_pieces)
    
def preprocess_dataframes(dict_of_center_csvs,list_of_track_pieces):
    track_piece_dict = {}
    for track_piece in list_of_track_pieces:
        track_piece_df = dict_of_center_csvs[track_piece]
        track_piece_df[track_piece_df.columns[0]] = track_piece_df[track_piece_df.columns[0]].str.replace('(', '')
        track_piece_df[track_piece_df.columns[2]] = track_piece_df[track_piece_df.columns[2]].str.replace(')', '')
        track_piece_df = track_piece_df.drop(track_piece_df.columns[1], axis=1)
        track_piece_df = track_piece_df.set_axis(['x', 'z'], axis=1)
        track_piece_dict[track_piece] = track_piece_df
    return(track_piece_dict)
    
def add_dicts_to_map_object(map_num):
    map_name = 'Map_' + map_num
    dict_of_center_csvs,list_of_track_pieces = get_map_csv_files(map_name)
    track_piece_dict = preprocess_dataframes(dict_of_center_csvs,list_of_track_pieces)
    return(track_piece_dict)









