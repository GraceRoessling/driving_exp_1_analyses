library(dplyr)
library(ggplot2)
library(tidyr)
library(tidyverse)
library(ggpubr)
library(rstatix)

csv_path = "C:\\Users\\graci\\Dropbox\\PAndA\\Thesis Experiment 1\\data\\main_data\\true_master_variable_df.csv"
main_df = read.csv(csv_path,stringsAsFactors=TRUE)

# Mean speed comparison
cols_to_keep <- grepl("mean_total_speed|condition", colnames(main_df))
fam_filtered_df <- main_df[, cols_to_keep]

long_data <- fam_filtered_df %>%
  pivot_longer(cols = starts_with("mean_total_speed_"),
               names_to = "column_name",
               values_to = "value")

mean_values <- long_data %>%
  group_by(condition, column_name) %>%
  summarise(mean_value = mean(value, na.rm = TRUE))

ggplot(mean_values, aes(x = column_name, y = mean_value, color = condition, group = condition)) +
  geom_line() +
  labs(x = "Trials 1-10", y = "Mean Speed",title = "Mean speed between trials 1 - 10") +
  theme_bw() +
  scale_x_discrete(labels = 1:10)



# Speed variance comparison
cols_to_keep <- grepl("var_total_speed|condition", colnames(main_df))
fam_filtered_df <- main_df[, cols_to_keep]

long_data <- fam_filtered_df %>%
  pivot_longer(cols = starts_with("var_total_speed_"),
               names_to = "column_name",
               values_to = "value")

var_values <- long_data %>%
  group_by(condition, column_name) %>%
  summarise(mean_value = mean(value, na.rm = TRUE))

ggplot(var_values, aes(x = column_name, y = mean_value, color = condition, group = condition)) +
  geom_line() +
  labs(x = "Trials 1-10", y = "Speed variance",title = "Speed variance between trials 1 - 10") +
  theme_bw() +
  scale_x_discrete(labels = 1:10)



# Steering variance comparison
cols_to_keep <- grepl("var_total_steering|condition", colnames(main_df))
fam_filtered_df <- main_df[, cols_to_keep]

long_data <- fam_filtered_df %>%
  pivot_longer(cols = starts_with("var_total_steering_"),
               names_to = "column_name",
               values_to = "value")

var_values <- long_data %>%
  group_by(condition, column_name) %>%
  summarise(mean_value = mean(value, na.rm = TRUE))

ggplot(var_values, aes(x = column_name, y = mean_value, color = condition, group = condition)) +
  geom_line() +
  labs(x = "Trials 1-10", y = "Steering variance",title = "Steering variance between trials 1 - 10") +
  theme_bw() +
  scale_x_discrete(labels = 1:10)
