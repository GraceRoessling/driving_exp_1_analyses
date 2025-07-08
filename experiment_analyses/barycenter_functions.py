import numpy as np
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
import pandas as pd

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
            elif subject_id == "grid" and track_piece_id == "t_turn":
                track_piece_trajectory_df = track_dataframe_dict["main_camera"][350:1000]
            elif subject_id == "grid" and track_piece_id == "symmetric_parabolic":
                track_piece_trajectory_df = track_dataframe_dict["main_camera"][550:1200]
            if len(familiar_trajectories) != len(familiar_group_ids): # checks when to switch to other experimental group list
                familiar_trajectories.append(track_piece_trajectory_df[['pos_x', 'pos_z']].values) # converts dataframe to np values
            else:
                unfamiliar_trajectories.append(track_piece_trajectory_df[['pos_x', 'pos_z']].values)
    return(familiar_trajectories,unfamiliar_trajectories)

def get_barycenter_per_group(condition,track_piece_object,group_trajectories,group_ids):
    initial_traj = group_trajectories[0] # this will be our initial trajectory that we start with and iteratively update

    for i in range(0, len(group_trajectories) - 1): # Go through each trajectory in this experimental group
        new_barycenter = [] # New Barycenter points added as trajectory is populated
        dist_matrix = cdist(initial_traj, group_trajectories[i + 1], 'euclidean') # DTW on inital trajectory (Barycenter) and subject trajectory
        path, cost = getCostMatrix(dist_matrix)
        # print(path) # Given a list of tuples, each coordinate can index their respective trajectories and be averaged
        for j in range(0, len(path)): # Traverses alignment path to index trajectories and generate points on the Barycenter Trajectory
            new_barycenter.append((initial_traj[path[j][0]] + group_trajectories[i + 1][path[j][1]])/2)
        initial_traj = new_barycenter
        #print(f'{group_ids[i]} updated Barycenter')
        x, y = zip(*initial_traj)
        #plt.plot(x, y)
    dba_fam = new_barycenter
    dba_fam = initial_traj

    #x1, y1 = zip(*dba_fam) #fam unzip and plot
    #plt.plot(x1, y1)
    pd.DataFrame(dba_fam).to_csv(f"C:/Users/graci/Dropbox/PAndA/Thesis Experiment 2/presentations/r_figures/{condition}_{track_piece_object.id}_DBA_traj.csv")

def plot_trajectories_for_group(condition,group_trajectories,track_piece_object):
    plt.figure(figsize=(12, 8))

    # Plot all subject trajectories in red
    for i, traj in enumerate(group_trajectories[0:12]):
        plt.plot(traj[:, 0], traj[:, 1], lw=3, color='gray',label=f'Subject {i+1}', alpha=0.6)

    # Get the centerline for reference
    track_piece_center_x, track_piece_center_y = track_piece_object.centerline_df['x'],track_piece_object.centerline_df['y']
    plt.plot(track_piece_center_x, track_piece_center_y, color='black', linestyle='dotted', lw=3, label='Centerline')

    

    # Plotting labels
    plt.title(f'Trajectories on Trial 10 for {track_piece_object.id} for {condition} group')
    plt.xlabel('X Position')
    plt.ylabel('Z Position')
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()
    #plt.savefig(f"C:/Users/graci/Dropbox/PAndA/Thesis Experiment 2/presentations/r_figures/{condition}_{track_piece_object.id}_all_trajectories.svg")