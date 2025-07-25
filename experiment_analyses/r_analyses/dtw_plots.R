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
  "Traffic Circ.",
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
  scale_x_discrete(labels = c("familiar" = "Constant", "unfamiliar" = "Variable")) +
  labs(
    title = "Mean Segment Cost by Condition",
    x = "Track Constancy",
    y = "Mean Segment Cost"
  ) +
  theme(legend.position = "none",
        panel.grid.major.x = element_blank(),
        plot.title = element_text(size = 20),
        axis.title.x = element_text(size = 30),
        axis.title.y = element_text(size = 30),
        axis.text.x = element_text(size = 15),
        axis.text.y = element_text(size = 20)
  )

model <- aov(Segment.Costs ~ Condition * Segments + Error(subject_id/(Condition * Segments)), data = data)
summary(model)

dtw.aov <- anova_test(
  data = data, dv = Segment.Costs, wid = subject_id,
  between = Condition, within = Segments,effect.size = "pes"
)


#post hoc

library(emmeans)
library(dplyr)

# Get estimated marginal means for Segments
emm <- emmeans(model, ~ Segments)

# Pairwise comparisons with Bonferroni correction, requesting confidence intervals
pairwise_comparisons <- pairs(emm, adjust = "bonferroni")

# Convert to data frame and include confidence intervals and p-values
summary_comparisons <- summary(pairwise_comparisons, infer = c(TRUE, TRUE))

# Check the names of the columns to know what is available
print(names(summary_comparisons))

# Usually the columns for confidence intervals are called "lower.CL" and "upper.CL"
# Let's rename for easier use:
summary_comparisons <- summary_comparisons %>%
  rename(
    conf.low = lower.CL,
    conf.high = upper.CL
  )

# Now get means and SDs by segment
segment_stats <- data %>%
  group_by(Segments) %>%
  summarise(
    mean_cost = mean(Segment.Costs, na.rm = TRUE),
    sd_cost = sd(Segment.Costs, na.rm = TRUE)
  )

# Extract segment names from contrast
summary_comparisons <- summary_comparisons %>%
  mutate(
    Segment1 = sub(" -.*", "", contrast),
    Segment2 = sub(".*- ", "", contrast)
  )

# Join means and SDs for each segment in the comparison
sig_comparisons <- summary_comparisons %>%
  filter(p.value < 0.05) %>%
  left_join(segment_stats, by = c("Segment1" = "Segments")) %>%
  rename(mean1 = mean_cost, sd1 = sd_cost) %>%
  left_join(segment_stats, by = c("Segment2" = "Segments")) %>%
  rename(mean2 = mean_cost, sd2 = sd_cost) %>%
  select(Segment1, mean1, sd1, Segment2, mean2, sd2, estimate, conf.low, conf.high, p.value)

print(sig_comparisons)

