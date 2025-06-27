
# Mean speed --------------------------------------------------------
mean_speed_columns <- grepl("avg_mean_speed|condition", colnames(main_df))
mean_speed_filtered_df <- main_df[, mean_speed_columns]

long_data <- mean_speed_filtered_df %>%
  pivot_longer(cols = starts_with("avg_mean_speed"),
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
                                levels = c("control", "scrambled_segments", "scrambled_landmarks"),
                                labels = c("Control Group", "SS Group", "SL Group"))

within_mean_speed_plot <- ggplot(mean_values, aes(x = column_name, y = mean, color = condition, group = condition)) +
  geom_point(position=pd_for_within,size = 5) +
  geom_line(position=pd_for_within,size = line_size) +
  geom_errorbar(aes(ymin = ci_lower, ymax = ci_upper), width = 0.2,position=pd_for_within) +
  labs(x = "Trials", y = "Mean Speed (m/s)", color = "Track Constancy", title = "Mean Speed Across Trials") +
  scale_x_discrete(labels = 1:10) +
  scale_color_manual(values = c("Control Group" = "#0000FF",
                                "SL Group" = "#FF4040",
                                "SS Group" = "#00CD00")) +
  larger_text_theme(base_size = 12) +
  theme(
    legend.position = "none",
    plot.title = element_text(size = 20),
    axis.title.x = element_text(size = 20),
    axis.title.y = element_text(size = 20),
    axis.text.x = element_text(size = 20),
    axis.text.y = element_text(size = 20)
  )

within_mean_speed_plot


# SD of Speed ------------------------------------------------------------------------------------
sd_speed_columns <- grepl("avg_sd_speed|condition", colnames(main_df))
sd_speed_df <- main_df[, sd_speed_columns]

long_data <- sd_speed_df %>%
  pivot_longer(cols = starts_with("avg_sd_speed"),
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
                                levels = c("control", "scrambled_segments", "scrambled_landmarks"),
                                labels = c("Control Group", "SS Group", "SL Group"))

within_sd_speed_plot <- ggplot(mean_values, aes(x = column_name, y = mean, color = condition, group = condition)) +
  geom_point(position=pd_for_within,size = 5) +
  geom_line(position=pd_for_within, size=line_size) +
  geom_errorbar(aes(ymin = ci_lower, ymax = ci_upper), width = 0.2,position=pd_for_within) +
  labs(x = "Trials", y = "SD of Speed ", color = "Track Constancy") +
  scale_x_discrete(labels = 1:10) +  
  scale_color_manual(values = c("Control Group" = "#0000FF","SL Group" = "#FF4040","SS Group" = "#00CD00")) +
  larger_text_theme(base_size = 12) +
  theme(
    legend.position = "none",
    plot.title = element_text(size = 20),
    axis.title.x = element_text(size = 20),
    axis.title.y = element_text(size = 20),
    axis.text.x = element_text(size = 20),
    axis.text.y = element_text(size = 20)
  )

within_mean_speed_plot #/ within_sd_speed_plot

#(within_mean_speed_plot | within_sd_speed_plot) + 
#  plot_layout(heights = c(1, 1)) +
#  plot_annotation(tag_levels = 'A')

