import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
from scipy.stats import ttest_ind

dtw_df = pd.read_csv("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 2/data/dtw_data_recovered.csv")
drawing_scores_df = pd.read_csv("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 2/data/drawing_scores.csv")
perf_score_df = pd.read_csv("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 2/data/main_analysis_30_total_subjects_corrected_steering_acc6.csv")

columns_to_keep = ["subject_id","low_vis_var_lane_dev_10", "low_vis_steering_acceleration_10"]
perf_score_df = perf_score_df[columns_to_keep] # only get the low visibility variability in lane position and steering acceleration values

df_merged = pd.merge(dtw_df, drawing_scores_df, on="subject_id", how="left")
df_merged = pd.merge(df_merged, perf_score_df, on="subject_id", how="left")

df_merged = df_merged.rename(columns={
    "condition_x":"condition",
    "score": "DTW_score",
    "Normalized Score": "Normalized_Drawing_Score",
    "Score":"Drawing_score",
    "Score Std" : "Drawing_Score_Std"
})

df_merged = df_merged.drop(columns=["condition_y"])
#df_merged.to_csv('C:/Users/graci/Dropbox/PAndA/Thesis Experiment 2/data/spatial_knowledge_and_steering_perf_scores.csv', index=False)
# sorted_by_drawing_score_df = df_merged.sort_values(by="Normalized_Drawing_Score", ascending=False).reset_index(drop=True)
# print(sorted_by_drawing_score_df)

reset_nested_dict = {
    "familiar":{
        "mule": "spiral",
        "trial": "t_turn",
    },
    "unfamiliar":{
        "debt":"t_turn",
        "debt": "asymmetric_parabolic_2",
        "grid": "symmetric_parabolic",
        "grid": "t_turn",
        "swarm": "t_turn"
    }
}

reset_df = pd.DataFrame({
    "subj_id" :     ["baggy", "bash", "boned", "cargo","five", "grip","judge", "mule","poker","polio", "rerun", "slate", "slept", "trial", "yeast",
                      "atom","blank", "brim", "chef", "clerk", "debt","filth", "grid", "lens", "limb", "most","proof","slimy", "swarm", "wok"],
    "condition":    ["familiar","familiar","familiar","familiar","familiar","familiar","familiar","familiar","familiar","familiar","familiar","familiar","familiar","familiar","familiar",
                     "unfamiliar", "unfamiliar", "unfamiliar", "unfamiliar", "unfamiliar", "unfamiliar", "unfamiliar", "unfamiliar", "unfamiliar", "unfamiliar", "unfamiliar", "unfamiliar", "unfamiliar", "unfamiliar", "unfamiliar"],
    "resets":       [0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,
                     0,0,0,0,0,2,0,2,0,0,0,0,0,1,0]
})

print(reset_df)

# Split data by group
constant_resets = reset_df.loc[reset_df["condition"]=="familiar", "resets"]
variable_resets = reset_df.loc[reset_df["condition"]=="unfamiliar", "resets"]

# Perform Welch’s t-test (handles unequal variances)
t_stat, p_val = ttest_ind(constant_resets, variable_resets, equal_var=False)

print(f"T = {t_stat:.2f}, p = {p_val:.3f}")

reset_df.to_csv('C:/Users/graci/Dropbox/PAndA/Thesis Experiment 2/data/resets_per_subj.csv', index=False)