library(ggplot2)
library(tidyverse)

csv_path = "C:\\Users\\graci\\Dropbox\\PAndA\\Thesis Experiment 3\\data\\drawing_scores.csv"
data = read.csv(csv_path,stringsAsFactors=TRUE)

model <- aov(Normalized.Score ~ Condition + Error(Drawing.ID/(Condition)), data = data)
summary(model)

dtw.aov <- anova_test(
  data = data, dv = Normalized.Score, wid = Drawing.ID,
  between = Condition,effect.size = "pes"
)