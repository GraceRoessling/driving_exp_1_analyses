library(ggplot2)
library(tidyverse)

csv_path = "C:\\Users\\graci\\Dropbox\\PAndA\\Thesis Experiment 2\\data\\resets_per_subj.csv"
data = read.csv(csv_path,stringsAsFactors=TRUE)



# If needed, ensure 'Condition' is a factor
data$condition <- as.factor(data$condition)

# Conduct independent t-test
t_test_result <- t.test(resets ~ condition, data = data, var.equal = TRUE)  # use var.equal=FALSE if variances are unequal

# Print results
print(t_test_result)


# Averaged into three groups
ggplot(data, aes(x = condition, y = resets, fill = condition)) +
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
  scale_x_discrete(
    labels = c("familiar" = "Constant Track", "unfamiliar" = "Variable Track")
  ) +
  labs(
    x = "Track Constancy",
    y = "Mean Number of Resets"
  ) +
  theme(legend.position = "none",
        panel.grid.major.x = element_blank(),
        plot.title = element_text(size = 20),
        axis.title.x = element_text(size = 30),
        axis.title.y = element_text(size = 30),
        axis.text.x = element_text(size = 20),
        axis.text.y = element_text(size = 30)
  )