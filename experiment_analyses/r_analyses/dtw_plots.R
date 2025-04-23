library(ggplot2)
library(tidyverse)

csv_path = "C:\\Users\\graci\\Dropbox\\PAndA\\Thesis Experiment 2\\data\\dtw_data.csv"
data = read.csv(csv_path,stringsAsFactors=TRUE)

data$Segments <- factor(data$Segments, levels = c(
  "chicane",
  "triple_s",
  "symmetric_parabolic",
  "traffic_circle",
  "asymmetric_parabolic_2",
  "t_turn",
  "asymmetric_parabolic_1",
  "spiral"
))

# Create a named vector for segment renaming
segment_labels <- c(
  "Chicane",
  "Triple-S",
  "Symm. Parab.",
  "Traffic Circle",
  "Asym. Parab. 1",
  "T-Turn",
  "Asym. Parab. 2",
  "Spiral"
)

# Each segment, each group plotted (2x8 BARS)
ggplot(data, aes(x = Segments, y = Segment.Costs, fill = Condition)) +
  # Bars showing the mean
  stat_summary(
    fun = mean,
    geom = "bar",
    position = position_dodge(width = 0.9),
    width = 0.8
  ) +
  # Error bars showing 95% CI
  stat_summary(
    fun.data = mean_cl_normal,
    geom = "errorbar",
    position = position_dodge(width = 0.9),
    width = 0.2
  ) +
  scale_fill_manual(values = c("familiar" = "#619CFF", "unfamiliar" = "#F8766D")) +
  scale_x_discrete(labels = segment_labels) +
  labs(
    title = "Mean Segment Costs by Segment Type and Condition",
    x = "Segment Type",
    y = "Mean Segment Cost",
    fill = "Condition"
  ) +
  theme_minimal() +
  theme(
    panel.grid.major.x = element_blank(),
    legend.position = "top"
  )

# Averaged into two groups
ggplot(data, aes(x = Condition, y = Segment.Costs, fill = Condition)) +
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
  scale_fill_manual(values = c("familiar" = "#619CFF", "unfamiliar" = "#F8766D")) +
  labs(
    title = "Mean Segment Cost by Condition",
    x = "Condition",
    y = "Mean Segment Cost"
  ) +
  theme_minimal() +
  theme(
    legend.position = "none"
  )


# Long format
model <- aov(Segment.Costs ~ Condition * Segments + Error(subject_id/(Condition*Segments)), data = data)
summary(model)

mean_lane_dev.aov <- anova_test(
  data = data, dv = Segment.Costs, wid = subject_id,
  between = Condition, within = Segments,effect.size = "pes"
)