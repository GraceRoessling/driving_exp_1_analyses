import pandas as pd
import numpy as np
import os
import subject
import trial
from IPython import embed

# ----------------------------------------------------------------------------------------------------------------------
# Helper funcs
def initialize_subjects(subject_id_dict, condition):
    subject_obj_dict = dict()
    for subject_id in subject_id_dict[condition]:
        subject_object = subject.Subject(subject_id, condition)
        subject_obj_dict[subject_id] = subject_object
    return subject_obj_dict

# ----------------------------------------------------------------------------------------------------------------------
# setup
subject_id_dict = {
    "familiar": ["boss", "chunk", "cod", "depth", "froze", "omen", "scrub", "sweat", "tweet", "wad"],
    "unfamiliar": ["chess", "class", "dust", "envoy", "flint", "lurch", "maker", "point", "shack", "wool"]
}

# Total list of trials
trial_str_list = ["T001","T002","T003","T004","T005","T006","T007","T008","T009","T010"]

# ----------------------------------------------------------------------------------------------------------------------
# main

familiar_subject_dict = initialize_subjects(subject_id_dict, "familiar")
for familiar_subject_id in familiar_subject_dict:
    trial.initialize_trials_for_one_subject(trial_str_list, familiar_subject_dict[familiar_subject_id])

unfamiliar_subject_dict = initialize_subjects(subject_id_dict, "unfamiliar")
for unfamiliar_subject_id in unfamiliar_subject_dict:
    trial.initialize_trials_for_one_subject(trial_str_list, unfamiliar_subject_dict[unfamiliar_subject_id])

# example of printing a single DF
print(unfamiliar_subject_dict[list(unfamiliar_subject_dict)[0]].trials[0].paths["main_camera"])