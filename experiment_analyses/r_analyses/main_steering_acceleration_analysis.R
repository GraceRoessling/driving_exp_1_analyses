# Analysis 4: Mean Steering Acceleration ----------------------------------------------------------------

# Test for validity ---------------------------------------------------------------------
# Create plot of data showing two-way interaction

vis_specific_steering_acceleration_columns <- grepl("steering_acceleration_10|condition", colnames(main_df))
vis_specific_steering_acceleration_filtered_df <- main_df[, vis_specific_steering_acceleration_columns]


main="Mean of Lane Deviation for Repeated vs Varied Track Groups"


# Calculate Mean & CI for error bars
CI_total_steering_acceleration_high_vis_familiar <- calculate_CI(familiar_df, "high_vis_steering_acceleration_10")
CI_total_steering_acceleration_low_vis_familiar <- calculate_CI(familiar_df, "low_vis_steering_acceleration_10")
CI_total_steering_acceleration_high_vis_unfamiliar <- calculate_CI(unfamiliar_df, "high_vis_steering_acceleration_10")
CI_total_steering_acceleration_low_vis_unfamiliar <- calculate_CI(unfamiliar_df, "low_vis_steering_acceleration_10")


# Plot the data
steering_acceleration_plot_df <- data.frame(stringsAsFactors=TRUE,visibility=c("Low_visibility","Low_visibility","High_visibility","High_visibility"), 
                                    familiarity=c("Constant","Variable","Constant","Variable"), mean_steering_accelerations=c(CI_total_steering_acceleration_low_vis_familiar$mean,CI_total_steering_acceleration_low_vis_unfamiliar$mean,CI_total_steering_acceleration_high_vis_familiar$mean,CI_total_steering_acceleration_high_vis_unfamiliar$mean),
                                    confidence_interval_lower=c(CI_total_steering_acceleration_low_vis_familiar$ci_lower,CI_total_steering_acceleration_low_vis_unfamiliar$ci_lower,CI_total_steering_acceleration_high_vis_familiar$ci_lower,CI_total_steering_acceleration_high_vis_unfamiliar$ci_lower),
                                    confidence_interval_upper=c(CI_total_steering_acceleration_low_vis_familiar$ci_upper,CI_total_steering_acceleration_low_vis_unfamiliar$ci_upper,CI_total_steering_acceleration_high_vis_familiar$ci_upper,CI_total_steering_acceleration_high_vis_unfamiliar$ci_upper))


mean_steering_acceleration_plot <- ggplot(steering_acceleration_plot_df, aes(x = visibility, y = mean_steering_accelerations, color = familiarity, group = familiarity)) +
  geom_point(position=pd_for_main, size=3) +
  geom_line(position=pd_for_main, size=1.04) +
  geom_errorbar( aes(x=visibility, ymin=confidence_interval_lower, ymax=confidence_interval_upper), size = 0.8, width=0.1,alpha=0.9,position=pd_for_main) +
  labs(x = "Visibility", y = bquote("Mean Abs. Steering\nAcceleration ( deg /"~s^2~")"), color = "Track Constancy") +
  scale_x_discrete(labels =c("High", "Low"),expand = c(0, 0.13)) +
  larger_text_theme(base_size = 12)+
  theme(legend.position="none") +
  coord_fixed(ratio = 0.04)+
  theme(legend.position="none")

mean_steering_acceleration_plot

# Long format
steering_acceleration_df <- main_df %>%
  select(subject_id, condition,low_vis_steering_acceleration_10, high_vis_steering_acceleration_10) %>%
  gather(key = "visibility", value = "steering_acceleration", low_vis_steering_acceleration_10, high_vis_steering_acceleration_10) 

steering_acceleration.aov <- anova_test(
  data = steering_acceleration_df, dv = steering_acceleration, wid = subject_id,
  between = condition, within = visibility
)

get_anova_table(steering_acceleration.aov)

mean_steering_anova <- aov(steering_acceleration ~ condition*visibility + Error(subject_id/visibility), steering_acceleration_df)
summary(mean_steering_anova)
eta_squared(mean_steering_anova, partial = TRUE)