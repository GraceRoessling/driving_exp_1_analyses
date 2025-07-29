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

pwc %>%
  select(visibility, group1, group2, conf.low, conf.high, p.adj)

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


# Get adjusted means for plotting
adj_means_df <- get_emmeans(pwc)

# Rename columns to match your ANOVA-style plotting code
adj_means_df <- adj_means_df %>%
  rename(
    sd_lane_devs = emmean,
    confidence_interval_lower = conf.low,
    confidence_interval_upper = conf.high,
    familiarity = condition # if "condition" in ANCOVA equals "familiarity" in your ANOVA plot
  )

# Plot using ggplot
sd_lane_dev_plot_ancova <- ggplot(adj_means_df, aes(x = visibility, y = sd_lane_devs, color = familiarity, group = familiarity)) +
  geom_point(position = pd_for_main, size = 8) +
  geom_line(position = pd_for_main, size = 1.4) +
  geom_errorbar(
    aes(ymin = confidence_interval_lower, ymax = confidence_interval_upper),
    width = 0.1, size = 1, alpha = 0.9, position = pd_for_main
  ) +
  labs(
    x = "Visibility",
    y = "SD of Lane Dev. (meters)",
    color = "Track Constancy",
    title = "SD of Lane Dev. for Constant vs. Variable Track Groups"
  ) +
  scale_x_discrete(labels = c("high_vis_sd_lane_dev_10" = "High", "low_vis_sd_lane_dev_10" = "Low"), expand = c(0, 0.1)) +
  scale_color_manual(
    values = c("control" = "#0000FF", "scrambled_landmarks" = "#FF4040","scrambled_segments" = "#00CD00"),
    labels = c("control" = "Control Group", "scrambled_landmarks" = "Scrambled Landmarks", "scrambled_segments"="Scrambled Segments")
  ) +
  theme(
    legend.position = "none",
    plot.title = element_text(size = 30),
    axis.title.x = element_text(size = 40),
    axis.title.y = element_text(size = 40),
    axis.text.x = element_text(size = 30),
    axis.text.y = element_text(size = 30)
  )


# Display the plot
sd_lane_dev_plot_ancova




# posthoc report!
library(emmeans)
library(dplyr)

# Fit the ANCOVA model using the correct data and variable names
model <- lm(sd_lane_dev ~ condition * visibility + total_steering_acceleration_1,
            data = sd_lane_dev_df_2)

# Get estimated marginal means (adjusted for covariate)
emm_results <- emmeans(model, ~ condition | visibility)

# Summarize with means, SEs, and 95% confidence intervals
summary_df <- summary(emm_results, infer = c(TRUE, TRUE)) %>%
  rename(
    mean = emmean,
    lower_ci = lower.CL,
    upper_ci = upper.CL
  ) %>%
  mutate(
    mean = round(mean, 2),
    SE = round(SE, 2),
    lower_ci = round(lower_ci, 2),
    upper_ci = round(upper_ci, 2)
  )

# Print APA-style table
print(summary_df)

# Post-hoc: Compare condition within each visibility level
pwc_condition_by_visibility <- sd_lane_dev_df_2 %>% 
  group_by(visibility) %>%
  emmeans_test(
    sd_lane_dev ~ condition, 
    covariate = total_steering_acceleration_1,
    p.adjust.method = "bonferroni"
  )

# Print to inspect significance of condition differences at each visibility level
print(pwc_condition_by_visibility)
