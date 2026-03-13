library(ggplot2)
library(tidyverse)

csv_path = "C:\\Users\\graci\\Dropbox\\PAndA\\Thesis Experiment 3\\data\\drawing_scores.csv"
data = read.csv(csv_path,stringsAsFactors=TRUE)

# Create a named vector for segment renaming
segment_labels <- c(
  "Control",
  "Scrambled Landmarks",
  "Scrambled Segments"
)

# Calculate means and 95% CIs for each condition
summary_stats <- data %>%
  group_by(Condition) %>%
  summarise(
    Mean = mean(Score, na.rm = TRUE),
    SD = sd(Score, na.rm = TRUE),
    N = n(),
    SE = SD / sqrt(N),
    CI_Lower = Mean - (1.96 * SE),
    CI_Upper = Mean + (1.96 * SE),
    .groups = 'drop'
  ) %>%
  select(Condition, Mean, CI_Lower, CI_Upper)

print("Summary Statistics: Mean Scores with 95% Confidence Intervals")
print(summary_stats)

model <- aov(Score ~ Condition + Error(Drawing.ID/(Condition)), data = data)
summary(model)

dtw.aov <- anova_test(
  data = data, dv = Score, wid = Drawing.ID,
  between = Condition,effect.size = "pes"
)

# Averaged into three groups
ggplot(data, aes(x = Condition, y = Score, fill = Condition)) +
  stat_summary(
    fun = mean,
    geom = "bar",
    width = 0.6
  ) +
  stat_summary(
    fun.data = mean_cl_normal,
    geom = "errorbar",
    width = 0.2
  ) +
  scale_fill_manual(values = c("control" = "#0000FF", "scrambled_landmarks" = "#FF4040","scrambled_segments" = "#00CD00"), labels = c("control" = "Control Group", "sl" = "Scrambled Landmarks Group", "ss" = "Scrambled Segments Group")) +
  scale_x_discrete(labels = segment_labels) +
  labs(
    x = "Configuration Constancy",
    y = "Mean Accuracy Score"
  ) +
  theme(legend.position = "none",
        panel.grid.major.x = element_blank(),
        plot.title = element_text(size = 20),
        axis.title.x = element_text(size = 30),
        axis.title.y = element_text(size = 30),
        axis.text.x = element_text(size = 20),
        axis.text.y = element_text(size = 30)
  )


# posthoc

library(rstatix)
library(emmeans)
library(dplyr)

# Perform pairwise t-tests with Bonferroni adjustment (for p-values)
posthoc <- data %>%
  pairwise_t_test(
    Score ~ Condition,
    p.adjust.method = "bonferroni"
  )
print(posthoc)

# Now compute emmeans and pairwise comparisons with confidence intervals
fit <- lm(Score ~ Condition, data = data)

emm <- emmeans(fit, specs = "Condition")

# Pairwise comparisons with confidence intervals and Bonferroni correction
pairwise_results <- pairs(emm, adjust = "bonferroni") %>% summary(infer = TRUE)

print(pairwise_results)
