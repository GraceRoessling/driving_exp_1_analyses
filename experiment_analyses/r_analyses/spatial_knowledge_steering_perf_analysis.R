library(ggplot2)
library(dplyr)

log_dtw_path = "C:\\Users\\graci\\Dropbox\\PAndA\\Manuscript (Dissertation)\\data\\log_dtw_data_exp1.csv"
log_dtw_data <- read.csv(log_dtw_path, stringsAsFactors = TRUE)

csv_path_1 = "C:\\Users\\graci\\Dropbox\\PAndA\\Manuscript (Dissertation)\\data\\spatial_knowledge_and_steering_perf_scores.csv"
data  = read.csv(csv_path_1,stringsAsFactors=TRUE)

# Load spatial knowledge and drawing scores data
csv_path_2 = "C:\\Users\\graci\\Dropbox\\PAndA\\Manuscript (Dissertation)\\data\\spatial_knowledge_and_steering_perf_scores.csv"
spatial_data <- read.csv(csv_path_2, stringsAsFactors = TRUE)

# Create the long format dataset like in ANCOVA (this ensures same data source)
mean_steering_dev_df_2 <- main_df %>%
  select(subject_id, condition, total_steering_acceleration_1, low_vis_steering_acceleration_10, high_vis_steering_acceleration_10) %>%
  gather(key = "visibility", value = "mean_steering_acceleration", low_vis_steering_acceleration_10, high_vis_steering_acceleration_10)

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
    spatial_data %>% select(subject_id, DTW_score, Normalized_Drawing_Score, Drawing_score, Drawing_Score_Std),
    by = "subject_id"
  ) %>%
  left_join(
    log_dtw_data %>% select(subject_id, condition, mean_log_DTW),
    by = c("subject_id", "condition")
  )

# --------------------------------------------------------------------------------------------

# Drawing score and Variability in Lane Pos. ==========================================================================
apa_regression(data, "low_vis_var_lane_dev_10", "Drawing_score")
apa_spearman(data,x = "Drawing_score",y = "low_vis_var_lane_dev_10")


# 4. Plot the data and line of best fit
plot <- ggplot(data, aes(x = Drawing_score, y = low_vis_var_lane_dev_10, color = condition)) +
  geom_point(size = 2) +   # scatter plot points
  geom_smooth(method = "lm", color = "red", se = TRUE) +  # line of best fit with confidence interval
  labs(
    x = "Drawing Score",
    y = "SD of Lane Dev. in Low Vis. (meters)"
  ) +
  scale_color_manual(
    name = "Condition",
    values = c(
      "familiar"   = "blue",
      "unfamiliar" = "red"
    ),
    labels = c(
      "familiar"   = "Constant Track",
      "unfamiliar" = "Variable Track"
    )
  ) +
  theme(
    legend.position = "none",
    plot.title = element_text(size = 20),
    axis.title.x = element_text(size = 20),
    axis.title.y = element_text(size = 20),
    axis.text.x = element_text(size = 15),
    axis.text.y = element_text(size = 15)
  )

# Show plot
print(plot)

# Drawing score and Steering Acc. ==========================================================================

apa_regression(data, "low_vis_steering_acceleration_10", "Drawing_score")
apa_spearman(data,x = "Drawing_score",y = "low_vis_steering_acceleration_10")
# 4. Plot the data and line of best fit
plot <- ggplot(data, aes(x = Drawing_score, y = low_vis_steering_acceleration_10, color = condition)) +
  geom_point(size = 2) +   # scatter plot points
  geom_smooth(method = "lm", color = "red", se = TRUE) +  # line of best fit with confidence interval
  scale_color_manual(
    values = c(
      "familiar"   = "blue",
      "unfamiliar" = "red"
    )
   ) +
   labs(
    x = "Drawing Score",
    y = bquote("Mean Steering Acc. in Low Vis. ( deg / "~s^2~")")
  ) +
  theme(
    legend.position = "none",
    plot.title = element_text(size = 20),
    axis.title.x = element_text(size = 20),
    axis.title.y = element_text(size = 20),
    axis.text.x = element_text(size = 15),
    axis.text.y = element_text(size = 15)
  )

# Show plot
print(plot)


# DTW_score and Variability in Lane Pos. ==========================================================================
apa_regression(data, "low_vis_var_lane_dev_10", "mean_log_DTW")
apa_spearman(data,x = "mean_log_DTW",y = "low_vis_var_lane_dev_10")
# 4. Plot the data and line of best fit
plot <- ggplot(data, aes(x = mean_log_DTW, y = low_vis_var_lane_dev_10, color = condition)) +
  geom_point(size = 2) +   # scatter plot points
  geom_smooth(method = "lm", color = "red", se = TRUE) +  # line of best fit with confidence interval
  scale_color_manual(
    values = c(
      "familiar"   = "blue",
      "unfamiliar" = "red"
    )
  ) +
  labs(
    x = "Mean Log DTW Score",
    y = "SD of Lane Dev. in Low Vis. (meters)"
  )  +
  theme(
    legend.position = "none",
    plot.title = element_text(size = 20),
    axis.title.x = element_text(size = 20),
    axis.title.y = element_text(size = 20),
    axis.text.x = element_text(size = 15),
    axis.text.y = element_text(size = 15)
  )


# Show plot
print(plot)

# DTW score and Steering Acc. ==========================================================================
apa_regression(data, "low_vis_steering_acceleration_10", "mean_log_DTW")
apa_spearman(data,x = "mean_log_DTW",y = "low_vis_steering_acceleration_10")
# 4. Plot the data and line of best fit
plot <- ggplot(data, aes(x = mean_log_DTW, y = low_vis_steering_acceleration_10, color = condition)) +
  geom_point(size = 2) +   # scatter plot points
  geom_smooth(method = "lm", color = "red", se = TRUE) +  # line of best fit with confidence interval
  scale_color_manual(
    values = c(
      "familiar"   = "blue",
      "unfamiliar" = "red"
    )
  ) +
   labs(
    x = "Mean Log DTW Score",
    y = "Mean Steering Acc. in Low Vis. ( deg / "~s^2~")"
  ) +
  theme(
    legend.position = "none",
    plot.title = element_text(size = 20),
    axis.title.x = element_text(size = 20),
    axis.title.y = element_text(size = 20),
    axis.text.x = element_text(size = 15),
    axis.text.y = element_text(size = 15)
  )

# Show plot
print(plot)