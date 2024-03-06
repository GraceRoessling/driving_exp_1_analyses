import os
file_path = "C:/Users/graci/Dropbox/PAndA/Thesis Experiment 1/data/main_data"
class Subject:
    "This is the subject class. A subject is a person object that has performance information affiliated to their driving behavior."
    def __init__(self, id, condition):
        self.condition = condition
        self.id = id
        
        self.path = self.get_subject_path()

    def get_subject_path(self):
        dir = f"{file_path}/{self.condition}"
        for filename in os.listdir(dir):
            if self.id in filename:
                subject_path = f"{dir}/{filename}"
                return(subject_path)













