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

# get ANCOVA table ------------------
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

# Simple main effect analysis

sd_lane_dev_df_2 %>%
  group_by(visibility) %>%
  anova_test(sd_lane_dev ~ total_steering_acceleration_1 + condition,effect.size = "pes")

pwc <- sd_lane_dev_df_2 %>% 
  group_by(visibility) %>%
  emmeans_test(
    sd_lane_dev ~ condition, covariate = total_steering_acceleration_1, p.adjust.method = "bonferroni"
  )


lp <- ggline(
  get_emmeans(pwc), x = "visibility", y = "emmean", 
  color = "condition", palette = "jco"
) +
  geom_errorbar(
    aes(ymin = conf.low, ymax = conf.high, color = condition), 
    width = 0.1
  )

pwc <- pwc %>% add_xy_position(x = "visibility", fun = "mean_se", step.increase = 0.2)
pwc.filtered <- pwc %>% filter(visibility == "high_vis_sd_lane_dev_10")
lp + 
  stat_pvalue_manual(
    pwc.filtered, hide.ns = TRUE, tip.length = 0,
    bracket.size = 0
  ) +
  labs(
    subtitle = get_test_label(sd_lane_dev_cov.aov,  detailed = TRUE),
    caption = get_pwc_label(pwc)
  )
