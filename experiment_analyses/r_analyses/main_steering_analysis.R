# Analysis 3: sd Steering ----------------------------------------------------------------
# Create plot of data showing two-way interaction
# relevant columns
total_sd_steering_high_vis_familiar = mean(familiar_df[["high_vis_sd_steering_10"]])
total_sd_steering_high_vis_unfamiliar = mean(unfamiliar_df[["high_vis_sd_steering_10"]])
total_sd_steering_low_vis_familiar = mean(familiar_df[["low_vis_sd_steering_10"]])
total_sd_steering_low_vis_unfamiliar = mean(unfamiliar_df[["low_vis_sd_steering_10"]])

# Calculate standard error for error bars
SE_total_sd_steering_high_vis_familiar = sd(familiar_df[["high_vis_sd_steering_10"]])/sqrt(length((familiar_df[["high_vis_sd_steering_10"]])))
SE_total_sd_steering_high_vis_unfamiliar = sd(unfamiliar_df[["high_vis_sd_steering_10"]])/sqrt(length((unfamiliar_df[["high_vis_sd_steering_10"]])))
SE_total_sd_steering_low_vis_familiar = sd(familiar_df[["low_vis_sd_steering_10"]])/sqrt(length((familiar_df[["low_vis_sd_steering_10"]])))
SE_total_sd_steering_low_vis_unfamiliar = sd(unfamiliar_df[["low_vis_sd_steering_10"]])/sqrt(length((unfamiliar_df[["low_vis_sd_steering_10"]])))

sd_steering_plot_df <- data.frame(stringsAsFactors=TRUE,visibility=c("Low_visibility","Low_visibility","High_visibility","High_visibility"), 
                                   familiarity=c("Constant","Variable","Constant","Variable"), sd_steering=c(total_sd_steering_low_vis_familiar,total_sd_steering_low_vis_unfamiliar,total_sd_steering_high_vis_familiar,total_sd_steering_high_vis_unfamiliar),
                                   standard_error=c(SE_total_sd_steering_high_vis_familiar,SE_total_sd_steering_high_vis_unfamiliar,SE_total_sd_steering_low_vis_familiar,SE_total_sd_steering_low_vis_unfamiliar))

ggplot(sd_steering_plot_df, aes(x = visibility, y = sd_steering, color = familiarity, group = familiarity)) +
  geom_point(position=pd_for_main, size=4) +
  geom_line(position=pd_for_main, size=1.04) +
  geom_errorbar( aes(x=visibility, ymin=sd_steering-standard_error, ymax=sd_steering+standard_error), width=0.1,alpha=0.9,position=pd_for_main) +
  labs(x = "Visibility", y = "SD of Steering Angle (degrees)", color = "Track Constancy")+
  scale_x_discrete(labels = c("High", "Low"),expand = c(0.1, 0.05)) +
  coord_fixed(ratio = 0.1)+
  larger_text_theme(base_size = 12)+
  theme(legend.position = c(0.7, .3))


# Long format
sd_steering_df <- main_df %>%
  select(subject_id, condition,low_vis_sd_steering_10, high_vis_sd_steering_10) %>%
  gather(key = "visibility", value = "sd_steering", low_vis_sd_steering_10, high_vis_sd_steering_10) 

sd_steering.aov <- anova_test(
  data = sd_steering_df, dv = sd_steering, wid = subject_id,
  between = condition, within = visibility
)

get_anova_table(sd_steering.aov)


