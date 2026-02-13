library(ggplot2)
library(tidyverse)
library(emmeans)
library(dplyr)
library(lme4)
library(gridExtra)
csv_path = "C:\\Users\\graci\\Dropbox\\PAndA\\Thesis Experiment 2\\data\\dtw_scores_per_track_segment_recovered.csv"
data = read.csv(csv_path,stringsAsFactors=TRUE)

colnames(data) <- c("subject_id", "Segments", "Condition", "Segment.Costs")

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

segment_order <- c(
  "chicane",
  "triple_s",
  "symmetric_parabolic",
  "traffic_circle",
  "asymmetric_parabolic_2",
  "t_turn",
  "asymmetric_parabolic_1",
  "spiral"
)

# Factor (for labeling, optional)
data$Segments <- factor(data$Segments, levels = segment_order)

# Numeric/ordinal version for modeling
data$Segments_num <- as.numeric(data$Segments)  # 1 = chicane, 2 = triple_s, ..., 8 = spiral


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

# Linear mixed effects model =======================================

lmm_model <- lmer(Segment.Costs ~ Segments * Condition + (1 | subject_id), data = data)
summary(lmm_model)

# Post-hoc comparisons for the interaction
emm_lmm <- emmeans(lmm_model, ~ Segments * Condition)

# Pairwise comparisons with Bonferroni correction
pairwise_lmm <- pairs(emm_lmm, adjust = "bonferroni")
summary_lmm_comparisons <- summary(pairwise_lmm, infer = c(TRUE, TRUE))

# Filter for significant comparisons (p < 0.05)
sig_lmm_comparisons <- summary_lmm_comparisons %>%
  filter(p.value < 0.05) %>%
  select(contrast, estimate, conf.low = lower.CL, conf.high = upper.CL, p.value)

print(sig_lmm_comparisons)

# Linear regression models with increasing complexity =======================================

# Model 1a: Simple linear regression (baseline)
model_1a <- lm(Segment.Costs ~ Segments_num * Condition, data = data)
cat("\n=== Model 1a: Simple Linear Regression ===\n")
print(summary(model_1a))

# Model 1b: Linear mixed effects with random intercepts
model_1b <- lmer(Segment.Costs ~ Segments_num * Condition + (1 | subject_id), data = data)
cat("\n=== Model 1b: Mixed Effects (Random Intercepts) ===\n")
print(summary(model_1b))

# Model 1c: Linear mixed effects with random intercepts and random slopes
model_1c <- lmer(Segment.Costs ~ Segments_num * Condition + (1 + Segments_num || subject_id), data = data)
cat("\n=== Model 1c: Mixed Effects (Random Intercepts + Random Slopes) ===\n")
print(summary(model_1c))

# Generate predictions for plotting
data$pred_1a <- predict(model_1a, newdata = data, re.form = NA)
data$pred_1b <- predict(model_1b, newdata = data, re.form = NA)
data$pred_1c <- predict(model_1c, newdata = data, re.form = NA)

# Create figure with three plots
p1 <- ggplot(data, aes(x = Segment.Costs, y = Segment.Costs, color = Condition)) +
  geom_point(alpha = 0.5, size = 2) +
  geom_line(aes(y = pred_1a), color = "black", linewidth = 1, alpha = 0.7) +
  scale_color_manual(values = c("familiar" = "#0000FF", "unfamiliar" = "#FF4040")) +
  labs(
    title = "Model 1a: Simple Linear Regression",
    x = "DTW Score",
    y = "Predicted DTW Score",
    color = "Condition"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(size = 14, face = "bold"),
    axis.title = element_text(size = 12),
    legend.position = "bottom"
  )

p2 <- ggplot(data, aes(x = Segment.Costs, y = Segment.Costs, color = Condition)) +
  geom_point(alpha = 0.5, size = 2) +
  geom_line(aes(y = pred_1b), color = "black", linewidth = 1, alpha = 0.7) +
  scale_color_manual(values = c("familiar" = "#0000FF", "unfamiliar" = "#FF4040")) +
  labs(
    title = "Model 1b: Random Intercepts",
    x = "DTW Score",
    y = "Predicted DTW Score",
    color = "Condition"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(size = 14, face = "bold"),
    axis.title = element_text(size = 12),
    legend.position = "bottom"
  )

p3 <- ggplot(data, aes(x = Segment.Costs, y = Segment.Costs, color = Condition)) +
  geom_point(alpha = 0.5, size = 2) +
  geom_line(aes(y = pred_1c, group = subject_id), color = "black", linewidth = 1, alpha = 0.3) +
  scale_color_manual(values = c("familiar" = "#0000FF", "unfamiliar" = "#FF4040")) +
  labs(
    title = "Model 1c: Random Intercepts + Random Slopes",
    x = "DTW Score",
    y = "Predicted DTW Score",
    color = "Condition"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(size = 14, face = "bold"),
    axis.title = element_text(size = 12),
    legend.position = "bottom"
  )

# Arrange the three plots
gridExtra::grid.arrange(p1, p2, p3, ncol = 3)

