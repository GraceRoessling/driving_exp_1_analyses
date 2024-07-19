import preprocess
import warnings
SUBJECT_PATH = "C:/Users/graci/Dropbox/PAndA/Thesis Experiment 1/data/main_data"
TRACK_CENTER_PATH = "C:/Users/graci/Dropbox/PAndA/Thesis Experiment 1/data/track_piece_center"
LANE_DEVIATION_PATH = "C:/Users/graci/Dropbox/PAndA/Thesis Experiment 1/data/lane_deviation_data"

warnings.filterwarnings("ignore")
subject_dict,master_dict,non_interp_dict = preprocess.run(SUBJECT_PATH, TRACK_CENTER_PATH, LANE_DEVIATION_PATH)

