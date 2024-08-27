# Create a vector of column names
col_names <- paste0("high_vis_mean_lane_dev_", 1:10)

# Function to calculate mean and standard error
calc_stats <- function(df, col_name) {
  mean_val <- mean(df[[col_name]])
  se_val <- sd(df[[col_name]]) / sqrt(length(df[[col_name]]))
  return(c(mean = mean_val, se = se_val))
}

# Calculate stats for high visibility
high_vis_familiar <- lapply(col_names, calc_stats, df = famliar_df)
high_vis_unfamiliar <- lapply(col_names, calc_stats, df = unfamiliar_df)

# Calculate stats for low visibility (assuming similar column names)
low_vis_col_names <- gsub("high", "low", col_names)
low_vis_familiar <- lapply(low_vis_col_names, calc_stats, df = famliar_df)
low_vis_unfamiliar <- lapply(low_vis_col_names, calc_stats, df = unfamiliar_df)

# Convert results to data frames
results <- data.frame(
  condition = rep(c("high_vis_familiar", "high_vis_unfamiliar", "low_vis_familiar", "low_vis_unfamiliar"), each = 10),
  trial = rep(1:10, 4),
  mean = c(sapply(high_vis_familiar, `[`, "mean"),
           sapply(high_vis_unfamiliar, `[`, "mean"),
           sapply(low_vis_familiar, `[`, "mean"),
           sapply(low_vis_unfamiliar, `[`, "mean")),
  se = c(sapply(high_vis_familiar, `[`, "se"),
         sapply(high_vis_unfamiliar, `[`, "se"),
         sapply(low_vis_familiar, `[`, "se"),
         sapply(low_vis_unfamiliar, `[`, "se"))
)