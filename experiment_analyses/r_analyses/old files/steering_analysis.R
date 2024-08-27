# Analysis 3: Var Steering ----------------------------------------------------------------

#if analyzing variance
# high_vis_string_steering = "high_vis_var_steering_10"
# low_vis_string_steering = "low_vis_var_steering_10"
# y_title = "Steering Variance"

# if analyzing SD
high_vis_string_steering = "high_vis_sd_steering_10"
low_vis_string_steering = "low_vis_sd_steering_10"
y_title = "SD of Steering Angle (degrees)"


# Create plot of data showing two-way interaction
# relevant columns
total_var_steering_high_vis_familiar = mean(famliar_df[[high_vis_string_steering]])
total_var_steering_high_vis_unfamiliar = mean(unfamiliar_df[[high_vis_string_steering]])
total_var_steering_low_vis_familiar = mean(famliar_df[[low_vis_string_steering]])
total_var_steering_low_vis_unfamiliar = mean(unfamiliar_df[[low_vis_string_steering]])

# Calculate standard error for error bars
SE_total_var_steering_high_vis_familiar = sd(famliar_df[[high_vis_string_steering]])/sqrt(length((famliar_df[[high_vis_string_steering]])))
SE_total_var_steering_high_vis_unfamiliar = sd(unfamiliar_df[[high_vis_string_steering]])/sqrt(length((unfamiliar_df[[high_vis_string_steering]])))
SE_total_var_steering_low_vis_familiar = sd(famliar_df[[low_vis_string_steering]])/sqrt(length((famliar_df[[low_vis_string_steering]])))
SE_total_var_steering_low_vis_unfamiliar = sd(unfamiliar_df[[low_vis_string_steering]])/sqrt(length((unfamiliar_df[[low_vis_string_steering]])))


var_steering_plot_df <- data.frame(stringsAsFactors=TRUE,visibility=c("Low_visibility","Low_visibility","High_visibility","High_visibility"), 
                                   familiarity=c("Constant","Variable","Constant","Variable"), var_steering=c(total_var_steering_low_vis_familiar,total_var_steering_low_vis_unfamiliar,total_var_steering_high_vis_familiar,total_var_steering_high_vis_unfamiliar),
                                   standard_error=c(SE_total_var_steering_high_vis_familiar,SE_total_var_steering_high_vis_unfamiliar,SE_total_var_steering_low_vis_familiar,SE_total_var_steering_low_vis_unfamiliar))
pd <- position_dodge(width = 0.1)

ggplot(var_steering_plot_df, aes(x = visibility, y = var_steering, color = familiarity, group = familiarity)) +
  geom_point(position=pd, size=4) +
  geom_line(position=pd, size=1.04) +
  geom_errorbar( aes(x=visibility, ymin=var_steering-standard_error, ymax=var_steering+standard_error), width=0.1,alpha=0.9,position=pd) +
  labs(x = "Visibility", y = y_title, color = "Track Constancy")+
  scale_x_discrete(labels = c("High", "Low"),expand = c(0.1, 0.05)) +
  coord_fixed(ratio = 0.1)+
  larger_text_theme(base_size = 12)+
  theme(legend.position = c(0.7, .3))


# Long format
var_steering_df <- main_df %>%
  select(subject_id, condition,low_vis_var_steering_10, high_vis_var_steering_10) %>%
  gather(key = "visibility", value = "var_steering", low_vis_var_steering_10, high_vis_var_steering_10) 

var_steering.aov <- anova_test(
  data = var_steering_df, dv = var_steering, wid = subject_id,
  between = condition, within = visibility
)

get_anova_table(var_steering.aov)


