## OSF Parent Folder Guide (Experiments 1 and 2)

This parent OSF folder contains two experiment directories with parallel structures and experiment-specific data, scripts, and project files.

### Global Structure

- Experiment_1/
	- data/
	- R_scripts/
	- osf_experiment_1.Rproj
	- README.md
- Experiment_2/
	- data/
	- R_scripts/
	- osf_experiment_2.Rproj
	- README.md

### What Each Experiment Folder Includes

- data/: CSV files required to run analyses for that experiment.
- R_scripts/: Analysis scripts (including post-test and ANCOVA analyses).
- osf_experiment_X.Rproj: RStudio project file for the experiment.
- README_X.md: Experiment-specific reproduction instructions, package requirements, and recommended script execution order.

### How To Use This Parent Folder

1. Choose the experiment folder you want to reproduce.
2. Open its corresponding .Rproj file in RStudio.
3. Follow the steps in that experiment's README file.

### Notes

- Experiment_1 and Experiment_2 are independent analysis pipelines.
- Install required R packages as listed in each experiment README before running scripts.
