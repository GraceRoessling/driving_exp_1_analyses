library(dplyr)
library(ggplot2)
library(tidyr)
library(tidyverse)
library(ggpubr)
library(rstatix)
library(gridExtra)
library(patchwork)

# for all track pieces (excluding straight pieces)
#csv_path = "C:\\Users\\graci\\Dropbox\\PAndA\\Thesis Experiment 1\\data\\main_data\\ultimate_master_variable_df.csv"
csv_path = "C:\\Users\\graci\\Dropbox\\PAndA\\Thesis Experiment 1\\data\\main_data\\corrected_steering_dev.csv"

# for single piece comparison (between left and right turn short pieces)
# csv_path = "C:\\Users\\graci\\Dropbox\\PAndA\\Thesis Experiment 1\\data\\main_data\\short_turn_piece_variable_df.csv"

main_df = read.csv(csv_path,stringsAsFactors=TRUE)

convert_var_to_sd <- function(df) {
  df %>%
    mutate(across(contains("var"), 
                  ~ sqrt(.),
                  .names = "{str_replace(.col, 'var', 'sd')}"))
}

# For all files
subject_id = main_df[["subject_id"]]
familiarity = main_df[["condition"]]
famliar_df <- main_df %>% filter(!grepl('unfamiliar', condition)) # if "unfamiliar" is in the row, take it out
unfamiliar_df <- main_df %>% filter(grepl('unfamiliar', condition)) # if "unfamiliar" is in the row, put it in

famliar_df <- convert_var_to_sd(famliar_df)
unfamiliar_df <- convert_var_to_sd(unfamiliar_df)

sd_famliar_df <- famliar_df[ , grepl( "sd_lane_dev" , names( famliar_df ) ) ]
sd_unfamiliar_df <- unfamiliar_df[ , grepl( "sd_lane_dev" , names( unfamiliar_df ) ) ]

# Analysis 4: Mean Lane Deviation ----------------------------------------------------------------

# Test for validity ---------------------------------------------------------------------
# Create plot of data showing two-way interaction

main="Mean of Lane Deviation for Repeated vs Varied Track Groups"

# relevant columns
total_mean_lane_dev_high_vis_familiar = mean(famliar_df[["high_vis_mean_lane_dev_10"]])
total_mean_lane_dev_high_vis_unfamiliar = mean(unfamiliar_df[["high_vis_mean_lane_dev_10"]])
total_mean_lane_dev_low_vis_familiar = mean(famliar_df[["low_vis_mean_lane_dev_10"]])
total_mean_lane_dev_low_vis_unfamiliar = mean(unfamiliar_df[["low_vis_mean_lane_dev_10"]])


# Calculate standard error for error bars
SE_total_var_lane_dev_high_vis_familiar = sd(famliar_df[["high_vis_mean_lane_dev_10"]])/sqrt(length((famliar_df[["high_vis_mean_lane_dev_10"]])))
SE_total_var_lane_dev_high_vis_unfamiliar = sd(unfamiliar_df[["high_vis_mean_lane_dev_10"]])/sqrt(length((unfamiliar_df[["high_vis_mean_lane_dev_10"]])))
SE_total_var_lane_dev_low_vis_familiar = sd(famliar_df[["low_vis_mean_lane_dev_10"]])/sqrt(length((famliar_df[["low_vis_mean_lane_dev_10"]])))
SE_total_var_lane_dev_low_vis_unfamiliar = sd(unfamiliar_df[["low_vis_mean_lane_dev_10"]])/sqrt(length((unfamiliar_df[["low_vis_mean_lane_dev_10"]])))


mean_lane_dev_plot_df <- data.frame(stringsAsFactors=TRUE,visibility=c("Low_visibility","Low_visibility","High_visibility","High_visibility"), 
                                    familiarity=c("Constant","Variable","Constant","Variable"), mean_lane_devs=c(total_mean_lane_dev_low_vis_familiar,total_mean_lane_dev_low_vis_unfamiliar,total_mean_lane_dev_high_vis_familiar,total_mean_lane_dev_high_vis_unfamiliar),
                                    standard_error=c(SE_total_var_lane_dev_high_vis_familiar,SE_total_var_lane_dev_high_vis_unfamiliar,SE_total_var_lane_dev_low_vis_familiar,SE_total_var_lane_dev_low_vis_unfamiliar))
pd <- position_dodge(width = 0.1)

mean_ld_plot <- ggplot(mean_lane_dev_plot_df, aes(x = visibility, y = mean_lane_devs, color = familiarity, group = familiarity)) +
  geom_point(position=pd, size=3) +
  scale_y_continuous(breaks = round(seq(-10, 10, by = 0.5),1))+
  geom_line(position=pd, size=1) +
  geom_errorbar( aes(x=visibility, ymin=mean_lane_devs-standard_error, ymax=mean_lane_devs+standard_error), width=0.1,alpha=0.9,position=pd) +
  labs(x = "Visibility", y = "Mean Lane Deviation (meters)", color = "Track Constancy") +
  scale_x_discrete(labels =c("High", "Low"),expand = c(0, 0.1)) +
  coord_fixed(ratio = 0.3)+
  larger_text_theme(base_size = 12)+
  theme(legend.position = "none")

# Long format
mean_lane_dev_df <- main_df %>%
  select(subject_id, condition,low_vis_mean_lane_dev_10, high_vis_mean_lane_dev_10) %>%
  gather(key = "visibility", value = "mean_lane_dev", low_vis_mean_lane_dev_10, high_vis_mean_lane_dev_10) 

mean_lane_dev.aov <- anova_test(
  data = mean_lane_dev_df, dv = mean_lane_dev, wid = subject_id,
  between = condition, within = visibility
)

get_anova_table(mean_lane_dev.aov)

# Analysis 5: Var Lane Deviation ----------------------------------------------------------------
#if analyzing variance
#high_vis_string_lane_dev = "high_vis_var_lane_dev_10"
#low_vis_string_lane_dev = "low_vis_var_lane_dev_10"
#y_title = "Lane Deviation Variance"

# if analyzing SD
high_vis_string_lane_dev = "high_vis_sd_lane_dev_10"
low_vis_string_lane_dev = "low_vis_sd_lane_dev_10"
y_title = "SD of Lane Deviation (meters)"
main="Standard Deviation of Lane Deviation for Repeated vs Varied Track Groups"

# Create plot of data showing two-way interaction
# relevant columns
total_var_lane_dev_high_vis_familiar = mean(famliar_df[[high_vis_string_lane_dev]])
total_var_lane_dev_high_vis_unfamiliar = mean(unfamiliar_df[[high_vis_string_lane_dev]])
total_var_lane_dev_low_vis_familiar = mean(famliar_df[[low_vis_string_lane_dev]])
total_var_lane_dev_low_vis_unfamiliar = mean(unfamiliar_df[[low_vis_string_lane_dev]])

# Calculate standard error for error bars
SE_total_var_lane_dev_high_vis_familiar = sd(famliar_df[[high_vis_string_lane_dev]])/sqrt(length((famliar_df[[high_vis_string_lane_dev]])))
SE_total_var_lane_dev_high_vis_unfamiliar = sd(unfamiliar_df[[high_vis_string_lane_dev]])/sqrt(length((unfamiliar_df[[high_vis_string_lane_dev]])))
SE_total_var_lane_dev_low_vis_familiar = sd(famliar_df[[low_vis_string_lane_dev]])/sqrt(length((famliar_df[[low_vis_string_lane_dev]])))
SE_total_var_lane_dev_low_vis_unfamiliar = sd(unfamiliar_df[[low_vis_string_lane_dev]])/sqrt(length((unfamiliar_df[[low_vis_string_lane_dev]])))


var_lane_dev_plot_df <- data.frame(stringsAsFactors=TRUE,visibility=c("Low_visibility","Low_visibility","High_visibility","High_visibility"), 
                                   familiarity=c("Constant","Variable","Constant","Variable"), var_lane_devs=c(total_var_lane_dev_low_vis_familiar,total_var_lane_dev_low_vis_unfamiliar,total_var_lane_dev_high_vis_familiar,total_var_lane_dev_high_vis_unfamiliar),
                                   standard_error=c(SE_total_var_lane_dev_high_vis_familiar,SE_total_var_lane_dev_high_vis_unfamiliar,SE_total_var_lane_dev_low_vis_familiar,SE_total_var_lane_dev_low_vis_unfamiliar))

pd <- position_dodge(width = 0.1)

var_ld_plot <- ggplot(var_lane_dev_plot_df, aes(x = visibility, y = var_lane_devs, color = familiarity, group = familiarity)) +
  geom_point(position=pd, size=3) +
  geom_line(position=pd, size=1) +
  geom_errorbar( aes(x=visibility, ymin=var_lane_devs-standard_error, ymax=var_lane_devs+standard_error), width=0.1, alpha=0.9,position=pd) +
  labs(x = "Visibility", y = y_title, color = "Track Exposure") +
  scale_x_discrete(labels =c("High", "Low"),expand = c(0, 0.1)) +
  larger_text_theme(base_size = 12)+
  coord_fixed(ratio = 1.47)+
  theme(legend.position="none")

var_ld_plot

(mean_ld_plot | var_ld_plot) + 
  plot_layout(heights = c(1, 1)) +
  plot_annotation(tag_levels = 'A')

# Long format
var_lane_dev_df <- main_df %>%
  select(subject_id, condition,low_vis_var_lane_dev_10, high_vis_var_lane_dev_10) %>%
  gather(key = "visibility", value = "var_lane_dev", low_vis_var_lane_dev_10, high_vis_var_lane_dev_10) 

var_lane_dev.aov <- anova_test(
  data = var_lane_dev_df, dv = var_lane_dev, wid = subject_id,
  between = condition, within = visibility
)

get_anova_table(var_lane_dev.aov)