import pandas as pd
import os
directory = r"C:\Users\graci\Dropbox\PAndA\Thesis Experiment 1\data\track_piece_center\Map_1"


# iterate over files in
# that directory
list_of_road_profiles = []
dict_of_center_csvs = {}
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    center_of_road = pd.read_csv(f)
    dict_of_center_csvs[filename] = center_of_road
    list_of_road_profiles.append(filename)


left_turn_short_df = dict_of_center_csvs["left_turn_short.csv"]

left_turn_short_df[left_turn_short_df.columns[0]] = left_turn_short_df[left_turn_short_df.columns[0]].str.replace('(', '')
left_turn_short_df[left_turn_short_df.columns[2]] = left_turn_short_df[left_turn_short_df.columns[2]].str.replace(')', '')
left_turn_short_df = left_turn_short_df.drop(left_turn_short_df.columns[1], axis=1)

left_turn_short_df = left_turn_short_df.set_axis(['x', 'z'], axis=1)









