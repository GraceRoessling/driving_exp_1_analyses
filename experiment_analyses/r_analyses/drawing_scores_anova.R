library(ggplot2)
library(tidyverse)

csv_path = "C:\\Users\\graci\\Dropbox\\PAndA\\Thesis Experiment 2\\data\\drawing_scores.csv"
data = read.csv(csv_path,stringsAsFactors=TRUE)

# Create a named vector for segment renaming
segment_labels <- c(
  "Constant",
  "Variable",

)


model <- aov(Normalized.Score ~ Condition + Error(Drawing.ID/(Condition)), data = data)
summary(model)

dtw.aov <- anova_test(
  data = data, dv = Normalized.Score, wid = Drawing.ID,
  between = Condition,effect.size = "pes"
)

# Averaged into three groups
ggplot(data, aes(x = Condition, y = Normalized.Score, fill = Condition)) +
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
    Normalized.Score ~ Condition,
    p.adjust.method = "bonferroni"
  )
print(posthoc)

# Now compute emmeans and pairwise comparisons with confidence intervals
fit <- lm(Normalized.Score ~ Condition, data = data)

emm <- emmeans(fit, specs = "Condition")

# Pairwise comparisons with confidence intervals and Bonferroni correction
pairwise_results <- pairs(emm, adjust = "bonferroni") %>% summary(infer = TRUE)

print(pairwise_results)
