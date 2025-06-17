# Analysis 8: Lane Deviation Variance with Steering Acceleration Covariate ----------------------------------------------------------------

main="mean of Lane Deviation for Repeated vs Varied Track Groups"

# Long format
mean_lane_dev_df_2 <- main_df %>%
  select(subject_id, condition,total_steering_acceleration_1,low_vis_mean_lane_dev_10, high_vis_mean_lane_dev_10) %>%
  gather(key = "visibility", value = "mean_lane_dev", low_vis_mean_lane_dev_10, high_vis_mean_lane_dev_10)

mean_lane_dev_cov.aov <- anova_test(
  data = mean_lane_dev_df_2, dv = mean_lane_dev, wid = subject_id,
  between = condition, within = visibility, covariate = total_steering_acceleration_1,effect.size = "pes"
)

mean_lane_cov_table <- get_anova_table(mean_lane_dev_cov.aov)

# Simple main effect analysis

mean_lane_dev_df_2 %>%
  group_by(visibility) %>%
  anova_test(mean_lane_dev ~ total_steering_acceleration_1 + condition,effect.size = "pes")

pwc <- mean_lane_dev_df_2 %>% 
  group_by(visibility) %>%
  emmeans_test(
    mean_lane_dev ~ condition, covariate = total_steering_acceleration_1, p.adjust.method = "bonferroni"
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
pwc.filtered <- pwc %>% filter(visibility == "high_vis_mean_lane_dev_10")
lp + 
  stat_pvalue_manual(
    pwc.filtered, hide.ns = TRUE, tip.length = 0,
    bracket.size = 0
  ) +
  labs(
    subtitle = get_test_label(mean_lane_dev_cov.aov,  detailed = TRUE),
    caption = get_pwc_label(pwc)
  )


# Get adjusted means for plotting
adj_means_df <- get_emmeans(pwc)

# Rename columns to match your ANOVA-style plotting code
adj_means_df <- adj_means_df %>%
  rename(
    mean_lane_devs = emmean,
    confidence_interval_lower = conf.low,
    confidence_interval_upper = conf.high,
    familiarity = condition # if "condition" in ANCOVA equals "familiarity" in your ANOVA plot
  )

# Plot using ggplot
mean_lane_dev_plot_ancova <- ggplot(adj_means_df, aes(x = visibility, y = mean_lane_devs, color = familiarity, group = familiarity)) +
  geom_point(position = pd_for_main, size = 8) +
  geom_line(position = pd_for_main, size = 1.4) +
  geom_errorbar(
    aes(ymin = confidence_interval_lower, ymax = confidence_interval_upper),
    width = 0.1, size = 1, alpha = 0.9, position = pd_for_main
  ) +
  labs(
    x = "Visibility",
    y = "Mean of Lane Dev. (meters)",
    color = "Track Constancy",
    title = "Mean of Lane Dev. for Constant vs. Variable Track Groups"
  ) +
  scale_x_discrete(labels = c("high_vis_mean_lane_dev_10" = "High", "low_vis_mean_lane_dev_10" = "Low"), expand = c(0, 0.1)) +
  scale_color_manual(
    values = c("familiar" = "#0000FF", "unfamiliar" = "#FF4040"),
    labels = c("familiar" = "Constant Track", "unfamiliar" = "Variable Track")
  ) +
  theme(
    legend.position = "none",
    plot.title = element_text(size = 40),
    axis.title.x = element_text(size = 40),
    axis.title.y = element_text(size = 40),
    axis.text.x = element_text(size = 30),
    axis.text.y = element_text(size = 30)
  )


# Display the plot
mean_lane_dev_plot_ancova