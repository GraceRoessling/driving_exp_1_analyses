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
    
    completion_seq_with_ans_nested_dict = { 
                                         "grip": {"order":1, "condition":"familiar", "drawing_id":"FvIH", "map_selection": "incorrect"},   "swarm": {"order":2, "condition":"unfamiliar", "drawing_id":"B3Fs", "map_selection":"incorrect"},   
                                         "five": {"order":3, "condition":"familiar", "drawing_id":"7p9e", "map_selection":"correct"},        "wok": {"order":4, "condition":"unfamiliar", "drawing_id":"Zq2a", "map_selection":"incorrect"},  
                                         "mule": {"order":5, "condition":"familiar", "drawing_id":"RRXX", "map_selection":"correct"},       "grid": {"order":6, "condition":"unfamiliar", "drawing_id":"9lgL", "map_selection":"correct"},
                                        "polio": {"order":7, "condition":"familiar", "drawing_id":"LfvQ", "map_selection":"correct"},       "atom": {"order":8, "condition":"unfamiliar", "drawing_id":"bd7i", "map_selection":"correct"},     
                                         "bash": {"order":9, "condition":"familiar", "drawing_id":"rT6Y", "map_selection":"incorrect"},    "slimy": {"order":10,"condition":"unfamiliar", "drawing_id":"QMXt", "map_selection":"correct"},  
                                        "slept": {"order":11,"condition":"familiar", "drawing_id":"W77r", "map_selection":"incorrect"},    "clerk": {"order":12,"condition":"unfamiliar", "drawing_id":"1jel", "map_selection":"correct"},
                                        "boned": {"order":13,"condition":"familiar", "drawing_id":"VKnw", "map_selection":"incorrect"},     "debt": {"order":14,"condition":"unfamiliar", "drawing_id":"Hqop", "map_selection":"correct"},  
                                        "yeast": {"order":15,"condition":"familiar", "drawing_id":"C1ca", "map_selection":"correct"},       "most": {"order":16,"condition":"unfamiliar", "drawing_id":"JwpD", "map_selection":"incorrect"},
                                        "cargo": {"order":17,"condition":"familiar", "drawing_id":"yrkT", "map_selection": "correct"},      "brim": {"order":18,"condition":"unfamiliar", "drawing_id": None,  "map_selection":None},
                                        "trial": {"order":19,"condition":"familiar", "drawing_id":"0X07", "map_selection":"correct"},       "lens": {"order":20,"condition":"unfamiliar", "drawing_id":"Id11", "map_selection":"incorrect"},
                                        "baggy": {"order":21,"condition":"familiar", "drawing_id":"jFlG", "map_selection":"correct"},       "chef": {"order":22,"condition":"unfamiliar", "drawing_id":"BBPd", "map_selection":"incorrect"},
                                        "slate": {"order":23,"condition":"familiar", "drawing_id":"RZUy", "map_selection":"correct"},       "limb": {"order":24,"condition":"unfamiliar", "drawing_id":"2UGt", "map_selection":"incorrect"},
                                        "rerun": {"order":25,"condition":"familiar", "drawing_id":"4ZPw", "map_selection":"correct"},      "blank": {"order":26,"condition":"unfamiliar", "drawing_id":"5E4C", "map_selection":"correct"},  
                                        "judge": {"order":27,"condition":"familiar", "drawing_id":"sSwD", "map_selection":"correct"},     "filth": {"order":28, "condition":"unfamiliar", "drawing_id":"qRmw", "map_selection":"incorrect"},
                                        "poker": {"order":29,"condition":"familiar", "drawing_id":"YdkM", "map_selection":"incorrect"},   "proof": {"order":30, "condition":"unfamiliar", "drawing_id":"zV13", "map_selection":"incorrect"}
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













