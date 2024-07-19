library(dplyr)
library(ggplot2)
library(tidyr)
library(tidyverse)
library(ggpubr)
library(rstatix)

# for all track pieces (excluding straight pieces)
csv_path = "C:\\Users\\graci\\Dropbox\\PAndA\\Thesis Experiment 1\\data\\main_data\\ultimate_master_variable_df.csv"

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

sd_famliar_df <- famliar_df[ , grepl( "sd" , names( famliar_df ) ) ]
sd_unfamiliar_df <- unfamiliar_df[ , grepl( "sd" , names( unfamiliar_df ) ) ]

# Analysis 1: Mean Speed ----------------------------------------------------------------

# Test for validity ---------------------------------------------------------------------
# Create plot of data showing two-way interaction
# relevant columns
total_mean_speed_high_vis_familiar = mean(famliar_df[["high_vis_mean_speed_10"]])
total_mean_speed_high_vis_unfamiliar = mean(unfamiliar_df[["high_vis_mean_speed_10"]])
total_mean_speed_low_vis_familiar = mean(famliar_df[["low_vis_mean_speed_10"]])
total_mean_speed_low_vis_unfamiliar = mean(unfamiliar_df[["low_vis_mean_speed_10"]])

# Calculate standard error for error bars
SE_total_mean_speed_high_vis_familiar = sd(famliar_df[["high_vis_mean_speed_10"]])/sqrt(length((famliar_df[["high_vis_mean_speed_10"]])))
SE_total_mean_speed_high_vis_unfamiliar = sd(unfamiliar_df[["high_vis_mean_speed_10"]])/sqrt(length((unfamiliar_df[["high_vis_mean_speed_10"]])))
SE_total_mean_speed_low_vis_familiar = sd(famliar_df[["low_vis_mean_speed_10"]])/sqrt(length((famliar_df[["low_vis_mean_speed_10"]])))
SE_total_mean_speed_low_vis_unfamiliar = sd(unfamiliar_df[["low_vis_mean_speed_10"]])/sqrt(length((unfamiliar_df[["low_vis_mean_speed_10"]])))

main = "Mean Speed for Repeated vs Varied Track Groups"

mean_speed_plot_df <- data.frame(stringsAsFactors=TRUE,visibility=c("Low_visibility","Low_visibility","High_visibility","High_visibility"), 
                                 familiarity=c("Repeated","Varied","Repeated","Varied"), mean_speeds=c(total_mean_speed_low_vis_familiar,total_mean_speed_low_vis_unfamiliar,total_mean_speed_high_vis_familiar,total_mean_speed_high_vis_unfamiliar),
                                 standard_error=c(SE_total_mean_speed_high_vis_familiar,SE_total_mean_speed_high_vis_unfamiliar,SE_total_mean_speed_low_vis_familiar,SE_total_mean_speed_low_vis_unfamiliar))
pd <- position_dodge(width = 0.1)

ggplot(mean_speed_plot_df, aes(x = visibility, y = mean_speeds, color = familiarity, group = familiarity)) +
  geom_point(position=pd) +
  geom_line(position=pd) +
  geom_errorbar( aes(x=visibility, ymin=mean_speeds-standard_error, ymax=mean_speeds+standard_error), width=0.4, color = "black", alpha=0.9,position=pd) +
  labs(x = "Visibility", y = "Mean Speed (m/s)", color = "Track Exposure")+
  ggtitle(main)+
  theme(plot.title = element_text(hjust = 0.5))

# Long format
mean_speed_df <- main_df %>%
  select(subject_id, condition,low_vis_mean_speed_10, high_vis_mean_speed_10) %>%
  gather(key = "visibility", value = "mean_speed", low_vis_mean_speed_10, high_vis_mean_speed_10) 

mean_speed.aov <- anova_test(
  data = mean_speed_df, dv = mean_speed, wid = subject_id,
  between = condition, within = visibility
)

get_anova_table(mean_speed.aov)

# Analysis 2: Var Speed ----------------------------------------------------------------

#if analyzing variance
# high_vis_string_speed = "high_vis_var_speed_10"
# low_vis_string_speed = "low_vis_var_speed_10"
# y_title = "Speed Variance"
# main="Speed Variance in Trial 10 (m/s^2)"

# if analyzing SD
high_vis_string_speed = "high_vis_sd_speed_10"
low_vis_string_speed = "low_vis_sd_speed_10"
y_title = "SD of Speed (m/s)"
main="Standard Deviation of Speed for Repeated vs Varied Track Groups"


# Create plot of data showing two-way interaction
# relevant columns
total_var_speed_high_vis_familiar = mean(famliar_df[[high_vis_string_speed]])
total_var_speed_high_vis_unfamiliar = mean(unfamiliar_df[[high_vis_string_speed]])
total_var_speed_low_vis_familiar = mean(famliar_df[[low_vis_string_speed]])
total_var_speed_low_vis_unfamiliar = mean(unfamiliar_df[[low_vis_string_speed]])

# Calculate standard error for error bars
SE_total_var_speed_high_vis_familiar = sd(famliar_df[[high_vis_string_speed]])/sqrt(length((famliar_df[[high_vis_string_speed]])))
SE_total_var_speed_high_vis_unfamiliar = sd(unfamiliar_df[[high_vis_string_speed]])/sqrt(length((unfamiliar_df[[high_vis_string_speed]])))
SE_total_var_speed_low_vis_familiar = sd(famliar_df[[low_vis_string_speed]])/sqrt(length((famliar_df[[low_vis_string_speed]])))
SE_total_var_speed_low_vis_unfamiliar = sd(unfamiliar_df[[low_vis_string_speed]])/sqrt(length((unfamiliar_df[[low_vis_string_speed]])))


var_speed_plot_df <- data.frame(stringsAsFactors=TRUE,visibility=c("Low_visibility","Low_visibility","High_visibility","High_visibility"), 
                                 familiarity=c("Repeated","Varied","Repeated","Varied"), var_speeds=c(total_var_speed_low_vis_familiar,total_var_speed_low_vis_unfamiliar,total_var_speed_high_vis_familiar,total_var_speed_high_vis_unfamiliar),
                                standard_error=c(SE_total_var_speed_high_vis_familiar,SE_total_var_speed_high_vis_unfamiliar,SE_total_var_speed_low_vis_familiar,SE_total_var_speed_low_vis_unfamiliar))

pd <- position_dodge(width = 0.1)
ggplot(var_speed_plot_df, aes(x = visibility, y = var_speeds, color = familiarity, group = familiarity)) +
  geom_point(position=pd) +
  geom_line(position=pd) +
  geom_errorbar( aes(x=visibility, ymin=var_speeds-standard_error, ymax=var_speeds+standard_error), width=0.4, color = "black", alpha=0.9,position=pd) +
  labs(x = "Visibility", y = y_title, color = "Track Exposure") +
  ggtitle(main)+
  theme(plot.title = element_text(hjust = 0.5))

# Long format
var_speed_df <- main_df %>%
  select(subject_id, condition,low_vis_var_speed_10, high_vis_var_speed_10) %>%
  gather(key = "visibility", value = "var_speed", low_vis_var_speed_10, high_vis_var_speed_10) 

var_speed.aov <- anova_test(
  data = var_speed_df, dv = var_speed, wid = subject_id,
  between = condition, within = visibility
)

get_anova_table(var_speed.aov)

# Analysis 3: Var Steering ----------------------------------------------------------------

#if analyzing variance
# high_vis_string_steering = "high_vis_var_steering_10"
# low_vis_string_steering = "low_vis_var_steering_10"
# y_title = "Steering Variance"

# if analyzing SD
high_vis_string_steering = "high_vis_sd_steering_10"
low_vis_string_steering = "low_vis_sd_steering_10"
y_title = "SD of Steering Angle (degrees)"
main="Standard Deviation of Steering Angle for Repeated vs Varied Track Groups"


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
                                familiarity=c("Repeated","Varied","Repeated","Varied"), var_steering=c(total_var_steering_low_vis_familiar,total_var_steering_low_vis_unfamiliar,total_var_steering_high_vis_familiar,total_var_steering_high_vis_unfamiliar),
                                standard_error=c(SE_total_var_steering_high_vis_familiar,SE_total_var_steering_high_vis_unfamiliar,SE_total_var_steering_low_vis_familiar,SE_total_var_steering_low_vis_unfamiliar))
pd <- position_dodge(width = 0.1)

ggplot(var_steering_plot_df, aes(x = visibility, y = var_steering, color = familiarity, group = familiarity)) +
  geom_point(position=pd) +
  geom_line(position=pd) +
  geom_errorbar( aes(x=visibility, ymin=var_steering-standard_error, ymax=var_steering+standard_error), width=0.4, color = "black", alpha=0.9,position=pd) +
  labs(x = "Visibility", y = y_title, color = "Track Exposure")+
  ggtitle(main)+
  theme(plot.title = element_text(hjust = 0.5))

# Long format
var_steering_df <- main_df %>%
  select(subject_id, condition,low_vis_var_steering_10, high_vis_var_steering_10) %>%
  gather(key = "visibility", value = "var_steering", low_vis_var_steering_10, high_vis_var_steering_10) 

var_steering.aov <- anova_test(
  data = var_steering_df, dv = var_steering, wid = subject_id,
  between = condition, within = visibility
)

get_anova_table(var_steering.aov)

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
                                 familiarity=c("Repeated","Varied","Repeated","Varied"), mean_lane_devs=c(total_mean_lane_dev_low_vis_familiar,total_mean_lane_dev_low_vis_unfamiliar,total_mean_lane_dev_high_vis_familiar,total_mean_lane_dev_high_vis_unfamiliar),
                                 standard_error=c(SE_total_var_lane_dev_high_vis_familiar,SE_total_var_lane_dev_high_vis_unfamiliar,SE_total_var_lane_dev_low_vis_familiar,SE_total_var_lane_dev_low_vis_unfamiliar))
pd <- position_dodge(width = 0.1)

ggplot(mean_lane_dev_plot_df, aes(x = visibility, y = mean_lane_devs, color = familiarity, group = familiarity)) +
  geom_point(position=pd) +
  scale_y_continuous(breaks = round(seq(-10, 10, by = 0.5),1))+
  geom_line(position=pd) +
  geom_errorbar( aes(x=visibility, ymin=mean_lane_devs-standard_error, ymax=mean_lane_devs+standard_error), width=0.4, color = "black", alpha=0.9,position=pd) +
  labs(x = "Visibility", y = "Lane Deviation (meters)", color = "Track Exposure")+
  ggtitle(main)+
  theme(plot.title = element_text(hjust = 0.5))

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
                                    familiarity=c("Repeated","Varied","Repeated","Varied"), var_lane_devs=c(total_var_lane_dev_low_vis_familiar,total_var_lane_dev_low_vis_unfamiliar,total_var_lane_dev_high_vis_familiar,total_var_lane_dev_high_vis_unfamiliar),
                                   standard_error=c(SE_total_var_lane_dev_high_vis_familiar,SE_total_var_lane_dev_high_vis_unfamiliar,SE_total_var_lane_dev_low_vis_familiar,SE_total_var_lane_dev_low_vis_unfamiliar))

pd <- position_dodge(width = 0.1)

ggplot(var_lane_dev_plot_df, aes(x = visibility, y = var_lane_devs, color = familiarity, group = familiarity)) +
  geom_point(position=pd) +
  geom_line(position=pd) +
  geom_errorbar( aes(x=visibility, ymin=var_lane_devs-standard_error, ymax=var_lane_devs+standard_error), width=0.4, color = "black", alpha=0.9,position=pd) +
  labs(x = "Visibility", y = y_title, color = "Track Exposure")+
  ggtitle(main)+
  theme(plot.title = element_text(hjust = 0.5))

# Long format
var_lane_dev_df <- main_df %>%
  select(subject_id, condition,low_vis_var_lane_dev_10, high_vis_var_lane_dev_10) %>%
  gather(key = "visibility", value = "var_lane_dev", low_vis_var_lane_dev_10, high_vis_var_lane_dev_10) 

var_lane_dev.aov <- anova_test(
  data = var_lane_dev_df, dv = var_lane_dev, wid = subject_id,
  between = condition, within = visibility
)

get_anova_table(var_lane_dev.aov)