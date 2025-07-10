import pandas as pd

rater_1_df = pd.read_csv("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 2/documentation/JH_rater_sheet.csv")
rater_2_df = pd.read_csv("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 2/documentation/MC_rater_sheet.csv")
rater_3_df = pd.read_csv("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 2/documentation/TT_rater_sheet.csv")

condition_column = ["constant", "constant","constant","constant","constant","variable","constant","constant","constant","constant","constant","variable","variable","constant","variable","constant","variable","variable","variable","constant","variable","constant","constant","variable","variable","variable","variable","variable","variable"]

print(len(condition_column))

def scored_drawing_summary(df1, df2, df3):
    """
    Takes three DataFrames with drawing scores and returns a DataFrame with:
    - "Drawing ID"
    - "Score" (sum of mean scores)
    - "Normalized Score" (Score / 20)
    - "Score Std" (standard deviation across the four mean score dimensions)
    
    Sorted by "Normalized Score" in descending order.
    """
    # List of score columns
    score_columns = ["Number of Segments", "Geometry", "Order of Segments", "Orientation"]
    
    # Merge dataframes on Drawing ID
    merged = df1.merge(df2, on="Drawing ID", suffixes=('_1', '_2'))
    merged = merged.merge(df3, on="Drawing ID")
    merged = merged.rename(columns={col: f"{col}_3" for col in score_columns})

    # Compute mean scores
    averaged_data = {"Drawing ID": merged["Drawing ID"]}
    for col in score_columns:
        averaged_data[col] = merged[[f"{col}_1", f"{col}_2", f"{col}_3"]].mean(axis=1)

    averaged_df = pd.DataFrame(averaged_data)

    # Compute total score and normalized score
    averaged_df["Score"] = averaged_df[score_columns].sum(axis=1)
    averaged_df["Normalized Score"] = averaged_df["Score"] / 20

    # Compute standard deviation across the four mean score dimensions
    averaged_df["Score Std"] = averaged_df[score_columns].std(axis=1)

    # Sort by normalized score descending
    result_df = averaged_df[["Drawing ID", "Score", "Normalized Score", "Score Std"]]
    result_df = result_df.sort_values(by="Normalized Score", ascending=False).reset_index(drop=True)

    result_df["Condition"] = condition_column

    summary = result_df.groupby("Condition").agg({
        "Score": ['mean', 'std'],
        "Normalized Score": ['mean', 'std'],
        "Score Std": ['mean', 'std']
    })

    # Flatten MultiIndex columns
    summary.columns = [' '.join(col).strip() for col in summary.columns]
    summary = summary.reset_index()
    return result_df,summary


columns_of_interest = ["Drawing ID","Number of Segments","Geometry","Order of Segments","Orientation"]
score_columns = ["Number of Segments", "Geometry", "Order of Segments", "Orientation"]

rater_1_df = rater_1_df[columns_of_interest][0:29]
rater_2_df = rater_2_df[columns_of_interest][0:29]
rater_3_df = rater_3_df[columns_of_interest][0:29]

aligned_rater2_df = rater_2_df.set_index("Drawing ID").loc[rater_1_df["Drawing ID"]].reset_index()
aligned_rater3_df = rater_3_df.set_index("Drawing ID").loc[rater_1_df["Drawing ID"]].reset_index()

result_df,summary = scored_drawing_summary(rater_1_df, aligned_rater2_df, aligned_rater3_df)

print(result_df)
print(summary)