
# Mean speed --------------------------------------------------------
mean_speed_columns <- grepl("mean_total_speed|condition", colnames(main_df))
mean_speed_filtered_df <- main_df[, mean_speed_columns]

long_data <- mean_speed_filtered_df %>%
  pivot_longer(cols = starts_with("mean_total_speed_"),
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

within_mean_speed_plot <- ggplot(mean_values, aes(x = column_name, y = mean_value, color = condition, group = condition)) +
  geom_point(position=pd_for_within,size = geom_point_size) +
  geom_line(position=pd_for_within,size = line_size) +
  geom_errorbar(aes(ymin = mean_value - se, ymax = mean_value + se), width = 0.2,position=pd_for_within) +
  labs(x = "Trials", y = "Mean Speed (m/s)", color = "Track Constancy") +
  scale_x_discrete(labels = 1:10) +
  coord_fixed(ratio = 0.6)+
  larger_text_theme(base_size = 12) +
  theme(legend.position = "none")+
  theme(plot.margin = unit(c(0.15, 0.15, 0.15, 0.15), 
                           "inches")) 


within_mean_speed_plot


# SD of Speed ------------------------------------------------------------------------------------
cols_to_keep <- grepl("sd_total_speed|condition", colnames(main_df))
fam_filtered_df <- main_df[, cols_to_keep]

pd_for_within <- position_dodge(width = 0.3)

long_data <- fam_filtered_df %>%
  pivot_longer(cols = starts_with("sd_total_speed_"),
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

within_sd_speed_plot <- ggplot(mean_values, aes(x = column_name, y = mean_value, color = condition, group = condition)) +
  geom_point(position=pd_for_within,size = geom_point_size) +
  geom_line(position=pd_for_within, size=line_size) +
  geom_errorbar(aes(ymin = mean_value - se, ymax = mean_value + se), width = 0.2,position=pd_for_within) +
  labs(x = "Trials", y = "SD of Speed (m/s)", color = "Track Constancy") +
  scale_x_discrete(labels = 1:10) +
  coord_fixed(ratio = 2)+
  larger_text_theme(base_size = 12) +
  theme(legend.position = "none")

#within_mean_speed_plot / within_sd_speed_plot

(within_mean_speed_plot | within_sd_speed_plot) + 
  plot_layout(heights = c(1, 1)) +
  plot_annotation(tag_levels = 'A')


































