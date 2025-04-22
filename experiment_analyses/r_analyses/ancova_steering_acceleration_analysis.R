# Analysis 9: Mean Steering Acceleration with Lap Time Covariate ----------------------------------------------------------------

main="Mean Steering Acceleration for Repeated vs Varied Track Groups"

# Long format
mean_steering_dev_df_2 <- main_df %>%
  select(subject_id, condition,total_lap_time_1,low_vis_steering_acceleration_10, high_vis_steering_acceleration_10) %>%
  gather(key = "visibility", value = "mean_steering_acceleration", low_vis_steering_acceleration_10, high_vis_steering_acceleration_10)

mean_steering_dev_cov.aov <- anova_test(
  data = mean_steering_dev_df_2, dv = mean_steering_acceleration, wid = subject_id,
  between = condition, within = visibility, covariate = total_lap_time_1,effect.size = "pes"
)

mean_steering_cov_table <- get_anova_table(mean_steering_dev_cov.aov)

# Analysis 10: Mean Steering Acceleration with Lap Time Covariate ----------------------------------------------------------------

main="Mean Steering Acceleration for Repeated vs Varied Track Groups"

# Long format
mean_steering_dev_df_2 <- main_df %>%
  select(subject_id, condition,total_steering_acceleration_1,low_vis_steering_acceleration_10, high_vis_steering_acceleration_10) %>%
  gather(key = "visibility", value = "mean_steering_acceleration", low_vis_steering_acceleration_10, high_vis_steering_acceleration_10)

mean_steering_dev_cov.aov <- anova_test(
  data = mean_steering_dev_df_2, dv = mean_steering_acceleration, wid = subject_id,
  between = condition, within = visibility, covariate = total_steering_acceleration_1,effect.size = "pes"
)

mean_steering_cov_table <- get_anova_table(mean_steering_dev_cov.aov)


