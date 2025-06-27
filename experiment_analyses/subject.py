import os

class Subject:
    "This is the subject class. A subject is a person object that has performance information affiliated to their driving behavior."
    
    subject_id_dict = {
    "control": ["agony","both","cargo","cheek","cub", "desk","dingy","fetch","final","floss","fried","mount","pagan","slot", "snarl","spoof","tribe", "untie","width","wish"],
    "scrambled_segments": ["brave","comic", "crop", "dial","donor","even","gave","gore","gray", "hump","jury","mud", "outer", "ozone", "relax","riot", "salon","unit", "upon", "zebra"],
    "scrambled_landmarks": ["arena","chain","cloth","crept", "disk","elm","flask","flip","game","grab","grant","guy","jam","line","marry","ounce","river","roar","shred", "spoon"]
    }

    def __init__(self, id, condition, dir_path):
        self.id = id
        self.condition = condition
        self.dir_path = dir_path
        self.path = self.get_subject_path()


    def get_subject_path(self):
        dir = f"{self.dir_path}/{self.condition}"
        for filename in os.listdir(dir):
            if self.id in filename:
                subject_path = f"{dir}/{filename}"
                return(subject_path)













