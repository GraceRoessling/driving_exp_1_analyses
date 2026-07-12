library(ggplot2)
library(dplyr)
library(tidyr)

# Set working directory to osf_experiment_1 folder
setwd(dirname(rstudioapi::getActiveDocumentContext()$path) %>% dirname())

# Load shared data/functions (main_df, apa_regression, apa_spearman)
source("./R_scripts/shared_variables_file.R")

log_dtw_path = "./data/log_dtw_data_exp1.csv"
log_dtw_data <- read.csv(log_dtw_path, stringsAsFactors = TRUE)

# Load spatial knowledge and drawing scores data
csv_path_2 = "./data/drawing_scores_exp1.csv"
spatial_data <- read.csv(csv_path_2, stringsAsFactors = TRUE)

# Create the long format dataset like in ANCOVA (this ensures same data source)
mean_steering_dev_df_2 <- main_df %>%
  select(subject_id, condition, total_steering_acceleration_1, low_vis_steering_acceleration_10, high_vis_steering_acceleration_10) %>%
  pivot_longer(
    cols = c(low_vis_steering_acceleration_10, high_vis_steering_acceleration_10),
    names_to = "visibility",
    values_to = "mean_steering_acceleration"
  )

# Extract only low visibility data
data <- mean_steering_dev_df_2 %>%
  filter(visibility == "low_vis_steering_acceleration_10") %>%
  rename(low_vis_steering_acceleration_10 = mean_steering_acceleration)

# Add lane deviation data from main_df
data <- data %>%
  left_join(
    main_df %>% select(subject_id, low_vis_var_lane_dev_10),
    by = "subject_id"
  )


# Merge with spatial knowledge data
data <- data %>%
  left_join(
    spatial_data %>% select(subject_id, Normalized.Score, Score, Score.Std),
    by = "subject_id"
  ) %>%
  left_join(
    log_dtw_data %>% select(subject_id, condition, mean_log_DTW),
    by = c("subject_id", "condition")
  )

# --------------------------------------------------------------------------------------------

analysis_theme <- theme(
  legend.position = "none",
  plot.title = element_text(size = 20),
  axis.title.x = element_text(size = 20),
  axis.title.y = element_text(size = 20),
  axis.text.x = element_text(size = 15),
  axis.text.y = element_text(size = 15)
)

plot_correlation <- function(df, x_var, y_var, x_label, y_label) {
  ggplot(df, aes(x = .data[[x_var]], y = .data[[y_var]], color = condition)) +
    geom_point(size = 2) +
    geom_smooth(method = "lm", color = "red", se = TRUE) +
    scale_color_manual(
      name = "Condition",
      values = c(
        "familiar" = "blue",
        "unfamiliar" = "red"
      ),
      labels = c(
        "familiar" = "Constant Track",
        "unfamiliar" = "Variable Track"
      )
    ) +
    labs(x = x_label, y = y_label) +
    analysis_theme
}

# DTW_score and Variability in Lane Pos. ==========================================================================
apa_spearman(data,x = "mean_log_DTW",y = "low_vis_var_lane_dev_10")
# 4. Plot the data and line of best fit
plot <- plot_correlation(
  data,
  x_var = "mean_log_DTW",
  y_var = "low_vis_var_lane_dev_10",
  x_label = "Mean Log DTW Score",
  y_label = "SD of Lane Dev. in Low Vis. (meters)"
)


# Show plot
print(plot)

# DTW score and Steering Acc. ==========================================================================
apa_spearman(data,x = "mean_log_DTW",y = "low_vis_steering_acceleration_10")
# 4. Plot the data and line of best fit
plot <- plot_correlation(
  data,
  x_var = "mean_log_DTW",
  y_var = "low_vis_steering_acceleration_10",
  x_label = "Mean Log DTW Score",
  y_label = "Mean Steering Acc. in Low Vis. ( deg / "~s^2~")"
)

# Show plot
print(plot)


# Drawing score and Variability in Lane Pos. ==========================================================================
apa_spearman(data,x = "Score",y = "low_vis_var_lane_dev_10")


# 4. Plot the data and line of best fit
plot <- plot_correlation(
  data,
  x_var = "Score",
  y_var = "low_vis_var_lane_dev_10",
  x_label = "Drawing Score",
  y_label = "SD of Lane Dev. in Low Vis. (meters)"
)

# Show plot
print(plot)

# Drawing score and Steering Acc. ==========================================================================
apa_spearman(data,x = "Score",y = "low_vis_steering_acceleration_10")
# 4. Plot the data and line of best fit
plot <- plot_correlation(
  data,
  x_var = "Score",
  y_var = "low_vis_steering_acceleration_10",
  x_label = "Drawing Score",
  y_label = bquote("Mean Steering Acc. in Low Vis. ( deg / "~s^2~")")
)

# Show plot
print(plot)