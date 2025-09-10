import pandas as pd
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt
import subject

# Upload the csv files of the three raters
rater_1_df = pd.read_csv("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 2/documentation/JH_rater_sheet.csv")
rater_2_df = pd.read_csv("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 2/documentation/MC_rater_sheet.csv")
rater_3_df = pd.read_csv("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 2/documentation/TT_rater_sheet.csv")

# Need to get map selection column, ID, and condition
nested_dict = subject.Subject.completion_seq_with_ans_nested_dict

def merge_dict_with_scores(nested_dict, df_scores):
    """
    Merge a nested dictionary of subject metadata with a dataframe of drawing scores.
    
    Parameters
    ----------
    nested_dict : dict
        A dictionary where keys are subject IDs and values are dictionaries containing
        at least {"condition", "drawing_id", "map_selection"}.
    df_scores : pd.DataFrame
        DataFrame with columns ["drawing_id", "drawing_score"].
    
    Returns
    -------
    pd.DataFrame
        Combined dataframe with columns:
        ["subject_id", "condition", "drawing_id", "drawing_score", "map_selection"]
    """
    
    # Convert nested dict into a dataframe
    df_dict = pd.DataFrame.from_dict(nested_dict, orient="index").reset_index()
    df_dict = df_dict.rename(columns={"index": "subject_id"})
    

    # Merge on drawing_id
    df_scores = df_scores.rename(columns={"Drawing ID": "drawing_id"})
    
    df_merged = pd.merge(df_dict, df_scores, on="drawing_id", how="left")
    
    # Keep only desired columns (drop order, etc. if not needed)
    df_final = df_merged[["subject_id", "condition", "drawing_id",'Normalized Score', 'Score', 'Score Std', "map_selection"]]
    
    return df_final

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

    # add columns to indicate the subject id, condition, and map selection answer based on the drawing_id
    result_df = merge_dict_with_scores(nested_dict, result_df)
    result_df = result_df.sort_values(by="Normalized Score", ascending=False).reset_index(drop=True)

    print(result_df)

    summary = result_df.groupby("condition").agg({
        "Score": ['mean', 'std'],
        "Normalized Score": ['mean', 'std'],
        "Score Std": ['mean', 'std']
    })

    # Flatten MultiIndex columns
    summary.columns = [' '.join(col).strip() for col in summary.columns]
    summary = summary.reset_index()
    result_df.to_csv('C:/Users/graci/Dropbox/PAndA/Thesis Experiment 2/data/drawing_scores.csv', index=False)  
    return result_df,summary


def compute_mean_segment_cost_per_subject(df):
    # Group by subject_id and calculate the mean segment cost
    mean_costs = df.groupby('drawing_id')['Score'].mean().reset_index()
    mean_costs.rename(columns={'Segment Costs': 'Mean Segment Cost'}, inplace=True)

    # Get the condition per subject_id (assuming one condition per subject)
    conditions = df[['drawing_id', 'condition']].drop_duplicates()

    # Merge mean costs with condition info
    result = pd.merge(mean_costs, conditions, on='drawing_id')

    # Sort so that 'familiar' condition comes first
    result['condition'] = pd.Categorical(result['condition'], categories=['familiar', 'unfamiliar'], ordered=True)
    result = result.sort_values('condition').reset_index(drop=True)

    # Calculate mean and std deviation for each condition group
    group_stats = result.groupby('condition')['Score'].agg(['mean', 'std']).to_dict('index')

    # Split data for t-test
    familiar_data = result[result['condition'] == 'familiar']['Score']
    unfamiliar_data = result[result['condition'] == 'unfamiliar']['Score']

    # Independent samples t-test (assumes unequal variances by default with 'equal_var=False')
    t_stat, p_value = ttest_ind(familiar_data, unfamiliar_data, equal_var=False)

    # Package t-test results nicely
    t_test_result = {
        't_statistic': t_stat,
        'p_value': p_value
    }

    return result, group_stats, t_test_result

def plot_mean_scores_bar(summary_df):
    """
    Plots a bar chart of the mean normalized scores for 'Constant' and 'Variable' track groups.
    
    Parameters:
    summary_df (pd.DataFrame): The summary dataframe output from scored_drawing_summary.
    """
    # Map to capitalized labels for clarity
    condition_map = {"familiar": "Constant", "unfamiliar": "Variable"}
    summary_df["condition"] = summary_df["condition"].map(condition_map)

    # Extract means and stds
    conditions = summary_df["condition"]
    means = summary_df["Normalized Score mean"]
    stds = summary_df["Normalized Score std"]

    # Define colors explicitly
    colors = ["blue", "red"]  # Blue for Constant, Red for Variable

    # Create the bar plot
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(conditions, means, yerr=stds, capsize=5, color=colors)

    # Aesthetics
    ax.set_xlabel('condition')
    ax.set_ylabel('Mean Accuracy Score')
    ax.set_ylim(0, 1)
    ax.bar_label(bars, fmt='%.2f', padding=3)

    plt.tight_layout()
    plt.show()


columns_of_interest = ["Drawing ID","Number of Segments","Geometry","Order of Segments","Orientation"]
score_columns = ["Number of Segments", "Geometry", "Order of Segments", "Orientation"]

rater_1_df = rater_1_df[columns_of_interest][0:29]
rater_2_df = rater_2_df[columns_of_interest][0:29]
rater_3_df = rater_3_df[columns_of_interest][0:29]

aligned_rater2_df = rater_2_df.set_index("Drawing ID").loc[rater_1_df["Drawing ID"]].reset_index()
aligned_rater3_df = rater_3_df.set_index("Drawing ID").loc[rater_1_df["Drawing ID"]].reset_index()

result_df,summary = scored_drawing_summary(rater_1_df, aligned_rater2_df, aligned_rater3_df)
subject_df, condition_stats, t_test_result = compute_mean_segment_cost_per_subject(result_df)
print(subject_df)
print(condition_stats)
print(t_test_result)

plot_mean_scores_bar(summary)