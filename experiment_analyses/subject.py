import os

class Subject:
    "This is the subject class. A subject is a person object that has performance information affiliated to their driving behavior."
    
    subject_id_dict = {
    "familiar": ["boss", "chunk", "cod", "depth", "froze", "omen", "scrub", "sweat", "tweet", "wad"],
    "unfamiliar": ["chess", "class", "dust", "envoy", "flint", "lurch", "maker", "point", "shack", "wool"]
    }


    file_path = "C:/Users/graci/Dropbox/PAndA/Thesis Experiment 1/data/main_data"
    def __init__(self, id, condition):
        self.id = id
        self.condition = condition
        self.path = self.get_subject_path()

    def get_subject_path(self):
        dir = f"{self.file_path}/{self.condition}"
        for filename in os.listdir(dir):
            if self.id in filename:
                subject_path = f"{dir}/{filename}"
                return(subject_path)













