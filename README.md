To use my pipeline, go to : 
experiment_analyses/jupyter_notebooks/Get_subject_data.ipynb

There are instructions on that Jupyter Notebook about how to extract the following information:
Note: the first code block will spam a bunch of warnings. Just ignore those...

For a given subject and trial (e.g. "boss" in trial "4"):
  > What is the map number associated to this trial? (if the subject is not in the familiar group, then the map number is not 1 unless its the last trial)?

  > What is the file path to the CSV file of this particular subject and trial?

  > What are the track pieces within the map for this subject and trial?

  > For a given track piece, was it in the high or low visibility condition? This is useful to know, as you may not want to train on data where subjects drove in foggy conditions.

  > What are the x and z coordinates of the center of the track for that track piece?

  > What are the x and z coordinates of the subject for that given track piece?

