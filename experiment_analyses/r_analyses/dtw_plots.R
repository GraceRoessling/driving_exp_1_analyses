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
  scale_fill_manual(values = c("familiar" = "#0000FF", "unfamiliar" = "#FF4040")) +
  scale_x_discrete(labels = segment_labels) +
  labs(
    title = "Mean Segment Costs by Segment Type and Condition",
    x = "Segment",
    y = "Mean DTW Cost",
    fill = "Condition"
  ) +
  theme(legend.position = "none",
    panel.grid.major.x = element_blank(),
    plot.title = element_text(size = 20),
    axis.title.x = element_text(size = 30),
    axis.title.y = element_text(size = 30),
    axis.text.x = element_text(size = 20),
    axis.text.y = element_text(size = 30)
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
  scale_fill_manual(values = c("familiar" = "#0000FF", "unfamiliar" = "#FF4040"), labels = c("familiar" = "Constant Track", "unfamiliar" = "Variable Track")) +
  labs(
    title = "Mean Segment Cost by Condition",
    x = "Condition",
    y = "Mean Segment Cost"
  ) +
  theme_minimal() +
  theme(
    legend.position = "none"
  )


model <- aov(Segment.Costs ~ Condition * Segments + Error(subject_id/(Condition * Segments)), data = data)
summary(model)

dtw.aov <- anova_test(
  data = data, dv = Segment.Costs, wid = subject_id,
  between = Condition, within = Segments,effect.size = "pes"
)