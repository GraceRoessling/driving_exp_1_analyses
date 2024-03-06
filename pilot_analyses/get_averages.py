import preprocess
import analysis_functions
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline


# Params -------------------------------------------------------------------
window_size = 35


# Load data ----------------------------------------------------------------
cam_position_df,vehicle_position_df,driving_vars_df,track_pieces,dict_of_track_piece_dfs = preprocess.get_dfs_for_subject("familiar","1",window_size)

# Time Window ------------------------------------------------------------
#min_time,max_time = 0,300
# min_time,max_time = 0,400
# min_time,max_time = 0,len(cam_position_df["moving_avg_speed"]) # whole time
# min_time,max_time = 3100,len(cam_position_df["moving_avg_speed"])

# Data Validation --------------------------------------------------------------------------------------------------------------------------------------------------------
# Plot it out
# fig, ax = plt.subplots(2, 1, figsize=(5, 5))

#plt.ylim(-1, 40)

## PLOT SPEED OVER TIME
# ax[0].plot(cam_position_df["time"][min_time:max_time], cam_position_df["speed"][min_time:max_time], c = "red")
# ax[0].plot(cam_position_df["time"][min_time:max_time], cam_position_df["moving_avg_speed"][min_time:max_time], c = "green")
# ax[1].plot(driving_vars_df["time"][min_time:max_time], driving_vars_df["throttle_position"][min_time:max_time], c = "black")
# plt.show()

# ax[0].set_title('Steering Angle')
# ax[0].plot(driving_vars_df["time"][min_time:max_time], driving_vars_df["steering_angle_transformed"][min_time:max_time], c = "green")
# ax[1].set_title('World Rotation of Vehicle')
# ax[1].plot(cam_position_df["time"][min_time:max_time], cam_position_df["rot_y"][min_time:max_time], c = "black")
# plt.show()


# Comparative Statistics --------------------------------------------------------------------------------------------------------------------------------------------------------
# How does the familiar group vs unfamliar group differ in performance for the 10th trial?



# steering, steering variance

# speed, speed variance

# throttle usage

# X,Z trajectories

# lap time