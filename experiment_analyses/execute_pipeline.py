import preprocess
import warnings
SUBJECT_PATH = "C:/Users/graci/Dropbox/PAndA/Thesis Experiment 3/data/main_data"
warnings.filterwarnings("ignore")

subject_dict = preprocess.run(SUBJECT_PATH)
#subject_dict,master_dict,non_interp_dict = preprocess.run(SUBJECT_PATH)
# subject_dict,master_dict,non_interp_dict = preprocess.run_one_subject(SUBJECT_PATH)

