library(tidyverse)
source("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 1/scripts/analysis_functions.R")


## GET CSV FILE =======================================================================================================================================

# Subject 2, Unfamiliar Group

"C:\Users\graci\Dropbox\PAndA\Thesis Experiment 1\scripts\pilot_data\unfamiliar\2\track_piece_csv\s_turn_short_collider\cam_pos.csv"

tracK_piece_1_cam_pos <- read_csv("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 1/scripts/pilot_data/familiar/1/trial_10_preprocessed_CSV/trial_10_cam_pos.csv")
tracK_piece_1_vehicle_pos <- read_csv("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 1/scripts/pilot_data/familiar/1/trial_10_preprocessed_CSV/trial_10_vehicle_pos.csv")
tracK_piece_1_drive_vars <- read_csv("C:/Users/graci/Dropbox/PAndA/Thesis Experiment 1/scripts/pilot_data/familiar/1/trial_10_preprocessed_CSV/trial_10_drive_var.csv")
