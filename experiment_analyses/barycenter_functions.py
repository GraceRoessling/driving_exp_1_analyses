import numpy as np
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt

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

def process_groups(familiar_group_ids,unfamiliar_group_ids,subject_dict):
    familiar_trajectories = []
    unfamiliar_trajectories = []
    for group in [familiar_group_ids, unfamiliar_group_ids]:
        for subject_id in group:
            # Get objects associated with a given subject and their trial
            subject_object = subject_dict[subject_id] 
            trial_object_eleven = subject_object.trials[9]
            
            trial_df_eleven = trial_object_eleven.trajectory_df # Get trajectory data frame
            if len(familiar_trajectories) != len(familiar_group_ids): # checks when to switch to other experimental group list
                familiar_trajectories.append(trial_df_eleven[['pos_x', 'pos_z']].values) # converts dataframe to np values
            else:
                unfamiliar_trajectories.append(trial_df_eleven[['pos_x', 'pos_z']].values)
    return(familiar_trajectories,unfamiliar_trajectories)

def get_barycenter_per_group(group_trajectories, group_ids):
    initial_traj = group_trajectories[0] # this will be our initial trajectory that we start with and iteratively update

    for i in range(0, len(group_trajectories) - 1): # Go through each trajectory in this experimental group
        new_barycenter = [] # New Barycenter points added as trajectory is populated
        dist_matrix = cdist(initial_traj, group_trajectories[i + 1], 'euclidean') # DTW on inital trajectory (Barycenter) and subject trajectory
        path, cost = getCostMatrix(dist_matrix)
        # print(path) # Given a list of tuples, each coordinate can index their respective trajectories and be averaged
        for j in range(0, len(path)): # Traverses alignment path to index trajectories and generate points on the Barycenter Trajectory
            new_barycenter.append((initial_traj[path[j][0]] + group_trajectories[i + 1][path[j][1]])/2)
        initial_traj = new_barycenter
        print(f'{group_ids[i]} updated Barycenter')
        x, y = zip(*initial_traj)
        plt.plot(x, y)
    dba_fam = new_barycenter