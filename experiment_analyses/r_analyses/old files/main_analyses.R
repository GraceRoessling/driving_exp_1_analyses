library(dplyr)
library(ggplot2)
library(tidyr)
library(tidyverse)
library(ggpubr)
library(rstatix)
library(gridExtra)
library(patchwork)

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

# Function to create a larger text theme
larger_text_theme <- function(base_size = 14) {
  theme(base_size = base_size) +
    theme(
      axis.title = element_text(size = rel(2)),
      axis.text = element_text(size = rel(2)),
      plot.title = element_text(size = rel(2.5), face = "bold"),
      legend.title = element_text(size = rel(2.1)),
      legend.text = element_text(size = rel(2))
      )
    
}

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
                                 familiarity=c("Constant","Variable","Constant","Variable"), mean_speeds=c(total_mean_speed_low_vis_familiar,total_mean_speed_low_vis_unfamiliar,total_mean_speed_high_vis_familiar,total_mean_speed_high_vis_unfamiliar),
                                 standard_error=c(SE_total_mean_speed_high_vis_familiar,SE_total_mean_speed_high_vis_unfamiliar,SE_total_mean_speed_low_vis_familiar,SE_total_mean_speed_low_vis_unfamiliar))

pd <- position_dodge(width = 0.1)

mean_speed_plot <- ggplot(mean_speed_plot_df, aes(x = visibility, y = mean_speeds, color = familiarity, group = familiarity)) +
  geom_point(position=pd,size=5) +
  geom_line(position=pd, size=1.04) +
  geom_errorbar( aes(x=visibility, ymin=mean_speeds-standard_error, ymax=mean_speeds+standard_error), width=0.1, alpha=0.9,position=pd) +
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
                                 familiarity=c("Constant","Variable","Constant","Variable"), var_speeds=c(total_var_speed_low_vis_familiar,total_var_speed_low_vis_unfamiliar,total_var_speed_high_vis_familiar,total_var_speed_high_vis_unfamiliar),
                                standard_error=c(SE_total_var_speed_high_vis_familiar,SE_total_var_speed_high_vis_unfamiliar,SE_total_var_speed_low_vis_familiar,SE_total_var_speed_low_vis_unfamiliar))

pd <- position_dodge(width = 0.1)
var_speed_plot = ggplot(var_speed_plot_df, aes(x = visibility, y = var_speeds, color = familiarity, group = familiarity)) +
  geom_point(position=pd,size = 5) +
  geom_line(position=pd, size=1) +
  geom_errorbar( aes(x=visibility, ymin=var_speeds-standard_error, ymax=var_speeds+standard_error), width=0.1, alpha=0.9,position=pd) +
  labs(x = "Visibility", y = y_title, color = "Track Constancy") +
  scale_x_discrete(labels = c("High", "Low"),expand = c(0, 0.2)) +
  coord_fixed(ratio = 0.9)+
  larger_text_theme(base_size = 1.5)+
  theme(legend.position = "none")+
  theme(plot.margin = unit(c(0.15, 0.15, 0.15, 0.15), 
                           "inches")) 

var_speed_plot

(mean_speed_plot | var_speed_plot) + 
  plot_layout(heights = c(1, 1)) +
  plot_annotation(tag_levels = 'A')


# Long format
var_speed_df <- main_df %>%
  select(subject_id, condition,low_vis_var_speed_10, high_vis_var_speed_10) %>%
  gather(key = "visibility", value = "var_speed", low_vis_var_speed_10, high_vis_var_speed_10) 

var_speed.aov <- anova_test(
  data = var_speed_df, dv = var_speed, wid = subject_id,
  between = condition, within = visibility
)

get_anova_table(var_speed.aov)


