library(ggplot2)
library(tidyverse)

csv_path = "C:\\Users\\graci\\Dropbox\\PAndA\\Thesis Experiment 2\\data\\drawing_scores.csv"
data = read.csv(csv_path,stringsAsFactors=TRUE)

# Create a named vector for segment renaming
segment_labels <- c(
  "Constant",
  "Variable"
)


# If needed, ensure 'Condition' is a factor
data$Condition <- as.factor(data$Condition)

# Conduct independent t-test
t_test_result <- t.test(Score ~ Condition, data = data, var.equal = TRUE)  # use var.equal=FALSE if variances are unequal

# Print results
print(t_test_result)

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

