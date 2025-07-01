import numpy as np
from scipy.spatial import cKDTree
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.collections import LineCollection
import numpy as np

def get_speeds_along_centerline(track_centerline_x, track_centerline_y, speed_df, position_df):
    """
    Given centerline coordinates and subject trajectory data,
    return a dictionary mapping each centerline index to the subject's speed
    at the closest position in the trajectory.

    Parameters:
    - track_centerline_x: Series or array of x coordinates for centerline
    - track_centerline_y: Series or array of y coordinates for centerline
    - speed_df: DataFrame with columns ['velocity_magnitude', 'time']
    - position_df: DataFrame with columns ['pos_x', 'pos_y', 'time']

    Returns:
    - Dictionary mapping centerline index to speed at closest trajectory point
    """

    centerline_coords = np.column_stack((track_centerline_x.values, track_centerline_y.values))
    trajectory_coords = position_df[['pos_x', 'pos_y']].values
    trajectory_times = position_df['time'].values

    # Build spatial tree of trajectory positions
    trajectory_tree = cKDTree(trajectory_coords)

    # Find closest trajectory point for each centerline point
    distances, indices = trajectory_tree.query(centerline_coords)

    # Use those indices to find the corresponding times and look up speeds
    closest_times = trajectory_times[indices]

    # Interpolate the speed at those times using speed_df
    speed_at_times = np.interp(closest_times, speed_df['time'], speed_df['velocity_magnitude'])

    # Build dictionary mapping centerline index to speed
    centerline_speed_dict = {idx: speed for idx, speed in enumerate(speed_at_times)}

    return centerline_speed_dict

def average_centerline_speeds(centerline_speed_dicts):
    """
    Given a list of dictionaries (one per subject) mapping centerline indices to speeds,
    compute the average speed at each centerline index across all subjects.

    Parameters:
    - centerline_speed_dicts: List of dicts, where each dict maps centerline index -> speed

    Returns:
    - Dictionary mapping centerline index to average speed across all subjects
    """
    aggregated_speeds = defaultdict(list)

    # Collect speeds for each centerline index
    for subject_dict in centerline_speed_dicts:
        for idx, speed in subject_dict.items():
            aggregated_speeds[idx].append(speed)

    # Compute average speed at each index
    averaged_speeds = {idx: np.mean(speeds) for idx, speeds in aggregated_speeds.items()}

    return averaged_speeds


def plot_centerline_speed_heatmap(condition,track_centerline_x, track_centerline_y, average_speed_dict, trial_number):
    """
    Plots a heatmap along the centerline using average speeds from multiple subjects.

    Parameters:
    - track_centerline_x: array-like x coordinates of centerline
    - track_centerline_y: array-like y coordinates of centerline
    - average_speed_dict: dict mapping centerline index to average speed
    - trial_number: integer, used for labeling
    """

    # Convert centerline coordinates to NumPy arrays
    x_vals = np.array(track_centerline_x)
    y_vals = np.array(track_centerline_y)

    # Create line segments from centerline
    segments = [
        [[x_vals[i], y_vals[i]], [x_vals[i + 1], y_vals[i + 1]]]
        for i in range(len(x_vals) - 1)
    ]

    # Get speed values from average_speed_dict
    speed_values = np.array([average_speed_dict.get(i, 0) for i in range(len(x_vals) - 1)])

    # Normalize speeds for color mapping
    norm = plt.Normalize(vmin=0, vmax=25)
    cmap = cm.get_cmap("coolwarm")

    # Create LineCollection with average speeds
    lc = LineCollection(segments, cmap=cmap, norm=norm, linewidth=6)
    lc.set_array(speed_values)

    # Plot
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.add_collection(lc)
    ax.plot(x_vals, y_vals, color='gray', linestyle='dotted', lw=1.5, alpha=0.5)  # optional reference line

    # Add colorbar and labels
    cbar = plt.colorbar(lc, ax=ax)
    cbar.set_label("Average Speed (m/s)")

    ax.autoscale()
    ax.set_aspect('equal', 'box')
    plt.title(f"Average Heatmap for {condition}")
    plt.xticks([])  # Removes X-axis numbers
    plt.yticks([])
    plt.grid(True)
    plt.tight_layout()
    #plt.show()
    plt.savefig(f"C:/Users/graci/Dropbox/PAndA/Thesis Experiment 2/presentations/r_figures/{condition}_g_heatmap.svg")
