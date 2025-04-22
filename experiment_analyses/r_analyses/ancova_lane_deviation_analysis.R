# Analysis 6: Mean Lane Deviation with Lap Time Covariate ----------------------------------------------------------------

main="Mean of Lane Deviation for Repeated vs Varied Track Groups"

# Long format
mean_lane_dev_df_2 <- main_df %>%
  select(subject_id, condition,total_lap_time_1,low_vis_mean_lane_dev_10, high_vis_mean_lane_dev_10) %>%
  gather(key = "visibility", value = "mean_lane_dev", low_vis_mean_lane_dev_10, high_vis_mean_lane_dev_10)

mean_lane_dev_cov.aov <- anova_test(
  data = mean_lane_dev_df_2, dv = mean_lane_dev, wid = subject_id,
  between = condition, within = visibility, covariate = total_lap_time_1,effect.size = "pes"
)

mean_lane_cov_table <- get_anova_table(mean_lane_dev_cov.aov)

# Analysis 7: Mean Lane Deviation with Steering Acceleration Covariate ----------------------------------------------------------------

main="Mean of Lane Deviation for Repeated vs Varied Track Groups"

# Long format
mean_lane_dev_df_2 <- main_df %>%
  select(subject_id, condition,total_steering_acceleration_1,low_vis_mean_lane_dev_10, high_vis_mean_lane_dev_10) %>%
  gather(key = "visibility", value = "mean_lane_dev", low_vis_mean_lane_dev_10, high_vis_mean_lane_dev_10)

mean_lane_dev_cov.aov <- anova_test(
  data = mean_lane_dev_df_2, dv = mean_lane_dev, wid = subject_id,
  between = condition, within = visibility, covariate = total_steering_acceleration_1,effect.size = "pes"
)

mean_lane_cov_table <- get_anova_table(mean_lane_dev_cov.aov)

# Analysis 8: Lane Deviation Variance with Lap Time Covariate ----------------------------------------------------------------

main="SD of Lane Deviation for Repeated vs Varied Track Groups"

# Long format
sd_lane_dev_df_2 <- main_df %>%
  select(subject_id, condition,total_lap_time_1,low_vis_sd_lane_dev_10, high_vis_sd_lane_dev_10) %>%
  gather(key = "visibility", value = "sd_lane_dev", low_vis_sd_lane_dev_10, high_vis_sd_lane_dev_10)

sd_lane_dev_cov.aov <- anova_test(
  data = sd_lane_dev_df_2, dv = sd_lane_dev, wid = subject_id,
  between = condition, within = visibility, covariate = total_lap_time_1,effect.size = "pes"
)

sd_lane_cov_table <- get_anova_table(sd_lane_dev_cov.aov)



# Analysis 8: Lane Deviation Variance with Steering Acceleration Covariate ----------------------------------------------------------------

main="SD of Lane Deviation for Repeated vs Varied Track Groups"

# Long format
sd_lane_dev_df_2 <- main_df %>%
  select(subject_id, condition,total_steering_acceleration_1,low_vis_sd_lane_dev_10, high_vis_sd_lane_dev_10) %>%
  gather(key = "visibility", value = "sd_lane_dev", low_vis_sd_lane_dev_10, high_vis_sd_lane_dev_10)

sd_lane_dev_cov.aov <- anova_test(
  data = sd_lane_dev_df_2, dv = sd_lane_dev, wid = subject_id,
  between = condition, within = visibility, covariate = total_steering_acceleration_1,effect.size = "pes"
)

sd_lane_cov_table <- get_anova_table(sd_lane_dev_cov.aov)
