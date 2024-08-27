
vis_specific_mean_speed_columns <- grepl("mean_speed_10|condition", colnames(main_df))
vis_specific_mean_speed_filtered_df <- main_df[, vis_specific_mean_speed_columns]


# Analysis 1: Mean Speed ----------------------------------------------------------------

# Test for validity ---------------------------------------------------------------------
# Create plot of data showing two-way interaction
# relevant columns

# Calculate Mean & CI for error bars
CI_total_speed_high_vis_familiar <- calculate_CI(familiar_df, "high_vis_mean_speed_10")
CI_total_speed_low_vis_familiar <- calculate_CI(familiar_df, "low_vis_mean_speed_10")
CI_total_speed_high_vis_unfamiliar <- calculate_CI(unfamiliar_df, "high_vis_mean_speed_10")
CI_total_speed_low_vis_unfamiliar <- calculate_CI(unfamiliar_df, "low_vis_mean_speed_10")


main = "Mean Speed for Repeated vs Varied Track Groups"

mean_speed_plot_df <- data.frame(stringsAsFactors=TRUE,visibility=c("Low_visibility","Low_visibility","High_visibility","High_visibility"), 
                                 familiarity=c("Constant","Variable","Constant","Variable"), mean_speeds=c(CI_total_speed_low_vis_familiar$mean,CI_total_speed_low_vis_unfamiliar$mean,CI_total_speed_high_vis_familiar$mean,CI_total_speed_high_vis_unfamiliar$mean),
                                 confidence_interval_lower=c(CI_total_speed_low_vis_familiar$ci_lower,CI_total_speed_low_vis_unfamiliar$ci_lower,CI_total_speed_high_vis_familiar$ci_lower,CI_total_speed_high_vis_unfamiliar$ci_lower),
                                 confidence_interval_upper=c(CI_total_speed_low_vis_familiar$ci_upper,CI_total_speed_low_vis_unfamiliar$ci_upper,CI_total_speed_high_vis_familiar$ci_upper,CI_total_speed_high_vis_unfamiliar$ci_upper))

mean_speed_plot <- ggplot(mean_speed_plot_df, aes(x = visibility, y = mean_speeds, color = familiarity, group = familiarity)) +
  geom_point(position=pd_for_main,size=5) +
  geom_line(position=pd_for_main, size=1.04) +
  geom_errorbar( aes(x=visibility, ymin=confidence_interval_lower, ymax=confidence_interval_upper), width=0.1,size = 0.8, alpha=0.9,position=pd_for_main) +
  labs(x = "Visibility", y = "Mean Speed (m/s)", color = "Track Constancy")+
  scale_x_discrete(labels = c("High", "Low"),expand = c(0, 0.13))+
  theme(legend.position="none") +
  coord_fixed(ratio = 0.08)+
  larger_text_theme(base_size = 12)+
  theme(legend.position = "none")+
  theme(plot.margin = unit(c(0.15, 0.15, 0.15, 0.15), 
                           "inches")) 

mean_speed_plot

# Long format
mean_speed_df <- main_df %>%
  select(subject_id, condition,low_vis_mean_speed_10, high_vis_mean_speed_10) %>%
  gather(key = "visibility", value = "mean_speed", low_vis_mean_speed_10, high_vis_mean_speed_10) 

mean_speed.aov <- anova_test(
  data = mean_speed_df, dv = mean_speed, wid = subject_id,
  between = condition, within = visibility
)

mean_speed_anova_table <- get_anova_table(mean_speed.aov)

mean_speed_anova <- aov(mean_speed ~ condition*visibility + Error(subject_id/visibility), mean_speed_df)
summary(mean_speed_anova)
eta_squared(mean_speed_anova, partial = TRUE)

# Analysis 2: Var Speed ----------------------------------------------------------------

vis_specific_sd_speed_columns <- grepl("sd_speed_10|condition", colnames(main_df))
vis_specific_sd_speed_filtered_df <- main_df[, vis_specific_sd_speed_columns]

# relevant columns

# Calculate Mean & CI for error bars
CI_total_sd_speed_high_vis_familiar <- calculate_CI(familiar_df, "high_vis_sd_speed_10")
CI_total_sd_speed_low_vis_familiar <- calculate_CI(familiar_df, "low_vis_sd_speed_10")
CI_total_sd_speed_high_vis_unfamiliar <- calculate_CI(unfamiliar_df, "high_vis_sd_speed_10")
CI_total_sd_speed_low_vis_unfamiliar <- calculate_CI(unfamiliar_df, "low_vis_sd_speed_10")


main = " SD of Speed for Repeated vs Varied Track Groups"

sd_speed_plot_df <- data.frame(stringsAsFactors=TRUE,visibility=c("Low_visibility","Low_visibility","High_visibility","High_visibility"), 
                                 familiarity=c("Constant","Variable","Constant","Variable"), sd_speeds=c(CI_total_sd_speed_low_vis_familiar$mean,CI_total_sd_speed_low_vis_unfamiliar$mean,CI_total_sd_speed_high_vis_familiar$mean,CI_total_sd_speed_high_vis_unfamiliar$mean),
                                 confidence_interval_lower=c(CI_total_sd_speed_low_vis_familiar$ci_lower,CI_total_sd_speed_low_vis_unfamiliar$ci_lower,CI_total_sd_speed_high_vis_familiar$ci_lower,CI_total_sd_speed_high_vis_unfamiliar$ci_lower),
                                 confidence_interval_upper=c(CI_total_sd_speed_low_vis_familiar$ci_upper,CI_total_sd_speed_low_vis_unfamiliar$ci_upper,CI_total_sd_speed_high_vis_familiar$ci_upper,CI_total_sd_speed_high_vis_unfamiliar$ci_upper))

sd_speed_plot <- ggplot(sd_speed_plot_df, aes(x = visibility, y = sd_speeds, color = familiarity, group = familiarity)) +
  geom_point(position=pd_for_main,size=5) +
  geom_line(position=pd_for_main, size=1.04) +
  geom_errorbar( aes(x=visibility, ymin=confidence_interval_lower, ymax=confidence_interval_upper), width=0.1,size = 0.8, alpha=0.9,position=pd_for_main) +
  labs(x = "Visibility", y = "SD of Speed (m/s)", color = "Track Constancy")+
  scale_x_discrete(labels = c("High", "Low"),expand = c(0, 0.13))+
  theme(legend.position="none") +
  coord_fixed(ratio = 0.38)+
  larger_text_theme(base_size = 12)+
  theme(legend.position = "none")+
  theme(plot.margin = unit(c(0.15, 0.15, 0.15, 0.15), 
                           "inches")) 

sd_speed_plot

# Long format
sd_speed_df <- main_df %>%
  select(subject_id, condition,low_vis_sd_speed_10, high_vis_sd_speed_10) %>%
  gather(key = "visibility", value = "sd_speed", low_vis_sd_speed_10, high_vis_sd_speed_10) 

sd_speed.aov <- anova_test(
  data = sd_speed_df, dv = sd_speed, wid = subject_id,
  between = condition, within = visibility
)

get_anova_table(sd_speed.aov)

sd_speed_anova <- aov(sd_speed ~ condition*visibility + Error(subject_id/visibility), sd_speed_df)
summary(sd_speed_anova)
eta_squared(sd_speed_anova, partial = TRUE)


(mean_speed_plot | sd_speed_plot) + 
  plot_layout(heights = c(1, 1)) +
  plot_annotation(tag_levels = 'A')

