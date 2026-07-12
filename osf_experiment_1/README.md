# OSF Experiment 1 Analysis Reproduction Guide

This folder contains the data and R scripts needed to reproduce the main analyses for Experiment 1.

## Folder Structure

- `data/`: input CSV files used by the analyses.
- `R_scripts/`: R scripts and one R Markdown analysis file.
- `osf_experiment_1.Rproj`: RStudio project file.

## Requirements

- R (recommended: R 4.2+)
- RStudio (recommended, because some scripts use `rstudioapi` to set working directories)

## 1. Open the Project

1. Download and extract this OSF folder.
2. Open `osf_experiment_1.Rproj` in RStudio.

All scripts assume this folder as the project root.

## 2. Install Required R Packages

Run this once in the R console:

```r
pkgs <- c(
  "dplyr", "ggplot2", "tidyr", "tidyverse", "ggpubr", "rstatix",
  "gridExtra", "patchwork", "effectsize", "afex", "emmeans", "broom",
  "DescTools", "psych", "qqplotr", "pastecs", "scales", "ez",
  "Hmisc", "lme4", "lmerTest", "knitr", "rstudioapi"
)

to_install <- pkgs[!pkgs %in% rownames(installed.packages())]
if (length(to_install) > 0) install.packages(to_install)
```

## 3. Run the Analyses

Recommended order:

1. Run post-test analyses together:
    - `R_scripts/Post_test_1_analysis.Rmd`
    - `R_scripts/Post_test_2_analysis.R`
    - Required data files:
        - `data/dtw_data_exp1.csv` (Post-test 1)
        - `data/drawing_scores_exp1.csv` (Post-test 2)

2. Run ANCOVA scripts (each can be run independently after packages are installed):
    - `R_scripts/ancova_mean_speed.R`
    - `R_scripts/ancova_sd_speed.R`
    - `R_scripts/ancova_sd_lane_dev.R`
    - `R_scripts/ancova_steering_acceleration.R`
    - Required data files (shared across all ANCOVA scripts):
        - `data/main_steering_analysis_data.csv`
    - Note: all ANCOVA scripts source `R_scripts/shared_variables_file.R`, which loads and post-processes a single shared dataframe (`main_df`) before model-specific analyses.

3. Run correlation analyses:
    - `R_scripts/Post_tests_and_steering_corr.R`
    - Required data files:
        - `data/main_steering_analysis_data.csv` (via `R_scripts/shared_variables_file.R`)
        - `data/log_dtw_data_exp1.csv`
        - `data/drawing_scores_exp1.csv`