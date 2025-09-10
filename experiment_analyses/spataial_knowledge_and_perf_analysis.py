import pandas as pd

dtw_df = pd.read_csv("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 2/data/dtw_data_recovered.csv")
drawing_scores_df = pd.read_csv("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 2/data/drawing_scores.csv")

# Reorder dtw_df to match the subject_id order in drawing_scores_df
dtw_df = dtw_df.set_index("subject_id").loc[drawing_scores_df["subject_id"]].reset_index()



