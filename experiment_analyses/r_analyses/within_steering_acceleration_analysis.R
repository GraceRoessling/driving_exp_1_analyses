# Within Mean Lane Deviation ------------------------------------------------------------------------------
total_steering_acceleration_columns <- grepl("avg_steering_acceleration|condition", colnames(main_df))
total_steering_acceleration_filtered_df <- main_df[, total_steering_acceleration_columns]

long_data <- total_steering_acceleration_filtered_df %>%
  pivot_longer(cols = starts_with("avg_steering_acceleration_"),
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


within_steering_acceleration_plot <- ggplot(mean_values, aes(x = column_name, y = mean, color = condition, group = condition)) +
  geom_point(position=pd_for_within,size = geom_point_size) +
  geom_line(position=pd_for_within, size = line_size) +
  geom_errorbar(aes(ymin = ci_lower, ymax = ci_upper), width = 0.2,position=pd_for_within) +
  labs(x = "Trials", y = bquote("Mean Abs. Steering\nAcceleration ( deg/"~s^2~")"), color = "Track Constancy") +
  scale_x_discrete(labels = 1:10) +
  larger_text_theme(base_size = 12)+
  coord_fixed(ratio = 0.4)+
  theme(legend.position = "none")

within_steering_acceleration_plot