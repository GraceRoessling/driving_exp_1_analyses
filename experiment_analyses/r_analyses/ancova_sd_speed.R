
# Analysis 8: Mean Speed with Steering Acceleration Covariate ----------------------------------------------------------------


main="Mean Speed for Repeated vs Varied Track Groups"

# Long format
sd_speed_df <- main_df %>%
  select(subject_id, condition,total_steering_acceleration_1,low_vis_sd_speed_10, high_vis_sd_speed_10) %>%
  gather(key = "visibility", value = "sd_speed", low_vis_sd_speed_10, high_vis_sd_speed_10)

sd_speed.aov <- anova_test(
  data = sd_speed_df, dv = sd_speed, wid = subject_id,
  between = condition, within = visibility, covariate = total_steering_acceleration_1,effect.size = "pes"
)
sd_speed_ancova_table <- get_anova_table(sd_speed.aov)

# Simple main effect analysis

sd_speed_df %>%
  group_by(visibility) %>%
  anova_test(sd_speed ~ total_steering_acceleration_1 + condition,effect.size = "pes")

pwc <- sd_speed_df %>% 
  group_by(visibility) %>%
  emmeans_test(
    sd_speed ~ condition, covariate = total_steering_acceleration_1, p.adjust.method = "bonferroni"
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
pwc.filtered <- pwc %>% filter(visibility == "high_vis_sd_speed_10")
lp + 
  stat_pvalue_manual(
    pwc.filtered, hide.ns = TRUE, tip.length = 0,
    bracket.size = 0
  ) +
  labs(
    subtitle = get_test_label(sd_speed.aov,  detailed = TRUE),
    caption = get_pwc_label(pwc)
  )


# Get adjusted means for plotting
adj_means_df <- get_emmeans(pwc)

# Rename columns to match your ANOVA-style plotting code
adj_means_df <- adj_means_df %>%
  rename(
    sd_speed_devs = emmean,
    confidence_interval_lower = conf.low,
    confidence_interval_upper = conf.high,
    familiarity = condition # if "condition" in ANCOVA equals "familiarity" in your ANOVA plot
  )


# Plot using ggplot
sd_speed_plot_ancova <- ggplot(adj_means_df, aes(x = visibility, y = sd_speed_devs, color = familiarity, group = familiarity)) +
  geom_point(position = pd_for_main, size = 8) +
  geom_line(position = pd_for_main, size = 1.4) +
  geom_errorbar(
    aes(ymin = confidence_interval_lower, ymax = confidence_interval_upper),
    width = 0.1, size = 1, alpha = 0.9, position = pd_for_main
  ) +
  labs(
    x = "Visibility",
    y = "SD of Speed (m/s)",
    color = "Track Constancy",
    title = "SD of Speed for Control, SL, and SS Groups"
  ) +
  scale_x_discrete(labels = c("high_vis_sd_speed_10" = "High", "low_vis_sd_speed_10" = "Low"), expand = c(0, 0.1)) +
  scale_color_manual(
    values = c("control" = "#0000FF", "scrambled_landmarks" = "#FF4040","scrambled_segments" = "#00CD00"),
    labels = c("control" = "Control Group", "scrambled_landmarks" = "Scrambled Landmarks", "scrambled_segments"="Scrambled Segments")
  ) +
  theme(
    plot.title = element_text(size = 30),
    axis.title.x = element_text(size = 30),
    axis.title.y = element_text(size = 30),
    axis.text.x = element_text(size = 20),
    axis.text.y = element_text(size = 20)
  )


# Display the plot
sd_speed_plot_ancova

