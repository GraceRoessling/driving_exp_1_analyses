library(ggplot2)
library(tidyverse)

csv_path = "C:\\Users\\graci\\Dropbox\\PAndA\\Thesis Experiment 2\\data\\drawing_scores.csv"
data = read.csv(csv_path,stringsAsFactors=TRUE)

# Remap familiar/unfamiliar to constant/variable
data$condition <- recode(data$condition, "familiar" = "constant", "unfamiliar" = "variable")

# Create a named vector for segment renaming
segment_labels <- c(
  "Constant",
  "Variable"
)

# If needed, ensure 'Condition' is a factor
data$condition <- as.factor(data$condition)

# Conduct independent t-test
t_test_result <- t.test(Score ~ condition, data = data, var.equal = TRUE)

# Print t-test results
print(t_test_result)

# Calculate 95% CI for each group
constant_data <- data$Score[data$condition == "constant"]
variable_data <- data$Score[data$condition == "variable"]

constant_ci <- t.test(constant_data)$conf.int
variable_ci <- t.test(variable_data)$conf.int

cat("\n95% Confidence Intervals by Group:\n")
cat("Constant group: [", round(constant_ci[1], 3), ", ", round(constant_ci[2], 3), "]\n", sep = "")
cat("Variable group: [", round(variable_ci[1], 3), ", ", round(variable_ci[2], 3), "]\n\n", sep = "")

# Calculate Cohen's d
mean_constant <- mean(constant_data, na.rm = TRUE)
mean_variable <- mean(variable_data, na.rm = TRUE)
sd_constant <- sd(constant_data, na.rm = TRUE)
sd_variable <- sd(variable_data, na.rm = TRUE)
n_constant <- length(constant_data)
n_variable <- length(variable_data)

# Pooled standard deviation
pooled_sd <- sqrt(((n_constant - 1) * sd_constant^2 + (n_variable - 1) * sd_variable^2) / (n_constant + n_variable - 2))
cohens_d <- (mean_constant - mean_variable) / pooled_sd

cat("Cohen's d effect size:", round(cohens_d, 3), "\n")

# Averaged into three groups
ggplot(data, aes(x = condition, y = Normalized.Score, fill = condition)) +
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
  scale_fill_manual(values = c("constant" = "#0000FF", "variable" = "#FF4040"), labels = c("constant" = "Constant Track", "variable" = "Variable Track")) +
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

