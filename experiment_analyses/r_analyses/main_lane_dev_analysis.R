
# Analysis 4: Mean Lane Deviation ----------------------------------------------------------------

# Test for validity ---------------------------------------------------------------------
# Create plot of data showing two-way interaction

vis_specific_mean_ld_columns <- grepl("mean_lane_dev_10|condition", colnames(main_df))
vis_specific_mean_ld_filtered_df <- main_df[, vis_specific_mean_ld_columns]


main="Mean of Lane Deviation for Repeated vs Varied Track Groups"


# Calculate Mean & CI for error bars
CI_total_lane_dev_high_vis_familiar <- calculate_CI(familiar_df, "high_vis_mean_lane_dev_10")
CI_total_lane_dev_low_vis_familiar <- calculate_CI(familiar_df, "low_vis_mean_lane_dev_10")
CI_total_lane_dev_high_vis_unfamiliar <- calculate_CI(unfamiliar_df, "high_vis_mean_lane_dev_10")
CI_total_lane_dev_low_vis_unfamiliar <- calculate_CI(unfamiliar_df, "low_vis_mean_lane_dev_10")


# Plot the data
mean_lane_dev_plot_df <- data.frame(stringsAsFactors=TRUE,visibility=c("Low_visibility","Low_visibility","High_visibility","High_visibility"), 
                                    familiarity=c("Constant","Variable","Constant","Variable"), mean_lane_devs=c(CI_total_lane_dev_low_vis_familiar$mean,CI_total_lane_dev_low_vis_unfamiliar$mean,CI_total_lane_dev_high_vis_familiar$mean,CI_total_lane_dev_high_vis_unfamiliar$mean),
                                    confidence_interval_lower=c(CI_total_lane_dev_low_vis_familiar$ci_lower,CI_total_lane_dev_low_vis_unfamiliar$ci_lower,CI_total_lane_dev_high_vis_familiar$ci_lower,CI_total_lane_dev_high_vis_unfamiliar$ci_lower),
                                    confidence_interval_upper=c(CI_total_lane_dev_low_vis_familiar$ci_upper,CI_total_lane_dev_low_vis_unfamiliar$ci_upper,CI_total_lane_dev_high_vis_familiar$ci_upper,CI_total_lane_dev_high_vis_unfamiliar$ci_upper))


mean_ld_plot <- ggplot(mean_lane_dev_plot_df, aes(x = visibility, y = mean_lane_devs, color = familiarity, group = familiarity)) +
  geom_point(position=pd_for_main, size=3) +
  scale_y_continuous(breaks = round(seq(-10, 10, by = 0.5),1))+
  geom_line(position=pd_for_main, size=1.04) +
  geom_errorbar( aes(x=visibility, ymin=confidence_interval_lower, ymax=confidence_interval_upper), size = 0.8, width=0.1,alpha=0.9,position=pd_for_main) +
  labs(x = "Visibility", y = "Mean Abs. Lane \n Deviation (meters)", color = "Track Constancy") +
  scale_x_discrete(labels =c("High", "Low"),expand = c(0, 0.1)) +
  scale_y_continuous(breaks=number_ticks(5))+
  coord_fixed(ratio = 1.5)+
  larger_text_theme(base_size = 12)+
  theme(legend.position="none")+
  theme(plot.margin = unit(c(0.15, 0.15, 0.15, 0.15), 
                           "inches")) 

mean_ld_plot

# Long format
mean_lane_dev_df <- main_df %>%
  select(subject_id, condition,low_vis_mean_lane_dev_10, high_vis_mean_lane_dev_10) %>%
  gather(key = "visibility", value = "mean_lane_dev", low_vis_mean_lane_dev_10, high_vis_mean_lane_dev_10) 

mean_lane_dev.aov <- anova_test(
  data = mean_lane_dev_df, dv = mean_lane_dev, wid = subject_id,
  between = condition, within = visibility
)

mean_lane_dev_table <- get_anova_table(mean_lane_dev.aov)

mean_lane_dev_anova <- aov(mean_lane_dev ~ condition*visibility + Error(subject_id/visibility), mean_lane_dev_df)
summary(mean_lane_dev_anova)
eta_squared(mean_lane_dev_anova, partial = TRUE)

# Analysis 5: Var Lane Deviation ----------------------------------------------------------------

vis_specific_sd_ld_columns <- grepl("sd_lane_dev_10|condition", colnames(main_df))
vis_specific_sd_ld_filtered_df <- main_df[, vis_specific_sd_ld_columns]

# Create plot of data showing two-way interaction

# Calculate Mean & CI for error bars
CI_total_sd_lane_dev_high_vis_familiar <- calculate_CI(familiar_df, "high_vis_sd_lane_dev_10")
CI_total_sd_lane_dev_low_vis_familiar <- calculate_CI(familiar_df, "low_vis_sd_lane_dev_10")
CI_total_sd_lane_dev_high_vis_unfamiliar <- calculate_CI(unfamiliar_df, "high_vis_sd_lane_dev_10")
CI_total_sd_lane_dev_low_vis_unfamiliar <- calculate_CI(unfamiliar_df, "low_vis_sd_lane_dev_10")



sd_lane_dev_plot_df <- data.frame(stringsAsFactors=TRUE,visibility=c("Low_visibility","Low_visibility","High_visibility","High_visibility"), 
                                    familiarity=c("Constant","Variable","Constant","Variable"), sd_lane_devs=c(CI_total_sd_lane_dev_low_vis_familiar$mean,CI_total_sd_lane_dev_low_vis_unfamiliar$mean,CI_total_sd_lane_dev_high_vis_familiar$mean,CI_total_sd_lane_dev_high_vis_unfamiliar$mean),
                                    confidence_interval_lower=c(CI_total_sd_lane_dev_low_vis_familiar$ci_lower,CI_total_sd_lane_dev_low_vis_unfamiliar$ci_lower,CI_total_sd_lane_dev_high_vis_familiar$ci_lower,CI_total_sd_lane_dev_high_vis_unfamiliar$ci_lower),
                                    confidence_interval_upper=c(CI_total_sd_lane_dev_low_vis_familiar$ci_upper,CI_total_sd_lane_dev_low_vis_unfamiliar$ci_upper,CI_total_sd_lane_dev_high_vis_familiar$ci_upper,CI_total_sd_lane_dev_high_vis_unfamiliar$ci_upper))


sd_ld_plot <- ggplot(sd_lane_dev_plot_df, aes(x = visibility, y = sd_lane_devs, color = familiarity, group = familiarity)) +
  geom_point(position=pd_for_main, size=3) +
  geom_line(position=pd_for_main, size=1.04) +
  geom_errorbar( aes(x=visibility, ymin=confidence_interval_lower, ymax=confidence_interval_upper), width=0.1,size=0.8, alpha=0.9,position=pd_for_main) +
  labs(x = "Visibility", y = "SD of Abs. Lane \n Deviation (meters)", color = "Track Exposure") +
  scale_x_discrete(labels =c("High", "Low"),expand = c(0, 0.1)) +
  larger_text_theme(base_size = 12)+
  coord_fixed(ratio = 2)+
  theme(legend.position="none")

sd_ld_plot

(mean_ld_plot | sd_ld_plot) + 
  plot_layout(heights = c(1, 1)) +
  plot_annotation(tag_levels = 'A')

# Long format
sd_lane_dev_df <- main_df %>%
  select(subject_id, condition,low_vis_sd_lane_dev_10, high_vis_sd_lane_dev_10) %>%
  gather(key = "visibility", value = "sd_lane_dev", low_vis_sd_lane_dev_10, high_vis_sd_lane_dev_10) 

sd_lane_dev.aov <- anova_test(
  data = sd_lane_dev_df, dv = sd_lane_dev, wid = subject_id,
  between = condition, within = visibility
)

get_anova_table(sd_lane_dev.aov)

sd_lane_dev_anova <- aov(sd_lane_dev ~ condition*visibility + Error(subject_id/visibility), sd_lane_dev_df)
summary(sd_lane_dev_anova)
eta_squared(sd_lane_dev_anova, partial = TRUE)