library(dplyr)
library(ggplot2)
library(tidyr)
library(tidyverse)
library(ggpubr)
library(rstatix)
library(gridExtra)
library(patchwork)
library(effectsize)

# To compare between both visibility conditions without straight pieces
csv_path = "C:\\Users\\graci\\Dropbox\\PAndA\\Thesis Experiment 1\\data\\main_data\\main_analysis_df6.csv"

# To compare between left and right turn short pieces
# csv_path = "C:\\Users\\graci\\Dropbox\\PAndA\\Thesis Experiment 1\\data\\main_data\\short_turn_piece_variable_df.csv"


main_df = read.csv(csv_path,stringsAsFactors=TRUE)

# Hepler functions --------------------------------------------
convert_var_to_sd <- function(df) {
  df %>%
    mutate(across(contains("var"), 
                  ~ sqrt(.),
                  .names = "{str_replace(.col, 'var', 'sd')}"))
}

# Function to create a larger text theme
larger_text_theme <- function(base_size = 14) {
  theme(base_size = base_size) +
    theme(
      axis.title = element_text(size = rel(2)),
      axis.text = element_text(size = rel(2)),
      plot.title = element_text(size = rel(2.5), face = "bold"),
      legend.title = element_text(size = rel(2.1)),
      legend.text = element_text(size = rel(2))
    )
}


process_performance_metrics <- function(main_df, performance_metric) {
  # Step 1: Filter main_df for columns containing performance_metric
  performance_cols <- grep(performance_metric, names(main_df), value = TRUE)
  filtered_main_df <- main_df[, performance_cols]
  
  # Loop through trials 1 to 10
  for (i in 1:10) {
    # Convert iteration to string
    trial_number <- as.character(i)
    
    # Filter for columns containing trial_number
    trial_cols <- grep(trial_number, names(filtered_main_df), value = TRUE)
    temp_df <- filtered_main_df[, trial_cols]
    
    # Calculate row-wise average
    avg_values <- rowMeans(temp_df, na.rm = TRUE)
    
    # Add new column to main_df
    main_df[[paste0("avg_", performance_metric, "_", trial_number)]] <- avg_values
  }
  return(main_df)
}

number_ticks <- function(n) {function(limits) pretty(limits, n)}


reorder_mean_values <- function(mean_values) {
  library(dplyr)
  
  mean_values_ordered <- mean_values %>%
    # Convert column_name to numeric
    mutate(column_name_num = as.numeric(column_name)) %>%
    # Arrange first by condition, then by the numeric column_name
    arrange(condition, column_name_num) %>%
    # Remove the temporary numeric column
    select(-column_name_num)
  
  return(mean_values_ordered)
}

calculate_CI <- function(data, column_name, confidence_level = 0.95) {
  # Extract the column data
  column_data <- data[[column_name]]
  
  # Calculate the mean
  mean_value <- mean(column_data, na.rm = TRUE)
  
  # Calculate the standard error
  se <- sd(column_data, na.rm = TRUE) / sqrt(length(column_data))
  
  # Calculate the margin of error
  degrees_of_freedom <- length(column_data) - 1
  t_score <- qt((1 + confidence_level) / 2, df = degrees_of_freedom)
  margin_of_error <- t_score * se
  
  # Calculate the confidence interval
  ci_lower <- mean_value - margin_of_error
  ci_upper <- mean_value + margin_of_error
  
  # Return the results as a list
  return(list(
    mean = mean_value,
    ci_lower = ci_lower,
    ci_upper = ci_upper
  ))
}

# Define one dataframe for all files ----------------------------
subject_id = main_df[["subject_id"]]
familiarity = main_df[["condition"]]
main_df <- convert_var_to_sd(main_df)
main_df <- main_df %>% select(-contains('total')) # if "total" is in the row, take it out


# Main analysis : Separate into familiar and unfamiliar groups -----------------
familiar_df <- main_df %>% filter(!grepl('unfamiliar', condition)) # if "unfamiliar" is in the row, take it out
unfamiliar_df <- main_df %>% filter(grepl('unfamiliar', condition)) # if "unfamiliar" is in the row, put it in
sd_df <- main_df[ , grepl( "sd" , names( main_df ) ) ]
mean_df <- main_df[ , grepl( "mean" , names( main_df ) ) ]


# Within analysis : Dataframes for each analysis  -----------------
# average across low and high visibility  conditions for each metric

# speed analysis -----------------------------------------------
main_df = process_performance_metrics(main_df,"mean_speed")# Mean speed
main_df = process_performance_metrics(main_df,"sd_speed")# SD of Speed

# steering analysis --------------------------------------------
main_df = process_performance_metrics(main_df,"sd_steering")# SD of Steering Angle

# lane deviation analysis --------------------------------------
main_df = process_performance_metrics(main_df,"mean_lane_dev") # Mean lane deviation
main_df = process_performance_metrics(main_df,"sd_lane_dev") # SD of lane deviation

# steering acceleration analysis --------------------------------------
main_df = process_performance_metrics(main_df,"steering_acceleration") # steering acceleration

# -----------------------------------------------------------------------------------------------------------------
# Shared plotting vars
pd_for_main <- position_dodge(width = 0.1)
pd_for_within <- position_dodge(width = 0.3)
geom_point_size = 3
line_size = 1


print(colnames(main_df))
