library(dplyr)
library(ggplot2)
library(tidyr)
library(tidyverse)
library(ggpubr)
library(rstatix)

#csv_path = "C:\\Users\\graci\\Dropbox\\PAndA\\Thesis Experiment 1\\data\\main_data\\true_master_variable_df.csv"
csv_path = "C:\\Users\\graci\\Dropbox\\PAndA\\Thesis Experiment 1\\data\\main_data\\ultimate_master_variable_df.csv"

main_df = read.csv(csv_path,stringsAsFactors=TRUE)

# For all files
subject_id = main_df[["subject_id"]]
familiarity = main_df[["condition"]]
familiar_df <- main_df %>% filter(!grepl('unfamiliar', condition)) # if "unfamiliar" is in the row, take it out
unfamiliar_df <- main_df %>% filter(grepl('unfamiliar', condition)) # if "unfamiliar" is in the row, put it in

# Mean Speed Analysis ==============================================================================================================================
# Familiar Group -----------------------------------------------------------------------

fam_cols_to_keep <- grepl("mean_total_speed", colnames(familiar_df))
fam_filtered_df <- familiar_df[, fam_cols_to_keep]
num_rows <- nrow(fam_filtered_df)
num_cols <- ncol(fam_filtered_df)

# Create an empty plot
plot(1:num_cols, type = "n", xlab = "Column Number", ylab = "Value", 
     main = "Within-Subjects Analysis of Mean Speed Across Ten Trials (Familiar Group)", 
     xlim = c(1, num_cols), ylim = range(fam_filtered_df))

# Add lines for each subject with increased line width
for (row_idx in 1:num_rows) {
  subject_data <- fam_filtered_df[row_idx, ]
  lines(1:num_cols, subject_data, col = row_idx, lty = 1, lwd = 2)  # Increased line width to 2
}

# Add legend with increased line width
legend("bottomleft", legend = paste(familiar_df[["subject_id"]]), 
       col = 1:num_rows, lty = 1, lwd = 2)  # Increased line width in legend to 2

# Unfamiliar Group -----------------------------------------------------------------------
unfam_cols_to_keep <- grepl("mean_total_speed", colnames(unfamiliar_df))
unfam_filtered_df <- unfamiliar_df[, unfam_cols_to_keep]

num_rows <- nrow(unfam_filtered_df)
num_cols <- ncol(unfam_filtered_df)

# Create an empty plot
plot(1:num_cols, type = "n", xlab = "Column Number", ylab = "Value", 
     main = "Within-Subjects Analysis of Mean Speed Across Ten Trials (Unfamiliar Group)", xlim = c(1, num_cols), ylim = range(unfam_filtered_df))

# Add lines for each subject
for (row_idx in 1:num_rows) {
  subject_data <- unfam_filtered_df[row_idx, ]
  lines(1:num_cols, subject_data, col = row_idx, lty = 1,lwd = 2)
}

# Add legend with increased line width
legend("bottomleft", legend = paste(unfamiliar_df[["subject_id"]]), 
       col = 1:num_rows, lty = 1, lwd = 2)  # Increased line width in legend to 2

# Variance Speed Analysis ==============================================================================================================================
# Familiar Group -----------------------------------------------------------------------

fam_cols_to_keep <- grepl("var_total_speed", colnames(familiar_df))
fam_filtered_df <- familiar_df[, fam_cols_to_keep]

num_rows <- nrow(fam_filtered_df)
num_cols <- ncol(fam_filtered_df)

# Create an empty plot
plot(1:num_cols, type = "n", xlab = "Column Number", ylab = "Value", 
     main = "Within-Subjects Analysis of Speed Variance Across Ten Trials (Familiar Group)", xlim = c(1, num_cols), ylim = range(fam_filtered_df))

# Add lines for each subject
for (row_idx in 1:num_rows) {
  subject_data <- fam_filtered_df[row_idx, ]
  lines(1:num_cols, subject_data, col = row_idx, lty = 1)
}

# Add legend
legend("topright", legend = paste("Subject", 1:num_rows), col = 1:num_rows, lty = 1)


# Unfamiliar Group -----------------------------------------------------------------------
unfam_cols_to_keep <- grepl("var_total_speed", colnames(unfamiliar_df))
unfam_filtered_df <- unfamiliar_df[, unfam_cols_to_keep]

num_rows <- nrow(unfam_filtered_df)
num_cols <- ncol(unfam_filtered_df)

# Create an empty plot
plot(1:num_cols, type = "n", xlab = "Column Number", ylab = "Value", 
     main = "Within-Subjects Analysis of Speed Variance Across Ten Trials (Unfamiliar Group)", xlim = c(1, num_cols), ylim = range(unfam_filtered_df))

# Add lines for each subject
for (row_idx in 1:num_rows) {
  subject_data <- unfam_filtered_df[row_idx, ]
  lines(1:num_cols, subject_data, col = row_idx, lty = 1)
}

# Add legend
legend("topright", legend = paste("Subject", 1:num_rows), col = 1:num_rows, lty = 1)

# Variance Steering Analysis ==============================================================================================================================
# Familiar Group -----------------------------------------------------------------------

fam_cols_to_keep <- grepl("var_total_steering", colnames(familiar_df))
fam_filtered_df <- familiar_df[, fam_cols_to_keep]

num_rows <- nrow(fam_filtered_df)
num_cols <- ncol(fam_filtered_df)

# Create an empty plot
plot(1:num_cols, type = "n", xlab = "Column Number", ylab = "Value", 
     main = "Within-Subjects Analysis of Steering Variance Across Ten Trials (Familiar Group)", xlim = c(1, num_cols), ylim = range(fam_filtered_df))

# Add lines for each subject
for (row_idx in 1:num_rows) {
  subject_data <- fam_filtered_df[row_idx, ]
  lines(1:num_cols, subject_data, col = row_idx, lty = 1)
}

# Add legend
legend("topright", legend = paste("Subject", 1:num_rows), col = 1:num_rows, lty = 1)


# Unfamiliar Group -----------------------------------------------------------------------
unfam_cols_to_keep <- grepl("var_total_steering", colnames(unfamiliar_df))
unfam_filtered_df <- unfamiliar_df[, unfam_cols_to_keep]

num_rows <- nrow(unfam_filtered_df)
num_cols <- ncol(unfam_filtered_df)

# Create an empty plot
plot(1:num_cols, type = "n", xlab = "Column Number", ylab = "Value", 
     main = "Within-Subjects Analysis of Steering Variance Across Ten Trials (Unfamiliar Group)", xlim = c(1, num_cols), ylim = range(unfam_filtered_df))

# Add lines for each subject
for (row_idx in 1:num_rows) {
  subject_data <- unfam_filtered_df[row_idx, ]
  lines(1:num_cols, subject_data, col = row_idx, lty = 1)
}

# Add legend
legend("topright", legend = paste("Subject", 1:num_rows), col = 1:num_rows, lty = 1)


# Mean Lane Deviation Analysis ==============================================================================================================================
# Familiar Group -----------------------------------------------------------------------

fam_cols_to_keep <- grepl("mean_total_lane_dev", colnames(familiar_df))
fam_filtered_df <- familiar_df[, fam_cols_to_keep]
num_rows <- nrow(fam_filtered_df)
num_cols <- ncol(fam_filtered_df)

# Create an empty plot
plot(1:num_cols, type = "n", xlab = "Column Number", ylab = "Value", 
     main = "Within-Subjects Analysis of Mean Lane Deviation Across Ten Trials (Familiar Group)", 
     xlim = c(1, num_cols), ylim = range(fam_filtered_df))

# Add lines for each subject with increased line width
for (row_idx in 1:num_rows) {
  subject_data <- fam_filtered_df[row_idx, ]
  lines(1:num_cols, subject_data, col = row_idx, lty = 1, lwd = 2)  # Increased line width to 2
}

# Add legend with increased line width
legend("bottomleft", legend = paste(familiar_df[["subject_id"]]), 
       col = 1:num_rows, lty = 1, lwd = 2)  # Increased line width in legend to 2

# Unfamiliar Group -----------------------------------------------------------------------
unfam_cols_to_keep <- grepl("mean_total_lane_dev", colnames(unfamiliar_df))
unfam_filtered_df <- unfamiliar_df[, unfam_cols_to_keep]

num_rows <- nrow(unfam_filtered_df)
num_cols <- ncol(unfam_filtered_df)

# Create an empty plot
plot(1:num_cols, type = "n", xlab = "Column Number", ylab = "Value", 
     main = "Within-Subjects Analysis of Mean Lane Deviation Across Ten Trials (Unfamiliar Group)", xlim = c(1, num_cols), ylim = range(unfam_filtered_df))

# Add lines for each subject
for (row_idx in 1:num_rows) {
  subject_data <- unfam_filtered_df[row_idx, ]
  lines(1:num_cols, subject_data, col = row_idx, lty = 1,lwd = 2)
}

# Add legend with increased line width
legend("bottomleft", legend = paste(unfamiliar_df[["subject_id"]]), 
       col = 1:num_rows, lty = 1, lwd = 2)  # Increased line width in legend to 2











