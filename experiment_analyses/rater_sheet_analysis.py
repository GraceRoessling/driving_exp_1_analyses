import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols

rater_1_df = pd.read_csv("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 3/documentation/PR_rater_sheet.csv")
rater_2_df = pd.read_csv("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 3/documentation/VR_rater_sheet.csv")
rater_3_df = pd.read_csv("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 3/documentation/MM_rater_sheet.csv")

original_order_of_conditions = ["control", "scrambled_landmarks", "scrambled_segments", "control", "scrambled_landmarks",  "scrambled_segments",  "control", "scrambled_landmarks", "scrambled_segments", "control", 
                                "control", "scrambled_landmarks", "scrambled_segments", "scrambled_landmarks", "scrambled_segments", "control", "scrambled_landmarks", "scrambled_segments", "control", "scrambled_landmarks", 
                                "scrambled_segments", "control", "scrambled_landmarks", "scrambled_segments", "control", "control", "scrambled_landmarks", "scrambled_segments", "scrambled_landmarks", "scrambled_segments",
                                "control", "scrambled_landmarks", "scrambled_segments", "control", "scrambled_landmarks", "scrambled_segments", "control", "scrambled_landmarks", "scrambled_segments", "control", 
                                "scrambled_landmarks", "scrambled_segments", "control", "scrambled_landmarks", "scrambled_segments", "control", "scrambled_landmarks", "scrambled_segments", "control", "scrambled_landmarks", 
                                "scrambled_segments", "control", "scrambled_landmarks", "scrambled_segments", "control", "scrambled_landmarks", "scrambled_segments", "control", "scrambled_landmarks", "scrambled_segments"]

ranked_order_of_conditions = ["control","scrambled_landmarks","control","scrambled_landmarks","control","scrambled_landmarks","scrambled_landmarks","control","control","control",
                              "scrambled_landmarks","control","scrambled_segments","control","scrambled_segments","control","control","control","scrambled_landmarks","scrambled_segments",
                              "control","control","scrambled_landmarks","scrambled_landmarks","scrambled_segments","scrambled_segments","control","control","scrambled_landmarks","scrambled_landmarks",
                              "scrambled_landmarks","scrambled_landmarks","scrambled_segments","scrambled_segments","scrambled_segments","scrambled_segments","scrambled_segments","control","control","scrambled_landmarks",
                              "scrambled_segments","scrambled_segments","scrambled_landmarks","scrambled_segments","scrambled_segments","scrambled_landmarks","scrambled_landmarks","scrambled_landmarks","scrambled_segments","control",
                              "scrambled_landmarks","scrambled_landmarks","scrambled_segments","scrambled_segments","control","control","scrambled_segments","scrambled_landmarks","scrambled_segments","scrambled_segments"]

print(len(ranked_order_of_conditions))

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

    result_df["Condition"] = ranked_order_of_conditions

    summary = result_df.groupby("Condition").agg({
        "Score": ['mean', 'std'],
        "Normalized Score": ['mean', 'std'],
        "Score Std": ['mean', 'std']
    })

    # Flatten MultiIndex columns
    summary.columns = [' '.join(col).strip() for col in summary.columns]
    summary = summary.reset_index()
    return result_df,summary


def compute_mean_segment_cost_per_subject(df):
    # Group by subject and compute mean segment cost
    mean_costs = df.groupby('Drawing ID')["Normalized Score"].mean().reset_index()
    mean_costs.rename(columns={"Normalized Score": 'Mean Segment Cost'}, inplace=True)

    # Get 'Condition' column
    conditions = df[['Drawing ID', 'Condition']].drop_duplicates()

    # Merge
    result = pd.merge(mean_costs, conditions, on='Drawing ID')

    # Sort by Condition order
    result['Condition'] = pd.Categorical(result['Condition'],
                                         categories=['control', 'scrambled_landmarks', 'scrambled_segments'],
                                         ordered=True)
    result = result.sort_values('Condition').reset_index(drop=True)

    # Descriptives
    group_stats = result.groupby('Condition')['Mean Segment Cost'].agg(['mean', 'std']).to_dict('index')

    # One-way ANOVA
    model = ols('Q("Mean Segment Cost") ~ C(Condition)', data=result).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)

    return result, group_stats, anova_table


def plot_mean_scores_bar(summary_df):
    """
    Plots a bar chart of the mean normalized scores for 'Constant' and 'Variable' track groups.
    
    Parameters:
    summary_df (pd.DataFrame): The summary dataframe output from scored_drawing_summary.
    """
    # Map to capitalized labels for clarity
    condition_map = {"control": "Control", "scrambled_landmarks": "Scrambled Landmarks", "scrambled_segments": "Scrambled Segments"}
    summary_df["Condition"] = summary_df["Condition"].map(condition_map)

    # Extract means and stds
    conditions = summary_df["Condition"]
    means = summary_df["Normalized Score mean"]
    stds = summary_df["Normalized Score std"]

    # Define colors explicitly
    colors = ["blue", "red", "green"]  # Blue for Constant, Red for Variable

    # Create the bar plot
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(conditions, means, yerr=stds, capsize=5, color=colors)

    # Aesthetics
    ax.set_xlabel('Condition')
    ax.set_ylabel('Mean Accuracy Score')
    ax.set_ylim(0, 1)
    ax.bar_label(bars, fmt='%.2f', padding=3)

    plt.tight_layout()
    plt.show()


columns_of_interest = ["Drawing ID","Number of Segments","Geometry","Order of Segments","Orientation"]
score_columns = ["Number of Segments", "Geometry", "Order of Segments", "Orientation"]

rater_1_df = rater_1_df[columns_of_interest][0:60]
rater_2_df = rater_2_df[columns_of_interest][0:60]
rater_3_df = rater_3_df[columns_of_interest][0:60]

aligned_rater2_df = rater_2_df.set_index("Drawing ID").loc[rater_1_df["Drawing ID"]].reset_index()
aligned_rater3_df = rater_3_df.set_index("Drawing ID").loc[rater_1_df["Drawing ID"]].reset_index()

result_df,summary = scored_drawing_summary(rater_1_df, aligned_rater2_df, aligned_rater3_df)

# print(result_df)
# print(summary)

subject_df, condition_stats, t_test_result = compute_mean_segment_cost_per_subject(result_df)
print(subject_df)
print(condition_stats)
print(t_test_result)

plot_mean_scores_bar(summary)