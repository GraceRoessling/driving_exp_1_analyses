# Within Mean Lane Deviation ------------------------------------------------------------------------------
total_mean_ld_columns <- grepl("avg_mean_lane_dev|condition", colnames(main_df))
total_mean_ld_filtered_df <- main_df[, total_mean_ld_columns]

long_data <- total_mean_ld_filtered_df %>%
  pivot_longer(cols = starts_with("avg_mean_lane_dev_"),
               names_to = "column_name",
               values_to = "value")

mean_values <- long_data %>%
  group_by(condition, column_name) %>%
  summarise(
    ci = list(calculate_CI(cur_data(), "value")),
    .groups = "drop"
  ) %>%
  unnest_wider(ci)


mean_values <- mean_values %>%
  mutate(column_name = str_extract(column_name, "\\d+$"))
mean_values <- reorder_mean_values(mean_values)

mean_values <- mean_values %>%
  mutate(column_name = factor(as.numeric(column_name), levels = 1:10))

# Modify condition labels
mean_values$condition <- factor(mean_values$condition,
                                levels = c("familiar", "unfamiliar"),
                                labels = c("Constant Track", "Variable Track"))


within_mean_ld_plot <- ggplot(mean_values, aes(x = column_name, y = mean, color = condition, group = condition)) +
  geom_point(position = pd_for_within, size = 5) +
  geom_line(position=pd_for_within, size = line_size) +
  geom_errorbar(aes(ymin = ci_lower, ymax = ci_upper), width = 0.2,position=pd_for_within) +
  labs(x = "Trials", y = "Mean Lane Deviation (meters)", color = "Track Constancy", title = "Mean Lane Deviation Across Trials") +
  scale_x_discrete(labels = 1:10) +
  scale_color_manual(values = c("Constant Track" = "#0000FF", "Variable Track" = "#FF4040")) +  # Replace with actual condition levels
  larger_text_theme(base_size = 12) +
  theme(
    legend.position = "none",
    plot.title = element_text(size = 20),
    axis.title.x = element_text(size = 40),
    axis.title.y = element_text(size = 20),
    axis.text.x = element_text(size = 30),
    axis.text.y = element_text(size = 30)
  )

within_mean_ld_plot


# Within Standard Deviation of Lane Deviation -----------------------------------------------------------------
sd_ld_columns <- grepl("avg_sd_lane_dev_|condition", colnames(main_df))
sd_ld_filtered_df <- main_df[, sd_ld_columns]

long_data <- sd_ld_filtered_df %>%
  pivot_longer(cols = starts_with("avg_sd_lane_dev_"),
               names_to = "column_name",
               values_to = "value")

mean_values <- long_data %>%
  group_by(condition, column_name) %>%
  summarise(
    ci = list(calculate_CI(cur_data(), "value")),
    .groups = "drop"
  ) %>%
  unnest_wider(ci)

# Modify condition labels
mean_values$condition <- factor(mean_values$condition,
                                levels = c("familiar", "unfamiliar"),
                                labels = c("Constant Track", "Variable Track"))


within_sd_ld_plot <- ggplot(mean_values, aes(x = column_name, y = mean, color = condition, group = condition)) +
  geom_point(position = pd_for_within, size = 5) +
  geom_line(position = pd_for_within, size = line_size) +
  geom_errorbar(aes(ymin = ci_lower, ymax = ci_upper), width = 0.2, position = pd_for_within) +
  labs(x = "Trials", y = "SD of Lane Deviation (meters)", color = "Track Constancy", title = "SD of Lane Deviation Across Trials") +
  scale_x_discrete(labels = 1:10) +
  scale_color_manual(values = c("Constant Track" = "#0000FF", "Variable Track" = "#FF4040")) +  # Replace with actual condition levels
  larger_text_theme(base_size = 12) +
  theme(
    legend.position = "none",
    plot.title = element_text(size = 20),
    axis.title.x = element_text(size = 40),
    axis.title.y = element_text(size = 20),
    axis.text.x = element_text(size = 30),
    axis.text.y = element_text(size = 30)
  )



within_sd_ld_plot

#within_mean_ld_plot / within_sd_ld_plot
(within_mean_ld_plot | within_sd_ld_plot) + 
  plot_layout(heights = c(1, 1)) 

