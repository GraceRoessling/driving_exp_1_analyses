library(ggplot2)
# To compare between both visibility conditions without straight pieces
csv_path = "C:\\Users\\graci\\Dropbox\\PAndA\\Thesis Experiment 2\\data\\spatial_knowledge_and_steering_perf_scores.csv"
data  = read.csv(csv_path,stringsAsFactors=TRUE)

# Drawing score and Variability in Lane Pos. ==========================================================================
model <- lm(low_vis_var_lane_dev_10 ~ Normalized_Drawing_Score, data = data )

# 3. Get summary of the model
summary_model <- summary(model)

# Extract R-squared
r_squared <- summary_model$r.squared

# Report R-squared in APA format
cat(sprintf("The regression model accounted for %.2f%% of the variance in low visibility lane deviation (R² = %.3f).\n",
            r_squared * 100, r_squared))

# 4. Plot the data and line of best fit
plot <- ggplot(data, aes(x = Normalized_Drawing_Score, y = low_vis_var_lane_dev_10)) +
  geom_point(color = "black", size = 2) +   # scatter plot points
  geom_smooth(method = "lm", color = "red", se = TRUE) +  # line of best fit with confidence interval
  labs(
    x = "Normalized Drawing Score",
    y = "SD of Lane Dev. in Low Vis. (meters)"
  ) +
  theme(
    legend.position = "none",
    plot.title = element_text(size = 20),
    axis.title.x = element_text(size = 20),
    axis.title.y = element_text(size = 20),
    axis.text.x = element_text(size = 15),
    axis.text.y = element_text(size = 15)
  )

# Show plot
print(plot)

# Drawing score and Steering Acc. ==========================================================================
model <- lm(low_vis_steering_acceleration_10 ~ Normalized_Drawing_Score, data = data )

# 3. Get summary of the model
summary_model <- summary(model)

# Extract R-squared
r_squared <- summary_model$r.squared

# Report R-squared in APA format
cat(sprintf("The regression model accounted for %.2f%% of the variance in low visibility steering acceleration (R² = %.3f).\n",
            r_squared * 100, r_squared))

# 4. Plot the data and line of best fit
plot <- ggplot(data, aes(x = Normalized_Drawing_Score, y = low_vis_steering_acceleration_10)) +
  geom_point(color = "black", size = 2) +   # scatter plot points
  geom_smooth(method = "lm", color = "red", se = TRUE) +  # line of best fit with confidence interval
  labs(
    x = "Normalized Drawing Score",
    y = bquote("Mean Steering Acc. in Low Vis. ( deg / "~s^2~")")
  ) +
  theme(
    legend.position = "none",
    plot.title = element_text(size = 20),
    axis.title.x = element_text(size = 20),
    axis.title.y = element_text(size = 20),
    axis.text.x = element_text(size = 15),
    axis.text.y = element_text(size = 15)
  )

# Show plot
print(plot)


# DTW_score and Variability in Lane Pos. ==========================================================================
model <- lm(low_vis_var_lane_dev_10 ~ DTW_score, data = data )

# 3. Get summary of the model
summary_model <- summary(model)

# Extract R-squared
r_squared <- summary_model$r.squared

# Report R-squared in APA format
cat(sprintf("The regression model accounted for %.2f%% of the variance in low visibility lane deviation (R² = %.3f).\n",
            r_squared * 100, r_squared))

# 4. Plot the data and line of best fit
plot <- ggplot(data, aes(x = DTW_score, y = low_vis_var_lane_dev_10)) +
  geom_point(color = "black", size = 2) +   # scatter plot points
  geom_smooth(method = "lm", color = "red", se = TRUE) +  # line of best fit with confidence interval
  labs(
    x = "Mean DTW Score",
    y = "SD of Lane Dev. in Low Vis. (meters)"
  )  +
  theme(
    legend.position = "none",
    plot.title = element_text(size = 20),
    axis.title.x = element_text(size = 20),
    axis.title.y = element_text(size = 20),
    axis.text.x = element_text(size = 15),
    axis.text.y = element_text(size = 15)
  )


# Show plot
print(plot)

# DTW score and Steering Acc. ==========================================================================
model <- lm(low_vis_steering_acceleration_10 ~ DTW_score, data = data )

# 3. Get summary of the model
summary_model <- summary(model)

# Extract R-squared
r_squared <- summary_model$r.squared

# Report R-squared in APA format
cat(sprintf("The regression model accounted for %.2f%% of the variance in low visibility steering acceleration (R² = %.3f).\n",
            r_squared * 100, r_squared))

# 4. Plot the data and line of best fit
plot <- ggplot(data, aes(x = DTW_score, y = low_vis_steering_acceleration_10)) +
  geom_point(color = "black", size = 2) +   # scatter plot points
  geom_smooth(method = "lm", color = "red", se = TRUE) +  # line of best fit with confidence interval
  labs(
    x = "Mean DTW Score",
    y = "Mean Steering Acc. in Low Vis. ( deg / "~s^2~")"
  ) +
  theme(
    legend.position = "none",
    plot.title = element_text(size = 20),
    axis.title.x = element_text(size = 20),
    axis.title.y = element_text(size = 20),
    axis.text.x = element_text(size = 15),
    axis.text.y = element_text(size = 15)
  )

# Show plot
print(plot)