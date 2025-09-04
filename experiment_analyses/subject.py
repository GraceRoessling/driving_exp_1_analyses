import os

class Subject:
    "This is the subject class. A subject is a person object that has performance information affiliated to their driving behavior."
    
    subject_id_dict = {
    "familiar": ["baggy", "bash", "boned", "cargo","five", "grip","judge", "mule","poker","polio", "rerun", "slate", "slept", "trial", "yeast"],
    "unfamiliar": ["atom","blank", "brim", "chef", "clerk", "debt","filth", "grid", "lens", "limb", "most","proof","slimy", "swarm", "wok"]
    }

    completion_seq_dict = { "grip":"familiar","swarm": "unfamiliar","five": "familiar","wok": "unfamiliar","mule": "familiar","grid": "unfamiliar",
                            "polio": "familiar","atom": "unfamiliar","bash": "familiar","slimy": "unfamiliar","slept": "familiar","clerk": "unfamiliar",
                            "boned": "familiar","debt": "unfamiliar","yeast": "familiar","most": "unfamiliar","cargo": "familiar","brim": "unfamiliar",
                            "trial": "familiar","lens": "unfamiliar","baggy": "familiar","chef": "unfamiliar","slate": "familiar","limb": "unfamiliar",
                            "rerun": "familiar","blank": "unfamiliar","judge": "familiar","filth": "unfamiliar","poker": "familiar","proof": "unfamiliar"
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













