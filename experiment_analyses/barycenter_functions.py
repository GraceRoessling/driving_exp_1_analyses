import numpy as np
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
import pandas as pd
from scipy.spatial.distance import cdist
from scipy.spatial import procrustes
from scipy.interpolate import interp1d


def getCostMatrix(dist_mat):
    """
    Find minimum-cost path through matrix `dist_mat` using dynamic programming.

    The cost of a path is defined as the sum of the matrix entries on that
    path. See the following for details of the algorithm:

    - http://en.wikipedia.org/wiki/Dynamic_time_warping
    - https://www.ee.columbia.edu/~dpwe/resources/matlab/dtw/dp.m

    The notation in the first reference was followed, while Dan Ellis's code
    (second reference) was used to check for correctness. Returns a list of
    path indices and the cost matrix.
    """

    N, M = dist_mat.shape

    # Initialize the cost matrix
    cost_mat = np.zeros((N + 1, M + 1))
    for i in range(1, N + 1):
        cost_mat[i, 0] = np.inf
    for i in range(1, M + 1):
        cost_mat[0, i] = np.inf

    # Fill the cost matrix while keeping traceback information
    traceback_mat = np.zeros((N, M))
    for i in range(N):
        for j in range(M):
            penalty = [
                cost_mat[i, j],      # match (0)
                cost_mat[i, j + 1],  # insertion (1)
                cost_mat[i + 1, j]]  # deletion (2)
            i_penalty = np.argmin(penalty)
            cost_mat[i + 1, j + 1] = dist_mat[i, j] + penalty[i_penalty]
            traceback_mat[i, j] = i_penalty

    # Traceback from bottom right
    i = N - 1
    j = M - 1
    path = [(i, j)]
    while i > 0 or j > 0:
        tb_type = traceback_mat[i, j]
        if tb_type == 0:
            # Match
            i = i - 1
            j = j - 1
        elif tb_type == 1:
            # Insertion
            i = i - 1
        elif tb_type == 2:
            # Deletion
            j = j - 1
        path.append((i, j))

    # Strip infinity edges from cost_mat before returning
    cost_mat = cost_mat[1:, 1:]
    return (path[::-1], cost_mat) # Return cost_mat and path

def process_groups(familiar_group_ids,unfamiliar_group_ids,subject_dict, track_piece_id):
    familiar_trajectories = []
    unfamiliar_trajectories = []
    for group in [familiar_group_ids, unfamiliar_group_ids]:
        for subject_id in group:
            # Get objects associated with a given subject and their trial
            subject_object = subject_dict[subject_id] 
            trial_object_ten = subject_object.trials[9]
            # Get trajectory for track segment of interest
            track_piece_object_dict = trial_object_ten.pieces # dictionary that contains track_piece names and their associated track_piece_object instantiation
            track_piece_object = track_piece_object_dict[track_piece_id] # get the track piece object associated to the track piece
            # Get trajectory for a given piece
            track_dataframe_dict = track_piece_object.dataframes
            track_piece_trajectory_df = track_dataframe_dict["main_camera"]
            if subject_id == "trial" and track_piece_id == "t_turn":
                track_piece_trajectory_df = track_dataframe_dict["main_camera"][550:1350]
            elif subject_id == "swarm" and track_piece_id == "t_turn":
                track_piece_trajectory_df = track_dataframe_dict["main_camera"][500:1150]
            elif subject_id == "debt" and track_piece_id == "t_turn":
                track_piece_trajectory_df = track_dataframe_dict["main_camera"][:450]
            elif subject_id == "grid" and track_piece_id == "t_turn":
                track_piece_trajectory_df = track_dataframe_dict["main_camera"][350:1000]
            elif subject_id == "grid" and track_piece_id == "symmetric_parabolic":
                track_piece_trajectory_df = track_dataframe_dict["main_camera"][550:1200]
            if len(familiar_trajectories) != len(familiar_group_ids): # checks when to switch to other experimental group list
                familiar_trajectories.append(track_piece_trajectory_df[['pos_x', 'pos_z']].values) # converts dataframe to np values
            else:
                unfamiliar_trajectories.append(track_piece_trajectory_df[['pos_x', 'pos_z']].values)
    return(familiar_trajectories,unfamiliar_trajectories)

def procrustes_no_scaling(X, Y):
    """
    Align Y to X using Procrustes analysis without scaling.
    Only rotation and translation are applied.
    """
    X = np.array(X)
    Y = np.array(Y)

    # Subtract centroids
    muX = X.mean(axis=0)
    muY = Y.mean(axis=0)
    X0 = X - muX
    Y0 = Y - muY

    # Solve the orthogonal Procrustes problem (rotation only)
    U, _, Vt = np.linalg.svd(np.dot(Y0.T, X0))
    R = np.dot(U, Vt)

    # Apply rotation and translate back to original location
    Y_aligned = np.dot(Y0, R) + muX
    return Y_aligned


def resample_trajectory(traj, num_points=100):
    traj = np.array(traj)
    distances = np.cumsum(np.linalg.norm(np.diff(traj, axis=0), axis=1))
    distances = np.insert(distances, 0, 0)  # Include the starting point
    interp_x = interp1d(distances, traj[:, 0], kind='linear')
    interp_y = interp1d(distances, traj[:, 1], kind='linear')
    new_distances = np.linspace(0, distances[-1], num_points)
    resampled = np.stack([interp_x(new_distances), interp_y(new_distances)], axis=1)
    return resampled

def get_barycenter_per_group(condition, track_piece_object, group_trajectories, group_ids):
    initial_traj = group_trajectories[0]  # Use first trajectory as initial mean

    # Iteratively compute average trajectory (barycenter)
    for i in range(len(group_trajectories) - 1):
        new_barycenter = []
        dist_matrix = cdist(initial_traj, group_trajectories[i + 1], 'euclidean')
        path, cost = getCostMatrix(dist_matrix)

        for j in range(len(path)):
            pt1 = initial_traj[path[j][0]]
            pt2 = group_trajectories[i + 1][path[j][1]]
            new_barycenter.append((pt1 + pt2) / 2)

        initial_traj = np.array(new_barycenter)

    # ---- Align to the first subject trajectory using Procrustes ----
    num_points = 100
    resampled_barycenter = resample_trajectory(initial_traj, num_points=num_points)
    reference_traj = resample_trajectory(group_trajectories[0], num_points=num_points)

    # Procrustes alignment
    aligned_barycenter = procrustes_no_scaling(reference_traj, resampled_barycenter)

    # ---- Export ----
    output_path = f"C:/Users/graci/Dropbox/PAndA/Thesis Experiment 2/presentations/r_figures/{condition}_{track_piece_object.id}_DBA_traj_scaled2.csv"
    pd.DataFrame(aligned_barycenter, columns=["X", "Z"]).to_csv(output_path, index=False)


def plot_trajectories_for_group(condition,group_trajectories,track_piece_object):
    plt.figure(figsize=(12, 8))

    # Plot all subject trajectories in gray
    for i, traj in enumerate(group_trajectories[0:12]):
        if i == 0:
            plt.plot(traj[:, 0], traj[:, 1], lw=2, color='gray', label='Trajectories', alpha=0.6)
        else:
            plt.plot(traj[:, 0], traj[:, 1], lw=2, color='gray', alpha=0.6)

    # Get the centerline for reference
    track_piece_center_x, track_piece_center_y = track_piece_object.centerline_df['x'],track_piece_object.centerline_df['y']
    plt.plot(track_piece_center_x, track_piece_center_y, color='black', linestyle='dotted', lw=3, label='Road Center')

    # Plot the DBA trajectory
    dir_path = "C:/Users/graci/Dropbox/PAndA/Thesis Experiment 2/presentations/r_figures/"
    dba_file_path = dir_path + f"/{condition}_{track_piece_object.id}_DBA_traj_scaled2.csv"
    dba_df = pd.read_csv(dba_file_path)
    if condition == "Constant Track":
        dba_color = "blue"
    else:
        dba_color = "red"
    plt.plot(dba_df['X'], dba_df['Z'], color=dba_color, lw=4, label='Mean Trajectory')


    # Plotting labels
    plt.title(f'Trajectories on Trial 10 for {track_piece_object.id} for {condition} group')
    plt.xlabel('X Position')
    plt.ylabel('Z Position')
    
    # Other Plotting params
    ax = plt.gca()
    ax.autoscale()
    # if track_piece_object.id == 't_turn':
    #     ax.set_xlim([230, 390])
    #     ax.set_ylim([80, 175])
    # elif track_piece_object.id == 'symmetric_parabolic':
    #     ax.set_xlim([-120, -35])
    #     ax.set_ylim([-5, 80])
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    # plt.show()
    plt.savefig(f"C:/Users/graci/Dropbox/PAndA/Thesis Experiment 2/presentations/r_figures/{condition}_{track_piece_object.id}_all_trajectories_and_dba.svg")


def plot_comp_of_barycenters(track_piece_object):
    plt.figure(figsize=(12, 8))

    # Get the centerline for reference
    track_piece_center_x, track_piece_center_y = track_piece_object.centerline_df['x'],track_piece_object.centerline_df['y']
    plt.plot(track_piece_center_x, track_piece_center_y, color='black', linestyle='dotted', lw=3, label='Road Center')

    # Plot the DBA trajectory
    dir_path = "C:/Users/graci/Dropbox/PAndA/Thesis Experiment 2/presentations/r_figures/"
    constant_dba_file_path = dir_path + f"/Constant Track_{track_piece_object.id}_DBA_traj_scaled2.csv"
    variable_dba_file_path = dir_path + f"/Variable Track_{track_piece_object.id}_DBA_traj_scaled2.csv"
    
    constant_dba_df = pd.read_csv(constant_dba_file_path)
    variable_dba_df = pd.read_csv(variable_dba_file_path)
 
    plt.plot(constant_dba_df['X'], constant_dba_df['Z'], color='blue', lw=4, label='Constant Track Group')
    plt.plot(variable_dba_df['X'], variable_dba_df['Z'], color='red', lw=4, label='Variable Track Group')


    # Plotting labels
    plt.title(f'Mean Trajectories on Trial 10 for {track_piece_object.id}')
    plt.xlabel('X Position')
    plt.ylabel('Z Position')
    
    # Other Plotting params
    ax = plt.gca()
    ax.autoscale()
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    #plt.show()
    plt.savefig(f"C:/Users/graci/Dropbox/PAndA/Thesis Experiment 2/presentations/r_figures/{track_piece_object.id}_dba_comparison.svg")


import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.patheffects as pe

def plot_comp_of_barycenters_and_trajectories(familiar_group_trajectories, unfamiliar_group_trajectories, track_piece_object):
    plt.figure(figsize=(12, 8))

    # Plot all subject trajectories
    for i, traj in enumerate(familiar_group_trajectories[0:12]):
        if i == 0:
            plt.plot(traj[:, 0], traj[:, 1], lw=1, color='royalblue', label='Constant Track Group Trajectories', alpha=0.6)
        else:
            plt.plot(traj[:, 0], traj[:, 1], lw=1, color='royalblue', alpha=0.6)
    
    for i, traj in enumerate(unfamiliar_group_trajectories[0:12]):
        if i == 0:
            plt.plot(traj[:, 0], traj[:, 1], lw=1, color='red', label='Variable Track Group Trajectories', alpha=0.6)
        else:
            plt.plot(traj[:, 0], traj[:, 1], lw=1, color='red', alpha=0.6)

    # Get the centerline for reference
    track_piece_center_x, track_piece_center_y = track_piece_object.centerline_df['x'],track_piece_object.centerline_df['y']
    plt.plot(track_piece_center_x, track_piece_center_y, color='black', linestyle='dotted', lw=3, label='Road Center')

    # Plot the DBA trajectory
    dir_path = "C:/Users/graci/Dropbox/PAndA/Thesis Experiment 2/presentations/r_figures/"
    constant_dba_file_path = dir_path + f"/Constant Track_{track_piece_object.id}_DBA_traj_scaled2.csv"
    variable_dba_file_path = dir_path + f"/Variable Track_{track_piece_object.id}_DBA_traj_scaled2.csv"
    
    constant_dba_df = pd.read_csv(constant_dba_file_path)
    variable_dba_df = pd.read_csv(variable_dba_file_path)
 
    plt.plot(variable_dba_df['X'], variable_dba_df['Z'], color='red', lw=4,label='Variable Track Group',path_effects=[pe.Stroke(linewidth=7, foreground='black'), pe.Normal()])
    plt.plot(constant_dba_df['X'], constant_dba_df['Z'], color='royalblue', lw=4,label='Constant Track Group Mean Trajectory',path_effects=[pe.Stroke(linewidth=7, foreground='black'), pe.Normal()])
    
    # Plotting labels
    plt.title(f'Mean Trajectories on Trial 10 for {track_piece_object.id}')
    plt.xlabel('X Position')
    plt.ylabel('Z Position')
    
    # Other Plotting params
    ax = plt.gca()
    ax.autoscale()
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    #plt.show()
    plt.savefig(f"C:/Users/graci/Dropbox/PAndA/Thesis Experiment 2/presentations/r_figures/{track_piece_object.id}_dba_comparison.svg")