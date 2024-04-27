library(tidyverse)
library(dplyr)
library(ggplot2)
source("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 1/scripts/analysis_functions.R")


## GET CSV FILE =======================================================================================================================================

# Familiar Group
sub_1_fam_cam_pos <- read_csv("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 1/scripts/pilot_data/familiar/1/trial_10_preprocessed_CSV/trial_10_cam_pos.csv")
sub_1_fam_vehicle_pos <- read_csv("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 1/scripts/pilot_data/familiar/1/trial_10_preprocessed_CSV/trial_10_vehicle_pos.csv")
sub_1_fam_drive_vars <- read_csv("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 1/scripts/pilot_data/familiar/1/trial_10_preprocessed_CSV/trial_10_drive_var.csv")

# sub_2_fam_cam_pos <- read_csv("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 1/scripts/pilot_data/familiar/2/trial_10_preprocessed_CSV/trial_10_cam_pos.csv")
# sub_2_fam_vehicle_pos <- read_csv("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 1/scripts/pilot_data/familiar/2/trial_10_preprocessed_CSV/trial_10_vehicle_pos.csv")
# sub_2_fam_drive_vars <- read_csv("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 1/scripts/pilot_data/familiar/2/trial_10_preprocessed_CSV/trial_10_drive_var.csv")
# 
# sub_3_fam_cam_pos <- read_csv("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 1/scripts/pilot_data/familiar/3/trial_10_preprocessed_CSV/trial_10_cam_pos.csv")
# sub_3_fam_vehicle_pos <- read_csv("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 1/scripts/pilot_data/familiar/3/trial_10_preprocessed_CSV/trial_10_vehicle_pos.csv")
# sub_3_fam_drive_vars <- read_csv("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 1/scripts/pilot_data/familiar/3/trial_10_preprocessed_CSV/trial_10_drive_var.csv")

# Unfamiliar Group
# sub_1_unfam_cam_pos <- read_csv("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 1/scripts/pilot_data/unfamiliar/1/trial_10_preprocessed_CSV/trial_10_cam_pos.csv")
# sub_1_unfam_vehicle_pos <- read_csv("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 1/scripts/pilot_data/unfamiliar/1/trial_10_preprocessed_CSV/trial_10_vehicle_pos.csv")
# sub_1_unfam_drive_vars <- read_csv("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 1/scripts/pilot_data/unfamiliar/1/trial_10_preprocessed_CSV/trial_10_drive_var.csv")
# 
# sub_2_unfam_cam_pos <- read_csv("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 1/scripts/pilot_data/unfamiliar/2/trial_10_preprocessed_CSV/trial_10_cam_pos.csv")
# sub_2_unfam_vehicle_pos <- read_csv("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 1/scripts/pilot_data/unfamiliar/2/trial_10_preprocessed_CSV/trial_10_vehicle_pos.csv")
# sub_2_unfam_drive_vars <- read_csv("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 1/scripts/pilot_data/unfamiliar/2/trial_10_preprocessed_CSV/trial_10_drive_var.csv")
# 
# sub_3_unfam_cam_pos <- read_csv("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 1/scripts/pilot_data/unfamiliar/3/trial_10_preprocessed_CSV/trial_10_cam_pos.csv")
# sub_3_unfam_vehicle_pos <- read_csv("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 1/scripts/pilot_data/unfamiliar/3/trial_10_preprocessed_CSV/trial_10_vehicle_pos.csv")
# sub_3_unfam_drive_vars <- read_csv("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 1/scripts/pilot_data/unfamiliar/3/trial_10_preprocessed_CSV/trial_10_drive_var.csv")

# ======================================================================================================================================================

## GENERAL STATISTICS ===================================================================================================================================

get_statistics_per_subject(sub_1_fam_cam_pos,sub_1_fam_drive_vars)

steering = sub_1_fam_drive_vars$steering_angle_transformed
time_drive_vars = sub_1_fam_drive_vars$time

speed = sub_1_fam_cam_pos$speed
smooth_speed = sub_1_fam_cam_pos$smooth_speed
time_cam = sub_1_fam_cam_pos$time


# plot speed over time 
plot(speed ~ time, data=sub_1_fam_cam_pos)
plot(smooth_speed ~ time, data=sub_1_fam_cam_pos)
  

# plot steering over time
plot(steering ~ time, data=sub_1_fam_cam_pos)

## FOR EACH TRACK =====================================================================================================================================
straight_long_collider_drive_vars <- sub_1_fam_drive_vars %>% filter(grepl('straight_long_collider', current_track_piece))

plot(steering_angle_transformed ~ time, data=straight_long_collider_drive_vars)









