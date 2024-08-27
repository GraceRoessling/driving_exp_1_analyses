# Mean Lane Deviation ------------------------------------------------------------------------------
mean_ld_columns <- grepl("mean_total_lane_dev|condition", colnames(main_df))
mean_ld_filtered_df <- main_df[, mean_ld_columns]

long_data <- mean_ld_filtered_df %>%
  pivot_longer(cols = starts_with("mean_total_lane_dev_"),
               names_to = "column_name",
               values_to = "value")

mean_values <- long_data %>%
  group_by(condition, column_name) %>%
  summarise(
    mean_value = mean(value, na.rm = TRUE),
    se = sd(value, na.rm = TRUE) / sqrt(n())
  ) %>%
  ungroup()

# Modify condition labels
mean_values$condition <- factor(mean_values$condition,
                                levels = c("familiar", "unfamiliar"),
                                labels = c("Constant Track", "Variable Track"))


within_mean_ld_plot <- ggplot(mean_values, aes(x = column_name, y = mean_value, color = condition, group = condition)) +
  geom_point(position=pd_for_within,size = geom_point_size) +
  geom_line(position=pd_for_within, size = line_size) +
  geom_errorbar(aes(ymin = mean_value - se, ymax = mean_value + se), width = 0.2,position=pd_for_within) +
  labs(x = "Trials", y = "Mean Lane Dev (meters)", color = "Track Constancy") +
  scale_x_discrete(labels = 1:10) +
  larger_text_theme(base_size = 12) +
  coord_fixed(ratio = 2)+
  theme(legend.position = "none")



# Standard Deviation of Lane Deviation -----------------------------------------------------------------
sd_ld_columns <- grepl("sd_total_lane_dev|condition", colnames(main_df))
sd_ld_filtered_df <- main_df[, sd_ld_columns]

long_data <- sd_ld_filtered_df %>%
  pivot_longer(cols = starts_with("sd_total_lane_dev_"),
               names_to = "column_name",
               values_to = "value")

mean_values <- long_data %>%
  group_by(condition, column_name) %>%
  summarise(
    mean_value = mean(value, na.rm = TRUE),
    se = sd(value, na.rm = TRUE) / sqrt(n())
  ) %>%
  ungroup()

# Modify condition labels
mean_values$condition <- factor(mean_values$condition,
                                levels = c("familiar", "unfamiliar"),
                                labels = c("Constant Track", "Variable Track"))


within_sd_ld_plot <- ggplot(mean_values, aes(x = column_name, y = mean_value, color = condition, group = condition)) +
  geom_point(position=pd_for_within,size = geom_point_size) +
  geom_line(position=pd_for_within, size = line_size) +
  geom_errorbar(aes(ymin = mean_value - se, ymax = mean_value + se), width = 0.2,position=pd_for_within) +
  labs(x = "Trials", y = "SD of Lane Deviation (meters)", color = "Track Constancy") +
  scale_x_discrete(labels = 1:10) +
  larger_text_theme(base_size = 12) +
  coord_fixed(ratio = 3.6)+
  theme(legend.position = "none")


within_sd_ld_plot

#within_mean_ld_plot / within_sd_ld_plot
(within_mean_ld_plot | within_sd_ld_plot) + 
  plot_layout(heights = c(1, 1)) +
  plot_annotation(tag_levels = 'A')

