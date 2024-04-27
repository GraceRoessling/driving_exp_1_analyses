import os
import pandas as pd
import dataframe_helper_functions

class Trial:
    "This is the trial class. A trial is the smallest event in an experiment that consists of the subject driving along a single track."

    trial_str_list = ["T001","T002","T003","T004","T005","T006","T007","T008","T009","T010"]

    def __init__(self, id, number, subject):
        self.id = id
        self.number = number
        self.subject_id = subject.id
        self.paths = self.get_trial_paths(subject)

    def get_trial_paths(self,subject):
        path_to_csv = f"{subject.path}/S001/trackers"
        for filename in os.listdir(path_to_csv):
            if self.id in filename:
                if "main_camera" in filename:
                    main_cam_path = f"{path_to_csv}/{filename}"
                    main_cam_df = pd.read_csv (main_cam_path)
                elif "vehicle_movement" in filename:
                    vehicle_path = f"{path_to_csv}/{filename}"
                    vehicle_df = pd.read_csv (vehicle_path)
                elif "Vehicle_DrivingSim":
                    driving_sim_path = f"{path_to_csv}/{filename}"
                    driving_sim_df = pd.read_csv (driving_sim_path)
        main_cam_df,vehicle_df,driving_sim_df = dataframe_helper_functions.remove_NA(main_cam_df,vehicle_df,driving_sim_df)
        paths = {"main_camera":main_cam_df,
                "vehicle_movement":vehicle_df,
                "Vehicle_DrivingSim":driving_sim_df}
        return(paths)




    

