# Within SD Steering analysis ------------------------------------------------------------------------
sd_steering_columns <- grepl("avg_sd_steering|condition", colnames(main_df))
sd_steering_df <- main_df[, sd_steering_columns]

long_data <- sd_steering_df %>%
  pivot_longer(cols = starts_with("avg_sd_steering"),
               names_to = "column_name",
               values_to = "value")

mean_values <- long_data %>%
  group_by(condition, column_name) %>%
  summarise(
    mean_value = mean(value, na.rm = TRUE),
    se = sd(value, na.rm = TRUE) / sqrt(n())
  ) %>%
  ungroup()

# Modify condition labels
mean_values$condition <- factor(mean_values$condition,
                                levels = c("familiar", "unfamiliar"),
                                labels = c("Constant Track", "Variable Track"))

mean_values <- mean_values %>%
  mutate(column_name = str_extract(column_name, "\\d+$"))
mean_values <- reorder_mean_values(mean_values)

mean_values <- mean_values %>%
  mutate(column_name = factor(as.numeric(column_name), levels = 1:10))


ggplot(mean_values, aes(x = column_name, y = mean_value, color = condition, group = condition)) +
  geom_point(position=pd_for_within,size = geom_point_size) +
  geom_line(position=pd_for_within, size=line_size) +
  geom_errorbar(aes(ymin = mean_value - se, ymax = mean_value + se), width = 0.2,position=pd_for_within) +
  labs(x = "Trials", y = "SD of Steering (degrees)", color = "Track Constancy") +
  coord_fixed(ratio = 1.3)+
  larger_text_theme(base_size = 12) +
  theme(legend.position = "none")

# Check data ----------------------------------------------------
sd_familiar_df <- sd_steering_df %>% filter(!grepl('unfamiliar', condition)) # if "unfamiliar" is in the row, take it out
sd_unfamiliar_df <- sd_steering_df %>% filter(grepl('unfamiliar', condition)) # if "unfamiliar" is in the row, put it in
familiar_sd_values_list = sd_familiar_df[["avg_sd_steering_10"]]
unfamiliar_sd_values_list = sd_unfamiliar_df[["avg_sd_steering_10"]]

mean(familiar_sd_values_list)
mean(unfamiliar_sd_values_list)


