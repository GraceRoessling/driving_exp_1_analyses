
# Mean speed --------------------------------------------------------
mean_speed_columns <- grepl("avg_mean_speed|condition", colnames(main_df))
mean_speed_filtered_df <- main_df[, mean_speed_columns]

long_data <- mean_speed_filtered_df %>%
  pivot_longer(cols = starts_with("avg_mean_speed"),
               names_to = "column_name",
               values_to = "value")

mean_values <- long_data %>%
  group_by(condition, column_name) %>%
  summarise(
    ci = list(calculate_CI(cur_data(), "value")),
    .groups = "drop"
  ) %>%
  unnest_wider(ci)



mean_values <- mean_values %>%
  mutate(column_name = str_extract(column_name, "\\d+$"))
mean_values <- reorder_mean_values(mean_values)

mean_values <- mean_values %>%
  mutate(column_name = factor(as.numeric(column_name), levels = 1:10))

# Modify condition labels
mean_values$condition <- factor(mean_values$condition,
                                levels = c("familiar", "unfamiliar"),
                                labels = c("Constant Track", "Variable Track"))

within_mean_speed_plot <- ggplot(mean_values, aes(x = column_name, y = mean, color = condition, group = condition)) +
  geom_point(position=pd_for_within,size = 5) +
  geom_line(position=pd_for_within,size = line_size) +
  geom_errorbar(aes(ymin = ci_lower, ymax = ci_upper), width = 0.2,position=pd_for_within) +
  labs(x = "Trials", y = "Mean Speed (m/s)", color = "Track Constancy", title = "Mean Speed Across Trials") +
  scale_x_discrete(labels = 1:10) +
  scale_color_manual(values = c("Constant Track" = "#0000FF", "Variable Track" = "#FF4040")) +  # Replace with actual condition levels
  larger_text_theme(base_size = 12) +
  theme(
    legend.position = "none",
    plot.title = element_text(size = 20),
    axis.title.x = element_text(size = 40),
    axis.title.y = element_text(size = 20),
    axis.text.x = element_text(size = 30),
    axis.text.y = element_text(size = 30)
  )

within_mean_speed_plot



# Required libraries
library(tidyverse)
library(afex)       # For rmANOVA
library(emmeans)    # For post hoc contrasts, if needed

# --- Step 1: Prepare long-format data for RM-ANOVA ---
long_data_anova <- main_df %>%
  select(subject_id, condition, starts_with("avg_mean_speed")) %>%
  pivot_longer(
    cols = starts_with("avg_mean_speed"),
    names_to = "trial",
    names_pattern = "avg_mean_speed_(\\d+)",  # Extract trial number
    values_to = "mean_speed"
  ) %>%
  mutate(
    trial = as.factor(trial),
    condition = factor(condition, levels = c("familiar", "unfamiliar"),
                       labels = c("Constant Track", "Variable Track"))
  )

# --- Step 2: Run repeated-measures ANOVA ---
anova_result <- aov_ez(
  id = "subject_id",
  dv = "mean_speed",
  within = "trial",
  between = "condition",
  data = long_data_anova,
  type = 3,
  return = "afex_aov",
  es = "pes"  # <-- Change effect size to partial eta squared
)

# --- Step 3: Print summary ---
print(anova_result)

# --- Optional: Test simple effects or trend contrasts ---
# e.g., Pairwise comparisons at each trial (if interaction is significant)
emmeans(anova_result, ~ condition | trial) %>%
  pairs(adjust = "bonferroni")


# --- Step 4: Linear Mixed Model (LMM) Analysis ---
library(lme4)
library(lmerTest)  # for p-values
library(sjPlot)    # optional: for easy model summaries and plots

# Convert trial to numeric for linear slope modeling
long_data_anova <- long_data_anova %>%
  mutate(trial_numeric = as.numeric(as.character(trial)))

# Fit the model
lmm_model <- lmer(mean_speed ~ trial_numeric * condition + (trial_numeric | subject_id), data = long_data_anova)

# Model summary with fixed effects and p-values
summary(lmm_model)

# Optional: ANOVA-style table of fixed effects
anova(lmm_model, type = 3)

# Optional: Plot model estimates
plot_model(lmm_model, type = "pred", terms = c("trial_numeric", "condition"))







# SD of Speed ------------------------------------------------------------------------------------
sd_speed_columns <- grepl("avg_sd_speed|condition", colnames(main_df))
sd_speed_df <- main_df[, sd_speed_columns]

long_data <- sd_speed_df %>%
  pivot_longer(cols = starts_with("avg_sd_speed"),
               names_to = "column_name",
               values_to = "value")

mean_values <- long_data %>%
  group_by(condition, column_name) %>%
  summarise(
    ci = list(calculate_CI(cur_data(), "value")),
    .groups = "drop"
  ) %>%
  unnest_wider(ci)

# Modify condition labels
mean_values$condition <- factor(mean_values$condition,
                                levels = c("familiar", "unfamiliar"),
                                labels = c("Constant Track", "Variable Track"))

within_sd_speed_plot <- ggplot(mean_values, aes(x = column_name, y = mean, color = condition, group = condition)) +
  geom_point(position=pd_for_within,size = 5) +
  geom_line(position=pd_for_within, size=line_size) +
  geom_errorbar(aes(ymin = ci_lower, ymax = ci_upper), width = 0.2,position=pd_for_within) +
  labs(x = "Trials", y = "SD of Speed (m/s)", color = "Track Constancy") +
  scale_x_discrete(labels = 1:10) +
  scale_color_manual(values = c("Constant Track" = "#0000FF", "Variable Track" = "#FF4040")) +  # Replace with actual condition levels
  larger_text_theme(base_size = 12) +
  theme(
    legend.position = "none",
    plot.title = element_text(size = 20),
    axis.title.x = element_text(size = 40),
    axis.title.y = element_text(size = 20),
    axis.text.x = element_text(size = 30),
    axis.text.y = element_text(size = 30)
  )

#within_mean_speed_plot / within_sd_speed_plot

(within_mean_speed_plot | within_sd_speed_plot) + 
  plot_layout(heights = c(1, 1)) 


# Required libraries
library(tidyverse)
library(afex)       # For rmANOVA
library(emmeans)    # For post hoc contrasts, if needed

# --- Step 1: Prepare long-format data for RM-ANOVA ---
long_data_anova <- main_df %>%
  select(subject_id, condition, starts_with("avg_sd_speed")) %>%
  pivot_longer(
    cols = starts_with("avg_sd_speed"),
    names_to = "trial",
    names_pattern = "avg_sd_speed_(\\d+)",  # Extract trial number
    values_to = "sd_speed"
  ) %>%
  mutate(
    trial = as.factor(trial),
    condition = factor(condition, levels = c("familiar", "unfamiliar"),
                       labels = c("Constant Track", "Variable Track"))
  )

# --- Step 2: Run repeated-measures ANOVA ---
anova_result <- aov_ez(
  id = "subject_id",
  dv = "sd_speed",
  within = "trial",
  between = "condition",
  data = long_data_anova,
  type = 3,
  return = "afex_aov",
  es = "pes"  # <-- Change effect size to partial eta squared
)

# --- Step 3: Print summary ---
print(anova_result)

# --- Optional: Test simple effects or trend contrasts ---
# e.g., Pairwise comparisons at each trial (if interaction is significant)
emmeans(anova_result, ~ condition | trial) %>%
  pairs(adjust = "bonferroni")




