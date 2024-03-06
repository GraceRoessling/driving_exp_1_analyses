import os
import pandas as pd

class Trial:
    "This is the trial class. A trial is the smallest event in an experiment that consists of the subject driving along a single track."

    subject_id = ""
    id = ""
    map = False
    paths = {}

    def __init__(self, subject_id, id, paths):
        self.subject_id = subject_id
        self.id = id
        self.paths = paths

def get_trial_paths(trial_id,subject):
    path_to_csv = f"{subject.path}/S001/trackers"
    for filename in os.listdir(path_to_csv):
        if trial_id in filename:
            if "main_camera" in filename:
                main_cam_path = f"{path_to_csv}/{filename}"
                main_cam_df = pd.read_csv (main_cam_path)
            elif "vehicle_movement" in filename:
                vehicle_path = f"{path_to_csv}/{filename}"
                vehicle_df = pd.read_csv (vehicle_path)
            elif "Vehicle_DrivingSim":
                driving_sim_path = f"{path_to_csv}/{filename}"
                driving_sim_df = pd.read_csv (driving_sim_path)
    paths = {"main_camera":main_cam_df,
            "vehicle_movement":vehicle_df,
            "Vehicle_DrivingSim":driving_sim_df}
    return(paths)

def initialize_trials_for_one_subject(trial_str_list, subject):
    trial_object_list = []
    for trial_string in trial_str_list:
        subject_id = subject.id
        trial_id = trial_string
        trial_paths = get_trial_paths(trial_id,subject)
        trial = Trial(subject_id,trial_id, trial_paths)
        trial_object_list.append(trial)
    subject.trials = trial_object_list


    

