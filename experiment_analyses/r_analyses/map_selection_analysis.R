# Define the contingency table for the two groups
map_selection_two_groups <- matrix(c(
  10, 5,   # Constant Track: 10 correct, 5 incorrect
  6, 8     # Variable Track: 6 correct, 8 incorrect
), nrow = 2, byrow = TRUE)

rownames(map_selection_two_groups) <- c("Constant Track", "Variable Track")
colnames(map_selection_two_groups) <- c("Correct", "Incorrect")

# Perform the chi-square test and report the statistics
chi_square_results <- function(table) {
  # Perform the chi-square test without continuity correction
  test <- chisq.test(table, correct = FALSE)
  
  # Extract the necessary statistics
  result <- data.frame(
    Comparison = "Constant Track vs Variable Track",
    X2 = round(test$statistic, 3),
    df = test$parameter,
    Raw_p = round(test$p.value, 4),
    Adjusted_p = round(p.adjust(test$p.value, method = "bonferroni"), 4)
  )
  
  return(result)
}

# Run the chi-square test
chi_square_report <- chi_square_results(map_selection_two_groups)

# Print results
print(chi_square_report)
