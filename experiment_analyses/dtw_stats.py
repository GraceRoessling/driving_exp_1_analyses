import pandas as pd

dtw_df = pd.read_csv("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 2/data/dtw_data.csv")

def compute_mean_segment_cost_per_subject(df):
    # Group by subject_id and calculate the mean segment cost
    mean_costs = df.groupby('subject_id')['Segment Costs'].mean().reset_index()
    mean_costs.rename(columns={'Segment Costs': 'Mean Segment Cost'}, inplace=True)

    # Get the condition per subject_id (assuming one condition per subject)
    conditions = df[['subject_id', 'Condition']].drop_duplicates()

    # Merge mean costs with condition info
    result = pd.merge(mean_costs, conditions, on='subject_id')

    # Sort so that 'familiar' condition comes first
    result['Condition'] = pd.Categorical(result['Condition'], categories=['familiar', 'unfamiliar'], ordered=True)
    result = result.sort_values('Condition').reset_index(drop=True)

    # Calculate mean and std deviation for each condition group
    group_stats = result.groupby('Condition')['Mean Segment Cost'].agg(['mean', 'std']).to_dict('index')

    return result, group_stats


def analyze_segments_per_subject(csv_path):
    """
    Analyze the number of unique track segments per subject.
    
    Returns a DataFrame with:
    - subject_id
    - num_unique_segments: number of unique track_segment strings
    - num_total_rows: total number of rows for that subject
    - condition: familiar or unfamiliar
    """
    df = pd.read_csv(csv_path)
    
    analysis = df.groupby('subject_id').agg({
        'track_segment': 'nunique',
        'condition': 'first'
    }).reset_index()
    
    analysis.rename(columns={
        'track_segment': 'num_unique_segments',
        'condition': 'condition'
    }, inplace=True)
    
    # Add total row count per subject
    row_counts = df.groupby('subject_id').size().reset_index(name='num_total_rows')
    analysis = pd.merge(analysis, row_counts, on='subject_id')
    
    # Sort by subject_id
    analysis = analysis.sort_values('subject_id').reset_index(drop=True)
    
    return analysis


# Usage:
csv_path = "C:\\Users\\graci\\Dropbox\\PAndA\\Thesis Experiment 2\\data\\dtw_scores_per_track_segment_recovered.csv"
segments_analysis = analyze_segments_per_subject(csv_path)
print(segments_analysis)

# Count subjects per condition
subjects_per_group = segments_analysis.groupby('condition')['subject_id'].count()
print("\nNumber of subjects per group:")
print(subjects_per_group)

segments_analysis.to_csv('C:/Users/graci/Dropbox/PAndA/Thesis Experiment 2/data/segments_per_subject.csv', index=False)

# new_df,group_means = compute_mean_segment_cost_per_subject(dtw_df)
# new_df.to_csv('C:/Users/graci/Dropbox/PAndA/Thesis Experiment 2/data/dtw_per_subj.csv', index=False)
# print(new_df)
# print(group_means)
