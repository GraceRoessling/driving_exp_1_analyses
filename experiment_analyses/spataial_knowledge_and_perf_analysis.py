import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

dtw_df = pd.read_csv("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 2/data/dtw_data_recovered.csv")
drawing_scores_df = pd.read_csv("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 2/data/drawing_scores.csv")

def plot_drawing_vs_dtw_with_fit(df, drawing_col="Normalized_Drawing_Score", dtw_col="DTW_score"):
    dtw_col_values = df_merged[dtw_col]
    dtw_col_values_norm = (dtw_col_values - dtw_col_values.min()) / (dtw_col_values.max() - dtw_col_values.min())
    df[dtw_col] = dtw_col_values_norm
    # Keep only valid numeric rows
    df_clean = df[[drawing_col, dtw_col]].dropna()
    df_clean = df_clean.astype(float)

    x = df_clean[drawing_col]
    y = df_clean[dtw_col]

    plt.figure(figsize=(8,6))
    plt.scatter(x, y, color='blue', alpha=0.7, label='Data points')

    if len(x) > 1:  # need at least 2 points for regression
        slope, intercept, r_value, p_value, std_err = linregress(x, y)
        line = slope * x + intercept
        plt.plot(x, line, color='red', label=f'Best fit line (R²={r_value**2:.2f})')
    else:
        slope = intercept = r_value = p_value = std_err = float('nan')

    plt.xlabel(drawing_col.replace("_", " ").title())
    plt.ylabel(dtw_col.replace("_", " ").title())
    plt.title(f"{drawing_col.replace('_',' ').title()} vs {dtw_col.replace('_',' ').title()} with Fit")
    plt.legend()
    plt.grid(True)
    plt.show()

    print( {"slope": slope, "intercept": intercept, "r_squared": r_value**2, "p_value": p_value, "std_err": std_err})
df_merged = pd.merge(dtw_df, drawing_scores_df, on="subject_id", how="left")

df_merged = df_merged.rename(columns={
    "condition_x":"condition",
    "score": "DTW_score",
    "Normalized Score": "Normalized_Drawing_Score",
    "Score":"Drawing_score",
    "Score Std" : "Drawing_Score_Std"
})

df_merged = df_merged.drop(columns=["condition_y"])

print(df_merged["DTW_score"])

sorted_by_drawing_score_df = df_merged.sort_values(by="Normalized_Drawing_Score", ascending=False).reset_index(drop=True)

print(sorted_by_drawing_score_df)


plot_drawing_vs_dtw_with_fit(df_merged)